# Aria Automation Orchestrator

VMware Aria Automation Orchestrator (formerly vRealize Orchestrator) is VMware's workflow automation engine, orchestrating tasks across vSphere, NSX, and other VMware and third-party systems. It exposes workflows, actions, configurations, and their runtime state through a REST API (`/vco/api`), letting external systems run and monitor Orchestrator workflows programmatically instead of only through the Orchestrator client.

## Table of Contents

- [Aria Automation Orchestrator](#aria-automation-orchestrator)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`vmware_aria_automation_orchestrator-latest.json`](#vmware_aria_automation_orchestrator-latestjson)
    - [`vmware_aria_automation_orchestrator-8.x.json`](#vmware_aria_automation_orchestrator-8xjson)
  - [Studio Projects](#studio-projects)
    - [VMware Aria Automation Orchestrator Project](#vmware-aria-automation-orchestrator-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Curated `-latest` spec plus the full reference spec |
| [Studio Projects/VMware Aria Automation Orchestrator](./Studio%20Projects/VMware%20Aria%20Automation%20Orchestrator.project.json) | 21 workflows, one per curated operation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| VMware Aria Automation Orchestrator | 8.x |
| `VMware Aria Automation Orchestrator:latest` Integration Model | Required for the Studio Project |

## Integration Configuration

Import `vmware_aria_automation_orchestrator-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Orchestrator server. HTTP Basic Auth against vCenter Single Sign-On is the supported authentication mode.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<orchestrator-hostname-or-ip>",
    "base_path": "/vco/api"
  },
  "authentication": {
    "basicAuth": {
      "username": "<username>",
      "password": "<password>"
    }
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`vmware_aria_automation_orchestrator-latest.json`](./OpenAPIs/vmware_aria_automation_orchestrator-latest.json) | latest (curated) | 21 | Actively-maintained, common-CRUD automation spec |
| [`vmware_aria_automation_orchestrator-8.x.json`](./OpenAPIs/vmware_aria_automation_orchestrator-8.x.json) | 8.x | 21 | Full reference spec |

### `vmware_aria_automation_orchestrator-latest.json`

Covers the core resources for orchestration automation:

- **Workflows**: List/find, get definition, run, list runs, get run, get run state, cancel run, get run logs
- **User Interactions**: List, get, answer a waiting interaction
- **Actions**: List, get
- **Categories**: List, get
- **Configurations**: List, get, list attributes, set an attribute value
- **Packages**: List, get

### `vmware_aria_automation_orchestrator-8.x.json`

Full reference spec, same operation set as `-latest`.

---

## Studio Projects

### VMware Aria Automation Orchestrator Project

Backed by the **`VMware Aria Automation Orchestrator:latest`** Integration Model (see [`vmware_aria_automation_orchestrator-latest.json`](./OpenAPIs/vmware_aria_automation_orchestrator-latest.json) above). The project contains **21 workflows** organized into **6 folders**, one atomic workflow per API operation, following the naming convention `<Operation> <Resource>` (e.g. `Run Workflow`, `Get Workflow Run State`).

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Workflows | List Workflows, Get Workflow, Run Workflow, List Workflow Runs, Get Workflow Run, Get Workflow Run State, Cancel Workflow Run, Get Workflow Run Logs, Answer Workflow User Interaction | Find, run, and monitor workflows |
| User Interactions | List User Interactions, Get User Interaction | Waiting user-interaction lookups |
| Actions | List Actions, Get Action | Action lookups |
| Categories | List Categories, Get Category | Category lookups |
| Configurations | List Configurations, Get Configuration, List Configuration Attributes, Set Configuration Attribute Value | Configuration element CRUD |
| Packages | List Packages, Get Package | Package lookups |

#### Dependencies

| Dependency | Notes |
|---|---|
| `VMware Aria Automation Orchestrator:latest` Integration Model | Import from [`vmware_aria_automation_orchestrator-latest.json`](./OpenAPIs/vmware_aria_automation_orchestrator-latest.json) before importing the project |
| `Aria Automation Orchestrator` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Aria Automation Orchestrator` — update the `adapter_id` value in each workflow task if yours is named differently |
