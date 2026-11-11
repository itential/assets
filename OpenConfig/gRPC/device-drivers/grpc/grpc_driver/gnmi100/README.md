gNMI 0.10.0 protobuf definitions, vendored so the driver can send `union_replace`
(pygnmi bundles only the 0.8.0 stubs).

Source: https://github.com/openconfig/gnmi (proto/gnmi, proto/gnmi_ext) at commit
a4e40e60426e5b30ce29fd8115809d2dbe47584f (spec 0.10.0).

Local edits, so these load beside pygnmi's 0.8.0 stubs in one process:
- proto packages renamed `gnmi` -> `gnmi100`, `gnmi_ext` -> `gnmi100_ext`
- gnmi_ext import localised, file-level `gnmi_service` option removed
The wire format is unchanged. RPC paths stay `/gnmi.gNMI/<Method>`.

Regenerate: python -m grpc_tools.protoc -I. --python_out=. gnmi100/gnmi.proto gnmi100/gnmi_ext.proto
(then change the `from gnmi100 import gnmi_ext_pb2` line to `from grpc_driver.gnmi100 import gnmi_ext_pb2`)
