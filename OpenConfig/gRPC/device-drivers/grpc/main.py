#!/usr/bin/env python3
"""Itential Gateway 5 gRPC device driver.

One entry point, many operations (selected with --op or the GRPC_OP env var).
Connection details come from the Inventory Manager record piped to stdin;
command line flags override them. See README.md.
"""

import argparse
import contextlib
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from grpc_driver import poold, registry  # noqa: E402
from grpc_driver.errors import classify  # noqa: E402
from grpc_driver.executor import execute_direct  # noqa: E402
from grpc_driver.ops_gnmi import as_bool  # noqa: E402
from grpc_driver.session import ConnSpec  # noqa: E402

CONTROL_OPS = ("pool-status", "pool-stop")
POOL_MODES = ("auto", "off", "required")


def _read_stdin_inventory():
    if sys.stdin is None or sys.stdin.isatty():
        return None
    try:
        data = json.loads(sys.stdin.read() or "null")
        nodes = (data or {}).get("inventory_nodes") or []
        return nodes[0] if nodes else None
    except (json.JSONDecodeError, AttributeError):
        return None


def _load_payload_file(params, key, env_var):
    """Gateway 5.5.3+ delivers large decorator inputs as a file whose path is in an env var."""
    path = os.environ.get(env_var)
    if path:
        with open(path, encoding="utf-8") as fh:
            params[key] = fh.read()


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    p.add_argument("--op", default=os.environ.get("GRPC_OP"), help="Operation. Defaults to the GRPC_OP env var.")
    p.add_argument("--host")
    p.add_argument("--port", type=int)
    p.add_argument("--user")
    p.add_argument("--password")
    p.add_argument("--insecure")
    p.add_argument("--skip-verify", "--skip_verify", dest="skip_verify")
    p.add_argument("--path-cert", "--path_cert", dest="path_cert")
    p.add_argument("--path-key", "--path_key", dest="path_key")
    p.add_argument("--path-root", "--path_root", dest="path_root")
    p.add_argument("--override")
    p.add_argument("--token")
    p.add_argument("--timeout", type=int, help="Seconds to establish the channel")
    p.add_argument("--rpc-timeout", "--rpc_timeout", dest="rpc_timeout", type=int,
                   help="Overall deadline for the operation")
    p.add_argument("--max-concurrent", "--max_concurrent", dest="max_concurrent", type=int,
                   help="Max in-flight operations per host:port:user (default 8)")
    p.add_argument("--pool", choices=POOL_MODES, help="off (default), auto, or required")
    p.add_argument("--envelope", help="true = print the full result envelope instead of just the result")
    return p


def _split_extra(tokens):
    """Fold leftover ``--key value`` tokens into the operation's params (repeated keys become lists)."""
    params, i = {}, 0
    while i < len(tokens):
        token = tokens[i]
        if not token.startswith("--"):
            i += 1
            continue
        key, eq, value = token[2:].partition("=")
        if not eq:
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                value = tokens[i + 1]
                i += 1
            else:
                value = "true"
        key = key.replace("-", "_")
        if key in params:
            params[key] = (params[key] if isinstance(params[key], list) else [params[key]]) + [value]
        else:
            params[key] = value
        i += 1
    # The IM/MOP framework injects empty strings for unset optional fields.
    return {k: v for k, v in params.items() if v != ""}


def _opts(node):
    attrs = (node or {}).get("attributes") or {}
    options = (attrs.get("itential_driver_options") or {}).get("grpc") or {}
    return attrs, options


def _grpc_options(raw):
    if isinstance(raw, dict):
        return tuple(raw.items())
    return tuple(tuple(item) for item in (raw or []))


def resolve_connection(args, node):
    attrs, options = _opts(node)

    def pick(flag, attr_key=None, opt_key=None, default=None):
        value = getattr(args, flag, None)
        if value in (None, ""):
            value = attrs.get(attr_key) if attr_key else None
        if value in (None, "") and opt_key:
            value = options.get(opt_key)
        return default if value in (None, "") else value

    host = pick("host", "itential_host")
    user = pick("user", "itential_user", default="")
    password = pick("password", "itential_password", default="")
    token = pick("token", opt_key="token")
    if not host:
        raise SystemExit("host is required (inventory itential_host or --host)")
    if not token and not (user and password):
        raise SystemExit("credentials are required (itential_user/itential_password, or a token in driver options)")

    return ConnSpec(
        host=host,
        port=int(pick("port", opt_key="port") or pick("port", "itential_port", default=57400)),
        username=user,
        password=password,
        insecure=as_bool(pick("insecure", opt_key="insecure")),
        skip_verify=as_bool(pick("skip_verify", opt_key="skip_verify")),
        path_cert=pick("path_cert", opt_key="path_cert"),
        path_key=pick("path_key", opt_key="path_key"),
        path_root=pick("path_root", opt_key="path_root"),
        override=pick("override", opt_key="override"),
        token=token,
        timeout=int(pick("timeout", opt_key="timeout", default=10)),
        rpc_timeout=int(pick("rpc_timeout", opt_key="rpc_timeout", default=30)),
        max_concurrent=int(pick("max_concurrent", opt_key="max_concurrent", default=8)),
        grpc_options=_grpc_options(options.get("grpc_options")),
    )


def pool_mode(args, node):
    _, options = _opts(node)
    mode = args.pool or options.get("pool") or os.environ.get("GRPC_POOL") or "off"
    return mode if mode in POOL_MODES else "off"


def run_operation(spec, op, params, mode):
    """Execute through the pool daemon when allowed, otherwise on a private channel."""
    if mode != "off":
        payload = {"op": op, "conn": spec.to_dict(), "params": params}
        try:
            reply = poold.request(payload, timeout=spec.timeout + registry.deadline_for(op, params, spec) + 10)
        except poold.PoolUnavailable as exc:
            if mode == "required":
                raise RuntimeError(f"connection pool required but unavailable: {exc}")
            result, meta = execute_direct(spec, op, params)
            meta["mode"] = "fallback"
            meta["reason"] = str(exc)
            return result, meta
        except poold.PoolError as exc:
            raise RuntimeError(str(exc))
        if not reply.get("ok"):
            raise RemoteError(reply.get("error_type", "error"), reply.get("error", "unknown error"))
        return reply["result"], reply.get("pool", {})
    return execute_direct(spec, op, params)


class RemoteError(Exception):
    def __init__(self, error_type, message):
        super().__init__(message)
        self.error_type = error_type


def control(op):
    action = "__status__" if op == "pool-status" else "__stop__"
    try:
        reply = poold.request({"op": action}, spawn=False, timeout=10)
    except (poold.PoolUnavailable, poold.PoolError):
        return {"running": False}
    return dict(reply.get("result") or {}, running=True) if action == "__status__" else reply.get("result")


def emit(envelope, op, show_envelope):
    if op == "is-alive" and not show_envelope:
        sys.stdout.write("true" if envelope["success"] else "false")  # gw-manager parses the bare string
    elif show_envelope or not envelope["success"]:
        print(json.dumps(envelope, indent=2, default=str))
    else:
        result = envelope["result"]
        print(result if isinstance(result, str) else json.dumps(result, indent=2, default=str))
    if not envelope["success"]:
        print(json.dumps(envelope, default=str), file=sys.stderr)


def main(argv=None):
    parser = build_parser()
    args, extra = parser.parse_known_args(argv)
    registry.load_plugins(BASE_DIR)

    op = args.op
    if op in CONTROL_OPS:
        print(json.dumps(control(op), indent=2))
        return 0
    if not op or op not in registry.OPERATIONS:
        parser.error(f"--op / GRPC_OP must be one of: {', '.join(sorted(registry.OPERATIONS) + list(CONTROL_OPS))}")

    node = _read_stdin_inventory()
    params = _split_extra(extra)
    _load_payload_file(params, "config", "GRPC_CONFIG_FILE")
    show_envelope = as_bool(args.envelope)
    envelope = {"success": False, "op": op, "host": None, "device_name": (node or {}).get("name"),
                "result": None, "error": None, "error_type": None, "pool": None}
    try:
        spec = resolve_connection(args, node)
        envelope["host"] = spec.host
        with contextlib.redirect_stdout(sys.stderr):  # keep third-party prints out of the result stream
            result, meta = run_operation(spec, op, params, pool_mode(args, node))
        envelope.update(success=True, result=result, pool=meta)
    except RemoteError as exc:
        envelope.update(error=str(exc), error_type=exc.error_type)
    except SystemExit as exc:
        envelope.update(error=str(exc), error_type="invalid_input")
    except Exception as exc:  # noqa: BLE001
        etype, message, _ = classify(exc)
        envelope.update(error=message, error_type=etype)
    emit(envelope, op, show_envelope)
    return 0 if envelope["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
