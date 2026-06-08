#!/usr/bin/env python3
"""Ruckus Fastiron netmiko service for IAG5.

SSH CLI-based driver for Ruckus Fastiron (IronWare OS) switches.
Uses netmiko for SSH with paramiko<5 to retain support for ssh-rsa host keys
and legacy KEX algorithms advertised by these devices.

Actions: is-alive, run-command, get-config, send-command, set-config

Connection parameters (host, port, user, password, timeout, device_type) are
read from stdin as JSON in the gateway5 InventoryInfo format:

    {"inventory_nodes": [{"name": "...", "attributes": {
        "itential_host": "...", "itential_user": "...",
        "itential_password": "...",
        "itential_driver_options": {"netmiko": {"port": 22, "timeout": 30, ...}}
    }}]}

CLI flags for connection params override stdin values — useful for local testing.
"""

import argparse
import json
import os
import sys

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException


def _connect(conn):
    kwargs = dict(
        device_type=conn["device_type"],
        host=conn["host"],
        port=conn["port"],
        username=conn["user"],
        password=conn["password"],
        conn_timeout=conn["timeout"],
        # ssh-rsa host keys are disabled by default in paramiko 3.3+; re-enable for legacy devices
        disabled_algorithms={"pubkeys": []},
    )
    if conn.get("secret"):
        kwargs["secret"] = conn["secret"]
    return ConnectHandler(**kwargs)


def is_alive(conn, args) -> dict:
    device_name = conn.get("device_name") or conn["host"]
    try:
        with _connect(conn) as net:
            output = net.send_command("show version")
        return {
            "success": True,
            "alive": True,
            "host": conn["host"],
            "device_name": device_name,
            "output": output,
        }
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as e:
        return {
            "success": False,
            "alive": False,
            "host": conn["host"],
            "device_name": device_name,
            "error": str(e),
            "error_type": type(e).__name__,
        }
    except Exception as e:
        return {
            "success": False,
            "alive": False,
            "host": conn["host"],
            "device_name": device_name,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def run_command(conn, args) -> dict:
    if not args.command:
        return {"success": False, "host": conn["host"], "error": "command is required for action=run-command"}
    results = []
    send_kwargs = {}
    if conn.get("command_timeout") is not None:
        send_kwargs["read_timeout"] = conn["command_timeout"]
    try:
        with _connect(conn) as net:
            for cmd in args.command:
                try:
                    output = net.send_command(cmd, **send_kwargs)
                    results.append({"command": cmd, "output": output, "success": True})
                except Exception as e:
                    results.append({"command": cmd, "output": str(e), "success": False})
        return {"success": all(r["success"] for r in results), "host": conn["host"], "results": results}
    except Exception as e:
        return {
            "success": False,
            "host": conn["host"],
            "error": str(e),
            "error_type": type(e).__name__,
            "results": results,
        }


def get_config(conn, args) -> dict:
    cmd = "show running-config"
    if args.section:
        cmd = f"show running-config {args.section.strip()}"
    try:
        with _connect(conn) as net:
            output = net.send_command(cmd)
        return {
            "success": True,
            "host": conn["host"],
            "section": args.section or None,
            "config": output,
        }
    except Exception as e:
        return {"success": False, "host": conn["host"], "error": str(e), "error_type": type(e).__name__}


def send_command(conn, args) -> dict:
    device_name = conn.get("device_name") or conn["host"]
    if not args.command:
        return {
            "success": False,
            "host": conn["host"],
            "device_name": device_name,
            "error": "command is required for action=send-command",
        }
    try:
        with _connect(conn) as net:
            config_output = net.send_config_set(args.command)
            save_output = net.send_command("write memory")
        result = {
            "success": True,
            "host": conn["host"],
            "device_name": device_name,
            "commands": args.command,
            "output": config_output,
            "save_output": save_output,
        }
        if hasattr(args, "_changes_list"):
            result["_changes_list"] = args._changes_list
        return result
    except Exception as e:
        return {
            "success": False,
            "host": conn["host"],
            "device_name": device_name,
            "commands": args.command,
            "error": str(e),
            "error_type": type(e).__name__,
        }


_DISPATCH = {
    "is-alive":    is_alive,
    "run-command": run_command,
    "get-config":  get_config,
    "send-command": send_command,
    "set-config":  send_command,  # Config Manager broker alias — same logic, distinct output envelope
}


def _read_stdin_inventory():
    """Read the InventoryInfo JSON gateway5 pipes to stdin. Returns None if no data.

    When invoked directly via iagctl (no inventory node), stdin is an open pipe
    with no data and no EOF — select() prevents blocking indefinitely.
    """
    import select
    if sys.stdin.isatty():
        return None
    ready, _, _ = select.select([sys.stdin], [], [], 2.0)
    if not ready:
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
    netmiko_opts = (attrs.get("itential_driver_options") or {}).get("netmiko") or {}

    def pick(cli_val, *attr_keys, default=None):
        if cli_val is not None:
            return cli_val
        for key in attr_keys:
            val = netmiko_opts.get(key)
            if val is not None:
                return val
        for key in attr_keys:
            val = attrs.get(key)
            if val is not None:
                return val
        return default

    host        = pick(args.host,        "itential_host",     default=None)
    user        = pick(args.user,        "itential_user",     default=None)
    password    = pick(args.password,    "itential_password", default=None)
    port        = pick(args.port,        "port",              default=22)
    timeout     = pick(args.timeout,     "timeout",           default=30)
    device_type = pick(args.device_type, "device_type",       default="ruckus_fastiron")
    secret      = pick(args.secret,      "secret",            default=None)
    command_timeout = pick(args.command_timeout, "command_timeout", default=None)

    missing = [name for name, val in [("host", host), ("user", user), ("password", password)] if not val]
    if missing:
        raise SystemExit(
            f"missing required connection field(s): {', '.join(missing)} "
            f"(provide via --{missing[0]} or inventory attribute itential_{missing[0]})"
        )

    return {
        "host":            host,
        "port":            int(port),
        "user":            user,
        "password":        password,
        "timeout":         int(timeout),
        "device_type":     str(device_type),
        "secret":          secret or None,
        "command_timeout": int(command_timeout) if command_timeout is not None else None,
        "device_name":     (node or {}).get("name") or host,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ruckus Fastiron netmiko operations for IAG5")
    parser.add_argument("--op", default=os.environ.get("FASTIRON_OP"),
                        choices=list(_DISPATCH),
                        help="Operation to perform. Defaults to FASTIRON_OP env var.")

    # Connection params
    parser.add_argument("--host",         default=None, help="Override the inventory's itential_host")
    parser.add_argument("--port",         default=None, help="Override SSH port (default 22)")
    parser.add_argument("--user",         default=None, help="Override the inventory's itential_user")
    parser.add_argument("--password",     default=None, help="Override the inventory's itential_password")
    parser.add_argument("--secret",       default=None, help="Enable password (privileged EXEC)")
    parser.add_argument("--timeout",      default=None, help="Override SSH connection timeout (default 30s)")
    parser.add_argument("--command-timeout", "--command_timeout", dest="command_timeout", default=None,
                        help="Override CLI read timeout for run-command (use for slow commands)")
    parser.add_argument("--device-type", "--device_type", dest="device_type", default=None,
                        help="netmiko device type (default: ruckus_fastiron)")

    # Operation params
    parser.add_argument("--command",  action="append", default=None,
                        help="CLI command (repeatable; multi-line values are split into separate commands)")
    parser.add_argument("--commands", default=None,
                        help="JSON array of config commands for send-command workflow task")
    parser.add_argument("--config",   default=None,
                        help="Config block or JSON-encoded Config Manager changes array")
    parser.add_argument("--config_content", "--config-content", dest="config_content", default=None,
                        help="Config block (Config Manager remediation path)")
    parser.add_argument("--changes",  default=None,
                        help="Config Manager changes array (JSON string) — extracts non-null 'new' values as config lines")
    parser.add_argument("--options",  default=None,
                        help="Config Manager remediation options JSON (currently unused)")
    parser.add_argument("--section",  default=None,
                        help="Optional section for get-config (e.g. 'interface ethernet 1/1/1', 'vlan 100')")

    return parser


def _normalize_args(args):
    """Normalise empty-string CLI args injected by the IM/MOP framework to None.
    Also folds --commands (JSON array), --config, --config_content, and --changes
    into args.command for the send-command/set-config handlers."""
    for attr in ("host", "user", "password", "secret", "device_type",
                 "port", "timeout", "command_timeout",
                 "config", "config_content", "commands", "changes", "options", "section"):
        if getattr(args, attr, None) == "":
            setattr(args, attr, None)

    # send-command workflow task: --commands='["interface eth 1/1/1", "port-name uplink"]'
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

    # broker paths pass --config; detect if it is a CM changes array or a plain config block
    if args.config and not args.command:
        config_val = args.config.strip()
        if config_val.startswith("["):
            try:
                changes_list = json.loads(config_val)
                lines = _extract_commands_from_changes(changes_list)
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

    # Config Manager broker path: --changes '[{"parents":[],"old":...,"new":"..."}]'
    if args.changes and not args.command:
        raw = args.changes
        try:
            changes_list = json.loads(raw) if isinstance(raw, str) else raw
            lines = _extract_commands_from_changes(changes_list)
            if lines:
                args.command = lines
                args._changes_list = changes_list
        except (json.JSONDecodeError, TypeError, KeyError, AttributeError):
            pass
    args.changes = None

    # Split multi-line --command values into separate commands
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


def _extract_commands_from_changes(changes_list):
    """Extract device config lines from a Config Manager changes array."""
    lines = []
    for c in changes_list:
        new_val = str(c.get("new", "") or "").strip()
        old_val = str(c.get("old", "") or "").strip()
        if new_val:
            lines.append(new_val)
        elif old_val:
            # Deletion: prefix with 'no' for IronWare CLI style
            if old_val.startswith("no "):
                lines.append(old_val)
            else:
                lines.append(f"no {old_val}")
    return lines


def _format_for_humans(result, op):
    """Format output per operation.

    is-alive:    bare 'true'/'false' — gw-manager parses stdout literally for device state.
    run-command: plain text — IAP UI and MOP templates expect real newlines, not JSON.
    get-config:  plain text config.
    set-config:  JSON array of {result, parents, old, new} — Config Manager contract.
    send-command: JSON envelope.
    """
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
                    {
                        "result": True,
                        "parents": c.get("parents", []),
                        "old": c.get("old", ""),
                        "new": c.get("new", ""),
                    }
                    for c in changes_list
                ]
            else:
                output = [
                    {"result": True, "parents": [], "old": "", "new": cmd}
                    for cmd in (result.get("commands") or [])
                ]
            return json.dumps(output)
        else:
            print(result.get("error", "Configuration failed"), file=sys.stderr)
            return "[]"

    return json.dumps(result, indent=2, default=str)


def main() -> int:
    args = build_parser().parse_args()
    if not args.op:
        raise SystemExit("--op flag or FASTIRON_OP env var must be set")
    _normalize_args(args)
    node = _read_stdin_inventory()
    conn = _resolve_connection(args, node)
    result = _DISPATCH[args.op](conn, args)
    formatted = _format_for_humans(result, args.op)
    print(formatted, end="" if args.op == "is-alive" else "\n")
    if not result.get("success"):
        print(formatted, file=sys.stderr)
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
