Itential Platform's own Lifecycle Manager REST API: resource models, resource instances, resource actions/action-executions, and instance groups. Lets one Itential Platform (or Itential Gateway) automate network-service lifecycle management -- modeling a service, then creating/updating/deleting instances of it by running model-defined actions -- against another Itential Platform instance, or itself.

This project provides an OpenAPI spec for automating Lifecycle Manager on Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform_lifecycle_manager-latest.json`](#itential_platform_lifecycle_manager-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform - Lifecycle Manager Project](#itential-platform---lifecycle-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform - Lifecycle Manager OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform - Lifecycle Manager project containing all 22 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform - Lifecycle Manager:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform_lifecycle_manager-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

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
| [`itential_platform_lifecycle_manager-latest.json`](./OpenAPIs/itential_platform_lifecycle_manager-latest.json) | latest | 22 | Lifecycle Manager — see breakdown below |

### `itential_platform_lifecycle_manager-latest.json`

Hand-authored from Itential's own published per-operation API reference (docs.itential.com/itential-platform/6/6/api-reference/lifecycle-manager); no downloadable spec or navigable index page exists for this category, so the full slug list was recovered via the docs site's own 404-page suggestions. Covers all 22 confirmed Lifecycle Manager operations across Resource Models, Resource Instances, Actions/Action Executions, and Instance Groups -- the full real surface, not a curated subset. Resource instance lifecycle (create/update/delete) has no direct REST endpoints; it happens exclusively by running a model-defined action of that type via run-action/run-bulk-action.

- **Lifecycle Manager - Resource Models** (8 ops): Get Resource Model, Search Resource Models, Create Resource Model, Update Resource Model, Edit Resource Model (Generate Action Stubs), Delete Resource Model, ...
- **Lifecycle Manager - Resource Instances** (3 ops): Get Resource Instance, Search Resource Instances, Export Resource Instance
- **Lifecycle Manager - Actions** (6 ops): Run Resource Action, Run Bulk Resource Action, Validate Resource Model Actions, Get Action Execution, Search Action Executions, Cancel Action Execution
- **Lifecycle Manager - Instance Groups** (5 ops): Get Instance Group, Search Instance Groups, Create Instance Group, Update Instance Group Membership, Delete Instance Group

## Studio Projects

### Itential Platform - Lifecycle Manager Project

Backed by the **`Itential Platform - Lifecycle Manager:latest`** Integration Model (see [`itential_platform_lifecycle_manager-latest.json`](./OpenAPIs/itential_platform_lifecycle_manager-latest.json) above). The project contains **22 workflows** organized into **4 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Lifecycle Manager - Resource Models | 8 | Get Resource Model, Search Resource Models, Create Resource Model, Update Resource Model, Edit Resource Model (Generate Action Stubs), Delete Resource Model, ... |
| Lifecycle Manager - Resource Instances | 3 | Get Resource Instance, Search Resource Instances, Export Resource Instance |
| Lifecycle Manager - Actions | 6 | Run Resource Action, Run Bulk Resource Action, Validate Resource Model Actions, Get Action Execution, Search Action Executions, Cancel Action Execution |
| Lifecycle Manager - Instance Groups | 5 | Get Instance Group, Search Instance Groups, Create Instance Group, Update Instance Group Membership, Delete Instance Group |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform - Lifecycle Manager:latest` Integration Model | Import from [`itential_platform_lifecycle_manager-latest.json`](./OpenAPIs/itential_platform_lifecycle_manager-latest.json) before importing the project |
| `Itential Platform - Lifecycle Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform - Lifecycle Manager` — update the `adapter_id` value in each workflow task if yours is named differently |
