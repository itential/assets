# Nautobot

Nautobot is an open-source network source of truth and network automation platform — devices, racks, sites/locations, interfaces, prefixes, IP addresses, VLANs, and more, with an extensible plugin ecosystem.

This project provides OpenAPI specs for automating against Nautobot's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for network automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Nautobot REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Nautobot | 2.4.14 |
| Nautobot Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Nautobot instance.

Authentication is a token in the `Authorization` header:

```
Authorization: Token <your-nautobot-api-token>
```

Generate a token in Nautobot under your user profile → **API Tokens**.

## OpenAPIs

### `nautobot-latest.json` (curated)

Actively-maintained spec (`x-vendor-api-version: 2.4.14`). Trimmed to 363 of 2141 upstream operations covering common CRUD for network automation. The full upstream spec includes 221 operations from optional Nautobot plugin apps (Golden Config, BGP, Firewall, Chatops, Design Builder, and others) that vary by deployment — none of those are included here. Pull the full spec from a running Nautobot instance's `/api/swagger.json` endpoint if you need one of the excluded areas or a specific plugin's API.

Resources included, by category:

- **DCIM**: Locations, Location Types, Manufacturers, Device Types, Platforms, Devices, Interfaces, Cables, Connected Device, Racks
- **IPAM**: Namespaces, Prefixes, IP Addresses, VLANs, VLAN Groups, RIRs, VRFs, Route Targets
- **Virtualization**: Cluster Types, Cluster Groups, Clusters, Virtual Machines, Interfaces
- **Tenancy**: Tenant Groups, Tenants
- **Circuits**: Circuit Types, Providers, Circuits, Circuit Terminations
- **Extras**: Tags, Statuses, Roles, Custom Fields

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`nautobot-2.4.14.json`](./OpenAPIs/nautobot-2.4.14.json) | Full spec for Nautobot 2.4.14, including all optional plugin APIs. |

## Dependencies

| Dependency | Notes |
|---|---|
| Nautobot Integration Model | Import from an OpenAPI spec above to build automation against the REST API. |
