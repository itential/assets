#!/usr/bin/env python3
import sys
import json
import os
import urllib.request
import urllib.parse
import urllib.error


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def read_password(cfg_env):
    pw_file = cfg_env.get("DELINEA_PASSWORD_FILE") or os.environ.get("DELINEA_PASSWORD_FILE")
    if pw_file:
        try:
            with open(pw_file, "r") as f:
                return f.read().strip()
        except OSError as e:
            fail(f"failed to read DELINEA_PASSWORD_FILE: {e}")
    pw = cfg_env.get("DELINEA_PASSWORD") or os.environ.get("DELINEA_PASSWORD")
    if pw:
        return pw
    fail("DELINEA_PASSWORD_FILE or DELINEA_PASSWORD must be set")


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "get":
        fail("usage: delinea-plugin.py get")

    try:
        req_in = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        fail(f"failed to parse stdin: {e}")

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

    form = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    if domain and domain != "Local":
        form["domain"] = domain

    data = urllib.parse.urlencode(form).encode()
    try:
        resp = urllib.request.urlopen(f"{base_url}/oauth2/token", data=data, timeout=15)
        token_body = resp.read()
    except urllib.error.HTTPError as e:
        fail(f"oauth failed: status {e.code}")
    except Exception as e:
        fail(f"oauth request failed: {e}")

    try:
        token = json.loads(token_body).get("access_token")
    except json.JSONDecodeError:
        token = None
    if not token:
        fail("failed to parse oauth token response")

    field_url = f"{base_url}/api/v1/secrets/{path}/fields/{key}"
    req = urllib.request.Request(field_url, headers={"Authorization": f"Bearer {token}"})
    try:
        fresp = urllib.request.urlopen(req, timeout=15)
        raw_value = fresp.read().decode()
    except urllib.error.HTTPError as e:
        fail(f"secret fetch failed: status {e.code}")
    except Exception as e:
        fail(f"secret fetch failed: {e}")

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
    main()
