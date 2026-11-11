"""Brace-style text <-> gNMI JSON tree.

Configuration Manager's Golden Config parses ``get-config`` output as a string. A JSON tree can't be used
there, so the config is rendered as curly-brace text (``name value;`` leaves, ``name { ... }`` containers)
that the stock brace parser reads. Keyed list entries keep their gNMI spelling, ``interface[name=eth0] {``,
so a block's parents join straight back into a gNMI path. Strings that would read back as numbers or booleans
are quoted, so types survive a round trip.
"""

import json
import re

from grpc_driver.errors import DriverError

_BARE = re.compile(r'^[^\s";{}#\\]+$')
_TOKEN = re.compile(
    r'\s+|/\*.*?\*/|#[^\r\n]*|(?P<quoted>"(?:[^"\\]|\\.)*")|(?P<punct>[{};])|(?P<word>[^\s";{}#]+)', re.S)
_INDENT = "    "


# ---------------------------------------------------------------------- render

def _scalar(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    text = str(value)
    if _BARE.match(text) and text not in ("[", "]") and not _coerces(text):
        return text
    return json.dumps(text)


def _coerces(text):
    return text in ("true", "false", "null") or _number(text) is not None


def _number(text):
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text) if re.match(r"^-?\d+\.\d+$", text) else None
    except ValueError:
        return None


def _entries(value):
    """Yield (block name, child) for a dict; list items are named from their ``name`` key."""
    for key, child in value.items():
        if isinstance(child, list) and child and all(isinstance(i, dict) for i in child):
            for index, item in enumerate(child):
                label = item.get("name", item.get("id", index))
                yield f"{key}[{'name' if 'name' in item or 'id' not in item else 'id'}={label}]", item
        else:
            yield key, child


def render(tree, depth=0):
    pad = _INDENT * depth
    lines = []
    for key, child in _entries(tree):
        if isinstance(child, dict):
            if child:
                lines.append(f"{pad}{key} {{")
                lines.append(render(child, depth + 1))
                lines.append(f"{pad}}}")
            else:
                lines.append(f"{pad}{key} {{")
                lines.append(f"{pad}}}")
        elif isinstance(child, list):
            lines.append(f"{pad}{key} [ {' '.join(_scalar(i) for i in child)} ];")
        else:
            lines.append(f"{pad}{key} {_scalar(child)};")
    return "\n".join(line for line in lines if line != "")


def merge(into, value):
    if isinstance(value, dict) and isinstance(into, dict):
        for k, v in value.items():
            into[k] = merge(into.get(k), v) if k in into else v
        return into
    return value


def tree_from_notifications(response, path_elems):
    """Fold a gnmi.get() response into one dict. ``path_elems`` turns a path string into key names."""
    tree = {}
    for note in (response or {}).get("notification", []):
        prefix = note.get("prefix")
        for upd in note.get("update", []):
            if "val" not in upd:
                continue
            names = path_elems(prefix) + path_elems(upd.get("path"))
            node = upd["val"]
            for name in reversed(names):
                node = {name: node}
            merge(tree, node)
    return tree


# ----------------------------------------------------------------------- parse

def _tokens(text):
    for match in _TOKEN.finditer(text):
        if match.group("quoted") is not None:
            yield "word", json.loads(match.group("quoted")), True
        elif match.group("punct") is not None:
            yield "punct", match.group("punct"), False
        elif match.group("word") is not None:
            yield "word", match.group("word"), False


def _value(word, quoted):
    if quoted:
        return word
    if word == "true":
        return True
    if word == "false":
        return False
    if word == "null":
        return None
    number = _number(word)
    return word if number is None else number


def parse(text):
    """Brace text to a dict. Statements end with ``;``; a bare fragment is read one statement per line."""
    text = text or ""
    if not re.search(r"[;{}]", text):
        text = "\n".join(line.rstrip() + ";" for line in text.splitlines() if line.strip())
    root = {}
    stack, words, items = [root], [], None

    def statement():
        nonlocal words
        if not words:
            return
        key, rest = words[0][0], words[1:]
        if not rest:
            stack[-1].setdefault(key, {})
        elif len(rest) == 1 and isinstance(rest[0], list):
            stack[-1][key] = rest[0]
        elif len(rest) == 1:
            stack[-1][key] = _value(*rest[0])
        else:
            stack[-1][key] = " ".join(w[0] for w in rest)
        words = []

    for kind, tok, quoted in _tokens(text):
        if kind == "word" and not quoted and tok == "[":
            items = []
        elif kind == "word" and not quoted and tok == "]":
            words.append(items or [])
            items = None
        elif kind == "word":
            (items if items is not None else words).append(_value(tok, quoted) if items is not None else (tok, quoted))
        elif tok == "{":
            name = " ".join(w[0] for w in words)
            stack.append(stack[-1].setdefault(name, {}))
            words = []
        elif tok == "}":
            statement()
            if len(stack) == 1:
                raise DriverError("Unbalanced '}' in configuration text", "invalid_input")
            stack.pop()
        else:
            statement()
    statement()
    if len(stack) != 1:
        raise DriverError("Unterminated '{' in configuration text", "invalid_input")
    return root
