# f5-rest — IG5 Python script service

F5 BIG-IP driver using the iControl REST API. No SSH required — all operations
go over HTTPS to the BIG-IP management interface. Credential resolution is
handled by IG5's built-in mechanism; no vault integration in this driver.

Use the platform's built-in netsdk driver if you need SSH/TMSH access instead.

## Operations

| Service | Broker contract | What it does |
|---|---|---|
| `f5-rest-is-alive` | `is-alive` | `GET /mgmt/tm/sys/version` — returns `true` or `false` |
| `f5-rest-run-command` | `run-command` | Runs a bash or TMSH command via `/mgmt/tm/util/bash` |
| `f5-rest-get-config` | `get-config` | Runs the configured TMSH command and returns text output |
| `f5-rest-set-config` | `set-config` | Config Manager remediation broker entry point |
| `f5-rest-call` | — | Generic iControl REST passthrough — caller supplies verb, route, and body |

## Authentication

Token-based auth via `POST /mgmt/shared/authn/login`. A fresh token is obtained
at the start of each invocation and used for all subsequent calls. Tokens are
never cached or reused across invocations.

## Inventory Manager attributes

```json
{
  "name": "bigip-01",
  "attributes": {
    "itential_host": "192.0.2.100",
    "itential_port": 443,
    "itential_user": "admin",
    "itential_password": "changeme",
    "itential_driver_options": {
      "f5-rest": {
        "login_provider": "tmos",
        "verify_ssl": false,
        "timeout": 30,
        "get_config_command": "tmsh list all-properties",
        "save_config": true
      }
    }
  }
}
```

| Attribute | Default | Description |
|---|---|---|
| `itential_host` | — | BIG-IP management IP or hostname |
| `itential_port` | `443` | HTTPS management port |
| `itential_user` | — | BIG-IP username |
| `itential_password` | — | BIG-IP password (resolved by IG5) |
| `login_provider` | `tmos` | F5 auth provider — `tmos` for local accounts, or the name of your LDAP/AD/RADIUS provider |
| `verify_ssl` | `true` | Verify TLS certificate. Set `false` for self-signed certs. |
| `timeout` | `30` | Request timeout in seconds |
| `get_config_command` | `tmsh list all-properties` | TMSH command run by `get-config` |
| `save_config` | `true` | Run `tmsh save sys config` after `set-config` |

## Inventory Manager action mapping

```json
{
  "actions": [
    {
      "name": "is-alive",
      "action_type": "iag5-service",
      "action_config": {
        "service_name": "f5-rest-is-alive",
        "cluster_id": "your-cluster-id"
      }
    },
    {
      "name": "run-command",
      "action_type": "iag5-service",
      "action_config": {
        "service_name": "f5-rest-run-command",
        "cluster_id": "your-cluster-id"
      }
    },
    {
      "name": "get-config",
      "action_type": "iag5-service",
      "action_config": {
        "service_name": "f5-rest-get-config",
        "cluster_id": "your-cluster-id"
      }
    },
    {
      "name": "set-config",
      "action_type": "iag5-service",
      "action_config": {
        "service_name": "f5-rest-set-config",
        "cluster_id": "your-cluster-id"
      }
    }
  ]
}
```

## rest-call — generic REST passthrough

`f5-rest-call` is a workflow task (not a broker action) that lets workflows
call any iControl REST endpoint without a device-specific service per endpoint.
The driver handles authentication; the workflow author supplies the rest.

**Decorator inputs:**

| Field | Required | Description |
|---|---|---|
| `verb` | yes | HTTP method: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| `route` | yes | Full iControl path from root (e.g. `/mgmt/tm/ltm/virtual`) |
| `body` | no | JSON-encoded request body string |

**Examples:**

List all virtual servers:
```json
{"verb": "GET", "route": "/mgmt/tm/ltm/virtual"}
```

Add a pool member:
```json
{
  "verb": "POST",
  "route": "/mgmt/tm/ltm/pool/~Common~my-pool/members",
  "body": "{\"name\": \"10.0.0.5:80\"}"
}
```

Disable a node:
```json
{
  "verb": "PATCH",
  "route": "/mgmt/tm/ltm/node/~Common~node-01",
  "body": "{\"session\": \"user-disabled\"}"
}
```

The response is the raw JSON from iControl (or plain text if iControl returns non-JSON).

## Local testing

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# is-alive
F5_REST_OP=is-alive python main.py \
  --host 192.0.2.100 --user admin --password changeme

# run-command
F5_REST_OP=run-command python main.py \
  --host 192.0.2.100 --user admin --password changeme \
  --command "tmsh show sys version"

# rest-call (generic REST)
F5_REST_OP=rest-call python main.py \
  --host 192.0.2.100 --user admin --password changeme \
  --verb GET --route /mgmt/tm/ltm/virtual
```

## Dependencies

- `requests>=2.28.0`
