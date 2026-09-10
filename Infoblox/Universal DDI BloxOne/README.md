Infoblox Universal DDI (BloxOne) is Infoblox's cloud-managed DNS, DHCP, and IPAM platform, providing centralized visibility and control across hybrid and multi-cloud environments. The spec in this folder covers the DHCP and IPAM portions of the BloxOne REST API; DNS configuration is served by a separate BloxOne API surface not covered here.

This project provides an OpenAPI spec for automating against the BloxOne REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`infoblox_universal_ddi_bloxone-latest.json`](#infoblox_universal_ddi_bloxone-latestjson)
  - [`infoblox_universal_ddi_bloxone-1.json`](#infoblox_universal_ddi_bloxone-1json)
- [Studio Projects](#studio-projects)
  - [Infoblox Universal DDI (BloxOne) Project](#infoblox-universal-ddi-bloxone-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Infoblox Universal DDI (BloxOne) REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Infoblox Universal DDI (BloxOne)](./Studio%20Projects/Infoblox%20Universal%20DDI%20%28BloxOne%29.project.json) | 30 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Infoblox Universal DDI (BloxOne) | Cloud Services Portal API, version 1 |
| Infoblox Universal DDI (BloxOne) Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the Infoblox Cloud Services Portal (`https://csp.infoblox.com`).

Authentication is an API key in the `Authorization` header:

```
Authorization: Token <your-bloxone-api-key>
```

Generate an API key from the Infoblox Cloud Services Portal under **Administration → API Keys**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiKeyAuth": {
      "value": "<your-api-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "csp.infoblox.com",
    "base_path": "/api/ddi/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`infoblox_universal_ddi_bloxone-latest.json`](./OpenAPIs/infoblox_universal_ddi_bloxone-latest.json) | latest (curated) | 105 | Actively-maintained spec, trimmed to 105 of 119 upstream operations covering common CRUD for automation — see breakdown below |
| [`infoblox_universal_ddi_bloxone-1.json`](./OpenAPIs/infoblox_universal_ddi_bloxone-1.json) | 1 | 119 | Full spec for Infoblox Universal DDI (BloxOne) API version 1, including Automated Scope Management, DNS usage reporting, config-profile linking, and bulk import/copy operations not carried into the curated spec. |

### `infoblox_universal_ddi_bloxone-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1`). Trimmed to 105 of 119 upstream operations covering common CRUD for automation.

Resources included, by category:

- **DHCP**: Global DHCP config, DHCP Servers, DHCP Hosts (with associations), HA Groups, Fixed Addresses, Hardware Filters, Option Filters, Option Codes, Option Spaces, Option Groups, MAC Address Items, DHCP Filters, DHCP Service instances, Universal Service associations, lease actions (clear leases)
- **IPAM**: IP Spaces, Address Blocks (with ancestor/copy/next-available lookups), Subnets (with ancestor/copy/next-available lookups), Ranges (with next-available-IP), Addresses, Hosts

### `infoblox_universal_ddi_bloxone-1.json`

Full, unmodified vendor spec for Infoblox Universal DDI (BloxOne) API version 1 (119 operations) — the vendor's complete API surface, preserved as-is. See `infoblox_universal_ddi_bloxone-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### Infoblox Universal DDI (BloxOne) Project

Backed by the **`Infoblox Universal DDI (BloxOne):latest`** Integration Model (see [`infoblox_universal_ddi_bloxone-latest.json`](./OpenAPIs/infoblox_universal_ddi_bloxone-latest.json) above). The project contains **30 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec. DNS records aren't covered — as noted above, DNS configuration lives on a separate BloxOne API surface not included in this spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| IP Spaces | List, Create, Get, Update, Delete IP Space | IPAM IP space lifecycle |
| Address Blocks | List, Create, Get, Update, Delete Address Block | IPAM address block lifecycle |
| Subnets | List, Create, Get, Update, Delete Subnet | IPAM subnet lifecycle |
| Ranges | List, Create, Get, Update, Delete Range | IPAM range lifecycle |
| Addresses | List, Create, Get, Update, Delete Address | IPAM address lifecycle |
| DHCP Fixed Addresses | List, Create, Get, Update, Delete DHCP Fixed Address | DHCP fixed address lifecycle |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Infoblox Universal DDI (BloxOne):latest` Integration Model | Import from [`infoblox_universal_ddi_bloxone-latest.json`](./OpenAPIs/infoblox_universal_ddi_bloxone-latest.json) before importing the project |
| `Infoblox Universal DDI (BloxOne)` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Infoblox Universal DDI (BloxOne)` — update the `adapter_id` value in each workflow task if yours is named differently |
