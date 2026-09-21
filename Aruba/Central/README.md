# Central

Aruba Central is HPE Aruba Networking's cloud-based network management platform, providing unified configuration, monitoring, and orchestration for access points, switches, gateways, and SD-WAN/SD-Branch deployments across a customer's estate.

This project provides OpenAPI specs for automating against Aruba Central's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aruba_central-latest.json`](#aruba_central-latestjson)
  - [`aruba_central-2.0.json`](#aruba_central-20json)
- [Studio Projects](#studio-projects)
  - [Aruba Central Project](#aruba-central-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Aruba Central REST API OpenAPI specs — curated `-latest` plus a full reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 56 workflows in 8 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Aruba Central:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `aruba_central-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Central tenant's regional API gateway (e.g. `apigw-prod2.central.arubanetworks.com` — the exact host depends on which region your tenant was provisioned in).

Authentication is OAuth 2.0, authorization code grant, against Central's own OAuth2 provider. Register an API application under **Account Home > API Gateway > My Apps & Tokens**, then complete the one-time browser-based authorization:

1. Register an API application (grant type "Authorization Code") and note its Client ID/Secret.
2. Build the authorize URL with your Client ID and redirect URI, open it in a browser, and log in/approve.
3. Exchange the resulting authorization code immediately via `POST https://<your-region-gateway>/oauth2/token` with `grant_type=authorization_code`.
4. Seed the resulting `access_token`/`refresh_token` into the Itential Platform integration instance. Once seeded, the platform refreshes the token automatically going forward.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2AuthCode": {
      "client_id": "<client-id>",
      "client_secret": "<client-secret>",
      "token_url": "https://<your-region-gateway>/oauth2/token",
      "refresh_url": "https://<your-region-gateway>/oauth2/token",
      "authorization_url": "https://<your-region-gateway>/oauth2/authorize/central/api",
      "scope": "",
      "token": {
        "access_token": "<access-token>",
        "refresh_token": "<refresh-token>",
        "token_type": "Bearer",
        "expires_in": 7200
      }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-region-gateway>",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aruba_central-latest.json`](./OpenAPIs/aruba_central-latest.json) | latest (curated) | 56 | Curated to site, group, device, WLAN, guest, and label CRUD — see breakdown below |
| [`aruba_central-2.0.json`](./OpenAPIs/aruba_central-2.0.json) | 2.0 | 976 | Full reference spec covering Central's broader operation surface |

### `aruba_central-latest.json`

Resources included, by category:

- **Sites**: CRUD plus device association/unassociation
- **Groups**: CRUD, cloning, rename, default-group management, bulk properties lookup
- **Group Templates**: CRUD for per-group configuration templates
- **Device Inventory**: list/add/remove/stats for the subscription device inventory
- **Devices**: group assignment lookup, bulk move, template-variable CRUD
- **WLAN**: SSID profile CRUD, per-group listing
- **Guest**: guest portal CRUD, visitor account CRUD
- **Labels**: label CRUD plus device association/unassociation

### `aruba_central-2.0.json`

Full reference spec (976 operations across Central's AIOps, configuration, device management, firmware, guest, monitoring, platform, SD-WAN, and telemetry APIs). See `aruba_central-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Aruba Central Project

Backed by the **`Aruba Central:latest`** Integration Model (see [`aruba_central-latest.json`](./OpenAPIs/aruba_central-latest.json) above). The project contains **56 workflows** organized into **8 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Sites | 7 | List, create, get, update, delete, associate/unassociate devices |
| Groups | 9 | List, create, clone, update properties, delete, rename, default-group get/update, properties lookup |
| Group Templates | 5 | List, create, update, get, delete |
| Device Inventory | 5 | List, add, delete, get by serial, stats |
| Devices | 7 | Group lookup, bulk move, template-variable get/create/replace/update/delete |
| WLAN | 6 | Get, create, update, replace, list, delete |
| Guest | 10 | Portal list/create/get/replace/delete, visitor list/create/get/replace/delete |
| Labels | 7 | List, create, get, update, delete, associate/unassociate |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `Aruba Central:latest` Integration Model | Import from [`aruba_central-latest.json`](./OpenAPIs/aruba_central-latest.json) before importing the project |
| `Aruba Central` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Aruba Central` — update the `adapter_id` value in each workflow task if yours is named differently |
