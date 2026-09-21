# Prism Central

Nutanix Prism Central is the multi-cluster management plane for Nutanix Cloud Platform, providing centralized management of virtual machines, images, networks, and clusters across a Nutanix deployment. It exposes a namespaced v4 REST API — `vmm` (virtual machine management), `networking`, `clustermgmt`, and `prism` — at `https://<pc-ip>:9440/api/<namespace>/<version>/...`, authenticated with a static per-request API key.

This project provides a Studio Project of workflows covering the v4 API operations most useful for infrastructure automation, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Prism Central](#prism-central)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`nutanix-latest.json`](#nutanix-latestjson)
    - [`nutanix-v4.2.json`](#nutanix-v42json)
  - [Studio Projects](#studio-projects)
    - [Nutanix Prism Central Project](#nutanix-prism-central-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Nutanix v4 API OpenAPI specs — curated `-latest` plus the full spec across the relevant namespaces |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 39 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Nutanix Prism Central | pc.2024.3+ (v4 API GA) |
| `Nutanix:latest` Integration Model | Required to build automation against the OpenAPI specs |
| A Nutanix IAM service account with an API key | API key auth is only available for service accounts — see **Integration Configuration** below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to Prism Central.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Prism Central instance.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<pc-ip-or-hostname>",
    "port": "9440",
    "base_path": "/api"
  },
  "authentication": {
    "apiKeyAuthScheme": {
      "value": "<api-key>"
    }
  }
}
```

Nutanix v4 APIs support a static `X-Ntnx-Api-Key` header, issued to an IAM service account (API keys can't be created against a standard user account, and aren't manageable from the Prism Central UI — use the v4 IAM APIs or SDK). There's no login call or token refresh involved — the key is sent as-is on every request.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`nutanix-latest.json`](./OpenAPIs/nutanix-latest.json) | latest (curated) | 39 | Actively-maintained, trimmed to 39 of 418 upstream operations covering common CRUD for infrastructure automation — see breakdown below |
| [`nutanix-v4.2.json`](./OpenAPIs/nutanix-v4.2.json) | v4.2 | 418 | Full spec across the vmm, networking, clustermgmt, and prism namespaces |

### `nutanix-latest.json`

Actively-maintained spec (`x-vendor-api-version: v4.2`). Trimmed to 39 of 418 upstream operations across the `vmm`, `networking`, `clustermgmt`, and `prism` namespaces, covering common CRUD for infrastructure automation.

Resources included, by category:

- **Virtual Machines** (AHV): Create/list/get/update/delete, power operations (on/off/reboot/shutdown/power-cycle/reset), clone, category association/disassociation
- **Images**: Create/list/get/update/delete
- **Subnets**: Create/list/get/update/delete
- **VPCs**: Create/list/get/update/delete
- **Clusters**: Create/list/get/update/delete
- **Categories**: Create/list/get/update/delete

### `nutanix-v4.2.json`

Full spec (418 operations) across the `vmm`, `networking`, `clustermgmt`, and `prism` namespaces (all pinned to the `v4.2` release). Schema and operation names are namespace-prefixed (e.g. `Vmm`, `Networking`, `Clustermgmt`, `Prism`) to avoid collisions between namespaces.

---

## Studio Projects

### Nutanix Prism Central Project

Backed by the **`Nutanix:latest`** Integration Model (see [`nutanix-latest.json`](./OpenAPIs/nutanix-latest.json) above). The project contains **39 workflows** organized into **6 folders**, one atomic workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List Virtual Machines`, `Power On Virtual Machine`).

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Virtual Machines | List, Get, Create, Update, Delete, Power On, Power Off, Reboot, Shutdown, Power Cycle, Reset, Clone, Associate Categories, Disassociate Categories | Full AHV VM lifecycle |
| Images | List, Get, Create, Update, Delete | Image CRUD |
| Subnets | List, Get, Create, Update, Delete | Subnet CRUD |
| VPCs | List, Get, Create, Update, Delete | VPC CRUD |
| Clusters | List, Get, Create, Update, Delete | Cluster CRUD |
| Categories | List, Get, Create, Update, Delete | Category CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Nutanix:latest` Integration Model | Import from [`nutanix-latest.json`](./OpenAPIs/nutanix-latest.json) before importing the project |
| `Nutanix` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Nutanix` — update the `adapter_id` value in each workflow task if yours is named differently |
