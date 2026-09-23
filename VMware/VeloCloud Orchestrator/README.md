# VeloCloud Orchestrator

VMware (Broadcom) VeloCloud SD-WAN Orchestrator (VCO) is the centralized management plane for a VeloCloud SD-WAN deployment, provisioning and monitoring Edges, Gateways, and Customer (Enterprise) configuration across a fleet of sites. It exposes a REST API, informally called "APIv2," at the `/api/sdwan/v2` base path for provisioning Customers and Edges, managing Edge/Profile configuration modules, and reading Alerts, Events, and Client Devices.

## Table of Contents

- [VeloCloud Orchestrator](#velocloud-orchestrator)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`vmware_velocloud_sdwan_orchestrator-latest.json`](#vmware_velocloud_sdwan_orchestrator-latestjson)
    - [`vmware_velocloud_sdwan_orchestrator-6.4.0.json`](#vmware_velocloud_sdwan_orchestrator-640json)
  - [Studio Projects](#studio-projects)
    - [VMware VeloCloud Orchestrator Project](#vmware-velocloud-orchestrator-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | VCO Orchestration REST API (APIv2) OpenAPI specs — curated `-latest` plus the full reference |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 26 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| VeloCloud SD-WAN Orchestrator | 5.0.0.0+ (APIv2 base path `/api/sdwan/v2`; documented through 6.4.0) |
| `VMware VeloCloud SD-WAN Orchestrator:latest` Integration Model | Required to build automation against the OpenAPI specs |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the Orchestrator.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Orchestrator instance.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<vco-hostname>",
    "port": 443,
    "base_path": "/api/sdwan/v2"
  },
  "authentication": {
    "apiToken": {
      "value": "Token <api_token>"
    }
  }
}
```

Authentication is a static Orchestrator API token, provisioned per-user in the VCO UI (user preferences), and replayed on every request via the `Authorization` header — the full header value is `Token <api_token>`. This replaces the older JSON login + session-cookie flow, which is deprecated. A token can only be downloaded once at creation time, so store it securely when it's generated.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`vmware_velocloud_sdwan_orchestrator-latest.json`](./OpenAPIs/vmware_velocloud_sdwan_orchestrator-latest.json) | latest (curated) | 26 | Curated to Customers, Edges, Edge/Profile configuration modules, Alerts, Events, and Client Devices — see breakdown below |
| [`vmware_velocloud_sdwan_orchestrator-6.4.0.json`](./OpenAPIs/vmware_velocloud_sdwan_orchestrator-6.4.0.json) | 6.4.0 | 72 | Full reference spec covering Alerts, Application Maps, Clients, Configure, Customers, Edges, Events, Firewall Stats, Gateway Migration, Monitor, and Network Services |

### `vmware_velocloud_sdwan_orchestrator-latest.json`

Curated to the 26 operations covering the resources most SD-WAN day-2 automation actually touches:

- **Customers (Enterprises)**: list, create, fetch, delete
- **Edges**: list, provision, fetch, update, delete
- **Edge Configuration modules**: fetch/replace/update `deviceSettings`; fetch/create/replace/update `qos`
- **Profile Configuration modules**: fetch/replace/update `deviceSettings`; fetch/replace/update `qos`
- **Alerts**: list past triggered alerts for a Customer
- **Events**: list a Customer's time-ordered event history
- **Client Devices**: list and fetch VPN client devices

### `vmware_velocloud_sdwan_orchestrator-6.4.0.json`

Full reference spec (72 operations). Adds Application Maps (operator-only), BGP session state, per-Edge and per-Customer Firewall/health/flow/link/path/NNI statistics (including time-series variants), non-SD-WAN service/tunnel status, and Gateway Hitless Migration operations on top of everything in the curated spec.

---

## Studio Projects

### VMware VeloCloud Orchestrator Project

Backed by the **`VMware VeloCloud SD-WAN Orchestrator:latest`** Integration Model (see [`vmware_velocloud_sdwan_orchestrator-latest.json`](./OpenAPIs/vmware_velocloud_sdwan_orchestrator-latest.json) above). The project contains **26 workflows** organized into **6 folders**, one workflow per curated API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Customers | 4 | List, create, fetch, and delete Customers (Enterprises) |
| Edges | 5 | List, provision, fetch, update, and delete Edges |
| Edge Configuration | 7 | Fetch/replace/update the Edge `deviceSettings` module; fetch/create/replace/update the Edge `qos` module |
| Profile Configuration | 6 | Fetch/replace/update the Profile `deviceSettings` module; fetch/replace/update the Profile `qos` module |
| Monitoring | 2 | List Alerts and Events for a Customer |
| Clients | 2 | List and fetch Client (VPN) devices |

#### Dependencies

| Dependency | Notes |
|---|---|
| `VMware VeloCloud SD-WAN Orchestrator:latest` Integration Model | Import from [`vmware_velocloud_sdwan_orchestrator-latest.json`](./OpenAPIs/vmware_velocloud_sdwan_orchestrator-latest.json) before importing the project |
| `VeloCloud` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `VeloCloud` — update the `adapter_id` value in each workflow task if yours is named differently |
