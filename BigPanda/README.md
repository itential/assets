BigPanda is an AIOps platform that correlates alerts from monitoring, observability, and ITSM tools into deduplicated incidents, helping IT operations teams cut through alert noise and speed up root-cause response.

This project provides OpenAPI specs for automating against BigPanda's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`bigpanda-latest.json`](#bigpanda-latestjson)
  - [`bigpanda-v2.1.json`](#bigpanda-v21json)
- [Studio Projects](#studio-projects)
  - [BigPanda Project](#bigpanda-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | BigPanda REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/BigPanda](./Studio%20Projects/BigPanda.project.json) | 27 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| BigPanda Public APIs | v2.1 |
| BigPanda Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your BigPanda organization (`https://api.bigpanda.io`, or `https://eu-api.bigpanda.io` for EU-region organizations).

Authentication is a static Bearer token in the `Authorization` header — either an org-wide integration token or a per-user API key, both generated in BigPanda's UI with no login/exchange call required:

```
Authorization: Bearer <your-bigpanda-token>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearer_token": {
      "value": "<your-bigpanda-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.bigpanda.io",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`bigpanda-latest.json`](./OpenAPIs/bigpanda-latest.json) | latest (curated) | 27 | Actively-maintained spec, trimmed to 27 of 161 upstream operations — see breakdown below |
| [`bigpanda-v2.1.json`](./OpenAPIs/bigpanda-v2.1.json) | v2.1 | 161 | Full spec for BigPanda Public APIs v2.1 (161 operations) |

### `bigpanda-latest.json`

Actively-maintained spec (`x-vendor-api-version: v2.1`). Trimmed to 27 of 161 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Environments**: List, Create, Get, Update, Delete
- **Incidents**: List, Get, Assign, Unassign, Comment, Resolve, Snooze, Unsnooze, Merge, Activity Log
- **Alerts**: Send, Batch Resolve
- **Integrations**: List, Create, Get, Update, Delete
- **Tags**: List, Create, Get, Update, Delete

### `bigpanda-v2.1.json`

Full, unmodified vendor spec for BigPanda Public APIs v2.1 (161 operations) — the vendor's complete API surface, preserved as-is. See `bigpanda-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### BigPanda Project

Backed by the **`BigPanda:latest`** Integration Model (see [`bigpanda-latest.json`](./OpenAPIs/bigpanda-latest.json) above). The project contains **27 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Environments | List, Create, Get, Update, Delete Environment | Environment CRUD |
| Incidents | List, Get, Assign, Unassign, Comment, Resolve, Snooze, Unsnooze, Merge, Get Activities | Incident lifecycle |
| Alerts | Send Alert, Resolve Alerts | Alert ingestion and bulk resolution |
| Integrations | List, Create, Get, Update, Delete Integration | Webhook integration CRUD |
| Tags | List, Create, Get, Update, Delete Tag | Alert tag CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `BigPanda:latest` Integration Model | Import from [`bigpanda-latest.json`](./OpenAPIs/bigpanda-latest.json) before importing the project |
| `BigPanda` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `BigPanda` — update the `adapter_id` value in each workflow task if yours is named differently |
| `environment_id` / `incident_id` inputs | Most incident and activity workflows require an `environment_id` alongside the resource ID, since incidents in BigPanda live within an environment scope |
