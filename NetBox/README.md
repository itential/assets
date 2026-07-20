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
- [Studio Projects](#StudioProjects)
    - [`Netbox Inventory Sync`](#netbox-inventory-sync)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | NetBox REST API OpenAPI specs — curated `-latest` plus full dated versions |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| NetBox | 3.7 – 4.6 (see OpenAPIs below for exact spec versions available) |
| NetBox Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your NetBox instance.

Authentication is an API token in the `Authorization` header:

```
Authorization: Token <your-netbox-api-token>
```

Generate a token in NetBox under your user profile → **API Tokens**.

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

## `StudioProjects`

### `netbox-inventory-sync` [Netbox Inventory Sync.project.json]
This project contains workflows for creating inventories and populating them with nodes in Inventory Manager from Netbox
This pulls the netbox inventory through loops using pagination, check and creates a inventory called "Netbox" in inventory manager and adds all the devices to the "Netbox" Inventory. The "platform" for IAG5 is fetched using the "Manufacturer" of the device, i.e if cisco is "cisco-ios", juniper is "junos" and nokia/aclatel is "sros"
- Netbox Inventory Sync
- Get Netbox Inventory 
- Create Inventory And Add Nodes
- Add Device to Inventory

### `netbox-4.1.json`

Full, unmodified vendor spec for NetBox 4.1 (1073 operations) — the vendor's complete API surface, preserved as-is. See `netbox-latest.json` above for the curated subset if you just need common CRUD automation.

### `netbox-3.7.8.json`

Full, unmodified vendor spec for NetBox 3.7.8 (893 operations) — the vendor's complete API surface, preserved as-is. See `netbox-latest.json` above for the curated subset if you just need common CRUD automation.
