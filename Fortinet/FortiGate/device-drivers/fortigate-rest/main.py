#!/usr/bin/env python3
"""fortigate-rest — Fortinet FortiGate REST API driver for IG5.

Implements the IG5 device broker contracts via the FortiOS REST API:
is-alive, get-config, and rest-call. run-command and set-config are
intentionally NOT implemented as CLI passthrough (see below) -- they
return a structured "not supported" error instead of pretending to work.

FortiOS's REST API only supports static API-token (Bearer) authentication --
there is no username/password login flow like F5's iControl REST. A token is
generated once via an "API Administrator" account in FortiOS (GUI or the
`execute api-user generate-key` CLI command) and never expires unless
revoked, so there is no refresh logic in this driver.

Per-device configuration in Inventory Manager attributes:
  itential_host      — FortiGate management IP or hostname
  itential_port      — HTTPS port (default: 443)
  itential_password  — the FortiOS API token (resolved by IG5 — no vault
                        logic in this driver). itential_user is not used;
                        FortiOS tokens are not tied to a username at auth time.

  itential_driver_options.fortigate-rest:
    api_token   — overrides itential_password as the token source, if you
                  want to keep a separate admin password on the node
    vdom        — virtual domain name to scope monitor/cmdb calls to
                  (omit for single-VDOM appliances)
    verify_ssl  — verify TLS certificate (default: true)
    timeout     — request timeout seconds (default: 30)
    backup_scope — scope param for the get-config backup call:
                  "global" (default) or "vdom"

IMPORTANT — no CLI passthrough exists on FortiOS's REST API:
FortiOS's REST API has no equivalent of F5's /mgmt/tm/util/bash. Fortinet's
own support guidance is explicit that arbitrary CLI commands cannot be sent
over the API. Because of that:
  - run-command  returns {"success": false, "error": "..."} explaining the
                 limitation and pointing to rest-call instead.
  - set-config   (the Config Manager remediation broker entry point) returns
                 the same -- CM-style raw CLI change lines have no REST
                 endpoint to execute against. Real remediation on FortiGate
                 needs to target specific /api/v2/cmdb/<path> objects via
                 rest-call, which is a structured-object model rather than
                 CLI-line diffs.
  - rest-call    is therefore the primary way to change configuration through
                 this driver -- callers supply verb, route (e.g.
                 /api/v2/cmdb/firewall/policy/1), and a JSON body.

The FORTIGATE_REST_OP environment variable selects the operation (set by
IG5 per-service). CLI flags override stdin inventory values for local
testing.
"""

import os
import sys

# lib/ is private to this driver — not shared with other device-drivers/*.
sys.path.insert(0, os.path.dirname(__file__))

import argparse
import json

from lib.iag import (
    read_stdin_inventory,
    normalize_args,
    print_result,
)
from lib.rest import BearerAuth, RestSession


# ---------------------------------------------------------------------------
# FortiGate-specific session factory
# ---------------------------------------------------------------------------

def _make_session(conn: dict) -> RestSession:
    auth = BearerAuth(conn["token"])
    return RestSession(auth, verify_ssl=conn["verify_ssl"], timeout=conn["timeout"])


def _base(conn: dict) -> str:
    return f"https://{conn['host']}:{conn['port']}"


def _vdom_params(conn: dict) -> dict:
    return {"vdom": conn["vdom"]} if conn.get("vdom") else {}


_UNSUPPORTED_CLI = (
    "FortiOS's REST API does not support arbitrary CLI command execution -- "
    "there is no bash/CLI passthrough endpoint (unlike F5's /mgmt/tm/util/bash). "
    "Use rest-call to perform structured operations against /api/v2/cmdb/* or "
    "/api/v2/monitor/* endpoints instead, or use a CLI/SSH-based driver "
    "(e.g. netsdk) if raw CLI access is genuinely required."
)


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def is_alive(conn: dict, args) -> dict:
    try:
        session = _make_session(conn)
        r = session.get(
            _base(conn) + "/api/v2/monitor/system/status",
            params=_vdom_params(conn),
            raise_on_error=False,
        )
        return {"success": True, "alive": r.status_code == 200, "host": conn["host"]}
    except Exception as e:
        return {"success": False, "alive": False, "host": conn["host"],
                "error": str(e), "error_type": type(e).__name__}


def run_command(conn: dict, args) -> dict:
    return {"success": False, "host": conn["host"], "error": _UNSUPPORTED_CLI}


def get_config(conn: dict, args) -> dict:
    """Retrieve the full configuration via the REST config-backup endpoint.

    NOTE: Fortinet customers have reported this endpoint returning a
    truncated config on very large configurations (partial output rather
    than the full CLI-equivalent backup). Verify output completeness against
    a CLI-based backup if you rely on this for large or heavily-VDOM'd
    appliances.
    """
    try:
        session = _make_session(conn)
        params  = {"scope": conn["backup_scope"], **_vdom_params(conn)}
        r = session.get(_base(conn) + "/api/v2/monitor/system/config/backup",
                        params=params)
        return {"success": True, "host": conn["host"],
                "config_format": "text", "config": r.text}
    except Exception as e:
        return {"success": False, "host": conn["host"],
                "error": str(e), "error_type": type(e).__name__}


def rest_call(conn: dict, args) -> dict:
    """Generic FortiOS REST passthrough — caller supplies verb, route, body.

    route is the full path from root, e.g. /api/v2/cmdb/firewall/policy or
    /api/v2/monitor/system/status. vdom is applied automatically as a query
    param if configured on the device, unless already present in route.
    """
    if not args.verb or not args.route:
        return {"success": False, "host": conn["host"],
                "error": "verb and route are required for action=rest-call"}
    try:
        session = _make_session(conn)
        url     = _base(conn) + "/" + args.route.lstrip("/")
        body    = None
        if args.body:
            try:
                body = json.loads(args.body) if isinstance(args.body, str) else args.body
            except (json.JSONDecodeError, TypeError):
                body = args.body

        params = _vdom_params(conn) if "vdom=" not in args.route else {}
        r = session.request(args.verb.upper(), url, json=body, params=params)
        try:
            response_data = r.json()
        except Exception:
            response_data = r.text

        return {"success": True, "host": conn["host"],
                "status_code": r.status_code, "response": response_data}

    except Exception as e:
        result = {"success": False, "host": conn["host"],
                  "error": str(e), "error_type": type(e).__name__}
        if hasattr(e, "response") and e.response is not None:
            result["status_code"] = e.response.status_code
            try:
                result["error_body"] = e.response.json()
            except Exception:
                result["error_body"] = e.response.text
        return result


def set_config(conn: dict, args) -> dict:
    return {"success": False, "host": conn["host"], "error": _UNSUPPORTED_CLI}


_DISPATCH = {
    "is-alive":    is_alive,
    "run-command": run_command,
    "get-config":  get_config,
    "rest-call":   rest_call,
    "set-config":  set_config,
}


# ---------------------------------------------------------------------------
# Connection resolution
# ---------------------------------------------------------------------------

def _resolve_connection(args, node) -> dict:
    attrs       = ((node or {}).get("attributes") or {})
    driver_opts = dict((attrs.get("itential_driver_options") or {}).get("fortigate-rest") or {})

    def pick(cli_val, attr_key, default=None):
        if cli_val is not None:
            return cli_val
        v = attrs.get(attr_key)
        return v if v is not None else default

    host  = pick(args.host, "itential_host")
    port  = int(pick(args.port, "itential_port", 443))

    # FortiOS auth is a static API token, not a username/password login --
    # the token is expected in itential_password by convention, with an
    # explicit driver-option override for devices that also need a separate
    # admin password recorded for other purposes.
    token = driver_opts.pop("api_token", None) or pick(args.password, "itential_password")

    vdom         = driver_opts.pop("vdom", None)
    verify_ssl   = driver_opts.pop("verify_ssl", True)
    timeout      = int(driver_opts.pop("timeout", 30) or 30)
    backup_scope = driver_opts.pop("backup_scope", None) or "global"

    if isinstance(verify_ssl, str):
        verify_ssl = verify_ssl.lower() not in ("false", "0", "no")

    missing = [n for n, v in [("host", host), ("password (API token)", token)] if not v]
    if missing:
        raise SystemExit(
            f"missing required field(s): {', '.join(missing)} "
            f"(set itential_{missing[0].split()[0]} on the inventory node)"
        )

    return {
        "host": host, "port": port, "token": token, "vdom": vdom,
        "verify_ssl": verify_ssl, "timeout": timeout,
        "backup_scope": backup_scope,
        "device_name": (node or {}).get("name") or host,
    }


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="fortigate-rest: Fortinet FortiGate REST API driver for IG5"
    )
    parser.add_argument("--op", default=os.environ.get("FORTIGATE_REST_OP"),
                        choices=list(_DISPATCH),
                        help="Operation. Defaults to FORTIGATE_REST_OP env var.")
    parser.add_argument("--host",     default=None)
    parser.add_argument("--port",     type=int, default=None)
    parser.add_argument("--password", default=None, help="FortiOS API token")
    parser.add_argument("--timeout",  type=int, default=None)

    # rest-call
    parser.add_argument("--verb",  default=None,
                        help="HTTP verb for rest-call (GET POST PUT DELETE)")
    parser.add_argument("--route", default=None,
                        help="FortiOS REST route (e.g. /api/v2/cmdb/firewall/policy)")
    parser.add_argument("--body",  default=None,
                        help="JSON request body for rest-call")

    # accepted for interface parity with other drivers; always resolve to
    # the unsupported-CLI error in run-command/set-config
    parser.add_argument("--command", action="append", default=None)
    parser.add_argument("--commands", default=None)
    parser.add_argument("--config",         default=None)
    parser.add_argument("--config_content", "--config-content",
                        dest="config_content", default=None)
    parser.add_argument("--changes", default=None)
    parser.add_argument("--options", default=None)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    args = build_parser().parse_args()
    if not args.op:
        raise SystemExit("--op flag or FORTIGATE_REST_OP env var must be set")
    normalize_args(args)
    node = read_stdin_inventory()
    conn = _resolve_connection(args, node)
    result = _DISPATCH[args.op](conn, args)
    return print_result(result, args.op)


if __name__ == "__main__":
    sys.exit(main())
