# Address Manager

BlueCat Address Manager is a DDI (DNS-DHCP-IPAM) platform, providing unified management of IP address space (configurations, blocks, and networks for IPv4 and IPv6), DNS zones and resource records, and DHCP ranges.

This project provides OpenAPI specs for automating against Address Manager's RESTful v2 API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`bluecat_address_manager-latest.json`](#bluecat_address_manager-latestjson)
  - [`bluecat_address_manager-2.0.json`](#bluecat_address_manager-20json)
- [Studio Projects](#studio-projects)
  - [BlueCat Address Manager Project](#bluecat-address-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Address Manager RESTful v2 API OpenAPI specs — curated `-latest` plus the full reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 46 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Address Manager | RESTful v2 API |
| `BlueCat Address Manager:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `bluecat_address_manager-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Address Manager instance.

Authentication is HTTP Basic Auth against a static API token: send `POST /api/v2/sessions` with a Basic Auth header of `username:password` to obtain an `apiToken` (the response also includes a ready-to-use, base64-encoded `basicAuthenticationCredentials` value). Configure that value, prefixed with `Basic `, as the integration's static credential — no login call is made from workflows.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<address-manager-host>",
    "port": "443",
    "base_path": "/api/v2"
  },
  "authentication": {
    "apiKeyAuth": {
      "value": "Basic <base64-username:apiToken>"
    }
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`bluecat_address_manager-latest.json`](./OpenAPIs/bluecat_address_manager-latest.json) | latest (curated) | 46 | Curated to configurations, IP blocks/networks/addresses, DHCP ranges, and DNS views/zones/resource records — see breakdown below |
| [`bluecat_address_manager-2.0.json`](./OpenAPIs/bluecat_address_manager-2.0.json) | 2.0 | 60 | Full reference spec for the Address Manager RESTful v2 API, built from BlueCat's official API Guide |

### `bluecat_address_manager-latest.json`

Built from BlueCat's official Address Manager RESTful v2 API Guide, curated to the core DDI CRUD surface.

Resources included, by category:

- **Configurations**: list, create, get, update, delete; list/create blocks and views under a configuration
- **IP Blocks & Networks**: search, get, update, delete blocks; list/create networks under a block; search, get, update, delete networks (IPv4 and IPv6)
- **IP Addresses**: list/assign addresses under a network; search, get, update, clear addresses
- **DHCP**: list/create ranges under a network; get, update, delete ranges (IPv4 and IPv6)
- **DNS Zones & Records**: search, get, update, delete views; list/create zones under a view; search, get, update, delete zones; list/create resource records under a zone; search, get, update, delete resource records

### `bluecat_address_manager-2.0.json`

Full reference spec for the Address Manager RESTful v2 API, built from the same source. Adds server registration and deployment (push configuration to DNS/DHCP servers) and tag management on top of the curated DDI categories above.

## Studio Projects

### BlueCat Address Manager Project

Backed by the **`BlueCat Address Manager:latest`** Integration Model (see [`bluecat_address_manager-latest.json`](./OpenAPIs/bluecat_address_manager-latest.json) above). The project contains **46 workflows** organized into **5 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| DNS Zones & Records | 18 | Views, zones, resource records |
| IP Blocks & Networks | 12 | Blocks, networks |
| IP Addresses | 6 | Addresses |
| Configurations | 5 | Configurations |
| DHCP | 5 | Ranges |

#### Dependencies

| Dependency | Notes |
|---|---|
| `BlueCat Address Manager:latest` Integration Model | Import from [`bluecat_address_manager-latest.json`](./OpenAPIs/bluecat_address_manager-latest.json) before importing the project |
| `BlueCat Address Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `BlueCat Address Manager` — update the `adapter_id` value in each workflow task if yours is named differently |
