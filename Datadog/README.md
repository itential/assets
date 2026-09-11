Datadog is a monitoring and observability platform for infrastructure, applications, and logs, unifying metrics, traces, and logs into dashboards, monitors, and incident workflows.

This project provides OpenAPI specs for automating against Datadog's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for observability automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`datadog-latest.json`](#datadog-latestjson)
  - [`datadog-2.0.json`](#datadog-20json)
  - [`datadog_legacy-1.0.json`](#datadog_legacy-10json)
- [Studio Projects](#studio-projects)
  - [Datadog Project](#datadog-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Datadog REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Datadog](./Studio%20Projects/Datadog.project.json) | 24 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Datadog Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Datadog site (e.g. `api.datadoghq.com` or `api.datadoghq.eu`).

Authentication is an API key in the `DD-API-KEY` header (and an application key in `DD-APPLICATION-KEY` for endpoints that require one):

```
DD-API-KEY: <your-datadog-api-key>
DD-APPLICATION-KEY: <your-datadog-application-key>
```

Generate both from Datadog under **Organization Settings → API Keys** and **Application Keys**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiKeyAuth": {
      "value": "<your-api-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.datadoghq.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`datadog-latest.json`](./OpenAPIs/datadog-latest.json) | latest (curated) | 39 | Actively-maintained, curated for common CRUD for observability automation — see breakdown below |
| [`datadog-2.0.json`](./OpenAPIs/datadog-2.0.json) | 2.0 | 1198 | Full spec for Datadog API v2.0. |
| [`datadog_legacy-1.0.json`](./OpenAPIs/datadog_legacy-1.0.json) | 1.0 | 235 | Legacy Datadog API v1.0 spec. |

### `datadog-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0`). Trimmed to 39 of 1198 upstream operations. Datadog's full API surface spans dozens of specialized products (Security Monitoring, Synthetics, RUM, CI Visibility, APM, Cost Management, and more) that are out of scope for general-purpose automation; this spec keeps only the cross-cutting operational primitives. Note that this spec snapshot has no bare Monitor, Dashboard, or SLO CRUD endpoints upstream (only narrow sub-resources like notification rules and report status), so those resources are excluded here rather than partially represented. Pull the full spec from [Datadog's official OpenAPI description](https://github.com/DataDog/datadog-api-client-python/blob/master/.generator/schemas/v2/openapi.yaml) if you need one of the excluded product areas.

Resources included, by category:

- **Incident response**: Downtimes, Maintenance Windows, Incidents (create/get/search)
- **Logs**: Event submission, Event search
- **Metrics**: Active metric listing, Scalar and timeseries queries
- **Tagging**: Tag enrichment rules
- **Access management**: Users, Roles

### `datadog-2.0.json`

Full, unmodified vendor spec for Datadog API v2.0 (1198 operations) — the vendor's complete API surface, preserved as-is. See `datadog-latest.json` above for the curated subset if you just need common CRUD automation.

### `datadog_legacy-1.0.json`

Full, unmodified vendor spec for the legacy Datadog API v1.0 (235 operations) — the vendor's complete API surface, preserved as-is. See `datadog-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Datadog Project

Backed by the **`Datadog:latest`** Integration Model (see [`datadog-latest.json`](./OpenAPIs/datadog-latest.json) above). The project contains **24 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Incidents | List, Create, Get, Update, Delete Incident | Incident lifecycle |
| Downtimes | List, Create, Get, Update, Cancel Downtime | Downtime scheduling |
| Maintenance Windows | List, Create, Update, Delete Maintenance Window | Maintenance window management |
| Roles | List, Create, Get, Update, Delete Role | RBAC role management |
| Users | List, Create, Get, Update, Disable User | User management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Datadog:latest` Integration Model | Import from [`datadog-latest.json`](./OpenAPIs/datadog-latest.json) before importing the project |
| `Datadog` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Datadog` — update the `adapter_id` value in each workflow task if yours is named differently |
