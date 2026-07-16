PagerDuty is an incident response and on-call management platform used to detect, alert, and coordinate response to operational incidents — covering services, escalation policies, on-call schedules, and the incidents raised against them.

This project provides OpenAPI specs for automating against PagerDuty's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for incident and on-call automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`pagerduty-latest.json`](#pagerduty-latestjson)
  - [`pagerduty-2.0.0.json`](#pagerduty-200json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | PagerDuty REST API OpenAPI specs — curated `-latest` plus the full dated spec |

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
