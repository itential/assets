# DX NetOps Spectrum

DX NetOps Spectrum (formerly CA Spectrum) is Broadcom's fault and availability management platform for network infrastructure, modeling devices, connections, and services to provide real-time monitoring, root-cause analysis, and alarm management. The OneClick Web Services API exposes this data over HTTP for devices, models, relationships, attributes, actions, alarms, events, and notification subscriptions.

This project provides an OpenAPI spec for automating against the OneClick Web Services API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`dx_netops_spectrum-latest.json`](#dx_netops_spectrum-latestjson)
  - [`dx_netops_spectrum-24.3.json`](#dx_netops_spectrum-243json)
- [Studio Projects](#studio-projects)
  - [DX NetOps Spectrum Project](#dx-netops-spectrum-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | OneClick Web Services API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 29 workflows in 11 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `DX NetOps Spectrum:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `dx_netops_spectrum-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your OneClick server. The API is rooted at `/spectrum/restful` — this must be set in the instance's `server.base_path` field, since the platform builds the request URL from `protocol`/`host`/`port`/`base_path` rather than any path in the OpenAPI spec itself.

Authentication is HTTP Basic Auth, using a local Spectrum user account's username and password (SSO-only accounts can't authenticate this way — the account must exist in Spectrum's local user management). Spectrum 24.3.10+ also offers a UI-generated static bearer token as an alternative, but Basic Auth needs no separate token-generation step and is available on all supported versions.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-oneclick-host>",
    "port": "443",
    "base_path": "/spectrum/restful"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`dx_netops_spectrum-latest.json`](./OpenAPIs/dx_netops_spectrum-latest.json) | latest (curated) | 29 | Curated to alarm, model/device, association, connectivity, attribute, event, landscape, action, and subscription CRUD — see breakdown below |
| [`dx_netops_spectrum-24.3.json`](./OpenAPIs/dx_netops_spectrum-24.3.json) | 24.3 | 31 | Full spec for the OneClick Web Services API, covering Spectrum 24.3 |

### `dx_netops_spectrum-latest.json`

Curated to the core CRUD categories.

Resources included, by category:

- **Alarms**: list/query alarms (including XML search-criteria queries), alarm counts by severity, alarm filters, clear an alarm, update/acknowledge an alarm attribute
- **Model / Models**: create, get, update, delete a model; bulk attribute updates and XML-based model/device queries
- **Devices**: list devices
- **Associations**: get, create, delete associations between models
- **Connectivity**: get a device's connectivity
- **Attribute**: get an attribute's enumeration values
- **Events**: query events, create an event, create an event against a specific model
- **Landscapes**: list landscapes
- **Action**: issue an action against the SpectroSERVER
- **Subscription**: create, get, delete a notification subscription; list pending subscription requests

Several write operations (alarm/event/model queries and bulk updates) take a raw XML request document rather than JSON, per the vendor API's native XML-based request format — these are modeled as `application/xml` string bodies rather than fabricated JSON schemas.

### `dx_netops_spectrum-24.3.json`

Full spec for the OneClick Web Services API as documented for Spectrum 24.3, plus SNMPv3 profile administration. See `dx_netops_spectrum-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### DX NetOps Spectrum Project

Backed by the **`DX NetOps Spectrum:latest`** Integration Model (see [`dx_netops_spectrum-latest.json`](./OpenAPIs/dx_netops_spectrum-latest.json) above). The project contains **29 workflows** organized into **11 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Alarms | 6 | List/query alarms, alarm counts, alarm filters, clear an alarm, update/acknowledge an alarm |
| Model | 5 | Create, get, update, delete a model; bulk attribute updates |
| Subscription | 4 | Create, get, delete a subscription; list pending subscription requests |
| Associations | 3 | Get, create, delete associations between models |
| Events | 3 | Query events, create an event, create an event against a specific model |
| Models | 3 | Bulk XML-based device/model queries and attribute updates |
| Action | 1 | Issue an action against the SpectroSERVER |
| Attribute | 1 | Get an attribute's enumeration values |
| Connectivity | 1 | Get a device's connectivity |
| Devices | 1 | List devices |
| Landscapes | 1 | List landscapes |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `DX NetOps Spectrum:latest` Integration Model | Import from [`dx_netops_spectrum-latest.json`](./OpenAPIs/dx_netops_spectrum-latest.json) before importing the project |
| `DX NetOps Spectrum` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `DX NetOps Spectrum` — update the `adapter_id` value in each workflow task if yours is named differently |
