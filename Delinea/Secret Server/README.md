# Delinea Secret Server — Custom Secret Provider for Itential Gateway

Itential Gateway 5.5+ supports **external secret providers**: instead of storing credentials in Itential Gateway's own encrypted store, Itential Gateway resolves them at execution time from an external secrets system. Out of the box it supports **HashiCorp Vault (KV v2)** and **CyberArk CCP** — see Itential's docs on [configuring a custom secret provider plugin](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider) and [managing secret aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases). Delinea Secret Server isn't a built-in type, so this uses the third option — **`plugin`** — a small executable you provide that Itential Gateway calls to fetch a secret on demand.

This is a working example: a Python plugin for Delinea Secret Server Cloud, the registration steps, and how to reference the resulting alias from a device inventory (for example, a NetBox-synced inventory in Itential Platform).

## Architecture

```
Itential Platform (Inventory Manager / device sync)
        │  device attribute: "itential_password": "$GATEWAYSECRET_(DELINEA-IOSXE-PASSWORD)"
        ▼
Itential Gateway  ──(resolves alias)──▶  delinea-plugin.py  ──(OAuth2 password grant)──▶  Delinea Secret Server Cloud
        │
        ▼
Device driver (e.g. netmiko) ──▶ target device, using the resolved plaintext password
```

Itential Gateway resolves the `$GATEWAYSECRET_(...)` reference just before the value is used, so the plaintext password is never stored in Inventory Manager, in a sync template, or in Itential Gateway's own database — only the alias name is.

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

Itential Gateway invokes the plugin as `<command> get`, writing a JSON request to stdin and reading a JSON response from stdout. Configuration (the non-sensitive values registered with the provider) arrives via the JSON on stdin, in `config.env` — the plugin process does not otherwise inherit Itential Gateway's environment.

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

See [`delinea-plugin.py`](./delinea-plugin.py) for the full implementation. Copy it to the Itential Gateway host and make it executable:

```bash
chmod +x /opt/gateway/delinea-plugin.py
```

## Storing the Password

Never pass the Secret Server account's password as a raw `--env` value — it would be stored in the gateway's provider configuration. Instead, write it to a file the plugin reads at runtime, and only pass the file path via `--env`:

```bash
sudo tee /etc/gateway/delinea_password <<< 'the-service-account-password' > /dev/null
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

Use `$GATEWAYSECRET_(alias-name)` anywhere Itential Gateway resolves secrets at execution time — including inside device inventory attributes, for example a device synced from NetBox into Itential Platform:

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

## Verifying It's Working

- `iagctl get secret-providers` shows your provider.
- `iagctl describe secret <alias>` shows the correct provider/secret/key.
- The gateway log (`journalctl -u iagctl`) shows a line like `secret_resolution alias="..." provider="..." path="..." outcome=success` for each call that uses the alias.
- The device/API call using the resolved secret succeeds end to end.

## Adapting This Example

- **Different secret templates**: change `--key` to the field slug you need (e.g. `username`, `notes`), or omit `--key` when creating the alias to return the full secret as a JSON object.
- **Multiple secrets**: register one provider, then create as many `secret` aliases as you need against it — each just needs its own `--secret <id>` (and optionally `--key`).
- **Other Delinea deployments**: this targets Secret Server Cloud's OAuth2 password grant. An on-premises Secret Server instance with a different auth model (e.g. Windows-integrated auth) would need the OAuth section of the plugin adjusted accordingly.

## References

- [Itential Gateway — Configure a Custom Plugin Secret Provider](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider)
- [Itential Gateway — Manage Secret Aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases)
- [Delinea Secret Server REST API documentation](https://docs.delinea.com/online-help/secret-server/api-scripting/rest-api/index.htm)
