# ClearPass

ClearPass Policy Manager is HPE Aruba Networking's network access control (NAC) platform, providing AAA policy administration, endpoint visibility, and guest/BYOD onboarding for wired and wireless networks.

This project provides an OpenAPI spec for automating against ClearPass's Network Bound API (NBAPI) via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aruba_clearpass-latest.json`](#aruba_clearpass-latestjson)
  - [`aruba_clearpass-1.0.json`](#aruba_clearpass-10json)
- [Studio Projects](#studio-projects)
  - [Aruba ClearPass Project](#aruba-clearpass-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Aruba ClearPass NBAPI OpenAPI specs |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 73 workflows in 7 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Aruba ClearPass:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `aruba_clearpass-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your ClearPass Policy Manager appliance.

Authentication is OAuth 2.0, client credentials grant, against ClearPass's own built-in OAuth2 provider (`POST /api/oauth`). Register an API client in ClearPass under **Administration > API Services > API Clients** with grant type `client_credentials`, and note its Client ID/Secret — no user login or interactive consent is needed for this flow, and Itential Platform refreshes the token automatically once configured.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-api-client-id>",
      "client_secret": "<your-api-client-secret>",
      "token_url": "https://<your-clearpass-host>/api/oauth",
      "refresh_url": "",
      "scope": "",
      "token": { "access_token": "" }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-clearpass-host>",
    "base_path": "/api"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aruba_clearpass-latest.json`](./OpenAPIs/aruba_clearpass-latest.json) | latest (curated) | 73 | Full NBAPI CRUD surface for the 7 resources below — see breakdown |
| [`aruba_clearpass-1.0.json`](./OpenAPIs/aruba_clearpass-1.0.json) | 1.0 | 73 | Same operations, dated/pinned copy |

### `aruba_clearpass-latest.json`

Covers full create/read/update/delete for:

- **Network Devices**: AAA clients (NAS/RADIUS devices), by ID and by name
- **Network Device Groups**: subnet/regex/list-based device groupings, by ID and by name
- **Endpoints**: known/unknown/disabled device records, by ID and by MAC address
- **Local Users**: ClearPass local user accounts and the shared password policy, by ID and by user ID
- **Roles**: user roles, by ID and by name
- **Proxy Targets**: RADIUS/RadSec proxy destinations, by ID and by name
- **Static Host Lists**: IP/MAC address allow-lists, by ID and by name

### `aruba_clearpass-1.0.json`

Same 73 operations as `-latest`; kept as the dated/pinned copy per this repo's versioning convention.

## Studio Projects

### Aruba ClearPass Project

Backed by the **`Aruba ClearPass:latest`** Integration Model (see [`aruba_clearpass-latest.json`](./OpenAPIs/aruba_clearpass-latest.json) above). The project contains **73 workflows** organized into **7 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Network Devices | 10 | List, create, get/update/replace/delete by ID and by name |
| Network Device Groups | 10 | List, create, get/update/replace/delete by ID and by name |
| Endpoints | 10 | List, create, get/update/replace/delete by ID and by MAC address |
| Local Users | 13 | List, create, get/update/replace/delete by ID and by user ID, plus password policy get/replace/update |
| Roles | 10 | List, create, get/update/replace/delete by ID and by name |
| Proxy Targets | 10 | List, create, get/update/replace/delete by ID and by name |
| Static Host Lists | 10 | List, create, get/update/replace/delete by ID and by name |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `Aruba ClearPass:latest` Integration Model | Import from [`aruba_clearpass-latest.json`](./OpenAPIs/aruba_clearpass-latest.json) before importing the project |
| `Aruba ClearPass` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Aruba ClearPass` — update the `adapter_id` value in each workflow task if yours is named differently |
