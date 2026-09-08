Itential Platform's own Configuration Manager REST API: Golden Config trees/versions/nodes, compliance plans/runs/reports/grading, device groups, device templates, device backups, device configuration apply/patch, raw device reads, config parsers, and template rendering/parsing (Template Builder). Lets one Itential Platform (or Itential Gateway) automate configuration-compliance and device-configuration-templating workflows against another Itential Platform instance, or itself.

This project provides an OpenAPI spec for automating Configuration Manager on Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform_configuration_manager-latest.json`](#itential_platform_configuration_manager-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform - Configuration Manager Project](#itential-platform---configuration-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform - Configuration Manager OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform - Configuration Manager project containing all 88 workflows in 15 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform - Configuration Manager:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform_configuration_manager-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

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
| [`itential_platform_configuration_manager-latest.json`](./OpenAPIs/itential_platform_configuration_manager-latest.json) | latest | 88 | Configuration Manager — see breakdown below |

### `itential_platform_configuration_manager-latest.json`

Hand-authored from Itential's own published per-operation API reference (docs.itential.com/itential-platform/6/6/api-reference). Part of a 6-product split of Itential's platform-automation surface (Studio, Admin, Configuration Manager, Lifecycle Manager, Inventory Manager, FlowAI). Configuration Manager's real documented surface is large (150+ operations); this build includes the full Golden Config (trees/versions/nodes), Compliance (plans/plan-nodes/runs/reports/grading), device management (groups/templates/backups/configuration/raw-device-reads), config-parser, and Template Builder sub-areas -- everything needed to build and run configuration-compliance and templating automation. A handful of response schemas are undocumented on Itential's own public reference (rendered as empty examples there too) and are flagged inline in this spec rather than guessed.

- **Configuration Manager - Golden Config Trees** (8 ops): Create Golden Config Tree, Update Golden Config Tree, Delete Golden Config Tree, Delete Golden Config Trees (Bulk), Export Golden Config Tree, List Golden Config Trees, ...
- **Configuration Manager - Golden Config Tree Versions** (1 op): Get Golden Config Tree Version
- **Configuration Manager - Golden Config Nodes** (10 ops): Create Golden Config Node, Delete Golden Config Node, Add Device Groups to Node, Add Devices to Node, Add Tasks to Node, Remove Device Groups from Node, ...
- **Configuration Manager - Compliance Plans** (10 ops): Create Compliance Plan, Delete Compliance Plans, Get Compliance Plan, Get Compliance Plans Summary, Import Compliance Plans, Get Compliance Plan Score Trend, ...
- **Configuration Manager - Compliance Plan Nodes** (2 ops): Add Nodes to Compliance Plan, Remove Nodes from Compliance Plan
- **Configuration Manager - Compliance Runs** (3 ops): Run Compliance Plan, List Compliance Plan Runs, List Latest Compliance Plan Run per Plan
- **Configuration Manager - Compliance Reports** (8 ops): Get Compliance Report Totals for a Backup, Get Compliance Report Totals for a Device, Get Compliance Report Totals for a Task Instance, Get Compliance Reports Detail (Bulk), Get Compliance Report Detail, Get Compliance Report Metadata for a Batch, ...
- **Configuration Manager - Grading** (4 ops): Grade Compliance Reports for a Node, Grade a Single Compliance Report, Get Historical Graded Compliance Reports, Query Graded Compliance History (Paginated)
- **Configuration Manager - Device Groups** (10 ops): Create Device Group, Get Device Group by ID, Get Device Group by Name, List Device Groups, Update Device Group, Delete Device Groups, ...
- **Configuration Manager - Device Templates** (6 ops): Create Device Template, Search Device Templates, Get Config Spec Template, Update Device Template, Delete Device Templates, Apply Device Template
- **Configuration Manager - Backups** (7 ops): Back Up Device Config, Search Backups, List Devices with Backups, Get Backup by ID, Update Backup Metadata, Delete Backups, ...
- **Configuration Manager - Device Configuration** (4 ops): Get Device Configuration, Apply Device Configuration, Patch Device Configuration, Advanced Patch Device Configuration
- **Configuration Manager - Devices** (3 ops): Get Device, Search Devices (Paginated, Filtered), Get Devices (Basic Options)
- **Configuration Manager - Config Parsers** (7 ops): Create Config Parser, Get Config Parser, List Config Parsers, Update Config Parser, Delete Config Parser, Delete Config Parsers (Bulk), ...
- **Template Builder** (5 ops): Apply Template, Apply Templates (Bulk), Parse Template (TextFSM), Render Jinja2 Template with Cast, Render Jinja Template

## Studio Projects

### Itential Platform - Configuration Manager Project

Backed by the **`Itential Platform - Configuration Manager:latest`** Integration Model (see [`itential_platform_configuration_manager-latest.json`](./OpenAPIs/itential_platform_configuration_manager-latest.json) above). The project contains **88 workflows** organized into **15 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Configuration Manager - Golden Config Trees | 8 | Create Golden Config Tree, Update Golden Config Tree, Delete Golden Config Tree, Delete Golden Config Trees (Bulk), Export Golden Config Tree, List Golden Config Trees, ... |
| Configuration Manager - Golden Config Tree Versions | 1 | Get Golden Config Tree Version |
| Configuration Manager - Golden Config Nodes | 10 | Create Golden Config Node, Delete Golden Config Node, Add Device Groups to Node, Add Devices to Node, Add Tasks to Node, Remove Device Groups from Node, ... |
| Configuration Manager - Compliance Plans | 10 | Create Compliance Plan, Delete Compliance Plans, Get Compliance Plan, Get Compliance Plans Summary, Import Compliance Plans, Get Compliance Plan Score Trend, ... |
| Configuration Manager - Compliance Plan Nodes | 2 | Add Nodes to Compliance Plan, Remove Nodes from Compliance Plan |
| Configuration Manager - Compliance Runs | 3 | Run Compliance Plan, List Compliance Plan Runs, List Latest Compliance Plan Run per Plan |
| Configuration Manager - Compliance Reports | 8 | Get Compliance Report Totals for a Backup, Get Compliance Report Totals for a Device, Get Compliance Report Totals for a Task Instance, Get Compliance Reports Detail (Bulk), Get Compliance Report Detail, Get Compliance Report Metadata for a Batch, ... |
| Configuration Manager - Grading | 4 | Grade Compliance Reports for a Node, Grade a Single Compliance Report, Get Historical Graded Compliance Reports, Query Graded Compliance History (Paginated) |
| Configuration Manager - Device Groups | 10 | Create Device Group, Get Device Group by ID, Get Device Group by Name, List Device Groups, Update Device Group, Delete Device Groups, ... |
| Configuration Manager - Device Templates | 6 | Create Device Template, Search Device Templates, Get Config Spec Template, Update Device Template, Delete Device Templates, Apply Device Template |
| Configuration Manager - Backups | 7 | Back Up Device Config, Search Backups, List Devices with Backups, Get Backup by ID, Update Backup Metadata, Delete Backups, ... |
| Configuration Manager - Device Configuration | 4 | Get Device Configuration, Apply Device Configuration, Patch Device Configuration, Advanced Patch Device Configuration |
| Configuration Manager - Devices | 3 | Get Device, Search Devices (Paginated, Filtered), Get Devices (Basic Options) |
| Configuration Manager - Config Parsers | 7 | Create Config Parser, Get Config Parser, List Config Parsers, Update Config Parser, Delete Config Parser, Delete Config Parsers (Bulk), ... |
| Template Builder | 5 | Apply Template, Apply Templates (Bulk), Parse Template (TextFSM), Render Jinja2 Template with Cast, Render Jinja Template |

A handful of workflow names (`Create Device Template`, `Get Device`, `Update Device Template`) are prefixed with `Itential Platform - Configuration Manager` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform - Configuration Manager:latest` Integration Model | Import from [`itential_platform_configuration_manager-latest.json`](./OpenAPIs/itential_platform_configuration_manager-latest.json) before importing the project |
| `Itential Platform - Configuration Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform - Configuration Manager` — update the `adapter_id` value in each workflow task if yours is named differently |
