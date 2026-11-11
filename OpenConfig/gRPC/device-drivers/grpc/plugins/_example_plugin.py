"""Example plugin. Copy to plugins/<name>.py (no leading underscore) to enable.

Gives you two new operations without touching the driver:
  * ``interface-counters``: a vendor-specific gNMI helper
  * a new gRPC service reachable through ``gnoi`` as ``healthz.<Method>``
"""

from grpc_driver.registry import operation

# from grpc_driver.registry import register_service
# from my_protos import healthz_pb2, healthz_pb2_grpc
# register_service("healthz", healthz_pb2, healthz_pb2_grpc.HealthzStub, "Healthz")
#   -> grpc-gnoi-call with rpc=healthz.Get request='{...}'


@operation("interface-counters", idempotent=True, description="Read counters for one interface")
def interface_counters(session, params):
    name = params.get("name")
    path = f"/interfaces/interface[name={name}]/state/counters"
    return session.gnmi.get(path=[path], datatype="state")
