Akamai provides a global content delivery, security, and edge computing platform. This project covers the Akamai Edge DNS API, which manages authoritative DNS zones, record sets, change lists, and TSIG keys for domains hosted on Akamai's Edge DNS service.

This project provides an OpenAPI spec for automating against the Edge DNS REST API via an Integration Model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`akamai_edge_dns_api-latest.json`](#akamai_edge_dns_api-latestjson)
  - [`akamai_edge_dns_api-v2.json`](#akamai_edge_dns_api-v2json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Akamai Edge DNS REST API OpenAPI spec — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Akamai Edge DNS API | v2 |
| Akamai Edge DNS Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the Akamai Edge DNS API endpoint.

Authentication is a credential in the `Authorization` header:

```
Authorization: Bearer <client_token>
```

Generate EdgeGrid credentials in Akamai Control Center (Identity and Access Management) and use the client token as the bearer value.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`akamai_edge_dns_api-latest.json`](./OpenAPIs/akamai_edge_dns_api-latest.json) | latest (curated) | 60 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`akamai_edge_dns_api-v2.json`](./OpenAPIs/akamai_edge_dns_api-v2.json) | v2 | 60 | Full spec for the Akamai Edge DNS API, version v2. |

### `akamai_edge_dns_api-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: v2`, 60 operations). Every operation is CRUD or a provisioning action on the Edge DNS domain model (zones, versions, record sets, change lists, TSIG keys) or reference data those actions require (contracts, groups, nameservers, algorithms) — there is no separate admin, telemetry, or self-introspection surface to exclude, so nothing was removed.

Operations included, by category:

- **Zones**: Create, list, get settings, update settings; get aliases; get contract
- **Zone versions**: List versions, get a version, get a version's record sets, show differences between versions, reactivate a version; get/post the zone's master zone file, get a version's master zone file
- **Record sets**: Create, get, replace, delete a record set; create multiple record sets; get/replace a zone's record sets; get record set names/types for a zone
- **Change lists** (staged edits prior to activation): Create, list, search, get, delete; show diff against the base zone; get record set names/types for a change list; get/add a record set change; upload a master zone file to a change list; get/update change list settings; submit (activate) a change list
- **TSIG keys**: List keys; bulk-update a key across multiple zones; list zones using a key; get/update/delete a zone's key; list zones sharing a zone's key
- **Bulk zone requests** (async provisioning): Submit bulk-create request + check status + get result; submit bulk-delete request + check status + get result
- **Zone status checks**: Get DNSSEC status for zones; get secondary-zone transfer status
- **DNS reference data** (inputs required by the operations above, e.g. contract/group IDs for zone creation): Authoritative nameservers, contracts, groups, edge hostnames, record set types, DNSSEC algorithms, TSIG algorithms

### `akamai_edge_dns_api-v2.json`

Full, unmodified vendor spec for the Akamai Edge DNS API, version v2 — the vendor's complete API surface, preserved as-is. See `akamai_edge_dns_api-latest.json` above for the curated subset if you just need common CRUD automation.
