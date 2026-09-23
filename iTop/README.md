iTop is an open-source, web-based IT Service Management and CMDB platform from Combodo, covering tickets (incidents, requests, changes, problems), configuration items, contacts, and organizations, with a fully customizable data model.

This project provides an OpenAPI spec for automating against iTop's REST/JSON API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itop-latest.json`](#itop-latestjson)
  - [`itop-1.3.json`](#itop-13json)
- [Studio Projects](#studio-projects)
  - [iTop Project](#itop-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | iTop REST/JSON API OpenAPI spec — curated `-latest` plus the dated reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing the core REST/JSON operation workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `iTop:latest` Integration Model | Required to run the Studio Project below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to iTop's REST/JSON API.

## Integration Configuration

Import `itop-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your iTop instance.

Authentication is a static API token — an application token or a personal token generated in iTop — sent as the `Auth-Token` header.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "AuthToken": { "value": "<your-itop-api-token>" }
  },
  "server": {
    "protocol": "https",
    "host": "<your-itop-host>",
    "base_path": "/itop/webservices/rest.php"
  }
}
```

`base_path` is the full path to iTop's REST endpoint on your instance — adjust the `/itop` segment (or drop it) to match wherever iTop is installed.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`itop-latest.json`](./OpenAPIs/itop-latest.json) | latest (curated) | 1 | Single operation-dispatch endpoint covering list_operations, core/check_credentials, and the core/get, core/create, core/update, core/delete, and core/apply_stimulus actions |
| [`itop-1.3.json`](./OpenAPIs/itop-1.3.json) | 1.3 | 1 | Dated reference spec for the same REST/JSON API version |

### `itop-latest.json`

iTop's REST/JSON API is a single endpoint that dispatches on an `operation` field inside the request body rather than exposing one path per resource. This spec models that one endpoint, with the request body schema and per-operation examples covering:

- **Discovery**: `list_operations`
- **Auth check**: `core/check_credentials`
- **CRUD**: `core/get`, `core/create`, `core/update`, `core/delete` — against any object class (tickets such as UserRequest, Incident, and Change; CIs; contacts; organizations; and custom classes)
- **Lifecycle**: `core/apply_stimulus` — trigger a state transition on an object

### `itop-1.3.json`

Dated reference spec for REST/JSON API version 1.3, identical in shape to `itop-latest.json` without the curation metadata.

---

## Studio Projects

### iTop Project

Backed by the **`iTop:latest`** Integration Model (see [`itop-latest.json`](./OpenAPIs/itop-latest.json) above). The project contains **7 workflows** in a single folder.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Core | 7 | List Operations, Check Credentials, Get Object, Create Object, Update Object, Delete Object, Apply Stimulus |

Each workflow builds the required `json_data` payload for its operation and calls the same underlying REST/JSON endpoint — `class`, `key`, and `fields` are workflow inputs, so the same "Get Object"/"Create Object"/etc. workflow works against any object class (a ticket, a CI, a contact, ...).

#### Dependencies

| Dependency | Notes |
|---|---|
| `iTop:latest` Integration Model | Import from [`itop-latest.json`](./OpenAPIs/itop-latest.json) before importing the project |
| `iTop` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `iTop` — update the `adapter_id` value in each workflow task if yours is named differently |
