"""IG5 utilities for the f5-rest driver.

Private to device-drivers/f5-rest/ — not a shared library. Imported via:

    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from lib.iag import read_stdin_inventory, normalize_args, print_result
"""

import json
import sys


# ---------------------------------------------------------------------------
# Stdin / inventory
# ---------------------------------------------------------------------------

def read_stdin_inventory():
    """Read the InventoryInfo JSON that gateway5 pipes to stdin.

    Returns the first inventory node dict, or None if stdin is a TTY or
    the payload is missing/malformed.
    """
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
    return nodes[0] if nodes else None


# ---------------------------------------------------------------------------
# Config Manager helpers
# ---------------------------------------------------------------------------

def extract_changes(changes_list: list) -> list:
    """Convert a CM changes array to a flat list of config lines.

    New values are used as-is. Deletions are prefixed with 'no ' (generic)
    or 'delete ' for set-format lines starting with 'set '.
    """
    lines = []
    for c in changes_list:
        new_val = str(c.get("new", "") or "").strip()
        old_val = str(c.get("old", "") or "").strip()
        if new_val:
            lines.append(new_val)
        elif old_val:
            if old_val.startswith("set "):
                lines.append("delete " + old_val[4:])
            elif not old_val.startswith(("no ", "delete ")):
                lines.append("no " + old_val)
            else:
                lines.append(old_val)
    return lines


def build_set_config_output(commands: list, changes_list: list) -> list:
    """Build the JSON array that the set-config broker contract expects."""
    if changes_list:
        return [
            {"result": True, "parents": c.get("parents", []),
             "old": c.get("old", ""), "new": c.get("new", "")}
            for c in changes_list
        ]
    return [{"result": True, "parents": [], "old": "", "new": cmd}
            for cmd in commands]


# ---------------------------------------------------------------------------
# Arg normalization
# ---------------------------------------------------------------------------

_DEFAULT_STR_ATTRS = (
    "host", "user", "password", "config", "config_content",
    "commands", "options", "verb", "route", "body",
)


def normalize_args(args, extra_str_attrs=()):
    """Normalize argparse Namespace for IG5 invocation patterns.

    - Empty string args → None (IG5 injects empty strings for unused optional fields)
    - --commands JSON array → --command list
    - --config / --config_content → --command (with CM changes detection)
    - --changes CM array → --command
    - Multi-line --command values are split into separate commands
    """
    for attr in _DEFAULT_STR_ATTRS + tuple(extra_str_attrs):
        if getattr(args, attr, None) == "":
            setattr(args, attr, None)

    if not hasattr(args, "_changes_list"):
        args._changes_list = None

    # --commands JSON array → --command list
    commands = getattr(args, "commands", None)
    command = getattr(args, "command", None)
    if commands and not command:
        try:
            cmds = json.loads(commands) if isinstance(commands, str) else commands
            args.command = [str(c) for c in (cmds if isinstance(cmds, list) else [cmds])
                            if str(c).strip()]
        except (json.JSONDecodeError, TypeError):
            args.command = [commands] if commands.strip() else None
    if hasattr(args, "commands"):
        args.commands = None

    # --config / --config_content → --command (detect CM changes array by leading '[')
    for src_attr in ("config", "config_content"):
        src = getattr(args, src_attr, None)
        if src and not getattr(args, "command", None):
            src = src.strip()
            if src.startswith("["):
                try:
                    changes_list = json.loads(src)
                    lines = extract_changes(changes_list)
                    if lines:
                        args.command = lines
                        args._changes_list = changes_list
                except (json.JSONDecodeError, TypeError):
                    args.command = [src]
            else:
                args.command = [ln.strip() for ln in src.splitlines() if ln.strip()]
        if hasattr(args, src_attr):
            setattr(args, src_attr, None)

    # --changes CM JSON array
    changes = getattr(args, "changes", None)
    if changes and not getattr(args, "command", None):
        try:
            cl = json.loads(changes) if isinstance(changes, str) else changes
            lines = extract_changes(cl)
            if lines:
                args.command = lines
                args._changes_list = cl
        except (json.JSONDecodeError, TypeError):
            pass
    if hasattr(args, "changes"):
        args.changes = None

    # Split multi-line --command values
    command = getattr(args, "command", None)
    if command:
        split = []
        for raw in command:
            if raw is None:
                continue
            for line in raw.splitlines():
                line = line.strip()
                if line:
                    split.append(line)
        args.command = split or None


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_for_humans(result: dict, op: str) -> str:
    """Format an operation result dict for IG5 broker output.

    is-alive  → bare "true"/"false" string (no newline, no JSON)
    run-command → plain text output (or multi-command separator blocks)
    get-config  → plain text config
    set-config  → JSON array of CM result objects
    everything else → pretty JSON
    """
    if op == "is-alive":
        return "true" if result.get("alive") else "false"

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
            return json.dumps(result.get("_output", []))
        print(result.get("error", "Configuration failed"), file=sys.stderr)
        return "[]"

    return json.dumps(result, indent=2, default=str)


def print_result(result: dict, op: str) -> int:
    """Write formatted result to stdout (and stderr on failure). Returns exit code."""
    formatted = format_for_humans(result, op)
    print(formatted, end="" if op == "is-alive" else "\n")
    if not result.get("success"):
        print(formatted, file=sys.stderr)
    return 0 if result.get("success") else 1
