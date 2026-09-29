# Splunk

Splunk is a platform for searching, monitoring, and analyzing machine-generated data. A running Splunk Enterprise instance exposes a management REST API directly on its management port, requiring no separate gateway or middleware layer.

This project provides a Studio Project of workflows covering the management REST API operations most useful for automation, plus an OpenAPI spec for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Splunk](#splunk)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
    - [Request Body Format](#request-body-format)
  - [OpenAPIs](#openapis)
    - [`splunk-latest.json`](#splunk-latestjson)
  - [Studio Projects](#studio-projects)
    - [Splunk Project](#splunk-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Splunk management REST API OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 19 workflows in 3 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Splunk Enterprise | Any release exposing the management REST API on its management port (default `8089`) |
| `Splunk:latest` Integration Model | Required to build automation against the OpenAPI spec |
| A Splunk user with a password and sufficient role capabilities for search, saved search, and index administration | HTTP Basic Auth — see **Integration Configuration** below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the Splunk management port.

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Splunk instance's management port.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<splunk-host-or-ip>",
    "port": "8089"
  },
  "authentication": {
    "BasicAuth": {
      "username": "<username>",
      "password": "<password>"
    }
  }
}
```

Splunk accepts a static `Authorization: Basic` header built from a username and password. There's no login call or token exchange involved — the credentials are sent as-is on every request.

### Request Body Format

Every operation that accepts a body (creating a search job, controlling a job, creating or updating a saved search, dispatching a saved search, creating or updating an index) sends it as `application/x-www-form-urlencoded`, not JSON — this is how the Splunk management REST API accepts input on every version. Each workflow in the Studio Project exposes these fields under a single `body` input.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`splunk-latest.json`](./OpenAPIs/splunk-latest.json) | latest (curated) | 19 | Search job lifecycle, saved search CRUD/dispatch/history, and index list/create/get/update — see breakdown below |

### `splunk-latest.json`

Curated to 19 of the management REST API's operations, covering common CRUD and operational automation.

Resources included, by category:

- **Search Jobs**: List search jobs; create a search job; get a search job's status; cancel a search job; control a search job (pause/unpause/finalize/cancel/touch/setttl/setpriority); get a search job's results; get a search job's events; export (stream) search results without a persistent job
- **Saved Searches**: List saved searches; create, get, update, and delete a saved search; dispatch a saved search on demand; get a saved search's dispatch history
- **Indexes**: List indexes; create an index; get an index; update an index (including enabling/disabling it and adjusting retention/size limits)

---

## Studio Projects

### Splunk Project

Backed by the **`Splunk:latest`** Integration Model (see [`splunk-latest.json`](./OpenAPIs/splunk-latest.json) above). The project contains **19 workflows** organized into **3 folders**, one atomic workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `Get Search Job Status`, `Dispatch Saved Search`).

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Search Jobs | List Search Jobs, Create Search Job, Get Search Job Status, Cancel Search Job, Control Search Job, Get Search Job Results, Get Search Job Events, Export Search Results | Search job lifecycle: create, monitor, control, and retrieve results/events |
| Saved Searches | List Saved Searches, Create Saved Search, Get Saved Search, Update Saved Search, Delete Saved Search, Dispatch Saved Search, Get Saved Search History | Saved search CRUD, on-demand dispatch, and history |
| Indexes | List Indexes, Create Index, Get Index, Update Index | Index list/create/get/update |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Splunk:latest` Integration Model | Import from [`splunk-latest.json`](./OpenAPIs/splunk-latest.json) before importing the project |
| `Splunk` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Splunk` — update the `adapter_id` value in each workflow task if yours is named differently |
