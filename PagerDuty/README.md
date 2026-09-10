PagerDuty is an incident response and on-call management platform used to detect, alert, and coordinate response to operational incidents — covering services, escalation policies, on-call schedules, and the incidents raised against them.

This project provides OpenAPI specs for automating against PagerDuty's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for incident and on-call automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`pagerduty-latest.json`](#pagerduty-latestjson)
  - [`pagerduty-2.0.0.json`](#pagerduty-200json)
- [Studio Projects](#studio-projects)
  - [PagerDuty Project](#pagerduty-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | PagerDuty REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/PagerDuty](./Studio%20Projects/PagerDuty.project.json) | 29 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| PagerDuty REST API | 2.0.0 |
| PagerDuty Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your PagerDuty account (`https://api.pagerduty.com`).

Authentication is an API key in the `Authorization` header:

```
Authorization: Token token=<your-pagerduty-api-key>
```

Generate a REST API key in PagerDuty under **My Profile > User Settings > API Access**, or as a general access API key under **Integrations > API Access Keys**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "api_key": {
      "value": "<your-api-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.pagerduty.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`pagerduty-latest.json`](./OpenAPIs/pagerduty-latest.json) | latest (curated) | 88 | Actively-maintained spec, trimmed to 88 of 425 upstream operations — see breakdown below |
| [`pagerduty-2.0.0.json`](./OpenAPIs/pagerduty-2.0.0.json) | 2.0.0 | 425 | Full spec for PagerDuty REST API 2.0.0 (425 operations) |

### `pagerduty-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0.0`). Trimmed to 88 of 425 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Incidents**: List, Create, Get, Update, Merge, Snooze, Alerts, Notes, Status Updates, Responder Requests
- **Services**: List, Create, Get, Update, Delete, Integrations (event source keys)
- **Escalation Policies**: List, Create, Get, Update, Delete
- **Schedules**: List, Create, Get, Update, Delete, Overrides, On-Call Users
- **On-Calls**: List
- **Teams**: List, Create, Get, Update, Delete, Members, Escalation Policy Assignment, User Assignment
- **Users**: List, Create, Get, Update, Delete, Contact Methods, Notification Rules
- **Maintenance Windows**: List, Create, Get, Update, Delete
- **Business Services**: List, Create, Get, Update, Delete
- **Change Events**: List, Create, Get, Update
- **Priorities**: List
- **Tags**: List, Create, Get, Delete, Entity Assignment

### `pagerduty-2.0.0.json`

Full, unmodified vendor spec for PagerDuty REST API 2.0.0 (425 operations) — the vendor's complete API surface, preserved as-is. See `pagerduty-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### PagerDuty Project

Backed by the **`PagerDuty:latest`** Integration Model (see [`pagerduty-latest.json`](./OpenAPIs/pagerduty-latest.json) above). The project contains **29 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Incidents | List, Create, Get, Update Incident | Incident lifecycle |
| Services | List, Create, Get, Update, Delete Service | Service CRUD |
| Escalation Policies | List, Create, Get, Update, Delete Escalation Policy | Escalation policy CRUD |
| Schedules | List, Create, Get, Update, Delete Schedule | On-call schedule CRUD |
| Users | List, Create, Get, Update, Delete User | User CRUD |
| Teams | List, Create, Get, Update, Delete Team | Team CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `PagerDuty:latest` Integration Model | Import from [`pagerduty-latest.json`](./OpenAPIs/pagerduty-latest.json) before importing the project |
| `PagerDuty` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `PagerDuty` — update the `adapter_id` value in each workflow task if yours is named differently |
| `Accept` / `Content-Type` / `From` headers | PagerDuty's API requires these as explicit parameters on most calls; the generated workflows expose them as required inputs (`Accept` defaults to `application/vnd.pagerduty+json;version=2`, `Content-Type` to `application/json`, `From` to the acting user's email) rather than hardcoding them |
