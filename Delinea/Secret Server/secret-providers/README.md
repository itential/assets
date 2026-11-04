# Delinea Secret Server — Custom Secret Provider for Itential Gateway

## What This Is

A custom secret-provider plugin so Itential Gateway resolves Delinea Secret Server credentials at runtime instead of storing them in Gateway's own encrypted store — for device inventory passwords, Integration Model API credentials, and other Gateway-executed actions. One less place your team manages credentials, and rotation in Secret Server propagates automatically on the next run — no VPN needed between a SaaS Platform and an on-prem secrets manager, since only Gateway ever resolves the value.

Itential Gateway 5.5+ supports **external secret providers** out of the box for **HashiCorp Vault (KV v2)** and **CyberArk CCP** — see Itential's docs on [configuring a custom secret provider plugin](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider) and [managing secret aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases). Delinea Secret Server isn't a built-in type, so this uses the third option — **`plugin`** — a small executable you provide that Itential Gateway calls to fetch a secret on demand.

## Table of Contents

- [What This Is](#what-this-is)
- [Prerequisites](#prerequisites)
- [How Delinea Secret Server API Access Works](#how-delinea-secret-server-api-access-works)
- [The Plugin](#the-plugin)
- [How the Secret Value Is Handled](#how-the-secret-value-is-handled)
- [Storing the Password](#storing-the-password)
- [Registering the Provider and Alias](#registering-the-provider-and-alias)
- [Referencing the Alias](#referencing-the-alias)
  - [In Device Inventory](#in-device-inventory)
  - [In an Integration Model Instance](#in-an-integration-model-instance)
- [Verifying It's Working](#verifying-its-working)
- [Adapting This Example](#adapting-this-example)
- [References](#references)

## Prerequisites

- Itential Gateway 5.5 or later, with the `secret-provider` feature available (`iagctl create secret-provider --help` should show the `plugin`, `vault`, and `cyberark` provider types). See the [custom plugin provider docs](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider) for the full reference.
- A Delinea Secret Server Cloud tenant (`https://<tenant>.secretservercloud.com`) and a service account with access to the target secret(s).
- Python 3 on the Itential Gateway host (already required by Itential Gateway itself).

## How Delinea Secret Server API Access Works

Secret Server Cloud uses OAuth2 password grant, not a static API key:

1. `POST {base_url}/oauth2/token` with form body `grant_type=password&username=<user>&password=<pw>` (add `domain=<domain>` only if not using the default `Local` domain). Returns `access_token` + `refresh_token`.
2. `GET {base_url}/api/v1/secrets/{id}/fields/{fieldSlug}` with `Authorization: Bearer <access_token>` to fetch a specific field's value (e.g. `password`, `username`). This endpoint returns the value as a JSON-encoded string literal (e.g. `"my-password"`, quotes included) — decode it with a JSON parser rather than using the raw response bytes directly.

The secret `{id}` is the numeric ID Secret Server assigns (visible in the secret's URL, e.g. `.../app/#/secrets/382/general`) — the API addresses secrets by ID, not by name.

## The Plugin

Itential Gateway invokes the plugin as `<command> get`, writing a JSON request to stdin and reading a JSON response from stdout. Configuration (the `--env` values registered with the provider, such as the region or a file path) arrives via the JSON on stdin, in `config.env`. Keep credentials out of these values: reference a file instead (see [Storing the Password](#storing-the-password)). The plugin process does not otherwise inherit Itential Gateway's environment.

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

See [`plugin.py`](./plugin.py) for the full implementation. Copy it to the Itential Gateway host — renaming it to something provider-specific like `delinea-plugin.py` if you'll have more than one provider's plugin on the same host — and make it executable:

```bash
cp plugin.py /opt/gateway/delinea-plugin.py
chmod +x /opt/gateway/delinea-plugin.py
```

## How the Secret Value Is Handled

**The plugin's stdout is an in-memory pipe, not a terminal, a file, or a log.** Itential Gateway starts the plugin as a child process and connects its stdout to a buffer in Gateway's own memory. The `{"value": "..."}` response goes from the plugin into that buffer and nowhere else. It is the same mechanism as `$(command)` in a shell script or a `|` between two programs: nothing is displayed, and nothing is written to disk.

From there:

- Gateway resolves the alias on the Gateway host and passes the value to the device driver, service, or script that referenced it as an environment variable. The plaintext secret is not returned to Itential Platform.
- The pipe and the environment variable have the same access boundary: processes running as the Gateway service account, and root. On Linux, other users on the host cannot read either one (tested: `/proc/<pid>/fd` and `/proc/<pid>/environ` return "Permission denied" to a different user).
- For a successful lookup, Gateway logs one line with the alias, provider, path, and `outcome=success`. The value is not logged (tested on Gateway 5.5.3: a marker value did not appear in CLI output, the systemd journal, or `gateway.log`).

What the plugin does to keep it that way:

- stdout carries only the final `{"value": "..."}` response.
- On failure, Gateway includes the plugin's stderr in its error log without redaction. The plugin therefore writes only fixed text, an HTTP status code, or the provider's error type to stderr. It never writes a secret, a credential, a URL, a command line, or a response body.
- Credentials the plugin itself needs come from a file you control, never from the command line.
- The plugin connects over HTTPS with certificate verification on, does not follow redirects, does not log, and does not write files.
- The service account's password is sent only to `DELINEA_BASE_URL`, which must be an `https://` URL.

What you keep safe:

- Only the account Itential Gateway runs as, and root, can read the secret while Gateway is using it. These are the same accounts that already control Gateway and the devices it logs in to. Other users on the host cannot read it. Limit shell access to the Gateway host as you would for any system that handles credentials.
- Scope the plugin's identity to the specific secrets it needs.

## Storing the Password

Never pass the Secret Server account's password as a raw `--env` value — it would be stored in the gateway's provider configuration. Instead, write it to a file the plugin reads at runtime, and only pass the file path via `--env`:

```bash
# Reads the value without echoing it, so it stays out of shell history
read -rsp 'Service account password: ' SECRET
printf '%s' "$SECRET" | sudo sh -c 'umask 077; cat > /etc/gateway/delinea_password'
unset SECRET
sudo chown itential:itential /etc/gateway/delinea_password
sudo chmod 400 /etc/gateway/delinea_password
```

The file should contain just the raw password as a single line of plain text — no quotes, no `KEY=value` formatting:

```
$ cat /etc/gateway/delinea_password
the-service-account-password
```

The plugin reads the file's contents directly and strips any surrounding whitespace/newline, so a trailing newline (which `tee`/most editors add automatically) is fine.

## Registering the Provider and Alias

Full CLI reference: [configuring a custom secret provider plugin](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider) and [managing secret aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases).

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
iagctl create secret DELINEA-IOSXE-PASSWORD \
  --provider delinea-plugin \
  --secret 382 \
  --key password
```

Verify:
```bash
iagctl get secret-providers
iagctl describe secret DELINEA-IOSXE-PASSWORD
```

`describe secret` only shows the alias's metadata (provider/secret/key) — it never displays the resolved value.

## Referencing the Alias

Use `$GATEWAYSECRET_(alias-name)` anywhere Itential Gateway resolves secrets at execution time. This doc covers two callers in detail below — Inventory Manager Nodes and Integration Model instances — but Gateway resolves the same alias for other Gateway-executed actions too, including Config Manager command templates and GatewayManager tasks like `runService`/`runCode`/`sendCommand`/`sendConfig`. See [Itential Gateway — External Secrets Overview](https://docs.itential.com/itential-gateway/5/secrets/external-secrets/overview) for the complete list. Whichever one triggers it, the path is identical, and the plaintext secret never travels back to Platform:

```
Itential Platform
  • Inventory Manager Nodes
  • Integration Model instances (Gateway-executed)
  • Config Manager command templates
  • GatewayManager tasks (runService, runCode, sendCommand, sendConfig, ...)
        │
        ▼
Itential Gateway
        │  resolves $GATEWAYSECRET_(alias)
        ▼
delinea-plugin.py
        │  OAuth2 password grant
        ▼
Delinea Secret Server Cloud
```

### In Device Inventory

For example, a device synced from NetBox into Itential Platform:

```json
{
  "name": "device-name",
  "attributes": {
    "itential_host": "10.0.25.20",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "cisco_xe",
    "itential_user": "itential",
    "itential_password": "$GATEWAYSECRET_(DELINEA-IOSXE-PASSWORD)",
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

Itential Gateway resolves the alias just before the device driver call, so the real password is fetched fresh from Secret Server on every run rather than stored anywhere on the platform.

### In an Integration Model Instance

The same alias resolves in an **Integration Model instance's** credential fields too, as long as that instance's calls actually execute through Itential Gateway rather than directly from the Platform cluster:

- Set `proxyOverride.executionMode` to `cluster_no_proxy` or `proxy` — **not** `direct`. `direct` means Platform makes the call itself, Gateway is never involved, and the alias won't resolve.
- Optionally set `clusterOverride` to target a specific Gateway cluster instead of the Admin Essentials default.

```json
{
  "security": {
    "apiKey": {
      "value": "$GATEWAYSECRET_(DELINEA-API-TOKEN)"
    }
  },
  "proxyOverride": {
    "overrideProxyBehavior": true,
    "executionMode": "cluster_no_proxy",
    "proxy": {
      "auth": {
        "authMode": "none"
      }
    }
  }
}
```

Gateway resolves the alias just before the outbound call executes, same as the device inventory case — the real token is never sent back to Platform.

## Verifying It's Working

- `iagctl get secret-providers` shows your provider.
- `iagctl describe secret <alias>` shows the correct provider/secret/key.
- The gateway log (`journalctl -u iagctl`) shows a line like `secret_resolution alias="..." provider="..." path="..." outcome=success` for each call that uses the alias.
- The device/API call using the resolved secret succeeds end to end.
- To test the plugin directly, pipe a request into it, using the same `config.env` you registered, and check the result without printing it:
  ```bash
  echo '{"path":"382","key":"password","config":{"env":{"DELINEA_BASE_URL":"https://<tenant>.secretservercloud.com","DELINEA_USERNAME":"svc-account","DELINEA_PASSWORD_FILE":"/etc/gateway/delinea_password"}}}' \
    | /opt/gateway/delinea-plugin.py get \
    | python3 -c 'import sys, json; v = json.load(sys.stdin)["value"]; print("OK: plugin returned a value of", len(v), "characters")'
  ```
  The last command stops the value from reaching your screen. Without it, the plugin's output would print in your terminal and stay in its scrollback. When Itential Gateway runs the plugin, that output goes to Gateway's memory instead. If the plugin fails, its error message appears here, which is what Gateway would log.

## Adapting This Example

- **Different secret templates**: change `--key` to the field slug you need (e.g. `username`, `notes`), or omit `--key` when creating the alias to return the full secret as a JSON object.
- **Multiple secrets**: register one provider, then create as many `secret` aliases as you need against it — each just needs its own `--secret <id>` (and optionally `--key`).
- **Other Delinea deployments**: this targets Secret Server Cloud's OAuth2 password grant. An on-premises Secret Server instance with a different auth model (e.g. Windows-integrated auth) would need the OAuth section of the plugin adjusted accordingly.

## References

- [Itential Gateway — Configure a Custom Plugin Secret Provider](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider)
- [Itential Gateway — Manage Secret Aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases)
- [Delinea Secret Server REST API documentation](https://docs.delinea.com/online-help/secret-server/api-scripting/rest-api/index.htm)
