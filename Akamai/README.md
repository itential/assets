Akamai provides a global content delivery, security, and edge computing platform. This project covers the Akamai Edge DNS API, which manages authoritative DNS zones, record sets, change lists, and TSIG keys for domains hosted on Akamai's Edge DNS service.

This project provides an OpenAPI spec for automating against the Edge DNS REST API via an Integration Model.

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

### `akamai_apis-latest.json`

Actively-maintained spec (`x-vendor-api-version: v2`). This spec covers a single cohesive surface — Akamai Edge DNS zone management — so it is left untrimmed: all 60 upstream operations are included, spanning zones, change lists, record sets, TSIG keys, and DNS reference data.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`akamai_apis-v2.json`](./OpenAPIs/akamai_apis-v2.json) | Full spec for the Akamai Edge DNS API, version v2. |

## Dependencies

| Dependency | Notes |
|---|---|
| Akamai Edge DNS Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
