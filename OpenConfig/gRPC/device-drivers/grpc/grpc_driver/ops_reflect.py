"""Call any gRPC method without compiled stubs, using server reflection."""

import json

import grpc
from google.protobuf import descriptor_pb2, descriptor_pool, json_format, message_factory
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc

from grpc_driver.errors import DriverError
from grpc_driver.ops_gnmi import as_json
from grpc_driver.registry import operation


def _pool(session):
    """Descriptor pool for this channel, built once and kept for the life of a pooled session."""
    return session.cache.setdefault("reflection_pool", descriptor_pool.DescriptorPool())


def _load_symbol(session, pool, symbol):
    stub = reflection_pb2_grpc.ServerReflectionStub(session.channel)

    def ask(**kw):
        request = reflection_pb2.ServerReflectionRequest(**kw)
        for response in stub.ServerReflectionInfo(iter([request]), metadata=session.metadata,
                                                  timeout=session.spec.rpc_timeout):
            return response
        raise DriverError("Empty reflection response", "reflection_failed")

    response = ask(file_containing_symbol=symbol)
    if response.HasField("error_response"):
        raise DriverError(f"Reflection: {response.error_response.error_message}", "reflection_failed")
    protos = [descriptor_pb2.FileDescriptorProto.FromString(b) for b in response.file_descriptor_response.file_descriptor_proto]
    pending = {p.name: p for p in protos}

    def add(name):
        proto = pending.pop(name, None)
        if proto is None:
            return
        for dep in proto.dependency:
            if dep not in pending:
                try:
                    pool.FindFileByName(dep)
                    continue
                except KeyError:
                    extra = ask(file_by_filename=dep)
                    for b in extra.file_descriptor_response.file_descriptor_proto:
                        fp = descriptor_pb2.FileDescriptorProto.FromString(b)
                        pending.setdefault(fp.name, fp)
            add(dep)
        try:
            pool.Add(proto)
        except Exception:
            pass

    for name in list(pending):
        add(name)


@operation("call", description="Call any gRPC method via server reflection, e.g. method=gnoi.system.System/Time")
def call(session, params):
    method = params.get("method") or ""
    if "/" not in method:
        raise DriverError("method must look like package.Service/Method", "invalid_input")
    service, name = method.strip("/").split("/", 1)
    pool = _pool(session)
    try:
        service_desc = pool.FindServiceByName(service)
    except KeyError:
        _load_symbol(session, pool, service)
        try:
            service_desc = pool.FindServiceByName(service)
        except KeyError:
            raise DriverError(f"Service {service} not found via reflection", "unknown_rpc")
    if name not in service_desc.methods_by_name:
        raise DriverError(f"{service} has no method {name}", "unknown_rpc")
    desc = service_desc.methods_by_name[name]
    if desc.client_streaming:
        raise DriverError("Client-streaming methods are not supported by 'call'", "unsupported")

    request_cls = message_factory.GetMessageClass(desc.input_type)
    response_cls = message_factory.GetMessageClass(desc.output_type)
    request = json_format.ParseDict(as_json(params.get("payload"), "payload") or {}, request_cls())
    path = f"/{service}/{name}"
    kwargs = dict(request_serializer=request_cls.SerializeToString,
                  response_deserializer=response_cls.FromString)
    metadata, timeout = session.metadata, session.spec.rpc_timeout
    if desc.server_streaming:
        stream = session.channel.unary_stream(path, **kwargs)(request, metadata=metadata, timeout=timeout)
        return [json.loads(json_format.MessageToJson(m)) for m in stream]
    reply = session.channel.unary_unary(path, **kwargs)(request, metadata=metadata, timeout=timeout)
    return json.loads(json_format.MessageToJson(reply))
