LogicMonitor is a SaaS-based infrastructure performance monitoring platform providing full-stack observability for hybrid cloud, on-premises, and network environments — device and website monitoring, alerting, and scheduled maintenance windows.

This project provides OpenAPI specs for automating against LogicMonitor's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`logicmonitor-latest.json`](#logicmonitor-latestjson)
  - [`logicmonitor-3.0.0.json`](#logicmonitor-300json)
- [Studio Projects](#studio-projects)
  - [LogicMonitor Project](#logicmonitor-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | LogicMonitor REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/LogicMonitor](./Studio%20Projects/LogicMonitor.project.json) | 23 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| LogicMonitor | REST API v3 |
| LogicMonitor Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your LogicMonitor portal.

Authentication is a Bearer token in the `Authorization` header:

```
Authorization: Bearer <your-logicmonitor-api-token>
```

Generate an API token in LogicMonitor under **Settings → Users and Roles → API Tokens** (or via the admin API tokens endpoint).

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "BearerAuth": "<your-bearer-token>"
  },
  "server": {
    "protocol": "https",
    "host": "api.logicmonitor.com",
    "base_path": "/santaba/rest"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`logicmonitor-latest.json`](./OpenAPIs/logicmonitor-latest.json) | latest (curated) | 62 | Actively-maintained spec, trimmed to 62 of 353 upstream operations — see breakdown below |
| [`logicmonitor-3.0.0.json`](./OpenAPIs/logicmonitor-3.0.0.json) | 3.0.0 | 353 | Full spec for LogicMonitor REST API v3.0.0 (353 operations) |

### `logicmonitor-latest.json`

Actively-maintained spec (`x-vendor-api-version: 3.0.0`). Trimmed to 62 of 353 upstream operations covering common CRUD for automation. Also removed per-operation `security` overrides that only duplicated the spec's global security block.

Resources included, by category:

- **Devices**: Devices (with custom properties), trigger auto-discovery
- **Device Groups**: Device Groups (with custom properties), list devices in a group
- **Website Monitors**: Websites, Website Groups, list websites in a group
- **Alerts**: List/get alerts, acknowledge, escalate, add note
- **Scheduled Downtime (SDT)**: Scheduled downtime windows
- **Collectors**: Collectors, Collector Groups

### `logicmonitor-3.0.0.json`

Full, unmodified vendor spec for LogicMonitor REST API v3.0.0 (353 operations) — the vendor's complete API surface, preserved as-is. See `logicmonitor-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### LogicMonitor Project

Backed by the **`LogicMonitor:latest`** Integration Model (see [`logicmonitor-latest.json`](./OpenAPIs/logicmonitor-latest.json) above). The project contains **23 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Devices | Add, List, Get, Update, Delete Device | Device CRUD |
| Device Groups | Add, List, Get, Update, Delete Device Group | Device group CRUD |
| Alerts | List, Get, Acknowledge Alert | Alert monitoring |
| Websites | Add, List, Get, Update, Delete Website | Website monitor CRUD |
| Collectors | Add, List, Get, Update, Delete Collector | Collector CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `LogicMonitor:latest` Integration Model | Import from [`logicmonitor-latest.json`](./OpenAPIs/logicmonitor-latest.json) before importing the project |
| `LogicMonitor` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `LogicMonitor` — update the `adapter_id` value in each workflow task if yours is named differently |
