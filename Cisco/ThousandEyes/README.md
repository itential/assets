ThousandEyes is Cisco's network and internet performance monitoring platform, running synthetic tests from cloud and enterprise agents to measure network paths, application performance, and outages across the internet, cloud providers, and enterprise networks.

This project provides OpenAPI specs for automating against the ThousandEyes API v7 via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`thousandeyes-latest.json`](#thousandeyes-latestjson)
  - [`thousandeyes-7.0.105.json`](#thousandeyes-70105json)
- [Studio Projects](#studio-projects)
  - [ThousandEyes Project](#thousandeyes-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | ThousandEyes REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/ThousandEyes](./Studio%20Projects/ThousandEyes.project.json) | 32 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| ThousandEyes API | v7.0.105 |
| ThousandEyes Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your ThousandEyes organization (`https://api.thousandeyes.com/v7`).

Authentication is a static, long-lived Bearer token generated once in the ThousandEyes UI (**Account Settings > Users > API Tokens**, roughly 2-year validity) in the `Authorization` header — not an OAuth2 client-credentials exchange, despite some ThousandEyes documentation describing it as an OAuth2 bearer token:

```
Authorization: Bearer <your-thousandeyes-api-token>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearer_token": {
      "value": "<your-thousandeyes-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.thousandeyes.com",
    "base_path": "/v7"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`thousandeyes-latest.json`](./OpenAPIs/thousandeyes-latest.json) | latest (curated) | 32 | Actively-maintained spec, trimmed to 32 of 328 upstream operations — see breakdown below |
| [`thousandeyes-7.0.105.json`](./OpenAPIs/thousandeyes-7.0.105.json) | 7.0.105 | 328 | Full spec for ThousandEyes API v7.0.105 (328 operations) |

### `thousandeyes-latest.json`

Actively-maintained spec (`x-vendor-api-version: 7.0.105`). Trimmed to 32 of 328 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Tests**: List All Tests, plus full CRUD (List, Create, Get, Update, Delete) for HTTP Server Tests and Page Load Tests
- **Agents**: List, Get, Update, Delete
- **Alerts**: List, Get alert instances; List, Create, Get, Update, Delete alert rules
- **Labels**: List, Create, Get, Update, Delete (endpoint agent labels)
- **Tags**: List, Create, Get, Update, Delete

### `thousandeyes-7.0.105.json`

Full, unmodified vendor spec for ThousandEyes API v7.0.105 (328 operations) — the vendor's complete API surface, covering every test type (BGP, DNS, DNSSEC, FTP, SIP, Voice, Web Transaction, API, and more), test results, endpoint agents, dashboards, credentials, and administration. Preserved as-is. See `thousandeyes-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### ThousandEyes Project

Backed by the **`ThousandEyes:latest`** Integration Model (see [`thousandeyes-latest.json`](./OpenAPIs/thousandeyes-latest.json) above). The project contains **32 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Tests | List All Tests; List, Create, Get, Update, Delete HTTP Server Test; List, Create, Get, Update, Delete Page Load Test | Test inventory and CRUD for the two most common synthetic test types |
| Agents | List, Get, Update, Delete Agent | Cloud and enterprise agent management |
| Alerts | List, Get Alert; List, Create, Get, Update, Delete Alert Rule | Alert instances and the rules that generate them |
| Labels | List, Create, Get, Update, Delete Endpoint Label | Endpoint agent label CRUD |
| Tags | List, Create, Get, Update, Delete Tag | General-purpose resource tag CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `ThousandEyes:latest` Integration Model | Import from [`thousandeyes-latest.json`](./OpenAPIs/thousandeyes-latest.json) before importing the project |
| `ThousandEyes` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `ThousandEyes` — update the `adapter_id` value in each workflow task if yours is named differently |
