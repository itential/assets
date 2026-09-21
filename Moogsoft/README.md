Moogsoft (Enterprise / APEX AIOps) is an AIOps platform that correlates events into alerts and groups related alerts into Situations, helping IT operations teams reduce noise and speed up incident response.

This project provides OpenAPI specs for automating against Moogsoft's Graze API and Integrations API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`moogsoft-latest.json`](#moogsoft-latestjson)
  - [`moogsoft-v1.json`](#moogsoft-v1json)
- [Studio Projects](#studio-projects)
  - [Moogsoft Project](#moogsoft-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Moogsoft REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Moogsoft](./Studio%20Projects/Moogsoft.project.json) | 38 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Moogsoft Enterprise / APEX AIOps | Graze API v1 / Integrations API v1 |
| Moogsoft Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Moogsoft server.

Authentication is HTTP Basic, using a Moogsoft username and password (or the built-in Graze `graze`/`graze` service account):

```
Authorization: Basic <base64(username:password)>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basic_auth": {
      "username": "<your-moogsoft-username>",
      "password": "<your-moogsoft-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-moogsoft-host>",
    "port": "443"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`moogsoft-latest.json`](./OpenAPIs/moogsoft-latest.json) | latest (curated) | 38 | Actively-maintained spec, trimmed to 38 of 165 upstream operations — see breakdown below |
| [`moogsoft-v1.json`](./OpenAPIs/moogsoft-v1.json) | v1 | 165 | Full spec for the Graze API and Integrations API (165 operations) |

### `moogsoft-latest.json`

Actively-maintained spec (`x-vendor-api-version: v1`). Trimmed to 38 of 165 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Alerts**: List IDs, Get Details, List Actions, Assign, Deassign, Close, Resolve, Set Severity, Acknowledge/Unacknowledge, Add Custom Info
- **Situations**: List IDs, Get Details, Create, Assign, Deassign, Close, Resolve, Set Description, Add Custom Info, Add Alert to Situation, Remove Alert from Situation
- **Teams**: List, Get, Create, Update, Delete
- **Users**: List, Get Info, Get Roles, Create, Update
- **Integrations**: List, Create, Get, Update Configuration, Get Status, Update Status
- **Authentication**: Authenticate (connectivity check)

### `moogsoft-v1.json`

Full, unmodified vendor spec for the Graze API and Integrations API (165 operations) — the vendor's complete API surface, preserved as-is. See `moogsoft-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Moogsoft Project

Backed by the **`Moogsoft:latest`** Integration Model (see [`moogsoft-latest.json`](./OpenAPIs/moogsoft-latest.json) above). The project contains **38 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Alerts | List IDs, Get Details, List Actions, Assign, Deassign, Close, Resolve, Set Severity, Acknowledge/Unacknowledge, Add Custom Info | Alert lifecycle |
| Situations | List IDs, Get Details, Create, Assign, Deassign, Close, Resolve, Set Description, Add Custom Info, Add Alert, Remove Alert | Situation lifecycle |
| Teams | List, Get, Create, Update, Delete | Team CRUD |
| Users | List, Get Info, Get Roles, Create, Update | User CRUD |
| Integrations | List, Create, Get, Update Configuration, Get Status, Update Status | Integration status/configuration |
| Authentication | Authenticate | Connectivity/credential check |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Moogsoft:latest` Integration Model | Import from [`moogsoft-latest.json`](./OpenAPIs/moogsoft-latest.json) before importing the project |
| `Moogsoft` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Moogsoft` — update the `adapter_id` value in each workflow task if yours is named differently |
| `alert_id` / `sitn_id` inputs | Most alert and Situation workflows require the numeric ID of the target resource, typically obtained from a prior List/Get IDs call |
