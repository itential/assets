# Zero Networks

Zero Networks is a microsegmentation and network security platform that automates identity- and network-based access controls, enforcing least-privilege segmentation policies across on-premises, cloud, and OT/IoT assets. Its Portal API exposes network policy rules, reactive (MFA) policies, automatic-enforcement exclusions, internal access policies, RPC rules, custom groups, and asset lookups over a REST interface, authenticated with a static API key.

This project provides a Studio Project of workflows covering the Portal API's network policy and asset automation operations, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Zero Networks](#zero-networks)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`zero_networks-latest.json`](#zero_networks-latestjson)
    - [`zero_networks-1.26.3.json`](#zero_networks-1263json)
  - [Studio Projects](#studio-projects)
    - [Zero Networks Project](#zero-networks-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Zero Networks Portal API OpenAPI specs — curated `-latest` plus the full spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 40 workflows in 9 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Zero Networks Portal | Current SaaS release |
| `Zero Networks:latest` Integration Model | Required to build automation against the OpenAPI specs |
| A Zero Networks API key | Generate under Settings > Integrations > API — see **Integration Configuration** below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the Zero Networks Portal.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Zero Networks Portal tenant.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "portal.zeronetworks.com",
    "base_path": "/v1/api"
  },
  "authentication": {
    "api_key": "<api-key>"
  }
}
```

The Zero Networks Portal API supports a static API key — there's no login call or token refresh involved, the key is sent as-is on every request in the `Authorization` header.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`zero_networks-latest.json`](./OpenAPIs/zero_networks-latest.json) | latest (curated) | 40 | Actively-maintained, covering the Portal API's network policy and asset automation operations — see breakdown below |
| [`zero_networks-1.26.3.json`](./OpenAPIs/zero_networks-1.26.3.json) | 1.26.3 | 40 | Full published spec |

### `zero_networks-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.26.3`). The upstream spec lists 1596 paths, but only 40 operations across 20 paths have implemented request/response bodies — the remainder are unimplemented path stubs. All 40 implemented operations are already common CRUD for automation, so the full usable surface is carried through as `-latest`.

Resources included, by category:

- **Assets**: Search for an asset ID by FQDN
- **Custom Groups**: Create/get/update/delete, list/add/remove members
- **AE Exclusions**: Create/get/update/delete, inbound and outbound
- **Internal Access Policies**: Create/get/update/delete
- **MFA Policies**: Create/get/update/delete, inbound and outbound reactive policies
- **RPC Rules**: Create/get/update/delete
- **Network Rules**: Create/get/update/delete, inbound and outbound segmentation rules

### `zero_networks-1.26.3.json`

Full Portal API spec as published (1596 listed paths, 40 with implemented operations).

---

## Studio Projects

### Zero Networks Project

Backed by the **`Zero Networks:latest`** Integration Model (see [`zero_networks-latest.json`](./OpenAPIs/zero_networks-latest.json) above). The project contains **40 workflows** organized into **9 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Assets | Search Asset By FQDN | Asset ID lookup |
| Custom Groups | Create, Get, Update, Delete, List Members, Add Members, Remove Members | Custom group CRUD and membership |
| AE Exclusions | Create, Get, Update, Delete (inbound and outbound) | Automatic enforcement exclusion rule CRUD |
| Internal Access Policies | Create, Get, Update, Delete | Internal access policy CRUD |
| MFA Inbound Policies | Create, Get, Update, Delete | Inbound reactive MFA policy CRUD |
| MFA Outbound Policies | Create, Get, Update, Delete | Outbound reactive MFA policy CRUD |
| RPC Rules | Create, Get, Update, Delete | RPC rule CRUD |
| Network Rules Inbound | Create, Get, Update, Delete | Inbound network segmentation rule CRUD |
| Network Rules Outbound | Create, Get, Update, Delete | Outbound network segmentation rule CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Zero Networks:latest` Integration Model | Import from [`zero_networks-latest.json`](./OpenAPIs/zero_networks-latest.json) before importing the project |
| `Zero Networks` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Zero Networks` — update the `adapter_id` value in each workflow task if yours is named differently |
