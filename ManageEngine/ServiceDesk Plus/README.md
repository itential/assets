# ServiceDesk Plus

ManageEngine ServiceDesk Plus is an ITSM platform covering incident/request management, problem management, change management, and asset/configuration management (CMDB). This project targets the **on-premise** edition, which authenticates with a static per-technician API key rather than OAuth.

This project provides OpenAPI specs for automating against ServiceDesk Plus's on-premise REST API (V3) via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

> **Note:** ServiceDesk Plus Cloud uses OAuth 2.0 (3LO) via Zoho Accounts instead of a static token. That variant isn't covered here.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`manageengine_servicedesk_plus-latest.json`](#manageengine_servicedesk_plus-latestjson)
  - [`manageengine_servicedesk_plus-v3.json`](#manageengine_servicedesk_plus-v3json)
- [Studio Projects](#studio-projects)
  - [ManageEngine ServiceDesk Plus Project](#manageengine-servicedesk-plus-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | ServiceDesk Plus on-premise V3 REST API OpenAPI specs — curated `-latest` plus a dated reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 20 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| ServiceDesk Plus | On-premise, V3 REST API |
| `ManageEngine ServiceDesk Plus:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the ServiceDesk Plus server.

## Integration Configuration

Import `manageengine_servicedesk_plus-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your ServiceDesk Plus server.

Authentication is a static Authtoken: generate one from a technician's **User Profile > Generate Authtoken** (select **Never Expires**), or from **Admin > Developer Space > API** for an integration-scoped key. Send it in the `authtoken` header.

### Connection Properties

```json
{
  "authentication": {
    "AuthToken": {
      "value": "<your-authtoken>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-servicedeskplus-host>",
    "port": 8080,
    "base_path": "/api/v3"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`manageengine_servicedesk_plus-latest.json`](./OpenAPIs/manageengine_servicedesk_plus-latest.json) | latest (curated) | 20 | Curated to core CRUD across requests, problems, changes, and assets/CIs |
| [`manageengine_servicedesk_plus-v3.json`](./OpenAPIs/manageengine_servicedesk_plus-v3.json) | v3 | 26 | Reference spec — adds request notes, resolutions, and technician/requester lookups |

### `manageengine_servicedesk_plus-latest.json`

Built directly from ManageEngine's official on-premise REST API (V3) documentation. Covers list/get/add/edit/delete for the four core ITSM record types:

- **Requests**: helpdesk tickets — subject, requester, status, priority, category, technician, group
- **Problems**: problem records linked to requests
- **Changes**: change requests with stage/status workflow, risk, and approvals
- **Assets**: hardware/software assets and configuration items — ServiceDesk Plus models CIs as assets scoped to a CI-type product, so this one resource covers both

### `manageengine_servicedesk_plus-v3.json`

Same four record types, plus request notes (list/add), request resolutions (get/edit), and read-only technician/requester lookups for populating assignment fields.

## Studio Projects

### ManageEngine ServiceDesk Plus Project

Backed by the **`ManageEngine ServiceDesk Plus:latest`** Integration Model (see [`manageengine_servicedesk_plus-latest.json`](./OpenAPIs/manageengine_servicedesk_plus-latest.json) above). The project contains **20 workflows** organized into **4 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Requests | 5 | List, get, add, edit, delete |
| Problems | 5 | List, get, add, edit, delete |
| Changes | 5 | List, get, add, edit, delete |
| Assets | 5 | List, get, add, edit, delete |

#### Dependencies

| Dependency | Notes |
|---|---|
| `ManageEngine ServiceDesk Plus:latest` Integration Model | Import from [`manageengine_servicedesk_plus-latest.json`](./OpenAPIs/manageengine_servicedesk_plus-latest.json) before importing the project |
| `ManageEngine ServiceDesk Plus` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `ManageEngine ServiceDesk Plus` — update the `adapter_id` value in each workflow task if yours is named differently |
