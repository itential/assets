ForeScout Platform (CounterACT / eyeSight) discovers, classifies, and assesses the compliance posture of every device connecting to the network. The Web API exposes read-only visibility into discovered hosts, the host field definitions those hosts are classified against, and the policies/rules driving that classification.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`forescout-latest.json`](#forescout-latestjson)
- [Studio Projects](#studio-projects)
  - [ForeScout Project](#forescout-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | ForeScout Web API OpenAPI spec |
| [Studio Projects/ForeScout](./Studio%20Projects/ForeScout.project.json) | 6 workflows covering host lookup/listing, host field definitions, and policy listing |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| ForeScout Web API module | Must be installed and enabled on the Enterprise Manager / Appliance (Tools > Options > Modules > Web API) |
| `ForeScout` Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your ForeScout Enterprise Manager or standalone Appliance.

Authentication is a JWT, retrieved dynamically by posting Web API credentials to the login endpoint and used as-is on the `Authorization` header (no `Bearer ` prefix). Create the Web API username/password under **Tools > Options > Web API > User Settings** in the ForeScout console, and allow the Itential Platform host under **Client IPs** in that same dialog.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<forescout-host>",
    "base_path": ""
  },
  "authentication": {
    "webApiAuth": {
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://<forescout-host>/api/login",
        "responsePointer": ""
      },
      "parameters": {
        "username": "<web-api-username>",
        "password": "<web-api-password>"
      }
    }
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`forescout-latest.json`](./OpenAPIs/forescout-latest.json) | latest (curated) | 6 | Read-only Web API visibility surface — see breakdown below |

### `forescout-latest.json`

ForeScout doesn't publish a downloadable API reference, so there's no larger upstream spec to trim from — this spec covers the Web API's read-only visibility operations directly.

Resources included, by category:

- **Hosts**: Get by ID, Get by IP, Get by MAC, List
- **Host Fields**: List (field definitions used for classification and filtering)
- **Policies**: List (policies and their rules)

The Data Exchange (DEX) module (list and host-field updates) is not included — it uses HTTP Basic auth and XML request/response bodies, a different, incompatible auth method from the Web API's JWT header.

## Studio Projects

### ForeScout Project

Backed by the **`ForeScout:latest`** Integration Model (see [`forescout-latest.json`](./OpenAPIs/forescout-latest.json) above). The project contains **6 workflows** organized into **3 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Hosts | Get Host By ID, Get Host By IP, Get Host By MAC, List Hosts | Host lookup and listing |
| Host Fields | List Host Fields | Host field definitions |
| Policies | List Policies | Policies and their rules |

#### Dependencies

| Dependency | Notes |
|---|---|
| `ForeScout:latest` Integration Model | Import from [`forescout-latest.json`](./OpenAPIs/forescout-latest.json) before importing the project |
| `ForeScout` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `ForeScout` — update the `adapter_id` value in each workflow task if yours is named differently |
