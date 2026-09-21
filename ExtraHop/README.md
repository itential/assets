# ExtraHop

ExtraHop is a network detection and response (NDR) platform that analyzes network traffic to discover devices, surface security detections, and drive incident response. RevealX 360 is ExtraHop's SaaS product line, managed through a cloud console (CCP) that fronts the same REST API surface as ExtraHop's self-managed sensors.

This project provides OpenAPI specs for automating against the RevealX 360 REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`extrahop-latest.json`](#extrahop-latestjson)
  - [`extrahop-v1.json`](#extrahop-v1json)
- [Studio Projects](#studio-projects)
  - [ExtraHop Project](#extrahop-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | ExtraHop RevealX 360 REST API OpenAPI specs — curated `-latest` plus the full v1 resource surface |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 51 workflows in 7 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `ExtraHop:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `extrahop-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your RevealX 360 tenant.

RevealX 360 uses OAuth 2.0 client credentials: generate an ID/Secret pair on the RevealX 360 **API Access** page, then exchange them at `POST /oauth2/token` (HTTP Basic auth, `grant_type=client_credentials`, form-urlencoded) for a bearer access token — valid for 10 minutes, so the integration must re-authenticate on expiry. This is the same underlying `/api/v1` resource surface ExtraHop's self-managed sensors expose (with static API-key auth instead); RevealX 360's OAuth2 flow was chosen here as the broader, cloud-first entry point.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "OAuth2ClientCredentials": {
      "client_id": "<your-rest-api-id>",
      "client_secret": "<your-rest-api-secret>",
      "token_url": "https://<your-ccp-host>/oauth2/token"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-ccp-host>",
    "base_path": "/api/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`extrahop-latest.json`](./OpenAPIs/extrahop-latest.json) | latest (curated) | 51 | Curated to devices, detections, alerts, and watchlist CRUD — see breakdown below |
| [`extrahop-v1.json`](./OpenAPIs/extrahop-v1.json) | v1 | 269 | Full v1 REST API resource surface (configuration, detections, metrics, records, packets, system administration) |

### `extrahop-latest.json`

Curated to the core resources someone would realistically automate against RevealX 360.

Resources included, by category:

- **Devices**: list/search, get, update, tag/untag
- **Device Groups**: full CRUD, membership add/remove
- **Custom Devices**: full CRUD, criteria add/get/delete
- **Detections**: list, search, get, update (status/ticket/assignee/resolution)
- **Alerts**: full CRUD, assignment to devices and device groups
- **Tags**: full CRUD, device assignment
- **Threat Collections**: ExtraHop's watchlist equivalent — create/list/delete, list observables

### `extrahop-v1.json`

Full v1 REST API resource surface. See `extrahop-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### ExtraHop Project

Backed by the **`ExtraHop:latest`** Integration Model (see [`extrahop-latest.json`](./OpenAPIs/extrahop-latest.json) above). The project contains **51 workflows** organized into **7 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Alerts | 11 | Full CRUD, assignment to devices and device groups |
| Custom Devices | 9 | Full CRUD, criteria add/get/delete |
| Detections | 4 | List, search, get, update |
| Device Groups | 8 | Full CRUD, membership add/remove |
| Devices | 7 | List/search, get, update, tag/untag |
| Tags | 8 | Full CRUD, device assignment |
| Threat Collections | 4 | Create/list/delete, list observables |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `ExtraHop:latest` Integration Model | Import from [`extrahop-latest.json`](./OpenAPIs/extrahop-latest.json) before importing the project |
| `ExtraHop` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `ExtraHop` — update the `adapter_id` value in each workflow task if yours is named differently |
