# Puppet

Puppet Enterprise is a configuration management platform for defining infrastructure as code and enforcing it across a node inventory, with on-demand and scheduled orchestration of Puppet agent runs, tasks, and plans.

This project provides two peer OpenAPI specs — the Orchestrator API and the Node Classifier API — for building automation via an Integration Model, plus a Studio Project of ready-to-import workflows built on both.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`puppet_orchestrator-latest.json`](#puppet_orchestrator-latestjson)
  - [`puppet_orchestrator-v1.json`](#puppet_orchestrator-v1json)
  - [`puppet_node_classifier-latest.json`](#puppet_node_classifier-latestjson)
  - [`puppet_node_classifier-v1.json`](#puppet_node_classifier-v1json)
- [Studio Projects](#studio-projects)
  - [Puppet Project](#puppet-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Two peer specs — `puppet_orchestrator-latest.json` (job/task/plan orchestration) and `puppet_node_classifier-latest.json` (node group management) — each with a full dated counterpart |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 25 workflows in 8 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Puppet Enterprise Orchestrator:latest` Integration Model | Required for job/task/plan orchestration workflows |
| `Puppet Enterprise Node Classifier:latest` Integration Model | Required for node group and classification workflows |

## Integration Configuration

Import both OpenAPI specs from `OpenAPIs/` as Integration Models in **Admin > Integrations**, then create one integration instance per model against your Puppet Enterprise primary server.

Authentication for both APIs is a static RBAC token in the `X-Authentication` header. Generate one from the PE console (**My Account > Access tokens**) or with `puppet-access login` on the CLI.

The Orchestrator service listens on port 8143 and is rooted at `/orchestrator/v1`. The Node Classifier service listens on port 4433 and is rooted at `/classifier-api/v1`. Because the two services run on different ports, they're published as separate specs per this repo's one-host-per-spec rule, even though they're usually the same primary server.

### Connection Properties

Orchestrator instance:
```json
{
  "authentication": {
    "puppetAuthToken": {
      "value": "<your-rbac-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-puppet-primary-server>",
    "port": 8143,
    "base_path": "/orchestrator/v1"
  }
}
```

Node Classifier instance:
```json
{
  "authentication": {
    "puppetAuthToken": {
      "value": "<your-rbac-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-puppet-primary-server>",
    "port": 4433,
    "base_path": "/classifier-api/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`puppet_orchestrator-latest.json`](./OpenAPIs/puppet_orchestrator-latest.json) | latest | 15 | Curated Orchestrator subset — see breakdown below |
| [`puppet_orchestrator-v1.json`](./OpenAPIs/puppet_orchestrator-v1.json) | v1 | 17 | Full Orchestrator reference surface |
| [`puppet_node_classifier-latest.json`](./OpenAPIs/puppet_node_classifier-latest.json) | latest | 10 | Curated Node Classifier subset — see breakdown below |
| [`puppet_node_classifier-v1.json`](./OpenAPIs/puppet_node_classifier-v1.json) | v1 | 14 | Full Node Classifier reference surface |

### `puppet_orchestrator-latest.json`

Trimmed to 15 of 17 upstream operations covering job/task/plan orchestration, job monitoring, and node reachability.

Resources included, by category:

- **Commands**: Run Puppet On Demand (deploy), Run Task, Run Plan, Stop Job, Stop Plan
- **Jobs**: List Jobs, Get Job, Get Job Events, Get Job Report, Get Job Nodes
- **Plans**: List Plans, Get Plan
- **Tasks**: List Tasks, Get Task
- **Inventory**: Check Node Reachability

### `puppet_orchestrator-v1.json`

Full reference surface (17 operations), adding task-target creation (privilege-escalation scopes for tasks) and deployment node-usage reporting.

### `puppet_node_classifier-latest.json`

Trimmed to 10 of 14 upstream operations covering node group CRUD, node classification, class/environment discovery, and check-in history.

Resources included, by category:

- **Node Groups**: List, Create, Get, Create Or Replace (full overwrite by ID), Delete, Get Children
- **Classification**: List Classes, Classify Node
- **Discovery**: List Environments, List Node Check-Ins

### `puppet_node_classifier-v1.json`

Full reference surface (14 operations), adding resolved-rule inspection, standalone rule-to-PuppetDB-query translation, and class-cache refresh/timestamp operations.

## Studio Projects

### Puppet Project

Backed by the **`Puppet Enterprise Orchestrator:latest`** and **`Puppet Enterprise Node Classifier:latest`** Integration Models (see above). The project contains **25 workflows** organized into **8 folders**, one atomic workflow per curated operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Orchestrator Commands | 5 | Run Puppet On Demand, Run Task, Run Plan, Stop Job, Stop Plan |
| Orchestrator Jobs | 5 | List Jobs, Get Job, Get Job Events, Get Job Report, Get Job Nodes |
| Orchestrator Plans | 2 | List Plans, Get Plan |
| Orchestrator Tasks | 2 | List Tasks, Get Task |
| Orchestrator Inventory | 1 | Check Node Reachability |
| Node Groups | 6 | List, Create, Get, Create Or Replace, Delete, Get Children |
| Classification | 2 | List Classes, Classify Node |
| Discovery | 2 | List Environments, List Node Check-Ins |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Puppet Enterprise Orchestrator:latest` Integration Model | Import from [`puppet_orchestrator-latest.json`](./OpenAPIs/puppet_orchestrator-latest.json) before importing the project |
| `Puppet Enterprise Node Classifier:latest` Integration Model | Import from [`puppet_node_classifier-latest.json`](./OpenAPIs/puppet_node_classifier-latest.json) before importing the project |
| `Puppet-Orchestrator` integration instance | Create in **Admin > Integrations** with the Orchestrator connection properties above. Orchestrator workflows are wired to an instance named `Puppet-Orchestrator` — update `adapter_id` in each task if yours is named differently |
| `Puppet-NodeClassifier` integration instance | Create with the Node Classifier connection properties above. Node Groups/Classification/Discovery workflows are wired to an instance named `Puppet-NodeClassifier` |
