# CloudGenix

CloudGenix (now Palo Alto Networks Prisma SD-WAN) provides centralized configuration and monitoring for SD-WAN appliances (ION devices), sites, and tenants via a REST API on the CloudGenix cloud controller.

This project provides an OpenAPI spec for automating against the CloudGenix/Prisma SD-WAN controller API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cloudgenix-latest.json`](#cloudgenix-latestjson)
  - [`cloudgenix-1.0.json`](#cloudgenix-10json)
- [Studio Projects](#studio-projects)
  - [CloudGenix Project](#cloudgenix-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | CloudGenix/Prisma SD-WAN controller API OpenAPI specs |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 31 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `CloudGenix:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `cloudgenix-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your tenant's regional controller.

Authentication is a static API token generated in the CloudGenix/Prisma SD-WAN UI under **System > Access Management > Site Access > Auth Tokens**, sent as-is on every request — there is no login/session exchange.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "staticAuthToken": {
      "value": "<your-cloudgenix-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.<region>.cloudgenix.com",
    "base_path": ""
  }
}
```

Replace `<region>` with your tenant's controller region subdomain (e.g. `sase`, `sasecanada`, `sase-anz`).

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cloudgenix-latest.json`](./OpenAPIs/cloudgenix-latest.json) | latest | 31 | All 31 upstream operations across Elements, Firewall, Network, Policy, Site, and Tenant — see breakdown below |
| [`cloudgenix-1.0.json`](./OpenAPIs/cloudgenix-1.0.json) | 1.0 | 31 | Same content, dated per the vendor's own API version (1.0) |

### `cloudgenix-latest.json`

All 31 operations are read and create only — the CloudGenix API does not expose update/delete on these resources.

Resources included, by category:

- **Tenant**: Get Tenant, Create Tenant
- **Elements**: Get Elements, Create Element, Get Element Interfaces, Create Element Interface, Get Element Interface Status, Get Element SNMP Configuration
- **Sites**: Get Sites, Create Site, Get WAN Interfaces, Create WAN Interface, Get Site Link Health
- **Network**: Get LANs, Create LAN, Get WANs, Create WAN
- **Policy**: Get Application Definition, Create Application, Get Policy Sets, Create Policy Set, Get Policy Set Rules, Create Policy Set Rule
- **Firewall / Security**: Get Security Policy Sets, Create Security Policy Set, Get Security Policy Set Rules, Create Security Policy Set Rule, Get Security Zones, Create Security Zone, Get Site Security Zones, Create Site Security Zone

### `cloudgenix-1.0.json`

Identical content to `-latest.json`, kept as the dated file. Version `1.0` matches the vendor's own declared API version.

## Studio Projects

### CloudGenix Project

Backed by the **`CloudGenix:latest`** Integration Model (see [`cloudgenix-latest.json`](./OpenAPIs/cloudgenix-latest.json) above). The project contains **31 workflows** organized into **6 folders**, one per resource category.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Element | Create Element, Create Element Interface, Get Element Interface Status, Get Element Interfaces, Get Element SNMP Configuration, Get Elements | ION device (element) management |
| Firewall | Create Security Policy Set, Create Security Policy Set Rule, Create Security Zone, Create Site Security Zone, Get Security Policy Set Rules, Get Security Policy Sets, Get Security Zones, Get Site Security Zones | Zone-based security policy |
| Network | Create LAN, Create WAN, Get LANs, Get WANs | LAN/WAN network definitions |
| Policy | Create Application, Create Policy Set, Create Policy Set Rule, Get Application Definition, Get Policy Set Rules, Get Policy Sets | Application-based path/QoS policy |
| Site | Create Site, Create WAN Interface, Get Site Link Health, Get Sites, Get WAN Interfaces | Site and WAN interface management |
| Tenant | Create Tenant, Get Tenant | Tenant-level configuration |

#### Dependencies

| Dependency | Notes |
|---|---|
| `CloudGenix:latest` Integration Model | Import from [`cloudgenix-latest.json`](./OpenAPIs/cloudgenix-latest.json) before importing the project |
| `CloudGenix` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `CloudGenix` — update the `adapter_id` value in each workflow task if yours is named differently |
