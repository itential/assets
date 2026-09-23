# Sentinel

Sentinel (Sentinel Express) is Alianza's real-time converged-services platform for network operators, built on the Rhino telecom application server. REM (Rhino Element Manager) exposes a REST interface — the Sentinel Provisioning REST API — for provisioning Sentinel's service-layer resources: subscriber data, service plans, session types, subscriptions, and home zone routing.

This project provides OpenAPI specs for automating against the Sentinel Provisioning REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`sentinel_provisioning-latest.json`](#sentinel_provisioning-latestjson)
  - [`sentinel_provisioning-4.0.0.json`](#sentinel_provisioning-400json)
- [Studio Projects](#studio-projects)
  - [Sentinel Provisioning Project](#sentinel-provisioning-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Sentinel Provisioning REST API OpenAPI specs — curated `-latest` plus the full reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 24 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Sentinel Express | 4.0.0 (the provisioning resource model has been stable across the 2.x–4.x line) |
| `Sentinel Provisioning:latest` Integration Model | Required to build automation against the OpenAPI specs, and to run the Studio Project below |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your REM server.

Authentication is static HTTP Basic, using credentials configured through REM. The API defaults to XML but returns JSON when the request's `Accept` header is set to `application/json`.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-rem-username>",
      "password": "<your-rem-password>"
    }
  },
  "server": {
    "protocol": "http",
    "host": "<your-rem-host>",
    "base_path": "/rem/sentinel/api"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`sentinel_provisioning-latest.json`](./OpenAPIs/sentinel_provisioning-latest.json) | latest (curated) | 24 | Curated to the 5 core subscriber/service/routing provisioning resources — see breakdown below |
| [`sentinel_provisioning-4.0.0.json`](./OpenAPIs/sentinel_provisioning-4.0.0.json) | 4.0.0 | 44 | Full reference spec, adding the SQL/lookup admin-configuration sub-resources behind Subscriber Data and Home Zone |

### `sentinel_provisioning-latest.json`

Curated to 24 operations across 5 resources:

- **Plans**: list, create, get, update, delete
- **Session Types**: list, create, get, update, delete
- **Subscriptions**: list, create, get, update, delete
- **Subscriber Data**: create, get, update, delete (subscriber records, scoped by selection key)
- **Home Zone**: list, create, get, update, delete (zones)

### `sentinel_provisioning-4.0.0.json`

Full reference spec (44 operations). Adds the SQL/lookup admin-configuration sub-resources that back Subscriber Data (`lookupconfig`, `sqlconfig`, `fields`) and Home Zone (`sqlconfig`, `config`) — one-time environment setup rather than day-to-day provisioning, which is why they're left out of `-latest`.

## Studio Projects

### Sentinel Provisioning Project

Backed by the **`Sentinel Provisioning:latest`** Integration Model (see [`sentinel_provisioning-latest.json`](./OpenAPIs/sentinel_provisioning-latest.json) above). The project contains **24 workflows** — one atomic workflow per curated operation — organized into **5 folders** matching the OpenAPI resource categories above.

| Folder | Workflows |
|---|---|
| Plans | 5 |
| Session Types | 5 |
| Subscriptions | 5 |
| Subscriber Data | 4 |
| Home Zone | 5 |

Each workflow accepts a JSON object of the source operation's path/query parameters (and, for write operations, a `spec` object holding the request body) when run manually or called as a child workflow, and returns the full HTTP response envelope (`{ok, url, status, headers, text, body}`) from the adapter task.

Workflows are wired to an integration instance named **`Sentinel Provisioning`** via `adapter_id` — if your instance uses a different name, update `adapter_id` in each workflow task after importing.
