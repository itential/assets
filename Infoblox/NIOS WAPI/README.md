Infoblox NIOS is a DNS, DHCP, and IP address management (DDI) appliance platform. The NIOS Web API (WAPI) is its REST interface, exposing DNS zones and records, DHCP ranges and leases, IPAM networks and addresses, and Grid/member configuration as reference-based objects that can be created, read, updated, and deleted over HTTPS.

This project provides OpenAPI specs for automating against NIOS WAPI's REST endpoints via Integration Models, plus a Studio Project of ready-to-import CRUD workflows built on four of those models. Five `-latest` specs are provided — one general-purpose spec plus four object-domain specs (DHCP, DNS, Grid, IPAM) — each a curated subset covering common CRUD for automation. See **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
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
- [Studio Projects](#studio-projects)
  - [Infoblox NIOS WAPI Project](#infoblox-nios-wapi-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | NIOS WAPI OpenAPI specs — curated `-latest` plus the full dated spec, for the general API and each of the DHCP, DNS, Grid, and IPAM domains |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 199 workflows in 4 folders (DNS, IPAM, DHCP, Grid) |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Infoblox NIOS WAPI — DNS:latest`, `— IPAM:latest`, `— DHCP:latest`, `— Grid:latest` Integration Models | Required to run the Studio Project below |
| Infoblox NIOS | 8.6 (WAPI 2.14) — general spec targets WAPI 1.0.1 for backward compatibility |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to your Grid Master or member's WAPI endpoint.

## Integration Configuration

Import the OpenAPI specs from `OpenAPIs/` as Integration Models in **Admin > Integrations**, then create one integration per domain spec you need, each pointing at your Grid Master or member's hostname or IP.

Authentication is HTTP Basic — a NIOS administrator username and password:

```
Authorization: Basic <base64(username:password)>
```

Enable API access for the account under **Grid → Grid Manager → Members → API Settings** in the NIOS UI.

The instance's `authentication`/`server` properties should look like this once configured (the same credentials work across all four domain integrations, since they authenticate against the same Grid Master):

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<nios-admin-username>",
      "password": "<nios-admin-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<grid-master-hostname-or-ip>",
    "base_path": "/wapi/v2.14"
  }
}
```

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

**Platform compatibility note:** the four curated domain specs originally included WAPI's `_return_fields+` query parameter (an "add to the default field set" variant of `_return_fields`) on every List/Get operation. Itential Platform rejects any task input name containing a `+` character, which broke every workflow built on that parameter — confirmed against a real NIOS Grid. Removed from all four curated specs; `_return_fields` (no `+`) is still available for requesting specific fields.

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

Not used by the Studio Project below — its resources overlap with the four domain-specific specs, which cover the same ground with a cleaner, more complete operation set. Import it directly if you want a single general-purpose model instead of four domain-specific ones.

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

## Studio Projects

### Infoblox NIOS WAPI Project

Backed by the four domain-specific Integration Models above (`— DNS:latest`, `— IPAM:latest`, `— DHCP:latest`, `— Grid:latest`). The project contains **199 workflows** organized into **4 folders**, one workflow per curated operation across all four domain specs. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List DNS A Records`, `Get Next Available IP`).

Two IPAM resources are qualified with the domain name in their workflow titles (`IPAM Network`, `IPAM VLAN`) to avoid colliding with identically-named workflows from other vendors' Studio Projects in this repo — Itential Platform workflow names must be unique platform-wide, not just within a project, so if you're importing multiple projects from this repo into the same platform, watch for this class of collision.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| DNS | 71 | A, AAAA, CNAME, HOST (+ HOST_IPV4ADDR/HOST_IPV6ADDR sub-records), MX, NS, PTR, SRV, TXT records; DNS View; Authoritative/Delegated/Forward Zones |
| IPAM | 63 | IPAM Network (+ expand/next-IP/next-network/next-VLAN/resize/split), Network Container, IPv6 Network (+ actions), IPv6 Network Container, Network View, IPv4/IPv6 Address, IPAM VLAN, VLAN Range (+ next-VLAN-ID), VLAN View |
| DHCP | 40 | Fixed Address (v4/v6), Range (+ next-available-IP), IPv6 Range (+ next-available-IP), Shared Network (v4/v6), Lease (list/read/delete), DHCP Failover Association |
| Grid | 25 | Grid, Grid DNS/DHCP Properties, Member, Member DNS/DHCP Properties, Extensible Attribute Definition |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Infoblox NIOS WAPI — DNS:latest`, `— IPAM:latest`, `— DHCP:latest`, `— Grid:latest` Integration Models | Import each from its respective spec above before importing the project |
| `Infoblox DNS`, `Infoblox IPAM`, `Infoblox DHCP`, `Infoblox Grid` integration instances | Create in **Admin > Integrations** with the connection properties above, one per domain. Workflows are wired to these instance names — update the `adapter_id` value in each workflow task if yours are named differently |

**Testing status:** all 199 workflows were created and schema-validated against a running Itential Platform instance. A representative sample across all four domains — `List DNS A Records`, `List IPAM Networks`, `List Ranges`, `List Grids`, `List Grid DHCP Properties`, and `List Member DNS Properties` — was executed against a real Infoblox NIOS Grid and confirmed returning live data. The remaining workflows have not been individually executed.
