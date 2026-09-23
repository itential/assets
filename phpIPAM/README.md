phpIPAM is an open-source, web-based IP address management (IPAM) application for tracking sections, subnets, IP addresses, VLANs, and network devices.

This project provides OpenAPI specs for automating against phpIPAM's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for IPAM automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`phpipam-latest.json`](#phpipam-latestjson)
  - [`phpipam-1.8.2.json`](#phpipam-182json)
- [Studio Projects](#studio-projects)
  - [`phpIPAM.project.json`](#phpipamprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | phpIPAM REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | CRUD workflows for Sections, Subnets, Addresses, VLANs, and Devices |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| phpIPAM | 1.4+ (static app code token requires 1.4+) |
| phpIPAM API app | Required — created under Administration → API |

## Integration Configuration

phpIPAM's REST API is enabled per "API app" (Administration → API → create app), and every request is sent under that app's own path segment: `/api/<APP_ID>/...`.

Authentication is a token in the `token` header. Two options:

- **Static app code token (recommended)** — set the app's **App security** to `SSL with App code token` and enter a fixed code. That code is used directly as the token on every request — no login step, no expiry.
- **Dynamic session token** — set **App security** to `SSL with User token`, then `POST /user/` with HTTP Basic credentials to receive a token. The token expires after 6 hours and is reset on each successful request.

```json
{
  "authentication": {
    "tokenAuth": {
      "value": "<your-app-code-or-session-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<phpipam-server>",
    "base_path": "/api/<APP_ID>"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`phpipam-latest.json`](./OpenAPIs/phpipam-latest.json) | latest (curated) | 37 | Trimmed to 37 of 82 upstream operations covering common CRUD for IPAM automation — see breakdown below |
| [`phpipam-1.8.2.json`](./OpenAPIs/phpipam-1.8.2.json) | 1.8.2 | 82 | Full spec covering phpIPAM's documented REST API surface |

### `phpipam-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.8.2`). Trimmed to 37 of 82 upstream operations covering common CRUD for IPAM automation.

Resources included, by category:

- **Sections**: list, get, create, update, delete
- **Subnets**: list, get, create, update, delete, usage, child subnets, addresses within a subnet, first free address, CIDR search
- **Addresses**: get, create, update, delete, get by IP within a subnet, search by IP, search by hostname, first free address (get/create)
- **VLANs**: list, get, create, update, delete, subnets on a VLAN
- **Devices**: list, get, create, update, delete, addresses on a device, search

### `phpipam-1.8.2.json`

Full spec covering phpIPAM's documented REST API surface (82 operations): everything in `phpipam-latest.json` plus user/session token management, VLAN (L2) domains, VRFs, global search, and the longer tail of subnet/address sub-actions (recursive child listing, subnet resize/split, permissions, truncate, tags, custom fields, ping). See `phpipam-latest.json` above for the curated subset.

## Studio Projects

### `phpIPAM.project.json`

One workflow per curated operation in `phpipam-latest.json`, one folder per resource.

Every workflow's adapter task is wired to the Integration instance name `phpIPAM`. After importing, either name your Integration instance `phpIPAM`, or update the `adapter_id` value in each workflow task to match your own instance name.

**Sections**

| Workflow | Scope |
|---|---|
| List sections | Get a list of all sections |
| Create section | Create a new section |
| Update section | Update an existing section |
| Delete section | Delete a section by ID |
| Get section | Get a single section by ID |

**Subnets**

| Workflow | Scope |
|---|---|
| List subnets | Get a list of all subnets across all sections |
| Create subnet | Create a new subnet |
| Update subnet | Update an existing subnet |
| Get subnet | Get a single subnet by ID |
| Delete subnet | Delete a subnet by ID |
| Get subnet usage | Get address usage statistics for a subnet |
| List child subnets | Get the immediate child subnets of a subnet |
| List subnet addresses | Get all IP addresses within a subnet |
| Get first free address | Get the first available IP address in a subnet |
| Search subnet by CIDR | Search for a subnet by its CIDR notation |

**Addresses**

| Workflow | Scope |
|---|---|
| Create address | Create a new IP address |
| Get address | Get a single IP address by ID |
| Update address | Update an existing IP address |
| Delete address | Delete an IP address by ID |
| Get address by IP in subnet | Get an IP address by its IP value within a specific subnet |
| Search address by IP | Search for an IP address across all subnets |
| Search address by hostname | Search for IP addresses by hostname |
| Get first free address in subnet | Get the first available IP address in a subnet |
| Create address at first free IP | Create a new IP address at the first available IP in a subnet |

**VLANs**

| Workflow | Scope |
|---|---|
| List VLANs | Get a list of all VLANs |
| Create VLAN | Create a new VLAN |
| Update VLAN | Update an existing VLAN |
| Delete VLAN | Delete a VLAN by ID |
| Get VLAN | Get a single VLAN by ID |
| List VLAN subnets | Get the subnets assigned to a VLAN |

**Devices**

| Workflow | Scope |
|---|---|
| List devices | Get a list of all devices |
| Create device | Create a new device |
| Update device | Update an existing device |
| Delete device | Delete a device by ID |
| Get device | Get a single device by ID |
| List device addresses | Get the IP addresses assigned to a device |
| Search devices | Search devices by hostname, IP, or description |
