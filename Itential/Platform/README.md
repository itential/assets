Itential Platform's own REST API — Integration Models, integration instances, Automation Studio (projects and workflows), Workflow Builder, Workflow Engine validation, and Operations Manager (automations, jobs, tasks, triggers, events). Lets one Itential Platform (or Itential Gateway) automate the configuration and operation of another Itential Platform instance, or even itself.

This project provides an OpenAPI spec for automating against Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform-latest.json`](#itential_platform-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform Project](#itential-platform-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 83 workflows in 11 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

Authentication is a token retrieved dynamically: `POST /login` with a `username`/`password` body returns the token as the raw response body (no JSON envelope), which is then sent as the `token` query parameter on every subsequent call. Itential Platform automates the whole exchange, including re-retrieval on expiry.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiKeyAuth": {
      "value": "",
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://<target-platform-host>/login"
      },
      "parameters": {
        "username": "<your-username>",
        "password": "<your-password>"
      }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<target-platform-host>",
    "base_path": ""
  }
}
```

**Pointing this at the same Platform instance running the integration itself:** if the target is genuinely the same Platform, use the internal host/port the Platform container/process actually listens on, not any externally-mapped port — e.g. in a single-container Docker deployment mapping host port 3001 to the container's internal port 3000, use `localhost:3000` (the internal port), not `localhost:3001` (the host-mapped port), since the outbound call executes from inside that same container.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`itential_platform-latest.json`](./OpenAPIs/itential_platform-latest.json) | latest (curated) | 83 | Integration Models, integration instances, Automation Studio, Workflow Builder, Workflow Engine, and Operations Manager — see breakdown below |

### `itential_platform-latest.json`

Hand-authored from Itential's own published API reference (`docs.itential.com/itential-platform/6/api-reference`) — Itential doesn't publish this as a single downloadable spec file at a stable URL, only per-operation documentation pages (140+ pages across the full platform surface). Curated to 83 of the ~142 operations across the six service categories most relevant to Integration-Model-based build/deploy/run automation:

- **Integration Models** (8 ops): list, import, update, validate, get, delete, export, get security schemes
- **Integrations** (7 ops): list, create, get, update, update properties, delete, exchange auth-code for access token
- **Automation Studio — Projects** (8 ops): list, create, get, update, delete, export, add components, remove component
- **Automation Studio — Workflows** (8 ops): create/update a workflow, list workflows, get workflow detail by name, get single/multiple task details, list apps and adapters, validate a workflow
- **Workflow Builder** (8 ops): save, export, import, rename, delete a workflow; get task details, get tasks list, get schemas
- **Workflow Engine** (2 ops): validate a stored workflow by ID, validate a workflow object
- **Operations Manager — Automations** (10 ops): list, create, get, update, delete, clone, validate, export, import automations; list automation types
- **Operations Manager — Jobs** (11 ops): start, get, list, cancel, pause, resume, delete (single/bulk/multi), revert, continue-from
- **Operations Manager — Tasks** (8 ops): get, list, assign, claim, release, retry, finish a manual task, get manual task controller
- **Operations Manager — Triggers** (11 ops): list, create, get, update, delete (single/by-action-id), export, import, validate, run manual, run endpoint
- **Operations Manager — Events** (2 ops): list events, get event definition

Excluded within these six categories: Automation Studio Templates and Component Groups plus their import endpoints (14 ops — Configuration Manager/template tooling, a different automation surface), Automation Studio admin ACL-bypass project variants and thumbnail management (6 ops), Automation Studio reference-discovery introspection and method-options listing (3 ops), Workflow Builder's workflow group/ACL management (5 ops — access control, not build automation), Workflow Engine's task mocks, metrics, rate limits, worker activation, timezones, diff-to-html, and ad hoc query/evaluation endpoints (20 ops — a testing/ops-monitoring surface, not build automation), and Operations Manager's job watcher and job-group tagging endpoints plus large-data blob export (10 ops).

Excluded entirely: every other platform service category not covering Integration-Model build/deploy/run automation — Configuration Manager, Gateway Manager, JSON Forms, Inventory Manager, Lifecycle Manager, and roughly 30 more.

## Studio Projects

### Itential Platform Project

Backed by the **`Itential Platform:latest`** Integration Model (see [`itential_platform-latest.json`](./OpenAPIs/itential_platform-latest.json) above). The project contains **83 workflows** organized into **11 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Integration Models | 8 | List, import, update, validate, get, delete, export, get security schemes |
| Integrations | 7 | List, create, get, update, update properties, delete, auth-code exchange |
| Automation Studio - Projects | 8 | List, create, get, update, delete, export, add/remove components |
| Automation Studio - Workflows | 8 | Create/update workflow, list workflows, get workflow detail, task details, apps/adapters, validate |
| Workflow Builder | 8 | Save, export, import, rename, delete a workflow; task details/list, schemas |
| Workflow Engine | 2 | Validate a stored workflow by ID, validate a workflow object |
| Operations Manager - Automations | 10 | CRUD, clone, validate, export, import, list automation types |
| Operations Manager - Jobs | 11 | Start, get, list, cancel, pause, resume, delete, bulk delete, revert, continue-from |
| Operations Manager - Tasks | 8 | Get, list, assign, claim, release, retry, finish manual task, controller |
| Operations Manager - Triggers | 11 | CRUD, delete by action ID, export, import, validate, run manual/endpoint |
| Operations Manager - Events | 2 | List events, get event definition |

A handful of workflow names (e.g. `Update Workflow`, `List Workflows`, `Get Job`, `Delete Job`, `List Tasks`, `List Events`, `List Jobs`, `Bulk Delete Jobs`) are prefixed with `Itential Platform` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform:latest` Integration Model | Import from [`itential_platform-latest.json`](./OpenAPIs/itential_platform-latest.json) before importing the project |
| `Itential Platform` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform` — update the `adapter_id` value in each workflow task if yours is named differently |
