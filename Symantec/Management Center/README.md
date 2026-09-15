# Management Center

Symantec Management Center (Broadcom) centrally manages ProxySG, Advanced Secure Gateway, and other Symantec network security devices — deploying and monitoring devices, and authoring shared policy content (URL lists, IP lists, and category lists) that those devices consume.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`symantec_management_center-latest.json`](#symantec_management_center-latestjson)
- [Studio Projects](#studio-projects)
  - [Symantec Management Center Project](#symantec-management-center-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Management Center REST API OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 13 workflows in 3 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Symantec Management Center | REST API at `/api`, reachable on port 8082 |
| `Symantec Management Center:latest` Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Management Center appliance.

Authentication is a static API token, generated in the Management Center console under **Administration > Users > Generate Token** (up to 360-day validity) and replayed as-is on the `X-Auth-Token` header — no login call involved.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<mc-host>:8082",
    "base_path": ""
  },
  "authentication": {
    "apiKeyAuth": {
      "value": "<api-token>"
    }
  },
  "tls": {
    "enabled": true,
    "rejectUnauthorized": false
  },
  "variables": {}
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`symantec_management_center-latest.json`](./OpenAPIs/symantec_management_center-latest.json) | latest (curated) | 13 | Device inventory/health/license/status, policy CRUD and content management, and tenant listing — see breakdown below |

### `symantec_management_center-latest.json`

Symantec Management Center doesn't publish a downloadable OpenAPI/Swagger reference — the only machine-readable source found was the [Cortex XSOAR third-party integration](https://github.com/demisto/content/tree/master/Packs/SymantecManagementCenter) for Management Center, whose Python source implements 13 concrete REST calls against the MC API. This spec was built directly from that source; there's no larger machine-readable upstream to trim further, so all 13 operations are carried through as `-latest`.

Resources included, by category:

- **Devices**: List, Get, Get Health, Get License, Get Status
- **Policies**: List, Create, Get, Update, Delete, Get Content, Replace Content
- **Tenants**: List

The `system/info` connectivity-check endpoint (used only for a "test connectivity" action in the source integration) is excluded as self-introspection, not automation content.

## Studio Projects

### Symantec Management Center Project

Backed by the **`Symantec Management Center:latest`** Integration Model (see [`symantec_management_center-latest.json`](./OpenAPIs/symantec_management_center-latest.json) above). The project contains **13 workflows** organized into **3 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Devices | List Devices, Get Device, Get Device Health, Get Device License, Get Device Status | Managed device inventory, health, license, and status |
| Policies | List Policies, Create Policy, Get Policy, Update Policy, Delete Policy, Get Policy Content, Replace Policy Content | Policy CRUD and content (URL/IP/category list) management |
| Tenants | List Tenants | Configured tenants |

`Replace Policy Content` sends the policy's full resulting content in one call (the underlying API has no single-entry add/remove endpoint) — read the current content with `Get Policy Content` first, build the full entry list client-side, then pass it in as `requestBody`.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Symantec Management Center:latest` Integration Model | Import from [`symantec_management_center-latest.json`](./OpenAPIs/symantec_management_center-latest.json) before importing the project |
| `Symantec Management Center` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Symantec Management Center`; update the `adapter_id` value in each workflow task if yours is named differently |
