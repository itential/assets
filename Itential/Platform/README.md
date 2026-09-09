Itential Platform's own REST API — Automation Studio, Workflow Builder, Workflow Engine, JSON Forms, Method of Procedures, Integration Models and integration instances, platform health, Configuration Manager, Lifecycle Manager, Inventory Manager, Operations Manager, and FlowAI. Lets one Itential Platform (or Itential Gateway) automate the configuration and operation of another Itential Platform instance, or even itself.

This project provides one OpenAPI spec for Itential Platform's own REST API via a single Integration Model, plus 7 Studio Projects of ready-to-import workflows built on that same model — one Integration Model, matching how Itential ships the platform, with each Studio Project curating a different day-to-day activity.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform-latest.json`](#itential_platform-latestjson)
- [Studio Projects](#studio-projects)
  - [`Itential Platform - Studio.project.json`](#itential-platform---studioprojectjson)
  - [`Itential Platform - Admin.project.json`](#itential-platform---adminprojectjson)
  - [`Itential Platform - Configuration Manager.project.json`](#itential-platform---configuration-managerprojectjson)
  - [`Itential Platform - Lifecycle Manager.project.json`](#itential-platform---lifecycle-managerprojectjson)
  - [`Itential Platform - Inventory Manager.project.json`](#itential-platform---inventory-managerprojectjson)
  - [`Itential Platform - Operations Manager.project.json`](#itential-platform---operations-managerprojectjson)
  - [`Itential Platform - FlowAI.project.json`](#itential-platform---flowaiprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform OpenAPI spec (single Integration Model covering the full platform surface) |
| [Studio Projects/](./Studio%20Projects/) | 7 projects, each curating a different day-to-day activity: Studio, Admin, Configuration Manager, Lifecycle Manager, Inventory Manager, Operations Manager, FlowAI |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run any of the Studio Projects below |

## Integration Configuration

Import `itential_platform-latest.json` as an Integration Model in **Admin > Integrations**, then create a single integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself. All 7 Studio Projects are wired to the same integration instance, named `Itential Platform`.

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
| [`itential_platform-latest.json`](./OpenAPIs/itential_platform-latest.json) | latest | 305 | Full Itential Platform REST API surface used by the 7 Studio Projects below |

### `itential_platform-latest.json`

Sourced from Itential's downloadable OpenAPI 3.1 spec (docs.itential.com/openapi/api-reference-3.yaml) and published per-operation API reference (docs.itential.com/itential-platform/6/6/api-reference).

## Studio Projects

Every workflow's adapter task is wired to the Integration instance name `Itential Platform`. After importing, either name your Integration instance `Itential Platform`, or update the `adapter_id` value in each workflow task to match your own instance name.

### `Itential Platform - Studio.project.json`

Build, validate, run, and monitor Itential Platform workflows -- including manual-task transitions, MOP command-template execution, JSON Forms, and Jinja2/TextFSM templates -- against another Itential Platform instance or itself. Contains **43 workflows** organized into **6 folders**.

MOP command-template CRUD (create/list/get/update/delete/export/import) is left out here in favor of just the execution workflows (Command Templates - Run Commands) -- defining a template is a one-time setup activity, running one against a device is the repeatable workflow pattern.

| Folder | Workflows |
|---|---|
| Workflows | (8) Create Workflow, Get Apps and Adapters, Get Multiple Task Details, Get Task Details, Get Workflow Detail by Name, Studio List Workflows, ... |
| Workflow Builder | (8) Delete Workflow by Name, Export Workflow, Get Task Details (Workflow Builder), Get Tasks List, Get Workflow Schemas, Import Workflow, ... |
| Workflow Engine | (2) Validate Stored Workflow, Validate Workflow Object |
| Command Templates - Run Commands | (4) Run Command Against Multiple Devices, Run Command Against a Device, Run Command Template Against Devices, Run a Single Command From a Template |
| Templates | (12) Apply Template, Apply Templates (Bulk), Create Template (Jinja2/TextFSM), Delete Template, Export Template, Get Template, ... |
| JSON Forms | (9) Create JSON Form, Deep Validate JSON Form Definition, Delete JSON Forms, Get JSON Form, Import JSON Forms, List JSON Forms, ... |

### `Itential Platform - Admin.project.json`

Administer Itential Platform integrations and platform health/worker status against another Itential Platform instance or itself. Contains **30 workflows** organized into **6 folders**.

| Folder | Workflows |
|---|---|
| Integration Models | (8) Delete Integration Model, Export Integration Model, Get Integration Model, Get Integration Model Security Schemes, Import Integration Model, List Integration Models, ... |
| Integrations | (7) Create Integration Instance, Delete Integration Instance, Exchange Auth Code for Access Token, Get Integration Instance, List Integration Instances, Update Integration Instance, ... |
| Health | (7) Get Adapter Health, Get Application Health, Get Platform Health Status, Get Server Health, Get System Health, List Adapter Health, ... |
| Server | (2) Get Platform Configuration, Get Platform Configuration Property |
| Workflow Engine - Worker Status | (2) Check Staterator Active State (deprecated), Get Task/Job Worker Status |
| Workflow Engine - Worker Control | (4) Activate Job Worker, Activate Task Worker, Deactivate Job Worker, Deactivate Task Worker |

### `Itential Platform - Configuration Manager.project.json`

Build and run Golden Config, compliance, and device-template/backup/configuration automation against another Itential Platform instance or itself. Contains **74 workflows** organized into **13 folders**.

The full Configuration Manager REST API is available in the OpenAPI spec above; this project has been curated down to the operations worth promoting as workflow-building patterns.

| Folder | Workflows |
|---|---|
| Golden Config Trees | (8) Create Golden Config Tree, Delete Golden Config Tree, Delete Golden Config Trees (Bulk), Export Golden Config Tree, Get Golden Config Tree Summary, Import Golden Config Trees, ... |
| Golden Config Tree Versions | (1) Get Golden Config Tree Version |
| Golden Config Nodes | (10) Add Device Groups to Node, Add Devices to Node, Add Tasks to Node, Create Golden Config Node, Delete Golden Config Node, Get Devices on Golden Config Tree, ... |
| Compliance Plans | (10) Create Compliance Plan, Delete Compliance Plans, Get Compliance Plan, Get Compliance Plan Device Errors, Get Compliance Plan Score Trend, Get Compliance Plans Summary, ... |
| Compliance Plan Nodes | (2) Add Nodes to Compliance Plan, Remove Nodes from Compliance Plan |
| Compliance Runs | (3) List Compliance Plan Runs, List Latest Compliance Plan Run per Plan, Run Compliance Plan |
| Compliance Reports | (8) Get Compliance Report Detail, Get Compliance Report Metadata for a Batch, Get Compliance Report Node Summary, Get Compliance Report Totals for a Backup, Get Compliance Report Totals for a Device, Get Compliance Report Totals for a Task Instance, ... |
| Grading | (4) Get Historical Graded Compliance Reports, Grade Compliance Reports for a Node, Grade a Single Compliance Report, Query Graded Compliance History (Paginated) |
| Device Groups | (10) Add Devices to Group by ID, Add Devices to Group by Name, Create Device Group, Delete Device Groups, Delete Device Groups by Name, Get Device Group by ID, ... |
| Backups | (7) Back Up Device Config, Delete Backups, Get Backup by ID, Import Backups, List Devices with Backups, Search Backups, ... |
| Device Configuration | (1) Get Device Configuration |
| Devices | (3) Get Devices (Basic Options), Itential Platform - Configuration Manager Get Device, Search Devices (Paginated, Filtered) |
| Config Parsers | (7) Create Config Parser, Delete Config Parser, Delete Config Parsers (Bulk), Get Config Parser, Import Config Parsers, List Config Parsers, ... |

### `Itential Platform - Lifecycle Manager.project.json`

Model network services and run their lifecycle actions against another Itential Platform instance or itself. Contains **22 workflows** organized into **4 folders**.

| Folder | Workflows |
|---|---|
| Resource Models | (8) Create Resource Model, Delete Resource Model, Edit Resource Model (Generate Action Stubs), Export Resource Model, Get Resource Model, Import Resource Model, ... |
| Resource Instances | (3) Export Resource Instance, Get Resource Instance, Search Resource Instances |
| Actions | (6) Cancel Action Execution, Get Action Execution, Run Bulk Resource Action, Run Resource Action, Search Action Executions, Validate Resource Model Actions |
| Instance Groups | (5) Create Instance Group, Delete Instance Group, Get Instance Group, Search Instance Groups, Update Instance Group Membership |

### `Itential Platform - Inventory Manager.project.json`

Manage device/asset inventories, bulk-load nodes, and organize by tags against another Itential Platform instance or itself. Contains **24 workflows** organized into **4 folders**.

| Folder | Workflows |
|---|---|
| Inventories | (6) Create Inventory, Delete Inventory, Get Inventory Manager Stats, Get Inventory by Identifier, Inventory Manager Health Check, List Inventories |
| Nodes | (7) Build Inventory Filter, Bulk Load Inventory Nodes, Clear Inventory Nodes, Expand Node Identifiers to Full Documents, Get Node by Identifier, List Nodes (Cross-Inventory), ... |
| Actions | (5) Create Inventory Action, Delete Inventory Action, Get Inventory Action, List Actions (Cross-Inventory), List Actions for an Inventory |
| Tags | (6) Find Inventories and Nodes by Tags, Get Tag Usage Statistics, Get Tag by Identifier, List Accessible Tags, List Tags, List Tags for an Inventory |

### `Itential Platform - Operations Manager.project.json`

Start and monitor jobs, work manual tasks, and create/run triggers -- including cron-free scheduled triggers -- against another Itential Platform instance or itself. Contains **42 workflows** organized into **5 folders**.

Trigger workflows cover all four trigger types, including schedule triggers -- which are NOT cron-based. Itential uses a `firstRunAt` epoch timestamp plus a `repeat` interval tree instead of a cron expression. This is a real gap in Itential's own published OpenAPI spec (the schedule branch doesn't fully resolve there either); the schema was reconstructed from the fully-expanded read/export trigger shapes and should be spot-checked against a live platform before being treated as gospel.

| Folder | Workflows |
|---|---|
| Jobs | (11) Bulk Delete Jobs, Cancel Jobs, Continue Job From Task, Delete Job, Delete Jobs, Get Job, ... |
| Tasks | (8) Assign Task, Claim Task, Finish Manual Task, Get Manual Task Controller, Get Task, List Tasks, ... |
| Triggers | (11) Create Trigger, Delete Trigger, Delete Triggers by Action ID, Export Trigger, Get Trigger, Import Triggers, ... |
| Events | (2) Get Event Definition, List Events |
| Automations | (10) Clone Automation, Create Automation, Delete Automation, Export Automation, Get Automation, Import Automations, ... |

### `Itential Platform - FlowAI.project.json`

Invoke FlowAI agents and manage human-in-the-loop work items against another Itential Platform instance or itself. Contains **12 workflows** organized into **4 folders**.

The full FlowAI REST API (agent/project CRUD, LLM provider registration, admin variants, bundles) is available in the OpenAPI spec above, but this project deliberately narrows to the two patterns a customer workflow actually builds around: invoking an agent and consuming its result, and handing work off to a human when an agent needs input. Agent/project definition, LLM provider/credential setup, and bundle import/export are one-time build- or admin-time activities better done directly against the REST API (or the FlowAI UI) than wired into a repeatable workflow.

| Folder | Workflows |
|---|---|
| Sessions | (3) Get Agent Session, Start Agent Session, Update Agent Session State |
| Run Agent | (1) Run Agent Synchronously |
| Messages | (1) Get Session Messages |
| Work Items | (7) Assign Work Item, Cancel Work Item, Claim Work Item, Complete Work Item, Create Work Item, Get Work Item, ... |
