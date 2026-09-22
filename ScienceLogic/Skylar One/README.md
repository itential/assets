# Skylar One

Skylar One (formerly SL1) is ScienceLogic's IT infrastructure monitoring and AIOps platform. It discovers, monitors, and manages multi-vendor infrastructure and applications across hybrid environments, and exposes devices, device groups, organizations, alerts/events, assets, and monitoring policies through its REST API.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`skylar_one-latest.json`](#skylar_one-latestjson)
  - [`skylar_one-12.5.20.json`](#skylar_one-12520json)
- [Studio Projects](#studio-projects)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Skylar One REST API OpenAPI specs — curated `-latest` plus the full spec |
| [Studio Projects/](./Studio%20Projects/) | One workflow per curated operation, organized by resource category |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Skylar One (SL1) | 12.5.x (see OpenAPIs below) |
| Skylar One Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is HTTP Basic auth using a valid SL1 user account's username and password — credentials are validated against SL1's own user accounts, there is no separate API token or login/token-exchange step. (SL1's REST Toolkit also supports a configurable API-key header as an alternative, but it isn't modeled here since Basic auth is always available and requires no extra setup.) The base path for every resource is `/api` — this platform doesn't apply any path in the OpenAPI spec itself, so it must be set explicitly in the instance's `server.base_path` field (see below).

### Connection Properties

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-sl1-username>",
      "password": "<your-sl1-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-sl1-appliance-host>",
    "port": "443",
    "base_path": "/api"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`skylar_one-latest.json`](./OpenAPIs/skylar_one-latest.json) | latest (curated) | 125 | Trimmed to 125 of 727 upstream operations covering common CRUD for automation — see breakdown below |
| [`skylar_one-12.5.20.json`](./OpenAPIs/skylar_one-12.5.20.json) | 12.5.20 | 727 | Full spec covering SL1's complete documented REST resource surface. |

### `skylar_one-latest.json`

Actively-maintained spec (`x-vendor-api-version: 12.5.20`). Trimmed to 125 of 727 upstream operations covering common CRUD for infrastructure monitoring automation.

Resources included, by category:

- **Device**: List, Create, Get, Update, Replace, Delete; Detail; Interface (List, Create, Get, Update, Replace, Delete); Note (List, Create, Get, Update, Replace, Delete); Vitals
- **Device Group**: List, Create, Get, Update, Replace, Delete; Expanded Devices
- **Device Category / Device Class**: List, Get (read-only lookups)
- **Organization**: List, Create, Get, Update, Replace, Delete; Note (List, Create, Get, Update, Replace, Delete)
- **Alert**: List, Create, Get, Update
- **Event**: List, Get, Update, Delete
- **Cleared Event**: List, Get
- **Event Category**: Get, Update, Delete
- **Asset**: List, Create, Get, Update, Replace, Delete; Note (List, Create, Get, Update, Replace)
- **Interface**: List, Create, Get, Update, Replace, Delete
- **Collector Group**: List, Create, Get, Update, Replace, Delete
- **Discovery Session**: List, Create, Get, Update, Replace, Delete
- **Ticket**: List, Create, Get, Update, Replace; Note (List, Create, Get, Update, Replace)
- **Ticket Queue**: List, Create, Get, Update, Replace, Delete
- **Ticket State**: List, Create, Get, Update, Replace, Delete
- **Monitor**: Port, Process, Service policies (each: List, Create, Get, Update, Replace, Delete)

### `skylar_one-12.5.20.json`

Full spec covering SL1's documented REST resource surface (727 operations) — the complete resource hierarchy, preserved for reference. See `skylar_one-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### `Skylar One.project.json`

One workflow per curated operation from `skylar_one-latest.json`, organized into folders by resource category, wired to the `Skylar One:latest` Integration Model.

Every workflow's adapter task is wired to the Integration instance name `Skylar One`. After importing, either name your Integration instance `Skylar One`, or update the `adapter_id` value in each workflow task to match your own instance name.

| Folder | Workflows |
|---|---|
| Device | 20 |
| Monitor | 18 |
| Organization | 12 |
| Asset | 11 |
| Ticket | 10 |
| Device Group | 7 |
| Collector Group | 6 |
| Discovery Session | 6 |
| Interface | 6 |
| Ticket Queue | 6 |
| Ticket State | 6 |
| Alert | 4 |
| Event | 4 |
| Event Category | 3 |
| Cleared Event | 2 |
| Device Category | 2 |
| Device Class | 2 |
