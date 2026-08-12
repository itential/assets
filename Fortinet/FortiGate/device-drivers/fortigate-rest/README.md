# fortigate-rest — IG5 Python script service

Fortinet FortiGate driver using the FortiOS REST API. No SSH required — all
operations go over HTTPS to the FortiGate management interface. Credential
resolution is handled by IG5's built-in mechanism; no vault integration in
this driver.

FortiOS's REST API has real capability limits compared to CLI access — see
[No CLI passthrough](#no-cli-passthrough-run-command--set-config) below
before assuming this behaves identically to a CLI-based driver.

Use the platform's built-in netmiko driver (`itential_platform: fortinet`) if you need SSH/CLI access instead.

## Operations

| Service | Broker contract | What it does |
|---|---|---|
| `fortigate-rest-is-alive` | `is-alive` | `GET /api/v2/monitor/system/status` — returns `true` or `false` |
| `fortigate-rest-get-config` | `get-config` | `GET /api/v2/monitor/system/config/backup` — full CLI-style config as text |
| `fortigate-rest-run-command` | `run-command` | **Not supported** — see below |
| `fortigate-rest-set-config` | `set-config` | **Not supported** — see below |
| `fortigate-rest-call` | — | Generic FortiOS REST passthrough — caller supplies verb, route, and body |

## No CLI passthrough (`run-command` / `set-config`)

**FortiOS's REST API has no endpoint that executes arbitrary CLI commands** —
Fortinet's own support guidance is explicit that CLI commands cannot be sent
over the API. This isn't a gap in this driver; it's a real limitation of the
platform.

Because of that, `run-command` and `set-config` both return a structured
`{"success": false, "error": "..."}` explaining the limitation, rather than
silently doing nothing or faking success. Use `fortigate-rest-call` instead
for anything that needs to change configuration — it can reach any
`/api/v2/cmdb/*` object (FortiOS's structured config model), just not via
raw CLI-style `set`/`config`/`end` text. Use the netmiko option (see the
product README) if you need genuine CLI-style config application.

## Authentication

FortiOS's REST API only supports static API-token (Bearer) authentication —
there is no username/password login flow to obtain a session token. Generate
a token once via an API Administrator account (FortiOS GUI, or
`execute api-user generate-key <name> [expiry-minutes]` in the CLI) and put
it in `itential_password`. It does not expire unless revoked, so this driver
has no token-refresh logic.

## Inventory Manager attributes

```json
{
  "name": "fortigate-01",
  "attributes": {
    "itential_host": "192.0.2.200",
    "itential_port": 443,
    "itential_password": "<FortiOS API token>",
    "itential_driver_options": {
      "fortigate-rest": {
        "vdom": "root",
        "verify_ssl": false,
        "timeout": 30,
        "backup_scope": "global"
      }
    }
  }
}
```

| Attribute | Default | Description |
|---|---|---|
| `itential_host` | — | FortiGate management IP or hostname |
| `itential_port` | `443` | HTTPS management port |
| `itential_password` | — | The FortiOS API token (resolved by IG5). `itential_user` is not used — FortiOS tokens aren't tied to a username at auth time. |
| `vdom` | *(none)* | Virtual domain name to scope `monitor`/`cmdb` calls to. Omit for single-VDOM appliances. |
| `verify_ssl` | `true` | Verify TLS certificate. Set `false` for self-signed certs. |
| `timeout` | `30` | Request timeout in seconds |
| `backup_scope` | `global` | `scope` query param for the `get-config` backup call — `global` or `vdom` |
| `api_token` | — | Overrides `itential_password` as the token source, if you want to keep a separate admin password on the node for other purposes |

## Inventory Manager action mapping

```json
{
  "actions": [
    {
      "name": "is-alive",
      "action_type": "iag5-service",
      "action_config": {
        "service_name": "fortigate-rest-is-alive",
        "cluster_id": "your-cluster-id"
      }
    },
    {
      "name": "get-config",
      "action_type": "iag5-service",
      "action_config": {
        "service_name": "fortigate-rest-get-config",
        "cluster_id": "your-cluster-id"
      }
    }
  ]
}
```

`run-command` and `set-config` are intentionally omitted from this example —
see [No CLI passthrough](#no-cli-passthrough-run-command--set-config).

## rest-call — generic REST passthrough

`fortigate-rest-call` is a workflow task (not a broker action) that lets
workflows call any FortiOS REST endpoint without a device-specific service
per endpoint. The driver handles authentication; the workflow author
supplies the rest.

**Decorator inputs:**

| Field | Required | Description |
|---|---|---|
| `verb` | yes | HTTP method: `GET`, `POST`, `PUT`, `DELETE` |
| `route` | yes | Full FortiOS REST path from root (e.g. `/api/v2/cmdb/firewall/policy`) |
| `body` | no | JSON-encoded request body string |

**Examples:**

List all firewall policies:
```json
{"verb": "GET", "route": "/api/v2/cmdb/firewall/policy"}
```

Create a firewall address object:
```json
{
  "verb": "POST",
  "route": "/api/v2/cmdb/firewall/address",
  "body": "{\"name\": \"web-server-01\", \"subnet\": \"10.0.0.5/32\"}"
}
```

Disable a firewall policy:
```json
{
  "verb": "PUT",
  "route": "/api/v2/cmdb/firewall/policy/1",
  "body": "{\"status\": \"disable\"}"
}
```

The response is the raw JSON from FortiOS (or plain text if FortiOS returns
non-JSON). If the device has a `vdom` configured, it's applied automatically
as a query param unless the route already includes one.

## Known limitations

- **No CLI passthrough** — see above. Use the netmiko option (see the product README) if genuine CLI-style config application is required.
- **`get-config` may return a truncated config on very large or heavily-VDOM'd appliances.** Fortinet customers have reported the `/api/v2/monitor/system/config/backup` endpoint returning a partial config (vs. the full CLI-equivalent backup) in some cases. Verify output completeness against a CLI-based backup if this matters for your use case.

## Local testing

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# is-alive
FORTIGATE_REST_OP=is-alive python main.py \
  --host 192.0.2.200 --password <api-token>

# get-config
FORTIGATE_REST_OP=get-config python main.py \
  --host 192.0.2.200 --password <api-token>

# rest-call (generic REST)
FORTIGATE_REST_OP=rest-call python main.py \
  --host 192.0.2.200 --password <api-token> \
  --verb GET --route /api/v2/cmdb/firewall/policy
```

## Dependencies

- `requests>=2.28.0`
