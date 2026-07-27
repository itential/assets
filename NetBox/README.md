# NetBox

NetBox is an open-source network source of truth platform for IP address management (IPAM) and data center infrastructure management (DCIM) — devices, racks, sites, interfaces, prefixes, IP addresses, VLANs, and more.

This project provides OpenAPI specs for automating against NetBox's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for network automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`netbox-latest.json`](#netbox-latestjson)
  - [`netbox-4.1.json`](#netbox-41json)
  - [`netbox-3.7.8.json`](#netbox-378json)
- [Studio Projects](#studio-projects)
  - [`NetBox.project.json`](#netboxprojectjson)
  - [`NetBox Inventory Sync.project.json`](#netbox-inventory-syncprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | NetBox REST API OpenAPI specs — curated `-latest` plus full dated versions |
| [Studio Projects/](./Studio%20Projects/) | CRUD workflows for Devices, IP Addresses, Prefixes, and VLANs, plus a NetBox-to-Inventory-Manager sync project |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| NetBox | 3.7 – 4.6 (see OpenAPIs below for exact spec versions available) |
| NetBox Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is an API token in the `Authorization` header. NetBox 4.6+ generates **v2 tokens** by default — the header scheme depends on which version your token is:

```
# v2 (current standard, NetBox 4.6+)
Authorization: Bearer <key>.<token>

# v1 (legacy — deprecated in NetBox 4.6, removed in 5.0)
Authorization: Token <token>
```

Generate a token in NetBox under your user profile → **API Tokens**; the token's `Version` column tells you which format it is.

In Itential Platform's **Admin Essentials**, this goes in the integration's `authentication.tokenAuth.value` field — set it to the **full header value**, scheme prefix included, not just the bare key/token:

```json
"authentication": {
  "tokenAuth": {
    "value": "Bearer nbt_<KEY>.<TOKEN>"
  }
}
```

```json
"authentication": {
  "tokenAuth": {
    "value": "Token <TOKEN>"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`netbox-latest.json`](./OpenAPIs/netbox-latest.json) | latest (curated) | 329 | Trimmed to 329 of 1194 upstream operations covering common CRUD for network automation — see breakdown below |
| [`netbox-4.1.json`](./OpenAPIs/netbox-4.1.json) | 4.1 | 1073 | Full spec for NetBox 4.1. |
| [`netbox-3.7.8.json`](./OpenAPIs/netbox-3.7.8.json) | 3.7.8 | 893 | Full spec for NetBox 3.7.8. |

### `netbox-latest.json`

Actively-maintained spec (`x-vendor-api-version: 4.6.1`). Trimmed to 329 of 1194 upstream operations covering common CRUD for network automation. Pull the full spec from a running NetBox instance's `/api/schema/` endpoint if you need something not covered here.

Resources included, by category:

- **DCIM**: Regions, Site Groups, Sites, Locations, Racks, Manufacturers, Device Types, Device Roles, Platforms, Devices, Interfaces, MAC Addresses, Cables, Connected Device
- **IPAM**: RIRs, Aggregates, Roles, Prefixes, IP Ranges, IP Addresses, VLAN Groups, VLANs, VRFs
- **Virtualization**: Cluster Types, Cluster Groups, Clusters, Virtual Machines, Interfaces
- **Tenancy**: Tenant Groups, Tenants
- **Circuits**: Circuit Types, Providers, Circuits, Circuit Terminations
- **Extras**: Tags, Custom Fields

### `netbox-4.1.json`

Full, unmodified vendor spec for NetBox 4.1 (1073 operations) — the vendor's complete API surface, preserved as-is. See `netbox-latest.json` above for the curated subset if you just need common CRUD automation.

### `netbox-3.7.8.json`

Full, unmodified vendor spec for NetBox 3.7.8 (893 operations) — the vendor's complete API surface, preserved as-is. See `netbox-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### `NetBox.project.json`

Import via **Automation Studio > Projects > Import**. It contains one folder per resource, each with a List/Create/Get/Update/Delete workflow built on `netbox-latest.json`'s Integration Model.

Every workflow's adapter task is wired to the Integration instance name `NetBox`. After importing, either name your Integration instance `NetBox`, or update the `adapter_id` value in each workflow task to match your own instance name.

**Devices**

| Workflow | Scope |
|---|---|
| List Devices | Get a list of device objects |
| Create Device | Create a device object |
| Get Device | Get a device object by ID |
| Update Device | Update a device object by ID |
| Delete Device | Delete a device object by ID |

**IP Addresses**

| Workflow | Scope |
|---|---|
| List IP Addresses | Get a list of IP address objects |
| Create IP Address | Create an IP address object |
| Get IP Addresses | Get an IP address object by ID |
| Update IP Address | Update an IP address object by ID |
| Delete IP Address | Delete an IP address object by ID |

**Prefixes**

| Workflow | Scope |
|---|---|
| List Prefixes | Get a list of prefix objects |
| Create Prefix | Create a prefix object |
| Get Prefix | Get a prefix object by ID |
| Update Prefix | Update a prefix object by ID |
| Delete Prefix | Delete a prefix object by ID |

**VLANs**

| Workflow | Scope |
|---|---|
| List VLAN | Get a list of VLAN objects |
| Create VLAN | Create a VLAN object |
| Get VLAN | Get a VLAN object by ID |
| Update VLAN | Update a VLAN object by ID |
| Delete VLAN | Delete a VLAN object by ID |

### `NetBox Inventory Sync.project.json`

Import via **Automation Studio > Projects > Import**. Syncs NetBox's device inventory into Itential Platform's Inventory Manager — pages through every device in NetBox, creates a `NetBox` inventory if one doesn't already exist, and adds each device as a node. The IG5 `platform` value for each node is derived from the device's NetBox **Manufacturer** (e.g. Cisco → `cisco-ios`, Juniper → `junos`, Nokia/Alcatel → `sros`).

| Workflow | Scope |
|---|---|
| NetBox Inventory Sync | Orchestrator — pages through NetBox devices and syncs each one into Inventory Manager |
| Get NetBox Inventory | Retrieve one page of devices from NetBox |
| Create Inventory And Add Nodes | Create the `NetBox` inventory in Inventory Manager if it doesn't exist |
| Add Device to Inventory | Add a single device as a node, mapping its NetBox Manufacturer to an IG5 platform |
