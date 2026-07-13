Atlassian OpsGenie is an alert and on-call management platform that routes, acknowledges, escalates, and manages alerts and incidents from monitoring and observability tools, backed by team-based on-call scheduling.

This project provides OpenAPI specs for automating against OpsGenie's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | OpsGenie REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Atlassian OpsGenie | API v2 (with legacy v1 endpoints for incidents/maintenance) |
| OpsGenie Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your OpsGenie instance.

Authentication is an API key in the `Authorization` header, using the `GenieKey` scheme:

```
Authorization: GenieKey <your-opsgenie-api-key>
```

Generate an API key in OpsGenie under **Settings > API key management**.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`atlassian_opsgenie-latest.json`](./OpenAPIs/atlassian_opsgenie-latest.json) | latest (curated) | Trimmed to 108 of 170 upstream operations — see breakdown below |
| [`atlassian_opsgenie-2.0.0.json`](./OpenAPIs/atlassian_opsgenie-2.0.0.json) | 2.0.0 | Full, unmodified vendor spec |

### `atlassian_opsgenie-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0.0`). Trimmed to 108 of 170 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Alerts**: List, Get, Create, Delete, Count, Acknowledge/Unacknowledge, Close, Snooze, Escalate, Assign, Add Responders/Teams, Notes, Tags, Details, Description, Message, Priority, Logs, Recipients, Custom Actions
- **Incidents**: List, Get, Create, Delete, Close
- **Escalations**: List, Get, Create, Update, Delete
- **On-call Schedules**: List, Get, Create, Update, Delete, On-calls, Next On-calls, Timeline, Overrides, Rotations
- **Teams**: List, Get, Create, Update, Delete, Members, Routing Rules
- **Maintenance**: List, Get, Create, Update, Delete, Cancel
- **Policies**: Alert Policies, Notification Policies — List, Get, Create, Update, Delete, Enable, Disable
- **Integrations**: List, Get, Create, Update, Delete, Enable, Disable
- **Heartbeats**: List, Get, Create, Update, Delete, Enable, Disable, Ping
- **Forwarding Rules**: List, Get, Create, Update, Delete
- **Users**: List, Get, Create, Update, Delete
- **Account**: Get account info

Dropped as long-tail/admin: legacy v1 alert/notification policy endpoints (superseded by v2), saved searches, alert attachments, custom RBAC roles, per-team audit logs, calendar (`.ics`) exports, integration action/authenticate endpoints, and per-user personal admin (contact methods, personal notification rules and their steps, and per-user read-only lookups of teams/schedules/escalations/forwarding rules).
