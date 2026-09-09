Itential Platform's own administrative REST API: Integration Models, integration instances, Operations Manager automations/triggers/events, platform/adapter/application health, server configuration, and task/job worker control. Lets one Itential Platform (or Itential Gateway) automate the day-to-day operational management of another Itential Platform instance, or itself -- including the health/status checks used during onboarding to confirm the platform and its services are up.

This project provides an OpenAPI spec for automating Admin on Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform_admin-latest.json`](#itential_platform_admin-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform - Admin Project](#itential-platform---admin-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform - Admin OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform - Admin project containing 30 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform - Admin:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform_admin-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

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
| [`itential_platform_admin-latest.json`](./OpenAPIs/itential_platform_admin-latest.json) | latest | 30 | Admin — see breakdown below |

### `itential_platform_admin-latest.json`

Hand-authored from Itential's own published per-operation API reference (docs.itential.com/itential-platform/6/6/api-reference) plus, for the Health/Server/Worker-status operations, Itential's downloadable OpenAPI 3.1 spec at docs.itential.com/openapi/api-reference-3.yaml. Part of a 6-product split of Itential's platform-automation surface (Studio, Admin, Configuration Manager, Lifecycle Manager, Inventory Manager, FlowAI) grouped by the day-to-day activity they support rather than by backend service boundary. This product covers platform administration: Integration Model and integration instance CRUD, Operations Manager automation registration (create/update/delete/clone/validate/import/export -- the GBAC-governed automation-catalog side of Operations Manager, distinct from Studio's job/task execution), trigger and event management, platform/adapter/application/system/server health, server configuration lookup, and task/job worker activation control. Excludes Automation Studio project/component CRUD (a separate content-management surface).

- **Integration Models** (8 ops): List Integration Models, Import Integration Model, Update Integration Model, Validate Integration Model, Get Integration Model, Delete Integration Model, ...
- **Integrations** (7 ops): List Integration Instances, Create Integration Instance, Get Integration Instance, Update Integration Instance, Update Integration Instance Properties, Delete Integration Instance, ...
- **Health** (7 ops): Get Platform Health Status, Get Adapter Health, Get Application Health, List Adapter Health, List Application Health, Get Server Health, ...
- **Server** (2 ops): Get Platform Configuration, Get Platform Configuration Property
- **Workflow Engine - Worker Status** (2 ops): Check Staterator Active State (deprecated), Get Task/Job Worker Status
- **Workflow Engine - Worker Control** (4 ops): Activate Task Worker, Deactivate Task Worker, Activate Job Worker, Deactivate Job Worker

## Studio Projects

### Itential Platform - Admin Project

Backed by the **`Itential Platform - Admin:latest`** Integration Model (see [`itential_platform_admin-latest.json`](./OpenAPIs/itential_platform_admin-latest.json) above). The project contains **30 workflows** organized into **6 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Integration Models | 8 | List Integration Models, Import Integration Model, Update Integration Model, Validate Integration Model, Get Integration Model, Delete Integration Model, ... |
| Integrations | 7 | List Integration Instances, Create Integration Instance, Get Integration Instance, Update Integration Instance, Update Integration Instance Properties, Delete Integration Instance, ... |
| Health | 7 | Get Platform Health Status, Get Adapter Health, Get Application Health, List Adapter Health, List Application Health, Get Server Health, ... |
| Server | 2 | Get Platform Configuration, Get Platform Configuration Property |
| Workflow Engine - Worker Status | 2 | Check Staterator Active State (deprecated), Get Task/Job Worker Status |
| Workflow Engine - Worker Control | 4 | Activate Task Worker, Deactivate Task Worker, Activate Job Worker, Deactivate Job Worker |

A handful of workflow names (`List Events`) are prefixed with `Itential Platform - Admin` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform - Admin:latest` Integration Model | Import from [`itential_platform_admin-latest.json`](./OpenAPIs/itential_platform_admin-latest.json) before importing the project |
| `Itential Platform - Admin` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform - Admin` — update the `adapter_id` value in each workflow task if yours is named differently |
