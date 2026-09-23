# Automox

Automox is a cloud-native endpoint patch and configuration management platform for Windows, macOS, and Linux devices, delivered through a single console with no on-premises infrastructure required. Its Console API exposes device (server), device group, policy, organization, and user management over a REST interface at `https://console.automox.com/api`, authenticated with a static Bearer token.

This project provides a Studio Project of workflows covering the Console API operations most useful for endpoint patch automation, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Automox](#automox)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`automox_console-latest.json`](#automox_console-latestjson)
    - [`automox_console-2021-11-16.json`](#automox_console-2021-11-16json)
  - [Studio Projects](#studio-projects)
    - [Automox Console Project](#automox-console-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Automox Console API OpenAPI specs — curated `-latest` plus the full spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 21 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Automox Console | Current SaaS release |
| `Automox Console:latest` Integration Model | Required to build automation against the OpenAPI specs |
| An Automox API key | Generate under Console > Settings > API Keys — see **Integration Configuration** below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the Automox Console.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Automox Console tenant.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "console.automox.com",
    "base_path": "/api"
  },
  "authentication": {
    "bearerAuth": "<api-key>"
  }
}
```

The Automox Console API supports a static Bearer token — there's no login call or token refresh involved, the key is sent as-is on every request as an `Authorization: Bearer` header.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`automox_console-latest.json`](./OpenAPIs/automox_console-latest.json) | latest (curated) | 21 | Actively-maintained, trimmed to 21 of 44 upstream operations covering common CRUD for endpoint automation — see breakdown below |
| [`automox_console-2021-11-16.json`](./OpenAPIs/automox_console-2021-11-16.json) | 2021-11-16 | 44 | Full Console API spec |

### `automox_console-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2021-11-16`). Trimmed to 21 of 44 upstream operations, covering common CRUD for endpoint patch and configuration automation.

Resources included, by category:

- **Devices**: List/get/update/delete, batch update, list upcoming command queue, issue a command (e.g. trigger a patch scan or install)
- **Device Groups**: List/get/create/update/delete
- **Policies**: List/get/create/update/delete, schedule immediate remediation
- **Organizations**: List organization details
- **Users**: List/get

Dropped from the full spec: manual approval records, community worklets, data extracts, event logs, software package listings, compliance/reporting endpoints (needs-attention, non-compliance, pre-patch reports, policy stats), and API key administration.

### `automox_console-2021-11-16.json`

Full Console API spec (44 operations) as published.

---

## Studio Projects

### Automox Console Project

Backed by the **`Automox Console:latest`** Integration Model (see [`automox_console-latest.json`](./OpenAPIs/automox_console-latest.json) above). The project contains **21 workflows** organized into **5 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Devices | List, Get, Update, Delete, Batch Update, List Command Queue, Issue Command | Device (server) lifecycle and command dispatch |
| Device Groups | List, Get, Create, Update, Delete | Device group CRUD |
| Policies | List, Get, Create, Update, Delete, Schedule Remediation | Patch/configuration policy CRUD plus on-demand remediation |
| Organizations | List | Organization details |
| Users | List, Get | User lookups |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Automox Console:latest` Integration Model | Import from [`automox_console-latest.json`](./OpenAPIs/automox_console-latest.json) before importing the project |
| `Automox Console` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Automox Console` — update the `adapter_id` value in each workflow task if yours is named differently |
