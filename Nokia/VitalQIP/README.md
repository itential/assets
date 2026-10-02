# VitalQIP

Nokia VitalQIP is an enterprise DNS, DHCP, and IP address management (DDI) platform. Its RESTful API manages IPv4/IPv6 networks, subnets, and addresses, DNS zones and resource records, and IPv6 address blocks, ranges, and pools.

This project provides a Studio Project of workflows covering the RESTful API's IP address, subnet, zone, and resource record management operations, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [VitalQIP](#vitalqip)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`nokia_vitalqip-latest.json`](#nokia_vitalqip-latestjson)
    - [`nokia_vitalqip-1.0.0.json`](#nokia_vitalqip-100json)
  - [Studio Projects](#studio-projects)
    - [Nokia VitalQIP Project](#nokia-vitalqip-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | VitalQIP RESTful API OpenAPI specs — curated `-latest` plus the full spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 59 workflows in 12 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Nokia VitalQIP | RESTful API enabled |
| `Nokia VitalQIP:latest` Integration Model | Required to build automation against the OpenAPI specs |
| A VitalQIP API token | Generate via the VitalQIP RESTful API's token endpoint — see **Integration Configuration** below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to VitalQIP.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your VitalQIP RESTful API endpoint.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "vitalqip.example.com",
    "base_path": "/rest"
  },
  "authentication": {
    "bearerAuth": "<api-token>"
  }
}
```

VitalQIP supports a pre-generated Bearer token — there's no login call or token refresh involved from Itential Platform's side, the token is sent as-is on every request as an `Authorization: Bearer` header. `base_path` must be set explicitly to match your VitalQIP RESTful API deployment (commonly `/rest`) — this platform only applies the `server`/`host`/`port` fields from the spec, not any path suffix.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`nokia_vitalqip-latest.json`](./OpenAPIs/nokia_vitalqip-latest.json) | latest (curated) | 59 | Actively-maintained, trimmed to 59 of 60 upstream operations covering common CRUD for DDI automation — see breakdown below |
| [`nokia_vitalqip-1.0.0.json`](./OpenAPIs/nokia_vitalqip-1.0.0.json) | 1.0.0 | 60 | Full VitalQIP RESTful API spec |

### `nokia_vitalqip-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 59 of 60 upstream operations, covering common CRUD for DDI automation.

Resources included, by category:

- **V4 Network**: Get, delete, add, search
- **V6 Subnet**: Get by address, get by name, delete by address, delete by name, add, update, search, list addresses in subnet, list ranges in subnet
- **V6 Address**: Add, update, delete, get
- **V4 Subnet**: Add, update, search, get, delete, list addresses in subnet
- **V4 Address**: Add, update, delete, get
- **Resource Records**: Add, update, delete (single, by infra type, by name/address), get/search by name
- **Selected V4/V6 Address**: Delete, select an address within a range
- **Zone**: Add, modify, search, get, delete
- **V6 Block**: Add to pool, modify, search, get by UUID, delete (by block info, by address), assign
- **V6 Range**: Add, modify, search, delete
- **V6 Pool**: Add, modify, search, get by UUID, delete

Dropped from the full spec: the `/login` token-generation endpoint — this project's Bearer securityScheme uses a pre-generated token supplied directly, so no login/session step is needed. The vendor's own per-operation `Authentication` header parameter is also dropped from every operation for the same reason.

### `nokia_vitalqip-1.0.0.json`

Full VitalQIP RESTful API spec (60 operations) as published, including the `/login` token-generation endpoint.

---

## Studio Projects

### Nokia VitalQIP Project

Backed by the **`Nokia VitalQIP:latest`** Integration Model (see [`nokia_vitalqip-latest.json`](./OpenAPIs/nokia_vitalqip-latest.json) above). The project contains **59 workflows** organized into **12 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| V4 Network | Get, Delete, Add, Search | IPv4 network CRUD |
| V6 Subnet | Get By Address, Delete By Address, Get Addresses In Subnet, Get Ranges In Subnet, Get By Name, Delete By Name, Add, Update, Search | IPv6 subnet CRUD |
| V6 Address | Add, Update, Delete, Get | IPv6 address CRUD |
| V4 Subnet | Add, Update, Search, Get, Delete, Get Addresses In Subnet | IPv4 subnet CRUD |
| V4 Address | Add, Update, Delete, Get | IPv4 address CRUD |
| Resource Records | Delete Single, Delete By Infra Type, Delete By Name Or Address, Get By Name, Add, Delete, Update | DNS resource record CRUD |
| Selected V4 Address | Delete, Select In Range | IPv4 address selection within a range |
| Selected V6 Address | Delete, Select In Range | IPv6 address selection within a range |
| Zone | Add, Modify, Search, Get, Delete | DNS zone CRUD |
| V6 Block | Add To Pool, Modify, Search, Get By UUID, Delete By Block Info, Delete By Address, Assign | IPv6 address block CRUD and pool assignment |
| V6 Range | Search, Add, Delete, Modify | IPv6 range CRUD |
| V6 Pool | Search, Get By UUID, Add, Modify, Delete | IPv6 pool CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Nokia VitalQIP:latest` Integration Model | Import from [`nokia_vitalqip-latest.json`](./OpenAPIs/nokia_vitalqip-latest.json) before importing the project |
| `Nokia VitalQIP` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Nokia VitalQIP` — update the `adapter_id` value in each workflow task if yours is named differently |
| `orgName` job variable | Every workflow requires the VitalQIP organization name as a job input |
