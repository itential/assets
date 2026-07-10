#!/usr/bin/env python3
"""IAG custom secret-provider plugin for Azure Key Vault.

IAG invokes this as `azure-plugin.py get`, writing a JSON request to
stdin (`{"path": "<secret name>", "key": "<optional field>", "config":
{"env": {...}}}`) and reading a JSON response from stdout
(`{"value": "..."}`) on success. On failure, write a message to stderr
and exit non-zero.
"""
import sys
import json
import os
import urllib.request
import urllib.parse
import urllib.error


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def read_client_secret(cfg_env):
    secret_file = cfg_env.get("AZURE_CLIENT_SECRET_FILE") or os.environ.get("AZURE_CLIENT_SECRET_FILE")
    if secret_file:
        try:
            with open(secret_file, "r") as f:
                return f.read().strip()
        except OSError as e:
            fail(f"failed to read AZURE_CLIENT_SECRET_FILE: {e}")
    secret = cfg_env.get("AZURE_CLIENT_SECRET") or os.environ.get("AZURE_CLIENT_SECRET")
    if secret:
        return secret
    fail("AZURE_CLIENT_SECRET_FILE or AZURE_CLIENT_SECRET must be set")


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "get":
        fail("usage: azure-plugin.py get")

    try:
        req_in = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        fail(f"failed to parse stdin: {e}")

    path = req_in.get("path")
    key = req_in.get("key", "")
    cfg_env = req_in.get("config", {}).get("env", {})

    vault_url = cfg_env.get("AZURE_VAULT_URL") or os.environ.get("AZURE_VAULT_URL")
    tenant_id = cfg_env.get("AZURE_TENANT_ID") or os.environ.get("AZURE_TENANT_ID")
    client_id = cfg_env.get("AZURE_CLIENT_ID") or os.environ.get("AZURE_CLIENT_ID")
    client_secret = read_client_secret(cfg_env)

    if not vault_url or not tenant_id or not client_id or not client_secret:
        fail("AZURE_VAULT_URL, AZURE_TENANT_ID, AZURE_CLIENT_ID, and a client secret must be set in the plugin's environment")
    if not path:
        fail("no secret name provided")

    vault_url = vault_url.rstrip("/")

    # Step 1: OAuth2 client credentials grant against Azure AD (Entra ID),
    # scoped to Key Vault's own resource.
    form = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://vault.azure.net/.default",
    }
    data = urllib.parse.urlencode(form).encode()
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    try:
        resp = urllib.request.urlopen(token_url, data=data, timeout=15)
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

    # Step 2: fetch the secret by name. Key Vault returns the value as a
    # plain JSON field (unlike some other providers, no extra unwrapping
    # of the response body is needed).
    secret_url = f"{vault_url}/secrets/{path}?api-version=7.4"
    req = urllib.request.Request(secret_url, headers={"Authorization": f"Bearer {token}"})
    try:
        fresp = urllib.request.urlopen(req, timeout=15)
        secret_body = fresp.read()
    except urllib.error.HTTPError as e:
        fail(f"secret fetch failed: status {e.code}")
    except Exception as e:
        fail(f"secret fetch failed: {e}")

    try:
        value = json.loads(secret_body).get("value")
    except json.JSONDecodeError:
        fail("failed to parse secret response")
    if value is None:
        fail("secret response had no value field")

    # Optional: if the secret's value is itself a JSON object (e.g. a
    # username+password pair stored as one secret) and `key` was given,
    # pull that one field out. Otherwise return the value as-is.
    if key:
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict) and key in parsed:
                value = parsed[key]
        except (json.JSONDecodeError, TypeError):
            pass

    print(json.dumps({"value": value}))


if __name__ == "__main__":
    main()
