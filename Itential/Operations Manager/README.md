Itential Platform's own Operations Manager REST API: job and task execution/lifecycle, triggers (including cron-free schedule triggers, endpoint/webhook triggers, event-driven triggers, and manual triggers), events, and the automation-catalog registration that ties a workflow to a runnable/triggerable Automation. Lets one Itential Platform (or Itential Gateway) automate running, monitoring, and scheduling workflow automations on another Itential Platform instance, or itself.

This project provides an OpenAPI spec for automating Operations Manager on Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform_operations_manager-latest.json`](#itential_platform_operations_manager-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform - Operations Manager Project](#itential-platform---operations-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform - Operations Manager OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform - Operations Manager project containing 42 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform - Operations Manager:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform_operations_manager-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

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
| [`itential_platform_operations_manager-latest.json`](./OpenAPIs/itential_platform_operations_manager-latest.json) | latest | 42 | Operations Manager — see breakdown below |

### `itential_platform_operations_manager-latest.json`

Hand-authored from Itential's own downloadable OpenAPI 3.1 spec (docs.itential.com/openapi/api-reference-3.yaml) and per-operation reference pages. Split out as its own product from what was originally divided between Studio (job/task execution) and Admin (trigger/event/automation registration), since Operations Manager -- running, scheduling, and triggering automations -- is a distinct day-to-day activity in its own right. Covers Jobs (start/get/list/cancel/pause/resume/delete/bulk-delete/revert/continue-from), Tasks (get/list/assign/claim/release/retry/finish-manual-task/manual-task-controller), Triggers (full CRUD plus manual/endpoint run, validate, export/import -- including the schedule trigger type, which is NOT cron-based: Itential uses a firstRunAt epoch timestamp plus a 'repeat' interval tree instead of a cron expression), Events (list/get-definition), and Automations (the GBAC-governed catalog entry that registers a workflow as a triggerable/runnable Automation: CRUD, clone, validate, export/import, list types). Note: the exact request-body shape for creating/updating a schedule-type trigger is not fully resolvable from Itential's own published OpenAPI spec (the schedule branch renders as an unresolved generic type there too) -- the schema in this spec was reconstructed by cross-referencing the fully-expanded read/export trigger schemas, and should be spot-checked against a live platform before being treated as gospel.

- **Jobs** (11 ops): Start Job, Get Job, List Jobs, Cancel Jobs, Pause Jobs, Resume Jobs, ...
- **Tasks** (8 ops): Get Task, List Tasks, Assign Task, Claim Task, Release Task, Retry Task, ...
- **Triggers** (11 ops): Create Trigger, List Triggers, Get Trigger, Update Trigger, Delete Trigger, Delete Triggers by Action ID, ...
- **Events** (2 ops): List Events, Get Event Definition
- **Automations** (10 ops): List Automations, Create Automation, Get Automation, Update Automation, Delete Automation, Clone Automation, ...

## Studio Projects

### Itential Platform - Operations Manager Project

Backed by the **`Itential Platform - Operations Manager:latest`** Integration Model (see [`itential_platform_operations_manager-latest.json`](./OpenAPIs/itential_platform_operations_manager-latest.json) above). The project contains **42 workflows** organized into **5 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Jobs | 11 | Start Job, Get Job, List Jobs, Cancel Jobs, Pause Jobs, Resume Jobs, ... |
| Tasks | 8 | Get Task, List Tasks, Assign Task, Claim Task, Release Task, Retry Task, ... |
| Triggers | 11 | Create Trigger, List Triggers, Get Trigger, Update Trigger, Delete Trigger, Delete Triggers by Action ID, ... |
| Events | 2 | List Events, Get Event Definition |
| Automations | 10 | List Automations, Create Automation, Get Automation, Update Automation, Delete Automation, Clone Automation, ... |

A handful of workflow names (`Delete Job`, `Get Job`, `List Events`, `List Jobs`, `List Tasks`) are prefixed with `Itential Platform - Operations Manager` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform - Operations Manager:latest` Integration Model | Import from [`itential_platform_operations_manager-latest.json`](./OpenAPIs/itential_platform_operations_manager-latest.json) before importing the project |
| `Itential Platform - Operations Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform - Operations Manager` — update the `adapter_id` value in each workflow task if yours is named differently |
