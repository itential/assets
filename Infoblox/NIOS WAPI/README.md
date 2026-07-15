Infoblox NIOS is a DNS, DHCP, and IP address management (DDI) appliance platform. The NIOS Web API (WAPI) is its REST interface, exposing DNS zones and records, DHCP ranges and leases, IPAM networks and addresses, and Grid/member configuration as reference-based objects that can be created, read, updated, and deleted over HTTPS.

This project provides two complementary ways to automate against NIOS WAPI:

- **Studio Project workflows** built on the **Infoblox NIOS DDI Adapter** — network and DNS record CRUD workflows (assign the next available IP, create/modify/delete networks, network containers, and A/CNAME/NS/PTR/fixed-address DNS records).
- **OpenAPI specs** for building new automation directly against the WAPI REST endpoints via an Integration Model. Five `-latest` specs are provided — one general-purpose spec plus four object-domain specs (DHCP, DNS, Grid, IPAM) — each a curated subset covering common CRUD for automation. See **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Adapter (Studio Project workflows)](#adapter-studio-project-workflows)
  - [Integration Model (OpenAPI-based automation)](#integration-model-openapi-based-automation)
- [Studio Projects](#studio-projects)
  - [Infoblox NIOS DDI Project](#infoblox-nios-ddi-project)
- [OpenAPIs](#openapis)
  - [`infoblox_nios_wapi-latest.json`](#infoblox_nios_wapi-latestjson)
  - [`infoblox_nios_wapi-1.0.1.json`](#infoblox_nios_wapi-101json)
  - [`infoblox_nios_wapi_dhcp-latest.json`](#infoblox_nios_wapi_dhcp-latestjson)
  - [`infoblox_nios_wapi_dhcp-2.14.json`](#infoblox_nios_wapi_dhcp-214json)
  - [`infoblox_nios_wapi_dns-latest.json`](#infoblox_nios_wapi_dns-latestjson)
  - [`infoblox_nios_wapi_dns-2.14.json`](#infoblox_nios_wapi_dns-214json)
  - [`infoblox_nios_wapi_grid-latest.json`](#infoblox_nios_wapi_grid-latestjson)
  - [`infoblox_nios_wapi_grid-2.14.json`](#infoblox_nios_wapi_grid-214json)
  - [`infoblox_nios_wapi_ipam-latest.json`](#infoblox_nios_wapi_ipam-latestjson)
  - [`infoblox_nios_wapi_ipam-2.14.json`](#infoblox_nios_wapi_ipam-214json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | NIOS WAPI OpenAPI specs — curated `-latest` plus the full dated spec, for the general API and each of the DHCP, DNS, Grid, and IPAM domains |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing the network/DNS record CRUD workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Infoblox NIOS DDI Adapter | Required for the Studio Project workflows below |
| Infoblox NIOS WAPI Integration Model | Required only if building new automation directly against the OpenAPI specs |
| Infoblox NIOS | 8.6 (WAPI 2.14) — general spec targets WAPI 1.0.1 for backward compatibility |

## Integration Configuration

### Adapter (Studio Project workflows)

Install the [Infoblox NIOS DDI Adapter](https://gitlab.com/itentialopensource/adapters/adapter-infoblox) and configure an instance in **Admin > Adapters**, then update the `adapterId` job variable referenced by each workflow task to match your instance name before importing.

### Integration Model (OpenAPI-based automation)

To build automation directly against the REST API instead, import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Grid Master or member's hostname or IP.

Authentication is HTTP Basic — a NIOS administrator username and password:

```
Authorization: Basic <base64(username:password)>
```

Enable API access for the account under **Grid → Grid Manager → Members → API Settings** in the NIOS UI.

---

## Studio Projects

### Infoblox NIOS DDI Project

| Folder | Workflows | Scope |
|---|---|---|
| (root) | Assign Next IP | Allocate the next available IP address from a network |
| Network | Create Network, Delete Network | IPAM network CRUD |
| Network Container | Create Network Container, Delete Network Container | IPAM network container CRUD |
| DNS A Record | Create, Modify, Delete DNS A Record | A record CRUD |
| DNS CNAME Record | Create, Modify, Delete DNS CNAME Record | CNAME record CRUD |
| DNS NS Record | Create, Modify, Delete DNS NS Record | NS record CRUD |
| DNS PTR Record | Create, Modify, Delete DNS PTR Record | PTR record CRUD |
| DNS Fixed Address Record | Create, Modify, Delete DNS Fixed Address Record | DHCP fixed address CRUD |

All workflows read the adapter instance name from the `adapterId` job variable — set this input when running or calling each workflow.

#### Dependencies

| Dependency | Notes |
|---|---|
| [Infoblox NIOS DDI Adapter](https://gitlab.com/itentialopensource/adapters/adapter-infoblox) | Required for the Studio Project workflows. Update the `adapterId` job variable to match your instance name. |

---

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`infoblox_nios_wapi-latest.json`](./OpenAPIs/infoblox_nios_wapi-latest.json) | latest (curated) | 102 | General-purpose spec — see breakdown below |
| [`infoblox_nios_wapi_dhcp-latest.json`](./OpenAPIs/infoblox_nios_wapi_dhcp-latest.json) | latest (curated) | 40 | DHCP domain spec — see breakdown below |
| [`infoblox_nios_wapi_dns-latest.json`](./OpenAPIs/infoblox_nios_wapi_dns-latest.json) | latest (curated) | 71 | DNS domain spec — see breakdown below |
| [`infoblox_nios_wapi_grid-latest.json`](./OpenAPIs/infoblox_nios_wapi_grid-latest.json) | latest (curated) | 25 | Grid domain spec — see breakdown below |
| [`infoblox_nios_wapi_ipam-latest.json`](./OpenAPIs/infoblox_nios_wapi_ipam-latest.json) | latest (curated) | 63 | IPAM domain spec — see breakdown below |
| [`infoblox_nios_wapi-1.0.1.json`](./OpenAPIs/infoblox_nios_wapi-1.0.1.json) | 1.0.1 | 321 | Full general-purpose spec for WAPI 1.0.1 (321 operations). |
| [`infoblox_nios_wapi_dhcp-2.14.json`](./OpenAPIs/infoblox_nios_wapi_dhcp-2.14.json) | 2.14 | 132 | Full DHCP domain spec for WAPI 2.14 (132 operations). |
| [`infoblox_nios_wapi_dns-2.14.json`](./OpenAPIs/infoblox_nios_wapi_dns-2.14.json) | 2.14 | 241 | Full DNS domain spec for WAPI 2.14 (241 operations). |
| [`infoblox_nios_wapi_grid-2.14.json`](./OpenAPIs/infoblox_nios_wapi_grid-2.14.json) | 2.14 | 183 | Full Grid domain spec for WAPI 2.14 (183 operations). |
| [`infoblox_nios_wapi_ipam-2.14.json`](./OpenAPIs/infoblox_nios_wapi_ipam-2.14.json) | 2.14 | 104 | Full IPAM domain spec for WAPI 2.14 (104 operations). |

### `infoblox_nios_wapi-latest.json`

General-purpose spec (`x-vendor-api-version: 1.0.1`). Trimmed to 102 of 321 upstream operations covering common CRUD for automation.

Resources included, by category:

- **DNS records**: A, AAAA, CNAME, HOST, MX, NS, PTR, SRV, TXT
- **Zones**: Authoritative Zones
- **Views**: DNS Views
- **IPAM**: Networks, Network Containers, Network Views, Ranges, Fixed Addresses, Leases (read-only)
- **Grid**: Grid, Grid DNS Properties, Members
- **Extensible Attributes**: Extensible Attribute Definitions
- **Generic**: Reference-based get/update/delete endpoints used by WAPI for objects without a dedicated single-object path

### `infoblox_nios_wapi-1.0.1.json`

Full, unmodified vendor spec for WAPI 1.0.1 (321 operations) — the vendor's complete API surface, preserved as-is. See `infoblox_nios_wapi-latest.json` above for the curated subset if you just need common CRUD automation.

### `infoblox_nios_wapi_dhcp-latest.json`

DHCP domain spec (`x-vendor-api-version: 2.14`). Trimmed to 40 of 132 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Addressing**: Fixed Addresses (IPv4/IPv6)
- **Ranges**: Ranges, IPv6 Ranges (including next-available-IP)
- **Networks**: Shared Networks (IPv4/IPv6)
- **Leases**: Leases (read/delete)
- **High availability**: DHCP Failover Associations

### `infoblox_nios_wapi_dhcp-2.14.json`

Full, unmodified vendor spec for the DHCP domain, WAPI 2.14 (132 operations) — the vendor's complete API surface, preserved as-is. See `infoblox_nios_wapi_dhcp-latest.json` above for the curated subset if you just need common CRUD automation.

### `infoblox_nios_wapi_dns-latest.json`

DNS domain spec (`x-vendor-api-version: 2.14`). Trimmed to 71 of 241 upstream operations covering common CRUD for automation.

Resources included, by category:

- **DNS records**: A, AAAA, CNAME, HOST, HOST_IPV4ADDR, HOST_IPV6ADDR, MX, NS, PTR, SRV, TXT
- **Views**: DNS Views
- **Zones**: Authoritative Zones, Forward Zones, Delegated Zones

### `infoblox_nios_wapi_dns-2.14.json`

Full, unmodified vendor spec for the DNS domain, WAPI 2.14 (241 operations) — the vendor's complete API surface, preserved as-is. See `infoblox_nios_wapi_dns-latest.json` above for the curated subset if you just need common CRUD automation.

### `infoblox_nios_wapi_grid-latest.json`

Grid domain spec (`x-vendor-api-version: 2.14`). Trimmed to 25 of 183 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Grid**: Grid, Grid DNS Properties, Grid DHCP Properties
- **Members**: Grid Members, Member DNS Properties, Member DHCP Properties
- **Extensible Attributes**: Extensible Attribute Definitions

### `infoblox_nios_wapi_grid-2.14.json`

Full, unmodified vendor spec for the Grid domain, WAPI 2.14 (183 operations) — the vendor's complete API surface, preserved as-is. See `infoblox_nios_wapi_grid-latest.json` above for the curated subset if you just need common CRUD automation.

### `infoblox_nios_wapi_ipam-latest.json`

IPAM domain spec (`x-vendor-api-version: 2.14`). Trimmed to 63 of 104 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Networks**: Networks, Network Containers (IPv4/IPv6, including next-available-IP/network/vlan, split, and resize)
- **Views**: Network Views
- **Addresses**: IPv4 Addresses, IPv6 Addresses
- **VLANs**: VLANs, VLAN Views, VLAN Ranges (including next-available-VLAN-ID)

### `infoblox_nios_wapi_ipam-2.14.json`

Full, unmodified vendor spec for the IPAM domain, WAPI 2.14 (104 operations) — the vendor's complete API surface, preserved as-is. See `infoblox_nios_wapi_ipam-latest.json` above for the curated subset if you just need common CRUD automation.

---
