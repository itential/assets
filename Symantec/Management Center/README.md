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
  - [`symantec_management_center-1.0.json`](#symantec_management_center-10json)
- [Studio Projects](#studio-projects)
  - [Symantec Management Center Project](#symantec-management-center-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Management Center REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 121 workflows in 8 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Symantec Management Center | REST API at `/api`, reachable on port 8082 |
| `Symantec Management Center:latest` Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Management Center appliance. The API is rooted at `/api` — this must be set in the instance's `server.base_path` field, since the platform builds the request URL from `protocol`/`host`/`port`/`base_path` rather than any path in the OpenAPI spec itself.

Authentication is a static API token, generated in the Management Center console under **Administration > Users > Generate Token** (up to 360-day validity) and replayed as-is on the `X-Auth-Token` header — no login call involved.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<mc-host>:8082",
    "base_path": "/api"
  },
  "authentication": {
    "apiKeyAuth": {
      "value": "<api-token>"
    }
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`symantec_management_center-latest.json`](./OpenAPIs/symantec_management_center-latest.json) | latest (curated) | 121 | Alerts, device/device group management, file store, folders, jobs, policies, scripts, and tenants — see breakdown below |
| [`symantec_management_center-1.0.json`](./OpenAPIs/symantec_management_center-1.0.json) | 1.0 | 154 | Full spec covering every documented operation |

### `symantec_management_center-latest.json`

Trimmed to 121 of 154 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Alerts**: Raise, Get, List, Acknowledge, Unacknowledge, Update, Add Note
- **Devices**: List/Get, Health, License, Status, Connection, Software, Certificates, Command, Monitor/Unmonitor, Password, Attributes, Add/Remove
- **Device Groups**: List (root/search), Get, Children, Devices, Create (root/child), Update, Move, Delete, Attributes, Add/Remove Device
- **Files**: List, Get, Get Content, Upload, Update, Delete
- **Folders**: List, Get, Children, Types, Create (root/child), Update, Move, Delete, Entries (add/move/delete)
- **Jobs**: List, Get, Import, Update, Delete, Run, Cancel, Enable/Disable, Export, Result, Artifacts
- **Policies**: List, Get, Create, Update, Delete, Content (get/create/by version/type), Attributes, Versions, Folders, Targets (add/get/install/preview/enable/disable/delete/deployment), Install
- **Scripts**: List, Get, Create, Update, Delete, Content (get/create/by version), Attributes, Versions, Execute, Install
- **Tenants**: List, Get, Create, Update, Delete

### `symantec_management_center-1.0.json`

Full spec (154 operations across all 11 documented tag categories). The vendor's API overview lists its version as `1.0`.

## Studio Projects

### Symantec Management Center Project

Backed by the **`Symantec Management Center:latest`** Integration Model (see [`symantec_management_center-latest.json`](./OpenAPIs/symantec_management_center-latest.json) above). The project contains **121 workflows** organized into **8 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Alerts | 7 | Raise/query/acknowledge alerts and alert notes |
| Devices | 38 | Managed device inventory, health, license, status, connection, software, certificates, commands, monitoring, and device group CRUD/membership |
| Files | 6 | File store CRUD and content upload/download |
| Folders | 12 | Folder CRUD, children, types, and entry management |
| Jobs | 15 | Job CRUD, run/cancel/enable/disable, export, results, and artifacts |
| Policies | 25 | Policy CRUD, content and content versions, attributes, and deployment targets |
| Scripts | 13 | Script CRUD, content and content versions, attributes, execution, and installation |
| Tenants | 5 | Tenant CRUD |

`Create Policy Content`/`Create Script Content` send the object's full resulting content in one call (the underlying API has no single-entry add/remove endpoint) — read the current content first, build the full entry list client-side, then pass it in as `requestBody`.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Symantec Management Center:latest` Integration Model | Import from [`symantec_management_center-latest.json`](./OpenAPIs/symantec_management_center-latest.json) before importing the project |
| `Symantec Management Center` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Symantec Management Center`; update the `adapter_id` value in each workflow task if yours is named differently |
