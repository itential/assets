EfficientIP SOLIDserver is a DDI (DNS-DHCP-IPAM) management platform, providing unified management of DNS zones and records, DHCP scopes and leases, and IP address space (IPv4 and IPv6) alongside VLAN management.

This project provides OpenAPI specs for automating against SOLIDserver's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`efficientip_solidserver-latest.json`](#efficientip_solidserver-latestjson)
  - [`efficientip_solidserver-2.0.json`](#efficientip_solidserver-20json)
- [Studio Projects](#studio-projects)
  - [EfficientIP SOLIDserver Project](#efficientip-solidserver-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | EfficientIP SOLIDserver API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 153 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `EfficientIP SOLIDserver:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `efficientip_solidserver-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your SOLIDserver appliance.

Authentication is HTTP Basic Auth, using the username/password of a SOLIDserver account.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "BasicAuth": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-solidserver-host>",
    "base_path": "/api/v2.0"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`efficientip_solidserver-latest.json`](./OpenAPIs/efficientip_solidserver-latest.json) | latest (curated) | 153 | Curated to DNS, DHCP, IPAM, and VLAN — see breakdown below |
| [`efficientip_solidserver-2.0.json`](./OpenAPIs/efficientip_solidserver-2.0.json) | 2.0 | 231 | Full spec for the EfficientIP SOLIDserver API, version 2.0 |

### `efficientip_solidserver-latest.json`

Built directly from EfficientIP's own official OpenAPI 3.0.2 spec (bundled with their official [`solidserver-go-client`](https://github.com/EfficientIP-Labs/solidserver-go-client)), curated to the core DDI categories.

Resources included, by category:

- **DNS**: ACLs, resource records, servers, views, view parameters, zones, zone parameters
- **DHCP**: ACLs, ACL entries, failover relationships, groups, leases, ranges, scopes, shared networks, static leases, servers (IPv4 and IPv6 for every object)
- **IPAM**: address space, networks, pools, addresses, aliases (IPv4 and IPv6)
- **VLAN**: domains, ranges, VLANs

Excluded: Device Manager (physical device/port/link inventory), Application (load-balancing), and DNS Guardian (security policy) — all outside DDI automation scope. Within the kept categories, only "count" operations (return a count of matching objects, not needed for CRUD automation) were dropped — every other operation, including full IPv4/IPv6 parity, is included.

A handful of resource names are prefixed with `EfficientIP` (e.g. `EfficientIP Create DNS View`) to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

### `efficientip_solidserver-2.0.json`

Full, unmodified vendor spec for the EfficientIP SOLIDserver API, version 2.0 — the vendor's complete API surface (including Device Manager, Application, and DNS Guardian), preserved as-is. See `efficientip_solidserver-latest.json` above for the curated subset if you just need common DDI automation.

## Studio Projects

### EfficientIP SOLIDserver Project

Backed by the **`EfficientIP SOLIDserver:latest`** Integration Model (see [`efficientip_solidserver-latest.json`](./OpenAPIs/efficientip_solidserver-latest.json) above). The project contains **153 workflows** organized into **4 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| DHCP | 63 | ACLs, ACL entries, failover, groups, leases, ranges, scopes, shared networks, static leases, servers |
| IPAM | 43 | Address space, networks, pools, addresses, aliases |
| DNS | 32 | ACLs, resource records, servers, views, view/zone parameters, zones |
| VLAN | 15 | Domains, ranges, VLANs |

#### Dependencies

| Dependency | Notes |
|---|---|
| `EfficientIP SOLIDserver:latest` Integration Model | Import from [`efficientip_solidserver-latest.json`](./OpenAPIs/efficientip_solidserver-latest.json) before importing the project |
| `EfficientIP SOLIDserver` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `EfficientIP SOLIDserver` — update the `adapter_id` value in each workflow task if yours is named differently |
