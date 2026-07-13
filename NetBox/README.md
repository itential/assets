# NetBox

NetBox is an open-source network source of truth platform for IP address management (IPAM) and data center infrastructure management (DCIM) — devices, racks, sites, interfaces, prefixes, IP addresses, VLANs, and more.

This project provides OpenAPI specs for automating against NetBox's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for network automation — see **OpenAPIs** below.

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

| Spec | Version | Description |
|---|---|---|
| [`netbox-latest.json`](./OpenAPIs/netbox-latest.json) | latest (curated) | Trimmed to 329 of 1194 upstream operations covering common CRUD for network automation — see breakdown below |
| [`netbox-4.1.json`](./OpenAPIs/netbox-4.1.json) | 4.1 | Full spec for NetBox 4.1. |
| [`netbox-3.7.8.json`](./OpenAPIs/netbox-3.7.8.json) | 3.7.8 | Full spec for NetBox 3.7.8. |

### `netbox-latest.json`

Actively-maintained spec (`x-vendor-api-version: 4.6.1`). Trimmed to 329 of 1194 upstream operations covering common CRUD for network automation. Pull the full spec from a running NetBox instance's `/api/schema/` endpoint if you need something not covered here.

Resources included, by category:

- **DCIM**: Regions, Site Groups, Sites, Locations, Racks, Manufacturers, Device Types, Device Roles, Platforms, Devices, Interfaces, MAC Addresses, Cables, Connected Device
- **IPAM**: RIRs, Aggregates, Roles, Prefixes, IP Ranges, IP Addresses, VLAN Groups, VLANs, VRFs
- **Virtualization**: Cluster Types, Cluster Groups, Clusters, Virtual Machines, Interfaces
- **Tenancy**: Tenant Groups, Tenants
- **Circuits**: Circuit Types, Providers, Circuits, Circuit Terminations
- **Extras**: Tags, Custom Fields
