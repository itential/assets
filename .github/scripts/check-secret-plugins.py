#!/usr/bin/env python3
"""Static checks for secret-provider plugins (any path ending in secret-providers/plugin.py).

Gateway copies a failed plugin's stderr into its error log unredacted, and a plugin
handles live credentials, so these rules block the patterns that have leaked or could
leak them. Add `# secret-plugin: allow (reason)` to a line to accept a reviewed exception.
"""
import pathlib
import re
import sys

RULES = [
    (r'fail\(f?["\'].*\{\s*(e|exc|err|error|detail|body|resp|result)\b(?!\.code\b)[^}]*\}',
     "stderr message interpolates an exception, response or body; use describe_error() or fixed text"),
    (r'\.read\(\)\.decode\(errors', "error response body is read into a message"),
    (r'urlopen\(', "use a no-redirect opener: urllib forwards Authorization headers on redirects"),
    (r'verify\s*=\s*False|_create_unverified_context|CERT_NONE|check_hostname\s*=\s*False', "TLS verification disabled"),
    (r'shell\s*=\s*True|os\.system\(|os\.popen\(', "shell execution"),
    (r'\bimport\s+(logging|traceback|tempfile)\b|\blogging\.|traceback\.', "logging, tracebacks and temp files are not allowed"),
    (r'open\([^)]*,\s*["\'][wax+]', "plugin writes a file"),
    (r'os\.environ\[[^\]]+\]\s*=|os\.putenv\(', "plugin sets environment variables"),
    (r'sys\.stdout\.write\(', "write to stdout only through the single final print()"),
]

def check(path):
    problems = []
    text = path.read_text()
    for n, line in enumerate(text.splitlines(), 1):
        if "secret-plugin: allow" in line or line.lstrip().startswith("#"):
            continue
        for rx, msg in RULES:
            if re.search(rx, line):
                problems.append((n, msg))
        if re.search(r'\bprint\(', line) and "file=sys.stderr" not in line and 'json.dumps({"value"' not in line:
            problems.append((n, "print() that is not the final {\"value\": ...} response or a stderr message"))
    if text.count('print(json.dumps({"value"') != 1:
        problems.append((0, 'expected exactly one {"value": ...} print'))
    if "unexpected error" not in text:
        problems.append((0, "no top-level handler: an uncaught exception prints a traceback to stderr"))
    return problems

def main(argv):
    paths = [pathlib.Path(a) for a in argv] or [p for p in pathlib.Path(".").rglob("secret-providers/plugin.py")]
    bad = 0
    for p in sorted(paths):
        for n, msg in check(p):
            print(f"{p}:{n}: {msg}")
            bad += 1
    print(f"{len(paths)} plugin(s) checked, {bad} problem(s)")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
