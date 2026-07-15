#!/usr/bin/env python3
"""f5-rest — F5 BIG-IP iControl REST driver for IG5.

Implements the IG5 device broker contracts via the F5 iControl REST API:
is-alive, run-command, get-config, rest-call, and set-config.

Auth method is configured per-device via itential_driver_options.f5-rest.auth_method:

  token  (default) POST /mgmt/shared/authn/login → X-F5-Auth-Token
  oauth            OAuth2 client_credentials → Authorization: Bearer
                   Requires env vars: F5_OAUTH_CLIENT_ID, F5_OAUTH_CLIENT_SECRET
                   Optional:          F5_OAUTH_TOKEN_URL (defaults to /mgmt/shared/authn/oauth2/v1/token)
  basic            Authorization: Basic base64(user:pass) on every request
  bearer           Static pre-obtained Bearer token from env var F5_BEARER_TOKEN

Per-device configuration in Inventory Manager attributes:
  itential_host      — F5 management IP or hostname
  itential_port      — HTTPS port (default: 443)
  itential_user      — F5 username (used by token and basic auth)
  itential_password  — F5 password (resolved by IG5 — no vault logic in this driver)

  itential_driver_options.f5-rest:
    auth_method        — token | oauth | basic | bearer  (default: token)
    login_provider     — F5 auth provider for token auth (default: tmos)
    verify_ssl         — verify TLS certificate (default: true)
    timeout            — request timeout seconds (default: 30)
    get_config_command — bash command used for get-config
                         (default: tmsh list all-properties)
    save_config        — save sys config after set-config (default: true)

The F5_REST_OP environment variable selects the operation (set by IG5 per-service).
CLI flags override stdin inventory values for local testing.
"""

import argparse
import json
import os
import sys

# lib/ is private to this driver — not shared with other device-drivers/*.
sys.path.insert(0, os.path.dirname(__file__))

from lib.iag import (
    read_stdin_inventory,
    normalize_args,
    print_result,
    build_set_config_output,
)
from lib.rest import (
    TokenAuth,
    OAuth2ClientCredentials,
    BasicAuth,
    BearerAuth,
    RestSession,
)


# ---------------------------------------------------------------------------
# F5-specific session factory
# ---------------------------------------------------------------------------

def _make_session(conn: dict) -> RestSession:
    """Build a RestSession with the auth strategy configured for this device."""
    method   = conn["auth_method"]
    base     = f"https://{conn['host']}:{conn['port']}"
    verify   = conn["verify_ssl"]
    timeout  = conn["timeout"]

    if method == "token":
        auth = TokenAuth(
            token_url=f"{base}/mgmt/shared/authn/login",
            payload={
                "username":          conn["user"],
                "password":          conn["password"],
                "loginProviderName": conn["login_provider"],
            },
            token_path="token.token",
            header_name="X-F5-Auth-Token",
            verify_ssl=verify,
            timeout=timeout,
        )

    elif method == "oauth":
        token_url = (
            conn.get("oauth_token_url")
            or os.environ.get("F5_OAUTH_TOKEN_URL")
            or f"{base}/mgmt/shared/authn/oauth2/v1/token"
        )
        client_id     = conn.get("oauth_client_id")     or os.environ.get("F5_OAUTH_CLIENT_ID")
        client_secret = conn.get("oauth_client_secret") or os.environ.get("F5_OAUTH_CLIENT_SECRET")
        if not client_id or not client_secret:
            raise SystemExit(
                "auth_method=oauth requires F5_OAUTH_CLIENT_ID and "
                "F5_OAUTH_CLIENT_SECRET environment variables"
            )
        auth = OAuth2ClientCredentials(
            token_url=token_url,
            client_id=client_id,
            client_secret=client_secret,
            verify_ssl=verify,
            timeout=timeout,
        )

    elif method == "basic":
        auth = BasicAuth(conn["user"], conn["password"])

    elif method == "bearer":
        token = conn.get("bearer_token") or os.environ.get("F5_BEARER_TOKEN")
        if not token:
            raise SystemExit("auth_method=bearer requires F5_BEARER_TOKEN environment variable")
        auth = BearerAuth(token)

    else:
        raise SystemExit(
            f"unsupported auth_method {method!r}; "
            "choose from: token, oauth, basic, bearer"
        )

    return RestSession(auth, verify_ssl=verify, timeout=timeout)


def _base(conn: dict) -> str:
    return f"https://{conn['host']}:{conn['port']}"


def _bash(session: RestSession, base_url: str, cmd: str) -> str:
    """Run a bash command via /mgmt/tm/util/bash and return text output."""
    r = session.post(
        f"{base_url}/mgmt/tm/util/bash",
        json={"command": "run", "utilCmdArgs": f"-c '{cmd}'"},
    )
    return r.json().get("commandResult", "")


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def is_alive(conn: dict, args) -> dict:
    try:
        session = _make_session(conn)
        r = session.get(_base(conn) + "/mgmt/tm/sys/version", raise_on_error=False)
        return {"success": True, "alive": r.status_code == 200, "host": conn["host"]}
    except Exception as e:
        return {"success": False, "alive": False, "host": conn["host"],
                "error": str(e), "error_type": type(e).__name__}


def run_command(conn: dict, args) -> dict:
    if not args.command:
        return {"success": False, "host": conn["host"],
                "error": "command is required for action=run-command"}
    results = []
    try:
        session = _make_session(conn)
        base_url = _base(conn)
        for cmd in args.command:
            try:
                output = _bash(session, base_url, cmd)
                results.append({"command": cmd, "output": output, "success": True})
            except Exception as e:
                results.append({"command": cmd, "output": "", "success": False,
                                 "error": str(e)})
        return {"success": all(r["success"] for r in results),
                "host": conn["host"], "results": results}
    except Exception as e:
        return {"success": False, "host": conn["host"], "error": str(e),
                "error_type": type(e).__name__, "results": results}


def get_config(conn: dict, args) -> dict:
    cmd = conn.get("get_config_command") or "tmsh list all-properties"
    try:
        session  = _make_session(conn)
        output   = _bash(session, _base(conn), cmd)
        return {"success": True, "host": conn["host"],
                "config_format": "text", "config": output}
    except Exception as e:
        return {"success": False, "host": conn["host"],
                "error": str(e), "error_type": type(e).__name__}


def rest_call(conn: dict, args) -> dict:
    """Generic iControl REST passthrough — caller supplies verb, route, body."""
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

        r = session.request(args.verb.upper(), url, json=body)
        try:
            response_data = r.json()
        except Exception:
            response_data = r.text

        return {"success": True, "host": conn["host"],
                "status_code": r.status_code, "response": response_data}

    except Exception as e:
        resp = getattr(getattr(e, "response", None), None, None)
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
    """Config Manager remediation — run CM changes as bash/TMSH commands."""
    if not args.command:
        return {"success": False, "host": conn["host"],
                "error": "no config changes to apply"}
    try:
        session  = _make_session(conn)
        base_url = _base(conn)
        for cmd in args.command:
            _bash(session, base_url, cmd)
        if conn.get("save_config"):
            try:
                _bash(session, base_url, "tmsh save sys config")
            except Exception:
                pass
        changes_list = getattr(args, "_changes_list", None)
        output = build_set_config_output(args.command, changes_list)
        return {"success": True, "host": conn["host"],
                "_output": output, "_changes_list": changes_list}
    except Exception as e:
        return {"success": False, "host": conn["host"],
                "error": str(e), "error_type": type(e).__name__}


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
    driver_opts = dict((attrs.get("itential_driver_options") or {}).get("f5-rest") or {})

    def pick(cli_val, attr_key, default=None):
        if cli_val is not None:
            return cli_val
        v = attrs.get(attr_key)
        return v if v is not None else default

    host     = pick(args.host,     "itential_host")
    port     = int(pick(args.port, "itential_port", 443))
    user     = pick(args.user,     "itential_user")
    password = pick(args.password, "itential_password")

    # Pop driver-managed keys before passing the rest to auth/session
    auth_method    = driver_opts.pop("auth_method",        None) or "token"
    login_provider = driver_opts.pop("login_provider",     None) or "tmos"
    verify_ssl     = driver_opts.pop("verify_ssl",         True)
    timeout        = int(driver_opts.pop("timeout",        30) or 30)
    get_config_cmd = driver_opts.pop("get_config_command", None) or "tmsh list all-properties"
    save           = str(driver_opts.pop("save_config",    "true")).lower() not in ("false", "0", "no")

    # OAuth / bearer extras that may live in driver options
    oauth_token_url    = driver_opts.pop("oauth_token_url",    None)
    oauth_client_id    = driver_opts.pop("oauth_client_id",    None)
    oauth_client_secret= driver_opts.pop("oauth_client_secret",None)
    bearer_token       = driver_opts.pop("bearer_token",       None)

    if isinstance(verify_ssl, str):
        verify_ssl = verify_ssl.lower() not in ("false", "0", "no")

    missing = [n for n, v in [("host", host), ("user", user), ("password", password)] if not v]
    if auth_method in ("basic", "token") and missing:
        raise SystemExit(
            f"missing required field(s): {', '.join(missing)} "
            f"(set itential_{missing[0]} on the inventory node)"
        )

    return {
        "host": host, "port": port, "user": user, "password": password,
        "auth_method": auth_method, "login_provider": login_provider,
        "verify_ssl": verify_ssl, "timeout": timeout,
        "get_config_command": get_config_cmd, "save_config": save,
        "oauth_token_url": oauth_token_url,
        "oauth_client_id": oauth_client_id,
        "oauth_client_secret": oauth_client_secret,
        "bearer_token": bearer_token,
        "device_name": (node or {}).get("name") or host,
    }


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="f5-rest: F5 BIG-IP iControl REST driver for IG5"
    )
    parser.add_argument("--op", default=os.environ.get("F5_REST_OP"),
                        choices=list(_DISPATCH),
                        help="Operation. Defaults to F5_REST_OP env var.")
    parser.add_argument("--host",     default=None)
    parser.add_argument("--port",     type=int, default=None)
    parser.add_argument("--user",     default=None)
    parser.add_argument("--password", default=None)
    parser.add_argument("--timeout",  type=int, default=None)

    # run-command / set-config
    parser.add_argument("--command", action="append", default=None,
                        help="Bash or TMSH command (repeatable)")
    parser.add_argument("--commands", default=None,
                        help="JSON array of commands")
    parser.add_argument("--config",         default=None)
    parser.add_argument("--config_content", "--config-content",
                        dest="config_content", default=None)
    parser.add_argument("--changes", default=None)
    parser.add_argument("--options", default=None)

    # rest-call
    parser.add_argument("--verb",  default=None,
                        help="HTTP verb for rest-call (GET POST PUT PATCH DELETE)")
    parser.add_argument("--route", default=None,
                        help="iControl REST route (e.g. /mgmt/tm/ltm/virtual)")
    parser.add_argument("--body",  default=None,
                        help="JSON request body for rest-call")

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    args = build_parser().parse_args()
    if not args.op:
        raise SystemExit("--op flag or F5_REST_OP env var must be set")
    normalize_args(args)
    node = read_stdin_inventory()
    conn = _resolve_connection(args, node)
    result = _DISPATCH[args.op](conn, args)
    return print_result(result, args.op)


if __name__ == "__main__":
    sys.exit(main())
