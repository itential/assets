#!/usr/bin/env python3
"""Junos NETCONF service for IAG5.

Replaces CLI-based netmiko/scrapli flows for destructive Junos operations
that drop the SSH session mid-command (software add, reboot, halt).
NETCONF is RPC-over-SSH (port 830) — operations return cleanly even when
the underlying device restarts daemons.

Actions: is-alive, run-command, get-config, send-command, reboot

Connection parameters (host, port, user, password, timeout, lock options) are
read from stdin as JSON in the gateway5 InventoryInfo format:

    {"inventory_nodes": [{"name": "...", "attributes": {
        "itential_host": "...", "itential_user": "...",
        "itential_password": "...",
        "itential_driver_options": {"netconf": {"port": 830, ...}}
    }}]}

CLI flags for those connection params still exist and override stdin values
when both are present — useful for local testing without piping JSON.
"""

import argparse
import json
import os
import sys
import time
from xml.sax.saxutils import escape as _xml_escape

import lxml.etree as _etree

from ncclient import manager
from ncclient.operations.rpc import RPCError
from ncclient.transport.errors import AuthenticationError, SSHError


def _connect(conn):
    return manager.connect(
        host=conn["host"],
        port=conn["port"],
        username=conn["user"],
        password=conn["password"],
        hostkey_verify=False,
        device_params={"name": "junos"},
        timeout=conn["timeout"],
        allow_agent=False,
        look_for_keys=False,
    )


def is_alive(conn, args) -> dict:
    device_name = conn.get("device_name") or conn["host"]
    try:
        with _connect(conn) as m:
            if conn.get("command_timeout") is not None:
                m.timeout = conn["command_timeout"]
            try:
                rpc_reply = m.command(command="show version", format="text")
                output_nodes = rpc_reply.xpath(".//output")
                output = output_nodes[0].text if output_nodes else ""
                return {"success": True, "alive": True, "host": conn["host"], "device_name": device_name, "output": output or ""}
            except RPCError as e:
                return {"success": False, "alive": False, "host": conn["host"], "device_name": device_name, "error": str(e)}
    except (AuthenticationError, SSHError) as e:
        return {"success": False, "alive": False, "host": conn["host"], "device_name": device_name, "error": str(e), "error_type": type(e).__name__}
    except Exception as e:
        return {"success": False, "alive": False, "host": conn["host"], "device_name": device_name, "error": str(e), "error_type": type(e).__name__}


def run_command(conn, args) -> dict:
    if not args.command:
        return {"success": False, "host": conn["host"], "error": "command is required for action=run-command"}
    results = []
    try:
        with _connect(conn) as m:
            if conn.get("command_timeout") is not None:
                m.timeout = conn["command_timeout"]
            for cmd in args.command:
                try:
                    rpc_reply = m.command(command=cmd, format="text")
                    output_nodes = rpc_reply.xpath(".//output")
                    output = output_nodes[0].text if output_nodes else rpc_reply.xml
                    results.append({"command": cmd, "output": output or "", "success": True})
                except RPCError as e:
                    results.append({"command": cmd, "output": "", "success": False, "error": str(e)})
        return {"success": all(r["success"] for r in results), "host": conn["host"], "results": results}
    except Exception as e:
        return {"success": False, "host": conn["host"], "error": str(e), "error_type": type(e).__name__, "results": results}


_CONFIG_FORMATS = ("xml", "text", "set", "json")


def get_config(conn, args) -> dict:
    fmt = conn.get("config_format") or "xml"
    if fmt not in _CONFIG_FORMATS:
        return {"success": False, "host": conn["host"], "error": f"unsupported config_format {fmt!r}; choose from {_CONFIG_FORMATS}"}
    if fmt != "xml" and args.source == "candidate":
        return {"success": False, "host": conn["host"], "error": "config_format text/set/json reads from running only; use xml for candidate datastore"}
    try:
        with _connect(conn) as m:
            if fmt == "xml":
                reply = m.get_config(source=args.source, filter=("subtree", args.filter) if args.filter else None)
                try:
                    tree = _etree.fromstring(reply.data_xml.encode())
                    config_xml = _etree.tostring(tree, pretty_print=True).decode().strip()
                except Exception:
                    config_xml = reply.data_xml
                return {"success": True, "host": conn["host"], "source": args.source, "config_format": fmt, "config": config_xml}
            cmd = "show configuration"
            if fmt == "set":
                cmd += " | display set"
            elif fmt == "json":
                cmd += " | display json"
            rpc_reply = m.command(command=cmd, format="text")
            # show configuration variants return <configuration-output> or <json-output>,
            # not <output>; fall through all three xpaths before giving up.
            output_nodes = (rpc_reply.xpath(".//configuration-output")
                            or rpc_reply.xpath(".//json-output")
                            or rpc_reply.xpath(".//output"))
            output = (output_nodes[0].text or "").strip()
            return {"success": True, "host": conn["host"], "source": "running", "config_format": fmt, "config": output}
    except Exception as e:
        return {"success": False, "host": conn["host"], "error": str(e), "error_type": type(e).__name__}


def _acquire_candidate_lock(m, timeout: int, poll_interval: float) -> float:
    deadline = time.monotonic() + max(timeout, 0)
    start = time.monotonic()
    while True:
        try:
            m.lock(target="candidate")
            return time.monotonic() - start
        except RPCError as e:
            msg = str(e).lower()
            transient = (
                getattr(e, 'tag', None) == 'lock-denied'
                or "lock-denied" in msg
                or "lock denied" in msg
                or "in-use" in msg
                or "in use" in msg
                or "configuration database locked" in msg
            )
            if not transient or timeout == 0 or time.monotonic() >= deadline:
                raise
            time.sleep(poll_interval)


def send_command(conn, args) -> dict:
    device_name = conn.get("device_name") or conn["host"]
    if not args.command:
        return {"success": False, "host": conn["host"], "device_name": device_name, "error": "command is required for action=send-command"}
    fmt = conn.get("config_format") or "set"
    if fmt not in _CONFIG_FORMATS:
        return {"success": False, "host": conn["host"], "device_name": device_name, "error": f"unsupported config_format {fmt!r}; choose from {_CONFIG_FORMATS}"}
    dry_run = getattr(args, "dry_run", False)
    confirmed = getattr(args, "confirmed", False)
    confirm_timeout = getattr(args, "confirm_timeout", None) or 10
    try:
        with _connect(conn) as m:
            lock_wait = _acquire_candidate_lock(m, conn["lock_timeout"], conn["lock_poll_interval"])
            try:
                config_text = "\n".join(args.command)
                if fmt == "set":
                    m.load_configuration(action="set", config=config_text)
                elif fmt == "text":
                    m.load_configuration(action="merge", format="text", config=config_text)
                elif fmt == "xml":
                    m.load_configuration(format="xml", config=config_text)
                elif fmt == "json":
                    m.load_configuration(format="json", config=config_text)

                if dry_run:
                    validate_reply = m.validate(source="candidate")
                    try:
                        validate_xml = validate_reply.xml
                    except AttributeError:
                        validate_xml = str(validate_reply)
                    m.discard_changes()
                    result = {
                        "success": True,
                        "host": conn["host"],
                        "device_name": device_name,
                        "commands": args.command,
                        "lock_wait_seconds": round(lock_wait, 2),
                        "dry_run": True,
                        "validate": validate_xml,
                    }
                    if hasattr(args, '_changes_list'):
                        result["_changes_list"] = args._changes_list
                    return result

                commit_reply = m.commit(confirmed=confirmed, timeout=confirm_timeout if confirmed else None)
                try:
                    commit_xml = commit_reply.xml
                except AttributeError:
                    # Junos ncclient returns NCElement (not RPCReply); str() gives XML
                    try:
                        commit_xml = str(commit_reply)
                    except Exception:
                        commit_xml = ''
                result = {
                    "success": True,
                    "host": conn["host"],
                    "device_name": device_name,
                    "commands": args.command,
                    "lock_wait_seconds": round(lock_wait, 2),
                    "commit": commit_xml,
                }
                if confirmed:
                    result["confirmed"] = True
                    result["confirm_timeout_minutes"] = confirm_timeout
                if hasattr(args, '_changes_list'):
                    result["_changes_list"] = args._changes_list
                return result
            except Exception as inner:
                try:
                    m.discard_changes()
                except Exception:
                    pass
                return {
                    "success": False,
                    "host": conn["host"],
                    "device_name": device_name,
                    "commands": args.command,
                    "error": str(inner),
                    "error_type": type(inner).__name__,
                }
            finally:
                try:
                    m.unlock(target="candidate")
                except Exception:
                    pass
    except Exception as e:
        return {"success": False, "host": conn["host"], "device_name": device_name, "error": str(e), "error_type": type(e).__name__}


def reboot(conn, args) -> dict:
    rpc_completed = False
    rpc_result = {}
    try:
        with _connect(conn) as m:
            rpc = "<request-reboot>"
            if args.at:
                rpc += f"<at>{_xml_escape(args.at)}</at>"
            if args.message:
                rpc += f"<message>{_xml_escape(args.message)}</message>"
            rpc += "</request-reboot>"
            reply = m.rpc(rpc)
            rpc_completed = True
            rpc_result = {"success": True, "host": conn["host"], "at": args.at, "response": reply.xml}
        return rpc_result
    except Exception as e:
        if rpc_completed:
            # RPC reply was received; session closed during cleanup because device is rebooting.
            return rpc_result
        return {"success": False, "host": conn["host"], "error": str(e), "error_type": type(e).__name__}


_DISPATCH = {
    "is-alive": is_alive,
    "run-command": run_command,
    "get-config": get_config,
    "send-command": send_command,
    "set-config": send_command,   # broker alias — same logic, distinct output envelope
    "reboot": reboot,
}


def _read_stdin_inventory():
    """Read the InventoryInfo JSON gateway5 pipes to stdin. Returns None if no data."""
    if sys.stdin.isatty():
        return None
    raw = sys.stdin.read()
    if not raw or not raw.strip():
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict) or "inventory_nodes" not in data:
        return None
    nodes = data.get("inventory_nodes") or []
    if not nodes:
        return None
    return nodes[0]


def _resolve_connection(args, node):
    """Merge connection params: CLI args win over inventory attributes."""
    attrs = (node or {}).get("attributes", {}) or {}
    netconf_opts = (attrs.get("itential_driver_options") or {}).get("netconf") or {}

    def pick(cli_val, *attr_paths, default=None):
        if cli_val is not None:
            return cli_val
        for path in attr_paths:
            cursor = attrs
            for k in path:
                if not isinstance(cursor, dict):
                    cursor = None
                    break
                cursor = cursor.get(k)
            if cursor is not None:
                return cursor
        return default

    host = pick(args.host, ("itential_host",))
    user = pick(args.user, ("itential_user",))
    password = pick(args.password, ("itential_password",))
    port = pick(args.port, ("itential_driver_options", "netconf", "port"), default=830)
    timeout = pick(args.timeout, ("itential_driver_options", "netconf", "timeout"), default=30)
    command_timeout = pick(args.command_timeout, ("itential_driver_options", "netconf", "command_timeout"), default=None)
    config_format = pick(args.config_format, ("itential_driver_options", "netconf", "config_format"), default=None)
    lock_timeout = pick(args.lock_timeout, ("itential_driver_options", "netconf", "lock_timeout"), default=30)
    lock_poll_interval = pick(args.lock_poll_interval, ("itential_driver_options", "netconf", "lock_poll_interval"), default=2.0)

    missing = [name for name, val in [("host", host), ("user", user), ("password", password)] if not val]
    if missing:
        raise SystemExit(
            f"missing required connection field(s): {', '.join(missing)} "
            f"(provide via --{missing[0]} or inventory attribute itential_{missing[0]})"
        )

    return {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "timeout": int(timeout),
        "command_timeout": int(command_timeout) if command_timeout is not None else None,
        "config_format": str(config_format) if config_format is not None else None,
        "lock_timeout": int(lock_timeout),
        "lock_poll_interval": float(lock_poll_interval),
        "device_name": (node or {}).get("name") or host,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Junos NETCONF operations for IAG5")
    parser.add_argument("--op", default=os.environ.get("JUNOS_OP"),
                        choices=["get-config", "is-alive", "reboot", "run-command", "send-command", "set-config"],
                        help="Operation to perform. Defaults to JUNOS_OP env var.")

    parser.add_argument("--host", default=None, help="Override the inventory's itential_host")
    parser.add_argument("--port", type=int, default=None, help="Override the inventory's netconf port")
    parser.add_argument("--user", default=None, help="Override the inventory's itential_user")
    parser.add_argument("--password", default=None, help="Override the inventory's itential_password")
    parser.add_argument("--timeout", type=int, default=None, help="Override the netconf session timeout")
    parser.add_argument("--command-timeout", type=int, default=None,
                        help="Override RPC wait timeout for run-command (use for slow ops like software add)")
    parser.add_argument("--config_format", "--config-format", dest="config_format", default=None, choices=list(_CONFIG_FORMATS),
                        help="Config format for get-config/send-command: xml (default), text (curly), set, json")
    parser.add_argument("--lock_timeout", "--lock-timeout", dest="lock_timeout", type=int, default=None,
                        help="Override candidate-lock wait for send-command (0 = no wait)")
    parser.add_argument("--lock-poll-interval", type=float, default=None,
                        help="Override candidate-lock retry interval")

    parser.add_argument("--command", action="append", default=None,
                        help="Operational or set-style command (repeatable; multi-line values are split into separate commands)")
    parser.add_argument("--commands", default=None,
                        help="JSON array of set-style config commands for junos-netconf-send-command workflow task")
    parser.add_argument("--dry_run", "--dry-run", dest="dry_run", nargs="?", const=True, default=None,
                        help="Validate candidate config without committing (flag or true/false)")
    parser.add_argument("--confirmed", nargs="?", const=True, default=None,
                        help="Use confirmed commit — auto-rolls back unless a second commit arrives (flag or true/false)")
    parser.add_argument("--confirm_timeout", "--confirm-timeout", dest="confirm_timeout", type=int, default=None,
                        help="Minutes before auto-rollback for confirmed commit (default 10)")
    parser.add_argument("--config", default=None,
                        help="Multi-line set-style config block for junos-netconf-send-config workflow task")
    parser.add_argument("--config_content", "--config-content", dest="config_content", default=None,
                        help="Multi-line set-style config block (Config Manager remediation path)")
    parser.add_argument("--changes", default=None,
                        help="Config Manager changes array (JSON string) — extracts non-null 'new' values as config lines")
    parser.add_argument("--options", default=None,
                        help="Config Manager remediation options JSON (currently unused)")
    parser.add_argument("--source", default=None,
                        help="Datastore for get-config (running|candidate); defaults to running. Empty string treated as unset.")
    parser.add_argument("--filter", default=None, help="Optional subtree filter for get-config")
    parser.add_argument("--at", default=None, help="Junos time spec for reboot (e.g. '+5')")
    parser.add_argument("--message", default=None, help="Optional broadcast message for reboot")

    return parser


def _normalize_args(args):
    """The IM/MOP framework injects empty-string CLI args for every decorator-defined
    optional string field (e.g. --filter= --source= --at=). Normalize those to None
    so downstream code can treat them as 'unset'. Also splits multi-line --command
    values into separate commands — the MOP command-template framework joins
    multiple template lines with newlines into one --command value."""
    for attr in ("source", "filter", "at", "message", "host", "user", "password", "config", "config_content", "commands", "options"):
        if getattr(args, attr, None) == "":
            setattr(args, attr, None)

    # IAG5 passes booleans as "true"/"false" strings
    for attr in ("dry_run", "confirmed"):
        val = getattr(args, attr, None)
        if val is None or val == "":
            setattr(args, attr, False)
        elif isinstance(val, str):
            setattr(args, attr, val.lower() in ("true", "1", "yes"))

    # junos-netconf-send-command workflow task: --commands='["set ...", "set ..."]' (JSON array)
    if args.commands and not args.command:
        raw = args.commands
        try:
            cmds = json.loads(raw) if isinstance(raw, str) else raw
            if isinstance(cmds, list):
                args.command = [str(c) for c in cmds if str(c).strip()]
            else:
                args.command = [str(cmds)] if str(cmds).strip() else None
        except (json.JSONDecodeError, TypeError):
            args.command = [raw] if raw.strip() else None
    args.commands = None

    # broker paths pass --config or --config_content instead of --command; fold them in
    if args.config and not args.command:
        # adapter-inventory_manager passes the CM changes array as --config; detect and extract
        config_val = args.config.strip()
        if config_val.startswith('['):
            try:
                changes_list = json.loads(config_val)
                lines = []
                for c in changes_list:
                    new_val = str(c.get("new", "")).strip()
                    old_val = str(c.get("old", "")).strip()
                    if new_val:
                        lines.append(new_val)
                    elif old_val:
                        # Deletion: convert "set x y z" → "delete x y z"
                        if old_val.startswith("set "):
                            lines.append("delete " + old_val[4:])
                        elif not old_val.startswith("delete "):
                            lines.append("delete " + old_val)
                        else:
                            lines.append(old_val)
                if lines:
                    args.command = lines
                    args._changes_list = changes_list
            except (json.JSONDecodeError, TypeError, KeyError, AttributeError):
                args.command = [args.config]
        else:
            args.command = [args.config]
    args.config = None

    if args.config_content and not args.command:
        args.command = [args.config_content]
    args.config_content = None

    # Config Manager broker path: --changes '[{"parents":[],"old":...,"new":"set ..."}]'
    if args.changes and not args.command:
        raw = args.changes
        try:
            changes_list = json.loads(raw) if isinstance(raw, str) else raw
            lines = []
            for c in changes_list:
                new_val = str(c.get("new", "")).strip()
                old_val = str(c.get("old", "")).strip()
                if new_val:
                    lines.append(new_val)
                elif old_val:
                    if old_val.startswith("set "):
                        lines.append("delete " + old_val[4:])
                    elif not old_val.startswith("delete "):
                        lines.append("delete " + old_val)
                    else:
                        lines.append(old_val)
            if lines:
                args.command = lines
                args._changes_list = changes_list
        except (json.JSONDecodeError, TypeError, KeyError, AttributeError):
            pass
    args.changes = None

    if args.command:
        split = []
        for raw in args.command:
            if raw is None:
                continue
            for line in raw.splitlines():
                line = line.strip()
                if line:
                    split.append(line)
        args.command = split or None

    if args.source is None:
        args.source = "running"
    if args.source not in ("running", "candidate"):
        raise SystemExit(f"--source must be 'running' or 'candidate', got {args.source!r}")


def _format_for_humans(result, op):
    """run-command and get-config render as plain text so MOP command-template
    rules and the IAP UI show real line breaks instead of JSON-escaped \\n.
    is-alive outputs the bare string 'true' or 'false' (no newline, no JSON
    wrapper) — gw-manager's state endpoint parses stdout and expects exactly
    that literal string to set connectivity.
    Other ops keep the JSON envelope — they don't have natural text output."""
    if op == "is-alive":
        return "true" if result.get("alive", False) else "false"

    if op == "run-command":
        results = result.get("results") or []
        if not results:
            return f"ERROR: {result.get('error', 'connection failed')}"
        if len(results) == 1:
            r = results[0]
            text = r.get("output", "")
            if not r.get("success"):
                text = f"ERROR: {r.get('error', 'unknown error')}\n{text}".rstrip()
            return text
        parts = []
        for r in results:
            parts.append(f"=== {r['command']} ===")
            if not r.get("success"):
                parts.append(f"ERROR: {r.get('error', 'unknown error')}")
            if r.get("output"):
                parts.append(r["output"])
        return "\n".join(parts)

    if op == "get-config":
        if not result.get("success"):
            return f"ERROR: {result.get('error', 'config retrieval failed')}"
        return result.get("config", "")

    if op == "set-config":
        if result.get("success"):
            changes_list = result.get("_changes_list")
            if changes_list:
                output = [
                    {"result": True, "parents": c.get("parents", []), "old": c.get("old", ""), "new": c.get("new", "")}
                    for c in changes_list
                ]
            else:
                # Fallback when no original changes object available (e.g. --config_content path)
                output = [{"result": True, "parents": [], "old": "", "new": cmd} for cmd in (result.get("commands") or [])]
            return json.dumps(output)
        else:
            print(result.get("error", "Configuration failed"), file=sys.stderr)
            return "[]"

    return json.dumps(result, indent=2, default=str)


def main() -> int:
    args = build_parser().parse_args()
    if not args.op:
        raise SystemExit("--op flag or JUNOS_OP env var must be set")
    _normalize_args(args)
    node = _read_stdin_inventory()
    conn = _resolve_connection(args, node)
    result = _DISPATCH[args.op](conn, args)
    print(_format_for_humans(result, args.op), end="" if args.op == "is-alive" else "\n")
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
