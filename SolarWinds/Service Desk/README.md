# Service Desk

SolarWinds Service Desk (formerly Samanage) is a cloud-based IT service management platform for incident, problem, change, asset, and service-catalog management. It's a separate product from SolarWinds Orion NPM — different acquisition history, platform, and API — not to be confused with the Orion Platform's SWIS API.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`solarwinds_service_desk-latest.json`](#solarwinds_service_desk-latestjson)
  - [`solarwinds_service_desk-1.0.json`](#solarwinds_service_desk-10json)
- [Studio Projects](#studio-projects)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | SolarWinds Service Desk OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | One atomic workflow per curated operation, wired to `-latest` |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| SolarWinds Service Desk | Any tenant with API access enabled |
| API token | Admin-generated, from a Service Desk administrator account |

## Integration Configuration

Import `solarwinds_service_desk-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration instance for your tenant.

Authentication is a static, admin-generated API token, replayed as a `Bearer` value inside a vendor-specific header (not the standard `Authorization` header):

```
X-Samanage-Authorization: Bearer <token>
```

US tenants use `https://api.samanage.com`; EU and APJ tenants use `https://apieu.samanage.com` and `https://apiau.samanage.com` respectively — update the integration instance's server/host if your tenant isn't in the US region.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`solarwinds_service_desk-latest.json`](./OpenAPIs/solarwinds_service_desk-latest.json) | latest (curated) | 56 | Trimmed to 56 of 134 upstream operations — see breakdown below |
| [`solarwinds_service_desk-1.0.json`](./OpenAPIs/solarwinds_service_desk-1.0.json) | 1.0 | 134 | Full spec covering Service Desk's REST surface |

### `solarwinds_service_desk-latest.json`

Trimmed to 56 of 134 upstream operations.

Resources included:

- **Incidents**: list, create, get, update, delete
- **Problems**: list, create, get, update, delete
- **Changes**: list, create, get, update, delete
- **Catalog Items**: list, get, plus create Service Request (orders a catalog item on behalf of a requester)
- **Hardware assets**: list, create, get, update, delete
- **Other assets**: list, create, get, update, delete
- **Users**: list, create, get, update, delete
- **Groups**: list, create, get, update, delete
- **Departments**: list, create, get, update, delete
- **Sites**: list, create, get, update, delete
- **Categories**: list, create, get, update, delete
- **Comments**: create, update, delete — attachable to Incidents, Problems, or Changes

### `solarwinds_service_desk-1.0.json`

Full spec (134 operations) covering the resources above plus asset sub-types (mobiles, printers, software), contracts and purchase orders, warranties, memberships, roles, vendors, releases, change catalogs, tasks, time tracking, and audit trails. See `solarwinds_service_desk-latest.json` above for the curated automation-focused subset.

## Studio Projects

[`SolarWinds Service Desk.project.json`](./Studio%20Projects/SolarWinds%20Service%20Desk.project.json) — one atomic workflow per curated operation in `-latest`, organized into folders by resource category (Incidents, Problems, Changes, Catalog Items & Service Requests, Assets, Users & Groups, Reference Data, Comments).
