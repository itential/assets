# Cloudify

Cloudify is an open-source cloud orchestration platform for modeling, deploying, and managing multi-cloud and hybrid infrastructure and applications through TOSCA-based blueprints.

This project provides OpenAPI specs for automating against Cloudify Manager's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cloudify-latest.json`](#cloudify-latestjson)
  - [`cloudify-3.1.json`](#cloudify-31json)
- [Studio Projects](#studio-projects)
  - [Cloudify Project](#cloudify-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cloudify Manager API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 26 workflows in 8 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Cloudify:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `cloudify-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Cloudify Manager.

Authentication is HTTP Basic Auth, using a Cloudify Manager username and password.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "BasicAuth": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-cloudify-manager-host>",
    "base_path": "/api/v3.1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cloudify-latest.json`](./OpenAPIs/cloudify-latest.json) | latest (curated) | 26 | Curated to blueprint, deployment, execution, node/node-instance, and secret CRUD — see breakdown below |
| [`cloudify-3.1.json`](./OpenAPIs/cloudify-3.1.json) | 3.1 | 95 | Full spec for the Cloudify Manager REST API, version 3.1 |

### `cloudify-latest.json`

Built from Cloudify Manager's REST API v3.1, curated to the core blueprint/deployment lifecycle categories.

Resources included, by category:

- **Blueprints**: list, get, upload, delete, set visibility
- **Deployments**: list, create, delete, get capabilities, get outputs, set visibility
- **Executions**: list, start, get, update (cancel/resume/kill/requeue)
- **Nodes**: list
- **Node Instances**: list, get, update
- **Secrets**: list, get, create, update, delete
- **Events**: list
- **Status**: get

### `cloudify-3.1.json`

Full, unmodified vendor spec for the Cloudify Manager REST API, version 3.1, preserved as-is. See `cloudify-latest.json` above for the curated subset if you just need common blueprint/deployment automation.

## Studio Projects

### Cloudify Project

Backed by the **`Cloudify:latest`** Integration Model (see [`cloudify-latest.json`](./OpenAPIs/cloudify-latest.json) above). The project contains **26 workflows** organized into **8 folders**, one workflow per curated operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Blueprints | 5 | List, get, upload, delete, set visibility |
| Deployments | 6 | List, create, delete, get capabilities, get outputs, set visibility |
| Executions | 4 | List, start, get, update |
| Nodes | 1 | List |
| Node Instances | 3 | List, get, update |
| Secrets | 5 | List, get, create, update, delete |
| Events | 1 | List |
| Status | 1 | Get |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Cloudify:latest` Integration Model | Import from [`cloudify-latest.json`](./OpenAPIs/cloudify-latest.json) before importing the project |
| `Cloudify` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Cloudify` — update the `adapter_id` value in each workflow task if yours is named differently |
