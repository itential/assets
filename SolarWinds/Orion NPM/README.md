SolarWinds Orion Network Performance Monitor (NPM) monitors network device health, interface utilization, and availability across an environment. It's built on the Orion Platform, which exposes the SolarWinds Information Service (SWIS) — a query/CRUD API addressed via a SQL-like query language (SWQL) and a small set of generic verbs (Query, Read, Update, Delete, Create, Invoke) applied against entity types, rather than a resource-per-path REST API.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`solarwinds_orion_npm-latest.json`](#solarwinds_orion_npm-latestjson)
  - [`solarwinds_orion_npm-3.0.0.json`](#solarwinds_orion_npm-300json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | SolarWinds Orion NPM (SWIS) OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| SolarWinds Orion Platform | Any version exposing SWIS v3 (NPM module installed) |
| SWIS account | Any Orion user account with API access — no separate API key/token, same credentials as the Orion Web Console |

## Integration Configuration

Import `solarwinds_orion_npm-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Orion Platform's main poller.

Authentication is HTTP Basic, using an Orion user account's own username/password:

```
Authorization: Basic <base64(username:password)>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-orion-username>",
      "password": "<your-orion-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<orion-server>:<port>",
    "base_path": "/SolarWinds/InformationService/v3/Json"
  }
}
```

**Port varies by Orion Platform version:** `17774` is the current default (Orion Platform 2023.1+). `17778` was the default before that and may still be in use on older installations — confirm which port your Orion server actually listens on before configuring the instance.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`solarwinds_orion_npm-latest.json`](./OpenAPIs/solarwinds_orion_npm-latest.json) | latest (curated) | 24 | Trimmed to 24 of 792 upstream operations — see breakdown below |
| [`solarwinds_orion_npm-3.0.0.json`](./OpenAPIs/solarwinds_orion_npm-3.0.0.json) | 3.0.0 | 792 | Full, unmodified vendor spec covering the entire Orion Platform SWIS surface |

### `solarwinds_orion_npm-latest.json`

Sourced from SolarWinds' own officially-published OpenAPI spec ([`solarwinds/OrionSDK`](https://github.com/solarwinds/OrionSDK) on GitHub, served at `solarwinds.github.io/OrionSDK/swagger-ui/`). Trimmed to 24 of 792 upstream operations — the full spec spans SWIS's entire cross-module surface (NCM, SAM/DPI, IPAM, NetPath, SEUM, virtualization, Cisco ACI, agent management, and more), not just NPM.

Resources included:

- **Generic query/CRUD primitives** (usable against any SWIS entity, not just the ones below): `Query`/`QueryWithParameters` (SWQL search), `Read`/`Update`/`Delete` by entity URI, `BulkUpdate`, `BulkDelete`
- **Nodes**: create, unmanage, remanage, poll now
- **Interfaces**: create, discover on node, add to node, unmanage, remanage, set power level
- **Custom Properties**: create/modify/delete for both Nodes and Interfaces
- **Pollers**: create

### `solarwinds_orion_npm-3.0.0.json`

Full, unmodified vendor spec (792 operations, Swagger 2.0 as published) — the entire SWIS API surface across all Orion Platform modules. See `solarwinds_orion_npm-latest.json` above for the curated NPM-focused subset.
