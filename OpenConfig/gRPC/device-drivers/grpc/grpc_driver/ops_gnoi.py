"""gNOI (and any other compiled gRPC service) driven from protobuf service descriptors.

Every RPC of every registered service becomes callable as ``<alias>.<Method>``
with a JSON request body, so adding a service is one ``register_service`` call
instead of one hand-written wrapper per RPC.
"""

import json

from google.protobuf import json_format
from google.protobuf.descriptor import FieldDescriptor

from grpc_driver import registry
from grpc_driver.errors import DriverError
from grpc_driver.ops_gnmi import as_bool, as_json
from grpc_driver.registry import operation, register_service, register_stub

from gnoi.bgp import bgp_pb2, bgp_pb2_grpc
from gnoi.interface import interface_pb2, interface_pb2_grpc
from gnoi.layer2 import layer2_pb2, layer2_pb2_grpc
from gnoi.system import system_pb2, system_pb2_grpc

for alias, pb2, grpc_mod, service in (
    ("system", system_pb2, system_pb2_grpc, "System"),
    ("bgp", bgp_pb2, bgp_pb2_grpc, "BGP"),
    ("interface", interface_pb2, interface_pb2_grpc, "Interface"),
    ("layer2", layer2_pb2, layer2_pb2_grpc, "Layer2"),
):
    register_service(alias, pb2, getattr(grpc_mod, service + "Stub"), service)

READ_ONLY = {"system.Time", "system.Ping", "system.Traceroute", "system.RebootStatus"}
STREAM_LIMIT = 1000


def _method(rpc):
    try:
        alias, name = rpc.split(".", 1)
        pb2, stub_cls, service = registry.SERVICES[alias]
        descriptor = pb2.DESCRIPTOR.services_by_name[service].methods_by_name[name]
    except (ValueError, KeyError):
        known = sorted(
            f"{a}.{m.name}"
            for a, (pb2, _, svc) in registry.SERVICES.items()
            for m in pb2.DESCRIPTOR.services_by_name[svc].methods
        )
        raise DriverError(f"Unknown rpc '{rpc}'. Available: {', '.join(known)}", "unknown_rpc")
    return alias, name, stub_cls, descriptor


def invoke(session, alias, stub_cls, descriptor, request):
    """Call one RPC described by a protobuf method descriptor and return JSON-ready data."""
    stub_key = f"svc:{alias}"
    if stub_key not in registry.STUBS:
        register_stub(stub_key, stub_cls)
    rpc = getattr(session.stub(stub_key), descriptor.name)
    request_cls = descriptor.input_type._concrete_class
    message = json_format.ParseDict(request or {}, request_cls())
    metadata = session.metadata
    timeout = session.spec.rpc_timeout
    arg = iter([message]) if descriptor.client_streaming else message
    response = rpc(arg, metadata=metadata, timeout=timeout)
    if descriptor.server_streaming:
        out = []
        for item in response:
            out.append(json.loads(json_format.MessageToJson(item)))
            if len(out) >= STREAM_LIMIT:
                response.cancel()
                break
        return out
    return json.loads(json_format.MessageToJson(response))


@operation("gnoi", description="Invoke a gNOI RPC, e.g. rpc=system.Time request='{}'")
def gnoi(session, params):
    rpc = params.get("rpc")
    if not rpc:
        raise DriverError("rpc is required, e.g. system.Time", "invalid_input")
    alias, _, stub_cls, descriptor = _method(rpc)
    return invoke(session, alias, stub_cls, descriptor, as_json(params.get("request"), "request"))


@operation("gnoi-time", idempotent=True, description="gNOI system.Time")
def gnoi_time(session, params):
    return gnoi(session, {"rpc": "system.Time"})


@operation("gnoi-reboot", description="gNOI system.Reboot")
def gnoi_reboot(session, params):
    request = as_json(params.get("request"), "request") or {}
    if "method" not in request and params.get("method"):
        request["method"] = params["method"]
    if "message" not in request and params.get("message"):
        request["message"] = params["message"]
    if "delay" not in request and params.get("delay"):
        request["delay"] = int(params["delay"])
    return gnoi(session, {"rpc": "system.Reboot", "request": request})


# ---------------------------------------------------------------- dedicated services
# One service per common system RPC. The request is built from the protobuf descriptor, so flat inputs
# (destination, count, message, ...) map by field name; anything nested goes in ``request`` as JSON.

_INT_TYPES = (FieldDescriptor.TYPE_INT32, FieldDescriptor.TYPE_INT64,
              FieldDescriptor.TYPE_UINT32, FieldDescriptor.TYPE_UINT64)


def _flat_request(descriptor, params):
    request = dict(as_json(params.get("request"), "request") or {})
    for field in descriptor.input_type.fields:
        raw = params.get(field.name)
        if field.name in request or raw in (None, ""):
            continue
        if field.type == FieldDescriptor.TYPE_BOOL:
            request[field.name] = as_bool(raw)
        elif field.type in _INT_TYPES:
            try:
                request[field.name] = int(raw)
            except (TypeError, ValueError):
                raise DriverError(f"{field.name} must be an integer", "invalid_input")
        elif field.type in (FieldDescriptor.TYPE_STRING, FieldDescriptor.TYPE_ENUM):
            request[field.name] = str(raw)
    return request


def _register_rpc(name, rpc, description, idempotent=False, required=()):
    @operation(name, idempotent=idempotent, description=description)
    def _call(session, params):
        alias, _, stub_cls, descriptor = _method(rpc)
        request = _flat_request(descriptor, params)
        for field in required:
            if field not in request:
                raise DriverError(f"{field} is required", "invalid_input")
        return invoke(session, alias, stub_cls, descriptor, request)

    return _call


_register_rpc("gnoi-ping", "system.Ping", "gNOI system.Ping (streamed replies returned as a list)",
              idempotent=True, required=("destination",))
_register_rpc("gnoi-traceroute", "system.Traceroute", "gNOI system.Traceroute (streamed hops returned as a list)",
              idempotent=True, required=("destination",))
_register_rpc("gnoi-reboot-status", "system.RebootStatus", "gNOI system.RebootStatus", idempotent=True)
_register_rpc("gnoi-cancel-reboot", "system.CancelReboot", "gNOI system.CancelReboot")
