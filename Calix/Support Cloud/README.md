Calix Support Cloud (also known as Calix Cloud) manages TR-069/CWMP-based broadband CPE devices — ONTs, ONUs, and gateways — for broadband service providers, covering device inventory, subscriber records, device provisioning, and device groups.

This project provides an OpenAPI spec for automating against Calix Support Cloud's Subscriber/Device API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`calix_support_cloud-latest.json`](#calix_support_cloud-latestjson)
  - [`calix_support_cloud-1.0.0.json`](#calix_support_cloud-100json)
- [Studio Projects](#studio-projects)
  - [Calix Support Cloud Project](#calix-support-cloud-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Calix Support Cloud Subscriber/Device API OpenAPI specs |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 21 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Calix Support Cloud:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `calix_support_cloud-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Calix Support Cloud data center.

Authentication is HTTP Basic, using the "API for Web Clients (HTTPS)" username/password generated from Calix Support Cloud's administrative menu.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-api-username>",
      "password": "<your-api-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "gcs.calix.com",
    "port": 8444,
    "base_path": ""
  }
}
```

Calix Support Cloud runs from two data centers, each with its own base URL — use whichever your organization is provisioned against:

| Data Center Location | Host |
|---|---|
| United States (default) | `gcs.calix.com` |
| Canada | `gcs-ca.calix.com` |

Both listen on port `8444`.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`calix_support_cloud-latest.json`](./OpenAPIs/calix_support_cloud-latest.json) | latest (curated) | 21 | All 21 upstream operations — see breakdown below |
| [`calix_support_cloud-1.0.0.json`](./OpenAPIs/calix_support_cloud-1.0.0.json) | 1.0.0 | 21 | Full spec, identical in scope to `-latest` |

### `calix_support_cloud-latest.json`

Converted to OpenAPI 3.0 from Calix's published Postman collection ("Calix Cloud – Subscriber/Device API"), since Calix does not publish an OpenAPI/Swagger file directly. All 21 upstream operations are already in scope for automation, so the full spec is carried through as `-latest` with no operations cut.

Resources included:

- **Devices**: list/query by serial number, MAC address, registration ID, or IP address; get by ID; delete
- **Subscribers**: create, list/query by customId, name, phone, or email, get by ID, update, delete
- **Provisioning Records**: create, list/query by device or subscriber, get by ID, update, delete
- **Device Operations**: a single TR-069/CWMP RPC endpoint covering GetParameterValues, GetParameterNames, SetParameterValues, AddObject, DeleteObject, Reboot, and FactoryReset
- **Device Groups**: list, get by ID
- **Static Group Members**: list/query by device, get by ID, add device to group, remove by membership ID or by query

### `calix_support_cloud-1.0.0.json`

Full spec preserving the same 21 operations converted from the source Postman collection, given as its own dated file per repo convention. See `calix_support_cloud-latest.json` above for the actively-maintained copy.

## Studio Projects

### Calix Support Cloud Project

Backed by the **`Calix Support Cloud:latest`** Integration Model (see [`calix_support_cloud-latest.json`](./OpenAPIs/calix_support_cloud-latest.json) above). The project contains **21 workflows** organized into **6 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Devices | 3 | List, get by ID, delete |
| Subscribers | 5 | Create, list, get by ID, update, delete |
| Provisioning Records | 5 | Create, list, get by ID, update, delete |
| Device Operations | 1 | Run TR-069 device operation |
| Device Groups | 2 | List, get by ID |
| Static Group Members | 5 | List, get by ID, add, remove by ID, remove by query |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Calix Support Cloud:latest` Integration Model | Import from [`calix_support_cloud-latest.json`](./OpenAPIs/calix_support_cloud-latest.json) before importing the project |
| `calix-support-cloud` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `calix-support-cloud` — update the `adapter_id` value in each workflow task if yours is named differently |
