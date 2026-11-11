"""run-command: the action Command Templates call. One command per line.

  show version                      CLI command: gNMI Get with origin "cli" (Cisco IOS XR, Arista, ...)
  gnmi capabilities                 gNMI Capabilities
  gnmi get /system/config           gNMI Get (a native path may carry an origin, e.g. Cisco-IOS-XR-ifmgr-cfg:interfaces)
  gnoi system.Time                  any gNOI RPC, optionally followed by a JSON request body
  gnoi system.Ping {"destination": "10.0.0.1", "count": 2}
"""

import json

from grpc_driver import gnmi
from grpc_driver.errors import classify
from grpc_driver.ops_gnmi import as_json, as_list
from grpc_driver.ops_gnoi import _method, invoke
from grpc_driver.registry import operation


def split_commands(params):
    raw = params.get("command")
    if raw in (None, ""):
        raw = params.get("commands")
    lines = []
    for item in as_list(raw):
        lines += [line.strip() for line in str(item).splitlines()]
    return [line for line in lines if line]


def _text(value):
    return value if isinstance(value, str) else json.dumps(value, indent=2, default=str)


def _run_one(session, line):
    head, _, rest = line.partition(" ")
    rest = rest.strip()
    if head == "gnmi":
        verb, _, arg = rest.partition(" ")
        if verb == "capabilities":
            return _text(session.gnmi.capabilities())
        if verb == "get" and arg.strip():
            out = gnmi.get(session, [arg.strip()])
            values = [u.get("val") for n in out.get("notification", []) for u in n.get("update", [])]
            return _text(values[0] if len(values) == 1 else values)
        raise ValueError("gnmi commands: 'gnmi capabilities' or 'gnmi get <path>'")
    if head == "gnoi":
        rpc, _, body = rest.partition(" ")
        if not rpc:
            raise ValueError("gnoi commands: 'gnoi <service.Method> [json request]'")
        alias, _, stub_cls, descriptor = _method(rpc)
        return _text(invoke(session, alias, stub_cls, descriptor, as_json(body.strip() or None, "request")))
    out = gnmi.get(session, [line], origin="cli")
    values = [u.get("val") for n in out.get("notification", []) for u in n.get("update", [])]
    return "\n".join(_text(v) for v in values if v is not None)


@operation("run-command", description="Command Templates: CLI (gNMI cli origin), 'gnmi ...' and 'gnoi ...' commands")
def run_command(session, params):
    commands = split_commands(params)
    if not commands:
        return {"success": False, "host": session.spec.host, "error": "command is required for action=run-command",
                "results": []}
    results = []
    for line in commands:
        try:
            results.append({"command": line, "output": _run_one(session, line), "success": True})
        except Exception as exc:  # noqa: BLE001 - one failing command must not hide the others
            _, message, _ = classify(exc)
            results.append({"command": line, "output": message, "success": False})
    return {"success": all(r["success"] for r in results), "host": session.spec.host, "results": results}
