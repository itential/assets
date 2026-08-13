IP Fabric is a network assurance platform for automated network discovery, inventory, and verification.

This project provides an OpenAPI spec for automating against IP Fabric's REST API via an Integration Model, plus a Studio Project of workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`ip_fabric_api-latest.json`](#ip_fabric_api-latestjson)
- [Studio Projects](#studio-projects)
  - [IP Fabric Project](#ip-fabric-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | IP Fabric API OpenAPI spec, built from IP Fabric's official Postman collection and API reference docs |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 48 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `IP Fabric API:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to IP Fabric's REST API.

## Integration Configuration

Import `ip_fabric_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your IP Fabric instance.

Authentication is a static API token in a header:

```
X-API-Token: <your-ip-fabric-api-token>
```

Generate a token at Settings → API Tokens on your IP Fabric instance.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiToken": { "value": "<your-ip-fabric-api-token>" }
  },
  "server": {
    "protocol": "https",
    "host": "<your-instance>.ipfabric.io",
    "base_path": "/api/v7.8"
  }
}
```

> **Note:** IP Fabric doesn't publish a standalone downloadable OpenAPI file — each instance self-generates one from its own backend (reachable at `/api/rapidoc` on a live instance). The `servers` entry in the spec is a static placeholder (`https://HOSTNAME/api/v7.8`) since Itential Platform Integration Models require a static server URL; the actual host is configured per-instance as shown above.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`ip_fabric_api-latest.json`](./OpenAPIs/ip_fabric_api-latest.json) | latest (curated) | 48 | Built from IP Fabric's official Postman collection and API docs — see breakdown below |

### `ip_fabric_api-latest.json`

Operations included, by category:

- **Tables**: Query any table under `ACI`, `Addressing`, `FHRP`, `Interfaces`, `Inventory`, `Management`, `MPLS`, `Multicast`, `Neighbors`, `Networks`, `Platforms`, `QoS`, `Routing`, `Security`, `Spanning Tree`, `VLAN`, `VRF`, `VXLAN`, or `Wireless` — 32 operations across those 19 categories
- **Snapshots**: List, create, rename, delete, clone, download, load, lock, unload, unlock, get/update settings
- **Path Lookup**: Simulate a unicast or multicast path between two points
- **Jobs**: Cancel, download result, stop

## Studio Projects

### IP Fabric Project

Backed by the **`IP Fabric API:latest`** Integration Model (see [`ip_fabric_api-latest.json`](./OpenAPIs/ip_fabric_api-latest.json) above). The project contains **48 workflows** organized into **4 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Tables | 32 | Query any table across 19 categories (see above) |
| Snapshots | 12 | Snapshot lifecycle management |
| Path Lookup | 1 | Unicast/multicast path simulation |
| Jobs | 3 | Async job control |

The `Cancel IP Fabric Job` workflow is prefixed to avoid colliding with an identically-named workflow already published for another product — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `IP Fabric API:latest` Integration Model | Import from [`ip_fabric_api-latest.json`](./OpenAPIs/ip_fabric_api-latest.json) before importing the project |
| `IP Fabric` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `IP Fabric` — update the `adapter_id` value in each workflow task if yours is named differently |

**Testing status:** all 48 workflows were created and schema-validated against a running Itential Platform instance. The multi-segment path-parameter approach was verified against a live HTTP echo endpoint to confirm segments are sent unencoded. No IP Fabric test instance was available for this pass, so none have been executed against a real account.
