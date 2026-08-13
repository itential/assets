IP Fabric is a network assurance platform for automated network discovery, inventory, and verification.

This project provides an OpenAPI spec for automating against IP Fabric's REST API via an Integration Model, plus workflows built on that model. It also retains a set of pre-existing workflows built on the legacy IP Fabric adapter (snapshot creation, snapshot inventory comparison, network route comparison, service path analysis).

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
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing 48 new Integration Model workflows plus the pre-existing legacy adapter workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `IP Fabric API:latest` Integration Model | Required to run the Tables/Snapshots/Path Lookup/Jobs folders |
| [IP Fabric Adapter](https://gitlab.com/itentialopensource/adapters/adapter-ipfabric) | Required to run the Create Network Snapshot/Compare Snapshot Inventory/Analyze Service Path folders (legacy, unmigrated) |

> **Note:** This project does not require Itential Gateway for the Integration Model-backed folders. All API calls are made directly from Itential Platform to IP Fabric's REST API.

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

**Important context on sourcing:** IP Fabric does not publish a standalone official OpenAPI/Swagger file anywhere. Each live instance self-generates a complete `openapi.json` from its own backend, viewable via RapiDoc at `/api/rapidoc` — but that requires access to a real instance. The next-best official artifact is IP Fabric's own [public Postman collection](https://gitlab.com/ip-fabric/integrations/postman) (vendor-maintained, versioned per platform release; this spec was built from the `v7.8` collection), cross-referenced against [IP Fabric's official API reference docs](https://docs.ipfabric.io/latest/IP_Fabric_API/) for endpoints the collection didn't fully document (notably path lookup's request schema).

This spec was also cross-validated against the legacy [IP Fabric Adapter](https://gitlab.com/itentialopensource/adapters/adapter-ipfabric)'s full operation set (268 operations, recovered from its auto-generated OpenAPI export) to confirm coverage and catch renamed/removed endpoints. Of note: the legacy adapter's `deviceDiff` task now maps to `POST /tables/management/changes/devices` — the old `/deviceDiff` endpoint no longer exists in the current API.

**On the "tables" API surface:** IP Fabric's REST API has 200+ near-identical "tables" endpoints — one per data category (routing, addressing, interfaces, security, multicast, MPLS, wireless, and more), all sharing the exact same request shape (`columns`/`filters`/`attributeFilters`/`pagination`/`sort`/`snapshot`). Rather than modeling all 200+ 1:1, this spec groups them into 32 category-and-depth operations — one per top-level category (matching IP Fabric's own path taxonomy: `aci`, `addressing`, `fhrp`, `interfaces`, `inventory`, `management`, `mpls`, `multicast`, `neighbors`, `networks`, `platforms`, `qos`, `routing`, `security`, `spanning-tree`, `vlan`, `vrf`, `vxlan`, `wireless`), with a separate operation per path depth within a category where the category has tables at more than one depth (most tables are 1-3 path segments deep beyond the category name). Each operation takes the table's remaining path segments as **individual path parameters** (`seg1`, `seg2`, `seg3`) rather than one embedded-slash parameter — Itential Platform's OpenAPI adapter URL-encodes slashes within a single path parameter value, which would silently send the wrong URL to IP Fabric for any multi-segment table.

Adds the 12-operation snapshot lifecycle, the consolidated path-lookup (`graphs`) endpoint, and 3 job-control operations. Excludes appliance administration (`os/*`, `auth/*`, `settings/*`, `users/*`) as out of scope for network automation.

Operations included, by category:

- **Tables**: Query any table under `ACI`, `Addressing`, `FHRP`, `Interfaces`, `Inventory`, `Management`, `MPLS`, `Multicast`, `Neighbors`, `Networks`, `Platforms`, `QoS`, `Routing`, `Security`, `Spanning Tree`, `VLAN`, `VRF`, `VXLAN`, or `Wireless` — 32 operations across those 19 categories
- **Snapshots**: List, create, rename, delete, clone, download, load, lock, unload, unlock, get/update settings
- **Path Lookup**: Simulate a unicast or multicast path between two points
- **Jobs**: Cancel, download result, stop

## Studio Projects

### IP Fabric Project

Backed by the **`IP Fabric API:latest`** Integration Model (see [`ip_fabric_api-latest.json`](./OpenAPIs/ip_fabric_api-latest.json) above) for the new folders, plus the pre-existing legacy adapter folders.

#### Folder Structure

| Folder | Workflows | Scope | Backing |
|---|---|---|---|
| Tables | 32 | Query any table across 19 categories (see above) | `IP Fabric API:latest` Integration Model |
| Snapshots | 12 | Snapshot lifecycle management | `IP Fabric API:latest` Integration Model |
| Path Lookup | 1 | Unicast/multicast path simulation | `IP Fabric API:latest` Integration Model |
| Jobs | 3 | Async job control | `IP Fabric API:latest` Integration Model |
| Create Network Snapshot | 1 | Create a snapshot (legacy) | IP Fabric Adapter |
| Compare Snapshot Inventory | 2 | Diff device inventory between two snapshots (legacy) | IP Fabric Adapter |
| Analyze Service Path | 2 | Path lookup between two endpoints (legacy) | IP Fabric Adapter |
| (root) | 2 | Create Network Snapshot, Compare Network Routes From Snapshots (legacy) | IP Fabric Adapter |

The `Cancel IP Fabric Job` workflow is prefixed to avoid colliding with an identically-named workflow already published for another product — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `IP Fabric API:latest` Integration Model | Import from [`ip_fabric_api-latest.json`](./OpenAPIs/ip_fabric_api-latest.json) before importing the project. Backs the Tables, Snapshots, Path Lookup, and Jobs folders. |
| `IP Fabric` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `IP Fabric` — update the `adapter_id` value in each workflow task if yours is named differently |
| [IP Fabric Adapter](https://gitlab.com/itentialopensource/adapters/adapter-ipfabric) | Required for the legacy folders (unmigrated) |

**Testing status:** all 48 new workflows were created and schema-validated against a running Itential Platform instance. The multi-segment path-parameter approach was verified against a live HTTP echo endpoint to confirm segments are sent unencoded. No IP Fabric test instance was available for this pass, so none have been executed against a real account.
