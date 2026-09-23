# Enterprise

Starburst Enterprise is a self-hosted, Trino-based analytics platform for querying and governing data across catalogs. Its management REST API is exposed directly by the coordinator at `https://<host>:<port>/api/v1/...`, with a full OpenAPI specification available on every instance at `/api/v1/openApi`. Authentication is HTTP Basic Auth (base64-encoded username/password) for password-based deployments.

This project provides a Studio Project of workflows covering the REST API operations most useful for automation, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Enterprise](#enterprise)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`starburst_enterprise-latest.json`](#starburst_enterprise-latestjson)
    - [`starburst_enterprise-482-e.2.json`](#starburst_enterprise-482-e2json)
  - [Studio Projects](#studio-projects)
    - [Starburst Enterprise Project](#starburst-enterprise-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Starburst Enterprise REST API OpenAPI specs — curated `-latest` plus the full reconstructed spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 43 workflows in 9 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Starburst Enterprise | Any release exposing the `/api/v1` management REST API and `/api/v1/openApi` |
| `Starburst Enterprise:latest` Integration Model | Required to build automation against the OpenAPI specs |
| A Starburst Enterprise user or service account with a password | HTTP Basic Auth is only available for password-based deployments — see **Integration Configuration** below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the Starburst Enterprise coordinator.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Starburst Enterprise coordinator.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<coordinator-host-or-ip>",
    "port": "8443",
    "base_path": "/api"
  },
  "authentication": {
    "BasicAuth": {
      "username": "<username>",
      "password": "<password>"
    }
  }
}
```

Starburst Enterprise accepts a static `Authorization: Basic` header built from a username and password. There's no login call or token refresh involved — the credentials are sent as-is on every request.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`starburst_enterprise-latest.json`](./OpenAPIs/starburst_enterprise-latest.json) | latest (curated) | 43 | Actively-maintained, trimmed to 43 of 91 upstream operations covering common CRUD for automation — see breakdown below |
| [`starburst_enterprise-482-e.2.json`](./OpenAPIs/starburst_enterprise-482-e.2.json) | 482-e.2 | 91 | Full reconstructed spec across Built-in Access Control, Data Products, SQL Jobs, and Data Maintenance |

### `starburst_enterprise-latest.json`

Actively-maintained spec (`x-vendor-api-version: 482-e.2`). Trimmed to 43 of 91 upstream operations, covering common CRUD for automation.

Resources included, by category:

- **Roles**: Create/list/get/update/delete built-in access control roles
- **Grants**: Create/list/get/delete privilege grants on catalogs, schemas, tables, columns, and other entities
- **Location Grants**: Create/list/get/delete read/write grants scoped to a storage location pattern
- **Role Assignments**: Assign/remove roles to/from users and groups, list assignments for a user or group, list all assignments
- **Domains**: Create/list/get/update/delete data domains
- **Data Products**: Create/search/get/update/delete/publish data products
- **Tags**: List/update/delete tags
- **SQL Jobs**: Create/list/get/update/delete/execute ad hoc or scheduled SQL jobs
- **Data Maintenance**: Get/apply/delete cluster maintenance windows

### `starburst_enterprise-482-e.2.json`

Full reconstructed spec (91 operations) across Built-in Access Control (including column masks, row filters, audit logs, entity categories, and role-to-role nesting), Data Products (including clone/import/export, materialized views, sample queries, and per-product tag management), and SQL Jobs (including status/history).

---

## Studio Projects

### Starburst Enterprise Project

Backed by the **`Starburst Enterprise:latest`** Integration Model (see [`starburst_enterprise-latest.json`](./OpenAPIs/starburst_enterprise-latest.json) above). The project contains **43 workflows** organized into **9 folders**, one atomic workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List Roles`, `Create Grant`).

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Roles | List, Get, Create, Update, Delete | Role CRUD |
| Grants | List, Get, Create, Delete | Privilege grant management |
| Location Grants | List, Get, Create, Delete | Storage-location privilege grant management |
| Role Assignments | List All, List/Assign/Remove for User, List/Assign/Remove for Group | Role-to-subject assignment |
| Domains | List, Get, Create, Update, Delete | Data domain CRUD |
| Data Products | Search, Get, Create, Update, Publish, Delete | Data product lifecycle |
| Tags | List, Update, Delete | Tag management |
| SQL Jobs | List, Get, Create, Update, Delete, Execute | SQL job CRUD and execution |
| Data Maintenance | Get, Apply, Delete | Cluster maintenance window management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Starburst Enterprise:latest` Integration Model | Import from [`starburst_enterprise-latest.json`](./OpenAPIs/starburst_enterprise-latest.json) before importing the project |
| `Starburst` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Starburst` — update the `adapter_id` value in each workflow task if yours is named differently |
