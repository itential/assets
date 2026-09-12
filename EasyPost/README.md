# EasyPost

EasyPost is a multi-carrier shipping API that provides a single integration point for rating, label purchase, address verification, package tracking, customs documentation, insurance, and pickup scheduling across a wide range of carriers.

This project provides OpenAPI specs for automating against the EasyPost REST API via an Integration Model. Converted from EasyPost's official Postman collection, hand-verified against their API documentation. The `-latest` spec is a curated subset covering common CRUD for shipping automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`easypost-latest.json`](#easypost-latestjson)
  - [`easypost-2026-09-12.json`](#easypost-2026-09-12json)
- [Studio Projects](#studio-projects)
  - [EasyPost Project](#easypost-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | EasyPost REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/EasyPost](./Studio%20Projects/EasyPost.project.json) | 23 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| EasyPost REST API | v2 |
| EasyPost Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your EasyPost account (`https://api.easypost.com`).

Authentication is HTTP Basic, with your EasyPost API key as the username and **no password** — the password field must be present but left blank:

```
Authorization: Basic base64(<your-easypost-api-key>:)
```

Generate a Test or Production API key from your EasyPost dashboard under **API Keys**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basic": {
      "username": "<your-easypost-api-key>",
      "password": ""
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.easypost.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`easypost-latest.json`](./OpenAPIs/easypost-latest.json) | latest (curated) | 81 | Actively-maintained spec, trimmed to 81 of 110 upstream operations — see breakdown below |
| [`easypost-2026-09-12.json`](./OpenAPIs/easypost-2026-09-12.json) | 2026-09-12 | 110 | Full converted spec covering EasyPost's Postman collection (110 operations) |

EasyPost does not publish a downloadable OpenAPI/Swagger spec directly — only per-language SDK client repos and an official Postman collection (`postman.com/easypost-api`, announced on EasyPost's own blog). Both specs here were generated from that official collection with `postman-to-openapi` and then hand-corrected: request bodies were rebuilt with real property types and required-field information (the raw conversion only carried example payloads with no schema or required fields), path parameters were made explicit and required, every operation was given a unique `operationId`, and the security scheme was overridden to HTTP Basic to match EasyPost's actual auth mechanism (the collection modeled it as a bare API key). A few vendor artifacts in the source collection were also fixed: a literal example shipment ID baked into one URL instead of a path variable, an inconsistent path-variable name between two requests hitting the same EndShipper path, and the same collision between two Users requests — all normalized to one canonical path each.

### `easypost-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2026-09-12`). Trimmed to 81 of 110 upstream operations covering common CRUD for shipping automation.

Resources included, by category:

- **Addresses**: List, Create, Create and Verify, Get, Verify
- **Parcels**: Create, Get
- **Shipments**: List, Create (one-call buy), Get, Buy, Refund, Rerate, Insure, Label, Forms, SmartRate
- **Trackers**: List, Create, Get, Create Batch
- **Insurance**: List, Create, Get, Refund
- **Claims**: List, Create, Get, Cancel
- **Customs Info / Customs Items**: Create, Get
- **Pickups**: List, Create, Get, Buy, Cancel
- **Batches**: List, Create, Get, Add/Remove Shipments, Buy, Label, Manifest
- **Orders**: Get, Create (one-call buy), Buy
- **End Shippers**: List, Create, Get, Update
- **Carrier Accounts**: List, Create, Get, Update, Delete
- **Carrier Types / Carrier Metadata**: List
- **Rates**: Get
- **Scan Forms**: List, Create, Get
- **Events**: List, Get, List/Get Payloads
- **Webhooks**: List, Create, Get, Update, Delete
- **Users**: Get authenticated user, Update authenticated user, Create/Get/Update/Delete child user

Not included: EasyPost's own billing/Stripe funding flow (credit card and bank account setup, wallet charges), referral/reseller ("partner white label") administration, Reports, carrier-specific OAuth/FedEx registration flows, beta/Luma rate-prediction endpoints, SmartRate's `deliver_on`/`deliver_by` variants, API key retrieval, and the standalone ReadyDocs product. Pull the full spec below if you need one of these.

### `easypost-2026-09-12.json`

Full spec, converted from EasyPost's official Postman collection (110 operations) — the entire collection surface, hand-corrected for structural issues but not curated down. See `easypost-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### EasyPost Project

Backed by the **`EasyPost:latest`** Integration Model (see [`easypost-latest.json`](./OpenAPIs/easypost-latest.json) above). The project contains **23 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Shipments | List, Create, Get, Buy, Refund, Get Label | Shipment lifecycle |
| Addresses | List, Create, Create and Verify, Get, Verify | Address CRUD and verification |
| Parcels | Create, Get | Parcel CRUD |
| Trackers | List, Create, Get | Package tracking |
| Insurance | List, Create, Get | Shipment insurance |
| Pickups | List, Create, Get, Cancel | Pickup scheduling |

#### Dependencies

| Dependency | Notes |
|---|---|
| `EasyPost:latest` Integration Model | Import from [`easypost-latest.json`](./OpenAPIs/easypost-latest.json) before importing the project |
| `EasyPost` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `EasyPost` — update the `adapter_id` value in each workflow task if yours is named differently |
