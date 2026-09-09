Itential Platform's own Automation Studio / Workflow Builder / Workflow Engine / Operations Manager (jobs and tasks) / Method of Procedures command-template REST API. Lets one Itential Platform (or Itential Gateway) automate building, validating, running, and monitoring workflows -- including manual-task transitions and ad hoc device command execution -- on another Itential Platform instance, or itself.

This project provides an OpenAPI spec for automating Studio on Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform_studio-latest.json`](#itential_platform_studio-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform - Studio Project](#itential-platform---studio-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform - Studio OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform - Studio project containing 65 workflows in 9 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform - Studio:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform_studio-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

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
| [`itential_platform_studio-latest.json`](./OpenAPIs/itential_platform_studio-latest.json) | latest | 66 | Studio — see breakdown below |

### `itential_platform_studio-latest.json`

Hand-authored from Itential's own published per-operation API reference (docs.itential.com/itential-platform/6/6/api-reference), which has no downloadable spec file. Part of a 6-product split of Itential's platform-automation surface (Studio, Admin, Configuration Manager, Lifecycle Manager, Inventory Manager, FlowAI) grouped by the day-to-day activity they support rather than by backend service boundary. This product covers building and running automations: Automation Studio workflow CRUD/validation, Workflow Builder's save/export/import/rename, Workflow Engine validation, Operations Manager job lifecycle (start/cancel/pause/resume/delete/revert/continue), task lifecycle including manual-task assignment/claim/release/finish (the transition a human works through a manual task with), and Method of Procedures command templates (create/list/update/delete/import/export/diff) plus their execution against one or more devices. Excludes Automation Studio project/component CRUD (a separate content-management surface, not workflow-building), which is intentionally not modeled as Integration Model automation here.

- **Automation Studio - Workflows** (8 ops): Create Workflow, Update Workflow, List Workflows, Get Workflow Detail by Name, Get Multiple Task Details, Get Task Details, ...
- **Workflow Builder** (8 ops): Save Workflow, Export Workflow, Import Workflow, Rename Workflow, Get Task Details, Get Tasks List, ...
- **Workflow Engine** (2 ops): Validate Stored Workflow, Validate Workflow Object
- **Operations Manager - Jobs** (11 ops): Start Job, Get Job, List Jobs, Cancel Jobs, Pause Jobs, Resume Jobs, ...
- **Operations Manager - Tasks** (8 ops): Get Task, List Tasks, Assign Task, Claim Task, Release Task, Retry Task, ...
- **Method of Procedures - Templates** (7 ops): Create Command Template, List Command Templates, Update Command Template, Delete Command Template, Import Command Template, Export Command Template, ...
- **Method of Procedures - Run Commands** (4 ops): Run Command Against a Device, Run Command Against Multiple Devices, Run Command Template Against Devices, Run a Single Command From a Template
- **JSON Forms** (11 ops): Create JSON Form, List JSON Forms, Get JSON Form, Update JSON Form, Delete JSON Forms, Import JSON Forms, ...
- **Templates** (7 ops): Create Template (Jinja2/TextFSM), List Templates, Get Template, Update Template, Delete Template, Export Template, ...

## Studio Projects

### Itential Platform - Studio Project

Backed by the **`Itential Platform - Studio:latest`** Integration Model (see [`itential_platform_studio-latest.json`](./OpenAPIs/itential_platform_studio-latest.json) above). The project contains **65 workflows** organized into **9 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Workflows | 8 | Create Workflow, Get Apps and Adapters, Get Multiple Task Details, Get Task Details, Get Workflow Detail by Name, List Workflows, ... |
| Workflow Builder | 8 | Delete Workflow by Name, Export Workflow, Get Task Details, Get Tasks List, Get Workflow Schemas, Import Workflow, ... |
| Workflow Engine | 2 | Validate Stored Workflow, Validate Workflow Object |
| Operations Manager - Jobs | 11 | Cancel Jobs, Continue Job From Task, Delete Jobs, Bulk Delete Jobs, Delete Job, Get Job, ... |
| Operations Manager - Tasks | 8 | Assign Task, Claim Task, Finish Manual Task, Get Manual Task Controller, Get Task, List Tasks, ... |
| Command Templates | 6 | Create Command Template, Delete Command Template, Export Command Template, Import Command Template, List Command Templates, Update Command Template |
| Command Templates - Run Commands | 4 | Run Command Against Multiple Devices, Run Command Against a Device, Run Command Template Against Devices, Run a Single Command From a Template |
| JSON Forms | 11 | Create JSON Form, List JSON Forms, Get JSON Form, Update JSON Form, Delete JSON Forms, Import JSON Forms, ... |
| Templates | 7 | Create Template (Jinja2/TextFSM), List Templates, Get Template, Delete Template, Export Template, Import Templates, ... |

A handful of workflow names (`Update Template`) are prefixed with `Itential Platform - Studio` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform - Studio:latest` Integration Model | Import from [`itential_platform_studio-latest.json`](./OpenAPIs/itential_platform_studio-latest.json) before importing the project |
| `Itential Platform - Studio` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform - Studio` — update the `adapter_id` value in each workflow task if yours is named differently |
