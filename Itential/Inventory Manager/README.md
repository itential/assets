Itential Platform's own Inventory Manager REST API: inventories, bulk node loading, inventory actions, and tags. Lets one Itential Platform (or Itential Gateway) automate device/asset inventory management -- separate from Configuration Manager's device groups and Lifecycle Manager's service instances -- against another Itential Platform instance, or itself.

This project provides an OpenAPI spec for automating Inventory Manager on Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform_inventory_manager-latest.json`](#itential_platform_inventory_manager-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform - Inventory Manager Project](#itential-platform---inventory-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform - Inventory Manager OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform - Inventory Manager project containing all 24 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform - Inventory Manager:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform_inventory_manager-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

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
| [`itential_platform_inventory_manager-latest.json`](./OpenAPIs/itential_platform_inventory_manager-latest.json) | latest | 24 | Inventory Manager — see breakdown below |

### `itential_platform_inventory_manager-latest.json`

Hand-authored from Itential's own published per-operation API reference (docs.itential.com/itential-platform/6/6/api-reference/inventory-manager); no navigable index page exists for this category, so the full slug list was recovered via the docs site's llms.txt. Covers all 24 confirmed Inventory Manager operations across Inventories, Nodes, Actions, and Tags -- the full real surface, not a curated subset. Note this API has no per-node create/update/delete or update endpoints for inventories/actions/tags -- nodes are only bulk-loaded (which clears and reinserts) or bulk-cleared, and tags are created implicitly via the tags array on inventory/node payloads.

- **Inventory Manager - Inventories** (6 ops): Create Inventory, List Inventories, Get Inventory by Identifier, Delete Inventory, Get Inventory Manager Stats, Inventory Manager Health Check
- **Inventory Manager - Nodes** (7 ops): Bulk Load Inventory Nodes, Clear Inventory Nodes, List Nodes (Cross-Inventory), List Nodes for an Inventory, Get Node by Identifier, Expand Node Identifiers to Full Documents, ...
- **Inventory Manager - Actions** (5 ops): Create Inventory Action, List Actions (Cross-Inventory), List Actions for an Inventory, Get Inventory Action, Delete Inventory Action
- **Inventory Manager - Tags** (6 ops): List Tags, Get Tag by Identifier, Get Tag Usage Statistics, List Accessible Tags, List Tags for an Inventory, Find Inventories and Nodes by Tags

## Studio Projects

### Itential Platform - Inventory Manager Project

Backed by the **`Itential Platform - Inventory Manager:latest`** Integration Model (see [`itential_platform_inventory_manager-latest.json`](./OpenAPIs/itential_platform_inventory_manager-latest.json) above). The project contains **24 workflows** organized into **4 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Inventory Manager - Inventories | 6 | Create Inventory, List Inventories, Get Inventory by Identifier, Delete Inventory, Get Inventory Manager Stats, Inventory Manager Health Check |
| Inventory Manager - Nodes | 7 | Bulk Load Inventory Nodes, Clear Inventory Nodes, List Nodes (Cross-Inventory), List Nodes for an Inventory, Get Node by Identifier, Expand Node Identifiers to Full Documents, ... |
| Inventory Manager - Actions | 5 | Create Inventory Action, List Actions (Cross-Inventory), List Actions for an Inventory, Get Inventory Action, Delete Inventory Action |
| Inventory Manager - Tags | 6 | List Tags, Get Tag by Identifier, Get Tag Usage Statistics, List Accessible Tags, List Tags for an Inventory, Find Inventories and Nodes by Tags |

A handful of workflow names (`List Tags`) are prefixed with `Itential Platform - Inventory Manager` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform - Inventory Manager:latest` Integration Model | Import from [`itential_platform_inventory_manager-latest.json`](./OpenAPIs/itential_platform_inventory_manager-latest.json) before importing the project |
| `Itential Platform - Inventory Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform - Inventory Manager` — update the `adapter_id` value in each workflow task if yours is named differently |
