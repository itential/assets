# SurrealDB

SurrealDB is a multi-model database that supports document, graph, key-value, and relational data in a single engine, queried via SurrealQL over HTTP or WebSocket. A running SurrealDB server exposes a REST API directly, requiring no separate management layer.

This project provides a Studio Project of workflows covering the HTTP REST API operations most useful for automation, plus an OpenAPI spec for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [SurrealDB](#surrealdb)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
    - [Namespace and Database Headers](#namespace-and-database-headers)
  - [OpenAPIs](#openapis)
    - [`surrealdb-latest.json`](#surrealdb-latestjson)
  - [Studio Projects](#studio-projects)
    - [SurrealDB Project](#surrealdb-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | SurrealDB HTTP REST API OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 15 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| SurrealDB | Any release exposing the HTTP REST API on `/key/*`, `/sql`, `/import`, `/export`, `/health`, and `/version` |
| `SurrealDB:latest` Integration Model | Required to build automation against the OpenAPI spec |
| A SurrealDB root, namespace, database, or record user with a password | HTTP Basic Auth — see **Integration Configuration** below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the SurrealDB server.

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your SurrealDB server.

### Connection Properties

```json
{
  "server": {
    "protocol": "http",
    "host": "<surrealdb-host-or-ip>",
    "port": "8000"
  },
  "authentication": {
    "BasicAuth": {
      "username": "<username>",
      "password": "<password>"
    }
  }
}
```

SurrealDB accepts a static `Authorization: Basic` header built from a username and password. There's no login call or token refresh involved — the credentials are sent as-is on every request.

### Namespace and Database Headers

Every operation in this spec requires a `Surreal-NS` (namespace) and `Surreal-DB` (database) header identifying which namespace/database the request runs against. Each workflow in the Studio Project exposes these as `namespace`/`database` inputs.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`surrealdb-latest.json`](./OpenAPIs/surrealdb-latest.json) | latest (curated) | 15 | Record CRUD, raw SurrealQL queries, bulk import/export, health, and version — see breakdown below |

### `surrealdb-latest.json`

Trimmed to 15 of 24 documented HTTP API operations, covering common CRUD for automation.

Resources included, by category:

- **System**: Get health, get version
- **Records**: Select/create/update/merge/delete all records in a table; select/create/update/merge/delete a specific record by ID
- **Query**: Run a raw SurrealQL query
- **Data**: Export data for a namespace/database; import SurrealQL statements into a namespace/database

---

## Studio Projects

### SurrealDB Project

Backed by the **`SurrealDB:latest`** Integration Model (see [`surrealdb-latest.json`](./OpenAPIs/surrealdb-latest.json) above). The project contains **15 workflows** organized into **4 folders**, one atomic workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `Select Record`, `Delete All Records In Table`).

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| System | Get Health, Get Version | Server health and version checks |
| Records | Select All, Create In Table, Update All, Merge All, Delete All, Select, Create, Update, Merge, Delete | Record CRUD against a table or a specific record |
| Query | Run SurrealQL Query | Raw SurrealQL execution |
| Data | Export Data, Import Data | Bulk data export/import for a namespace/database |

#### Dependencies

| Dependency | Notes |
|---|---|
| `SurrealDB:latest` Integration Model | Import from [`surrealdb-latest.json`](./OpenAPIs/surrealdb-latest.json) before importing the project |
| `SurrealDB` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `SurrealDB` — update the `adapter_id` value in each workflow task if yours is named differently |
