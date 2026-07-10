# Delinea Secret Server — Custom Secret Provider for IAG

Itential Automation Gateway (IAG) 5.5 added support for **external secret providers**: instead of storing credentials in IAG's own encrypted store, IAG resolves them at execution time from an external secrets system. Out of the box it supports **HashiCorp Vault (KV v2)** and **CyberArk CCP**. Delinea Secret Server isn't a built-in type, so this uses the third option — **`plugin`** — a small executable you provide that IAG calls to fetch a secret on demand.

This writes up a working Delinea Secret Server Cloud integration: a Python plugin, the registration steps, how to reference the resulting alias from a device inventory (tested via a NetBox → IAG sync), and the non-obvious bugs we hit getting there.

## Architecture

```
Itential Platform (Inventory Manager / NetBox sync)
        │  device attribute: "itential_password": "$GATEWAYSECRET_(IOSXE-PASSWORD)"
        ▼
IAG5 Gateway  ──(resolves alias)──▶  delinea-plugin.py  ──(OAuth2 password grant)──▶  Delinea Secret Server Cloud
        │
        ▼
NetSDK broker (netmiko) ──▶ target device, using the resolved plaintext password
```

IAG resolves the `$GATEWAYSECRET_(...)` reference just before the value is used (e.g. before a NetSDK broker call), so the plaintext password is never stored in Inventory Manager, in the sync template, or in IAG's own database — only the alias name is.

## Prerequisites

- **IAG 5.5+, standard build.** We initially hit this on a `-flowai` internal build variant that reported version `5.5.0` but did *not* have the `secret-provider` feature at all (`iagctl create --help` had no `secret-provider` subcommand). If you don't see `secret-provider` / `secret-providers` in `iagctl create --help` / `iagctl get --help`, you're likely on a build that predates or excludes this feature — check with an unmodified 5.5.0 release build before assuming your Delinea setup is broken.
- A Delinea Secret Server Cloud tenant (`https://<tenant>.secretservercloud.com`) and a service account (or your own account, for testing) with access to the target secret.
- Python 3 on the IAG host (already required by IAG itself).

## How Delinea Secret Server API Access Works

Secret Server Cloud uses OAuth2 password grant, not a static API key:

1. `POST {base_url}/oauth2/token` with form body `grant_type=password&username=<user>&password=<pw>` (add `domain=<domain>` only if not using the default `Local` domain). Returns `access_token` + `refresh_token`.
2. `GET {base_url}/api/v1/secrets/{id}/fields/{fieldSlug}` with `Authorization: Bearer <access_token>` to fetch a specific field's value (e.g. `password`, `username`).

The secret `{id}` is the numeric ID Secret Server assigns (visible in the secret's URL, e.g. `.../app/#/secrets/382/general`) — the API addresses secrets by ID, not by name.

## The Plugin

IAG invokes the plugin as `<command> get`, writing a JSON request to stdin and reading a JSON response from stdout:

**Request (stdin):**
```json
{
  "path": "382",
  "key": "password",
  "config": {
    "env": {
      "DELINEA_BASE_URL": "https://<tenant>.secretservercloud.com",
      "DELINEA_USERNAME": "svc-account",
      "DELINEA_DOMAIN": "Local",
      "DELINEA_PASSWORD_FILE": "/etc/gateway/delinea_password"
    }
  }
}
```

**Response (stdout, exit 0):**
```json
{"value": "the-plaintext-secret"}
```

On failure: write a message to stderr and exit non-zero.

```python
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
```

Save this as `delinea-plugin.py` on the IAG host (e.g. `/opt/gateway/delinea-plugin.py`), then:

```bash
chmod +x /opt/gateway/delinea-plugin.py
```

## Storing the Password

Never pass the Secret Server account's password as a raw `--env` value — it would land in the gateway's stored provider config and in shell/process history. Instead, write it to a file the plugin reads at runtime:

```bash
sudo tee /etc/gateway/delinea_password <<< 'the-service-account-password' > /dev/null
sudo chown itential:itential /etc/gateway/delinea_password
sudo chmod 400 /etc/gateway/delinea_password
```

Only `DELINEA_PASSWORD_FILE` (a path, not a secret) gets passed to the plugin via `--env`.

**Important:** the plugin subprocess does **not** inherit the gateway service's own systemd environment — it's sandboxed and only receives what's explicitly passed via `--env` at registration time, delivered through the JSON on stdin (`config.env`), not as real OS environment variables. Read config from the parsed JSON, not `os.environ`, as shown above.

## Registering the Provider and Alias

```bash
# Provider: registers the plugin and its non-sensitive config
iagctl create secret-provider delinea-plugin \
  --type plugin \
  --command /opt/gateway/delinea-plugin.py \
  --env DELINEA_BASE_URL=https://<tenant>.secretservercloud.com \
  --env DELINEA_USERNAME=svc-account \
  --env DELINEA_DOMAIN=Local \
  --env DELINEA_PASSWORD_FILE=/etc/gateway/delinea_password \
  --description "Delinea Secret Server Cloud via OAuth2 password grant"

# Alias: maps a friendly name to a specific secret + field on that provider
iagctl create secret IOSXE-PASSWORD \
  --provider delinea-plugin \
  --secret 382 \
  --key password
```

Verify:
```bash
iagctl get secret-providers
iagctl describe secret IOSXE-PASSWORD
```

`describe secret` only shows the alias's metadata (provider/secret/key) — never the resolved value. That's by design.

## Referencing the Alias

Use `$GATEWAYSECRET_(alias-name)` anywhere IAG resolves secrets at execution time — we validated it directly inside a device's inventory attributes, synced from NetBox:

```json
{
  "name": "device-name",
  "attributes": {
    "itential_host": "10.0.25.20",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "cisco_xe",
    "itential_user": "itential",
    "itential_password": "$GATEWAYSECRET_(IOSXE-PASSWORD)",
    "itential_driver_options": {
      "netmiko": {
        "banner_timeout": 60,
        "conn_timeout": 60,
        "enable_fast_mode": true,
        "global_delay_factor": 3,
        "read_timeout_override": 600,
        "session_timeout": 300
      }
    }
  }
}
```

IAG resolves the alias just before invoking the NetSDK broker (`is-alive`, `get-config`, etc.), so the real password is fetched fresh from Secret Server on every call rather than stored anywhere on the platform.

## Bugs We Hit Along the Way (and Fixes)

1. **`$gateway_secret_(...)` doesn't exist — it's `$GATEWAYSECRET_(...)`.** Published docs (at the time of writing) show the lowercase-with-underscore form. The actual reference syntax in the platform code is `$GATEWAYSECRET_(alias-name)`, no underscore between GATEWAY and SECRET, all caps. Using the wrong syntax fails silently — IAG passes the literal string straight through as the password, with no error logged anywhere.

2. **Secret Server's field endpoint returns a JSON string literal, not a bare value.** `GET /api/v1/secrets/{id}/fields/{slug}` returns something like `"itential"` — quotes included. If your plugin does a naive `response.read().decode()` and uses that directly, the actual value used is `"itential"` (10 characters, quotes and all) instead of `itential` (8 characters), and device auth fails with no indication why. Always `json.loads()` the field response.

3. **Plugin subprocess environment is sandboxed.** Don't assume the plugin inherits the gateway service's systemd environment, even though *other* IAG service types (e.g. `python-script` services) do. Config only arrives via the JSON on stdin (`config.env`) — read it from there, not `os.environ`, or your plugin will silently fail with "must be set" errors despite the provider registration looking correct.

4. **(Unrelated to Delinea specifically, but worth knowing) `GATEWAY_SERVER_API_KEY_EXPIRATION` expects an integer, not a Go duration string.** If you see `iagctl login` succeed and the very next authenticated call fail with "api key has expired. please login" — even in the same session, immediately — check for a systemd environment override like `GATEWAY_SERVER_API_KEY_EXPIRATION=720h`. It needs a plain integer in minutes (e.g. `43200` for 30 days), matching the `api_key_expiration` value in `gateway.conf`. A duration-string value appears to parse to a near-zero expiration, so every token is born already expired.

## Testing Checklist

- [ ] `iagctl get secret-providers` shows your provider
- [ ] `iagctl describe secret <alias>` shows the correct provider/secret/key (metadata only, no value)
- [ ] Gateway log (`journalctl -u iagctl`) shows `secret_resolution alias="..." provider="..." path="..." outcome=success` for a real call — if you don't see this line at all for your test call, the alias syntax isn't being recognized (see bug #1)
- [ ] The actual device/API call using the resolved secret succeeds — resolution succeeding is not the same as the value being correct (see bug #2)
