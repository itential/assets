# Shipping 360

Shipping 360 is Pitney Bowes' multi-carrier shipping platform, providing a unified API to rate shipments, generate labels, manage pickups, and track parcel movement from creation through delivery across supported carriers.

This project provides OpenAPI specs for automating against the Shipping 360 REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for shipping automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`pitney_bowes_shipping_360-latest.json`](#pitney_bowes_shipping_360-latestjson)
  - [`pitney_bowes_shipping_360-1.0.0.json`](#pitney_bowes_shipping_360-100json)
- [Studio Projects](#studio-projects)
  - [Pitney Bowes Shipping 360 Project](#pitney-bowes-shipping-360-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Shipping 360 REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Pitney Bowes Shipping 360](./Studio%20Projects/Pitney%20Bowes%20Shipping%20360.project.json) | 25 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Shipping 360 REST API | v1/v2 |
| Pitney Bowes Shipping 360 Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Shipping 360 sandbox or production server.

Authentication is OAuth 2.0 client credentials. Exchange your API key/secret (sent as an HTTP Basic Authorization header, base64-encoded `key:secret`) for an access token at `POST https://shipping-api-sandbox.pitneybowes.com/oauth/token`, using an `application/x-www-form-urlencoded` body of `grant_type=client_credentials`. Itential Platform performs this exchange and re-retrieves the token automatically before it expires.

The API is rooted at `/shipping` (`/ca/shipping` for the Canada region) — this must be set in the instance's `server.base_path` field, since the platform builds the request URL from `protocol`/`host`/`port`/`base_path` rather than any path in the OpenAPI spec itself.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-api-key>",
      "client_secret": "<your-api-secret>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api-sandbox.sendpro360.pitneybowes.com",
    "base_path": "/shipping"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`pitney_bowes_shipping_360-latest.json`](./OpenAPIs/pitney_bowes_shipping_360-latest.json) | latest (curated) | 25 | Actively-maintained spec, trimmed to 25 of 34 upstream operations — see breakdown below |
| [`pitney_bowes_shipping_360-1.0.0.json`](./OpenAPIs/pitney_bowes_shipping_360-1.0.0.json) | 1.0.0 | 34 | Full Shipping 360 REST API spec |

### `pitney_bowes_shipping_360-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 25 of 34 upstream operations covering common CRUD for shipping automation.

Resources included, by category:

- **Shipments**: Create, List, Get, Cancel, Reprint
- **Rates**: Rate Shipment
- **Pickups**: List, Schedule, Check Availability, Cancel, Cancelled Pickup Document, Get Pickup Document
- **Defaults**: List, Create, Get by Id, Update, Delete
- **Print**: Print Document
- **Reference data**: Carrier Accounts, Carriers, Countries, Parcel Types, Services, Special Services
- **Jobs**: Get Job Status

Not included: Electronic Return Receipt (coversheet, BPOD download, signature image, stamp void) certified-mail add-ons, Electronic Trade Document upload, carrier facility management, and printer mapping configuration. Pull the full spec below if you need one of these.

### `pitney_bowes_shipping_360-1.0.0.json`

Full spec (34 operations) — the entire Shipping 360 REST API surface, preserved as-is. See `pitney_bowes_shipping_360-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Pitney Bowes Shipping 360 Project

Backed by the **`Pitney Bowes Shipping 360:latest`** Integration Model (see [`pitney_bowes_shipping_360-latest.json`](./OpenAPIs/pitney_bowes_shipping_360-latest.json) above). The project contains **25 workflows** organized into **7 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Shipments | Create, List, Get, Cancel, Reprint | Shipment lifecycle |
| Rates | Rate Shipment | Rate shopping |
| Pickups | List, Schedule, Check Availability, Cancel, Cancelled Pickup Document, Get Pickup Document | Pickup scheduling |
| Defaults | List, Create, Get by Id, Update, Delete | Default shipment configuration |
| Print | Print Document | Label/document printing |
| Reference | Get Carrier Accounts, Get Carriers, Get Countries, Get Parcel Types, Get Services, Get Special Services | Carrier and service discovery |
| Jobs | Get Job Status | Async job polling |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Pitney Bowes Shipping 360:latest` Integration Model | Import from [`pitney_bowes_shipping_360-latest.json`](./OpenAPIs/pitney_bowes_shipping_360-latest.json) before importing the project |
| `Pitney Bowes Shipping 360` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Pitney Bowes Shipping 360` — update the `adapter_id` value in each workflow task if yours is named differently |
