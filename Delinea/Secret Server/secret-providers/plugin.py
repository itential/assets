#!/usr/bin/env python3
"""IAG custom secret-provider plugin for Delinea Secret Server Cloud.

IAG invokes this as `delinea-plugin.py get`, writing a JSON request to
stdin (`{"path": "<secret id>", "key": "<field slug>", "config": {"env": {...}}}`)
and reading a JSON response from stdout (`{"value": "..."}`) on success.
On failure, write a message to stderr and exit non-zero.

Gateway copies stderr into its error log unredacted, so stderr must never
carry a secret value, a credential, a URL or a response body.
"""
import sys
import json
import os
import urllib.request
import urllib.parse
import urllib.error


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never follow redirects. urllib forwards the Authorization header to the
    redirect target, so following one could send a bearer token to another host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


def describe_error(e):
    """Short description of an exception that is safe to write to stderr.
    Never includes response bodies, URLs, command lines or file names."""
    if isinstance(e, urllib.error.HTTPError):
        return f"HTTP status {e.code}"
    if isinstance(e, urllib.error.URLError):
        return f"{type(e).__name__}: {e.reason}"
    if isinstance(e, OSError) and e.strerror:
        return e.strerror
    return type(e).__name__


def fail(msg):
    """Gateway copies stderr into its error log unredacted. Pass only fixed text
    and values from describe_error(); never a secret, credential, URL or response body."""
    print(msg, file=sys.stderr)
    sys.exit(1)


def read_password(cfg_env):
    pw_file = cfg_env.get("DELINEA_PASSWORD_FILE") or os.environ.get("DELINEA_PASSWORD_FILE")
    if pw_file:
        try:
            with open(pw_file, "r") as f:
                return f.read().strip()
        except OSError as e:
            fail(f"failed to read DELINEA_PASSWORD_FILE: {describe_error(e)}")
    pw = cfg_env.get("DELINEA_PASSWORD") or os.environ.get("DELINEA_PASSWORD")
    if pw:
        return pw
    fail("DELINEA_PASSWORD_FILE or DELINEA_PASSWORD must be set")


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "get":
        fail("usage: delinea-plugin.py get")

    try:
        req_in = json.load(sys.stdin)
    except json.JSONDecodeError:
        fail("failed to parse stdin: invalid JSON")

    path = req_in.get("path")
    key = req_in.get("key", "")
    cfg_env = req_in.get("config", {}).get("env", {})

    base_url = cfg_env.get("DELINEA_BASE_URL") or os.environ.get("DELINEA_BASE_URL")
    username = cfg_env.get("DELINEA_USERNAME") or os.environ.get("DELINEA_USERNAME")
    domain = cfg_env.get("DELINEA_DOMAIN") or os.environ.get("DELINEA_DOMAIN", "")
    password = read_password(cfg_env)

    if not base_url or not username or not password:
        fail("DELINEA_BASE_URL, DELINEA_USERNAME, and a password must be set in the plugin's environment")
    if not path:
        fail("no secret path provided")
    if not base_url.lower().startswith("https://"):
        fail("DELINEA_BASE_URL must start with https://")

    form = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    # "Local" is Secret Server's built-in (non-AD-integrated) domain and is
    # the implicit default — only send `domain` for actual AD/LDAP domains.
    if domain and domain != "Local":
        form["domain"] = domain

    # Step 1: OAuth2 password grant to get a bearer token.
    data = urllib.parse.urlencode(form).encode()
    try:
        resp = _opener.open(f"{base_url}/oauth2/token", data=data, timeout=15)
        token_body = resp.read()
    except urllib.error.HTTPError as e:
        fail(f"oauth failed: status {e.code}")
    except Exception as e:
        fail(f"oauth request failed: {describe_error(e)}")

    try:
        token = json.loads(token_body).get("access_token")
    except json.JSONDecodeError:
        token = None
    if not token:
        fail("failed to parse oauth token response")

    # Step 2: use the token to fetch the specific field value off the secret.
    field_url = (
        f"{base_url}/api/v1/secrets/{urllib.parse.quote(path, safe='')}"
        f"/fields/{urllib.parse.quote(key, safe='')}"
    )
    req = urllib.request.Request(field_url, headers={"Authorization": f"Bearer {token}"})
    try:
        fresp = _opener.open(req, timeout=15)
        raw_value = fresp.read().decode()
    except urllib.error.HTTPError as e:
        fail(f"secret fetch failed: status {e.code}")
    except Exception as e:
        fail(f"secret fetch failed: {describe_error(e)}")

    # Secret Server's field endpoint returns a JSON-encoded string literal
    # (e.g. `"itential"`), not a bare value — decode it, falling back to the
    # raw text for any field type that isn't JSON-quoted.
    try:
        value = json.loads(raw_value)
        if not isinstance(value, str):
            value = raw_value.strip()
    except json.JSONDecodeError:
        value = raw_value.strip()

    print(json.dumps({"value": value}))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # SystemExit from fail() is not an Exception
        # An uncaught exception prints a traceback to stderr, which Gateway copies into its error log.
        fail(f"unexpected error: {type(e).__name__}")
