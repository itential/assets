# FortiManager

FortiManager is Fortinet's centralized management platform for FortiGate devices, providing policy and object configuration, device provisioning, firmware management, and centralized logging/reporting across a FortiGate fleet.

This project provides an OpenAPI spec covering FortiManager's JSON-RPC API for building automation via an Integration Model — see **OpenAPIs** below.

**Requirements:** Itential Platform >= 6.4 · FortiManager >= 7.2.2 (for Bearer-token API authentication)

## Table of Contents

- [Contents](#contents)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`fortimanager_json_api-latest.json`](#fortimanager_json_api-latestjson)
  - [Why One Operation, and Why Bearer-Only](#why-one-operation-and-why-bearer-only)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/fortimanager_json_api-latest.json](./OpenAPIs/fortimanager_json_api-latest.json) | Single-endpoint Integration Model spec covering FortiManager's JSON-RPC API |

## Integration Configuration

Import `fortimanager_json_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration instance pointed at your FortiManager, authenticating with an API-administrator Bearer token (System Settings > Administrators, or `execute api-user generate-key <name>` in the FortiManager CLI).

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "fortimanager.example.com",
    "base_path": ""
  },
  "authentication": {
    "type": "http",
    "scheme": "bearer",
    "token": "<FortiManager API token>"
  },
  "tls": {
    "enabled": true,
    "rejectUnauthorized": false
  },
  "variables": {},
  "version": "latest"
}
```

Requires FortiManager >= 7.2.2 — older releases only support session-based JSON-RPC auth (a session token returned by an initial login call and echoed back in every subsequent request body), which can't be represented as an Integration Model security scheme. See [Why One Operation, and Why Bearer-Only](#why-one-operation-and-why-bearer-only) below.

## OpenAPIs

### `fortimanager_json_api-latest.json`

FortiManager's entire API surface — policy and object configuration (`pm/config`), device inventory and management (`dvmdb`, `dvm/cmd`), and provisioning workflows (`securityconsole`) — is addressed through **one JSON-RPC 2.0 endpoint** (`POST /jsonrpc`), not per-resource REST paths. This spec exposes that one operation (`jsonRpcCall`) with a generic request/response envelope; a workflow task selects the actual object or action by setting the request body's `method` (the RPC verb — `get`/`add`/`set`/`update`/`delete`/`exec`/`clone`/`move`) and `params[].url` (the target resource path).

The spec's request body includes worked examples for common patterns:

| Example | `method` | `url` | What it does |
|---|---|---|---|
| `getSystemStatus` | `get` | `/sys/status` | FortiManager version/build/status |
| `getAdomList` | `get` | `/dvmdb/adom` | List ADOMs |
| `getManagedDevices` | `get` | `/dvmdb/adom/root/device` | List devices managed in an ADOM |
| `addFirewallAddress` | `add` | `/pm/config/adom/root/obj/firewall/address` | Create a firewall address object |
| `getFirewallPolicies` | `get` | `/pm/config/adom/root/pkg/default/firewall/policy` | Read a policy package's rules |
| `addManagedDevice` | `exec` | `/dvm/cmd/add/device` | Promote a FortiGate into management |
| `installDeviceConfig` | `exec` | `/securityconsole/install/device` | Push the assigned policy package to a device |

See Fortinet's FortiManager JSON API documentation (FNDN) for the full set of `url` paths and object schemas — the spec's `data`/`filter`/`fields` fields are intentionally generic (`additionalProperties: true`) since their shape depends entirely on which object is being addressed.

### Why One Operation, and Why Bearer-Only

Itential Platform's OpenAPI-based Integration Models make literal HTTP calls matching a spec's path and method, so a faithful OpenAPI representation of a single real endpoint can only define one operation — synthetic per-resource paths would just fail at runtime, since FortiManager doesn't expose them as real HTTP routes. This is the Integration Model equivalent of `fortigate-rest-call` on the IG5 side (see the FortiGate product README): one generic passthrough, with workflows supplying the addressing.

Bearer-token auth (FortiManager >= 7.2.2) was chosen deliberately over the older session-based JSON-RPC login — a session token returned by an initial login call, then threaded through every subsequent request body — since that pattern isn't representable as an OpenAPI `securityScheme`, which models auth as a header, query parameter, cookie, or OAuth2 flow, not a value the caller embeds in the request body itself.
