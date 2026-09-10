# Nautobot

Nautobot is an open-source network source of truth and network automation platform — devices, racks, sites/locations, interfaces, prefixes, IP addresses, VLANs, and more, with an extensible plugin ecosystem.

This project provides OpenAPI specs for automating against Nautobot's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for network automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`nautobot-latest.json`](#nautobot-latestjson)
  - [`nautobot-2.4.14.json`](#nautobot-2414json)
- [Studio Projects](#studio-projects)
  - [Nautobot Project](#nautobot-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Nautobot REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Nautobot](./Studio%20Projects/Nautobot.project.json) | 25 workflows covering common CRUD automation |

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

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "tokenAuth": {
      "value": "<your-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-host>",
    "base_path": "/api"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`nautobot-latest.json`](./OpenAPIs/nautobot-latest.json) | latest (curated) | 363 | Trimmed to 363 of 2141 upstream operations — see breakdown below |
| [`nautobot-2.4.14.json`](./OpenAPIs/nautobot-2.4.14.json) | 2.4.14 | 2141 | Full spec for Nautobot 2.4.14, including all optional plugin APIs. |

### `nautobot-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.4.14`). Trimmed to 363 of 2141 upstream operations covering common CRUD for network automation. The full upstream spec includes 221 operations from optional Nautobot plugin apps (Golden Config, BGP, Firewall, Chatops, Design Builder, and others) that vary by deployment — none of those are included here. Pull the full spec from a running Nautobot instance's `/api/swagger.json` endpoint if you need one of the excluded areas or a specific plugin's API.

Resources included, by category:

- **DCIM**: Locations, Location Types, Manufacturers, Device Types, Platforms, Devices, Interfaces, Cables, Connected Device, Racks
- **IPAM**: Namespaces, Prefixes, IP Addresses, VLANs, VLAN Groups, RIRs, VRFs, Route Targets
- **Virtualization**: Cluster Types, Cluster Groups, Clusters, Virtual Machines, Interfaces
- **Tenancy**: Tenant Groups, Tenants
- **Circuits**: Circuit Types, Providers, Circuits, Circuit Terminations
- **Extras**: Tags, Statuses, Roles, Custom Fields

### `nautobot-2.4.14.json`

Full, unmodified vendor spec for Nautobot 2.4.14 (2141 operations), including all optional plugin APIs. See `nautobot-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### Nautobot Project

Backed by the **`Nautobot:latest`** Integration Model (see [`nautobot-latest.json`](./OpenAPIs/nautobot-latest.json) above). The project contains **25 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec — mirroring the same core resources as this repo's NetBox Studio Project.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Devices | List, Create, Get, Update, Delete Device | Device lifecycle |
| Locations | List, Create, Get, Update, Delete Location | Location lifecycle |
| IP Addresses | List, Create, Get, Update, Delete IP Address | IP address lifecycle |
| Prefixes | List, Create, Get, Update, Delete Prefix | Prefix lifecycle |
| VLANs | List, Create, Get, Update, Delete VLAN | VLAN lifecycle |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Nautobot:latest` Integration Model | Import from [`nautobot-latest.json`](./OpenAPIs/nautobot-latest.json) before importing the project |
| `Nautobot` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Nautobot` — update the `adapter_id` value in each workflow task if yours is named differently |
