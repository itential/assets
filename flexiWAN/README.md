# flexiWAN

flexiWAN is an open-source SD-WAN platform pairing the flexiManage central management system with flexiEdge routers, providing centralized configuration, monitoring, and orchestration of SD-WAN device fleets, tunnels, and traffic policies.

This project provides OpenAPI specs for automating against flexiManage's REST API via an Integration Model, plus a companion Studio Project — see **OpenAPIs** and **Studio Projects** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`flexiwan-latest.json`](#flexiwan-latestjson)
  - [`flexiwan-1.0.0.json`](#flexiwan-100json)
- [Studio Projects](#studio-projects)
  - [`flexiWAN.project.json`](#flexiwanprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | flexiManage REST API OpenAPI specs — curated `-latest` plus the full spec |
| [Studio Projects/](./Studio%20Projects/) | Device, tunnel, and policy CRUD workflows, one per curated operation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| flexiManage | 1.0.0 API (SaaS or self-hosted) |
| flexiWAN Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is a static Access Key sent as a Bearer token. Generate an Access Key in flexiManage under Account > Access Keys — there is no login/token-exchange step, and the key does not expire from inactivity.

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin Essentials**, then create an integration pointing at your flexiManage server. The API is rooted at `/api` — this must be set in the instance's `server.base_path` field, since the platform builds the request URL from `protocol`/`host`/`port`/`base_path` rather than any path in the OpenAPI spec itself.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearerAuth": "<ACCESS_KEY>"
  },
  "server": {
    "protocol": "https",
    "host": "manage.flexiwan.com",
    "port": 443,
    "base_path": "/api"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`flexiwan-latest.json`](./OpenAPIs/flexiwan-latest.json) | latest (curated) | 74 | Trimmed to 74 of 143 upstream operations covering device, tunnel, and policy automation — see breakdown below |
| [`flexiwan-1.0.0.json`](./OpenAPIs/flexiwan-1.0.0.json) | 1.0.0 | 143 | Full spec, sourced from flexiManage's published `openapi.yaml` |

### `flexiwan-latest.json`

Curated to 74 of 143 upstream operations covering device, tunnel, and policy automation.

Resources included, by category:

- **Devices**: list/get/update/delete, apply pending changes, get configuration, get status
- **Interfaces**: get status, run an interface action
- **Static Routes**: create, list, update, delete (per device)
- **Routing**: get/update OSPF configuration, list learned routes (per device)
- **DHCP**: create, list, get, update, reapply, delete DHCP servers (per device)
- **Tunnels**: list all tunnels, list device tunnels, update tunnel notification settings
- **Firewall Policies**: full CRUD, plus name-only list and metadata
- **MultiLink Policies**: full CRUD, plus name-only list and metadata
- **QoS Policies**: full CRUD, plus name-only list, metadata, and the QoS traffic map
- **Path Labels**: full CRUD
- **Peers**: create, list, update, delete
- **VRRP**: full CRUD on VRRP groups, plus status and VRRP-eligible interface listing
- **App Identifications**: create, list, get/update (custom and imported), reset (imported), list installed, delete

### `flexiwan-1.0.0.json`

Full spec (143 operations), sourced from flexiManage's published `openapi.yaml`, narrowed to a single auth method (Bearer) and a single server entry per this repo's Integration Model rules. See `flexiwan-latest.json` above for the curated subset if you just need device/tunnel/policy automation.

## Studio Projects

### `flexiWAN.project.json`

One folder per resource category, each with the corresponding CRUD workflows built on `flexiwan-latest.json`'s Integration Model. The project contains **74 workflows** across **14 folders**, one workflow per API operation.

Every workflow's adapter task is wired to the Integration instance name `flexiWAN`. After importing, either name your Integration instance `flexiWAN`, or update the `adapter_id` value in each workflow task to match your own instance name.
