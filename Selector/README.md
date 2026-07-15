Selector AI is a network observability and AIOps platform that correlates telemetry, logs, and events across network and infrastructure domains to support anomaly detection, root cause analysis, and inventory-driven analytics.

This project provides OpenAPI specs for automating against Selector AI's REST APIs via an Integration Model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`selector_ai_metastore_inventory-latest.json`](#selector_ai_metastore_inventory-latestjson)
  - [`selector_ai_query-latest.json`](#selector_ai_query-latestjson)
  - [`selector_ai_metastore_inventory-1.0.0.json`](#selector_ai_metastore_inventory-100json)
  - [`selector_ai_query-1.0.0.json`](#selector_ai_query-100json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Selector AI REST API OpenAPI specs — curated `-latest` plus full dated versions |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Selector AI | 1.0.0 (see OpenAPIs below for exact spec versions available) |
| Selector AI Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Selector AI instance.

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Obtain a token from your Selector AI instance credentials. See https://docs.selector.ai/ for details.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`selector_ai_metastore_inventory-latest.json`](./OpenAPIs/selector_ai_metastore_inventory-latest.json) | latest (curated) | 15 | Trimmed to 15 of 33 upstream operations — see breakdown below |
| [`selector_ai_query-latest.json`](./OpenAPIs/selector_ai_query-latest.json) | latest (curated) | 1 | Single-purpose, reviewed and confirmed already scoped — see breakdown below |
| [`selector_ai_metastore_inventory-1.0.0.json`](./OpenAPIs/selector_ai_metastore_inventory-1.0.0.json) | 1.0.0 | 33 | Full, unmodified vendor spec |
| [`selector_ai_query-1.0.0.json`](./OpenAPIs/selector_ai_query-1.0.0.json) | 1.0.0 | 1 | Full, unmodified vendor spec |

### `selector_ai_metastore_inventory-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 15 of 33 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Inventory**: create, list, get, update, and delete inventory items and item collections
- **Inventory Schema (v2)**: create, list, update, and delete inventory schema definitions

Excluded: legacy v1 schema endpoints (superseded by v2), bulk/CSV import-export utilities, and admin/diagnostic endpoints (health, logs, config, version, opstats). Pull the full spec from the dated file above if you need something not covered here.

### `selector_ai_query-latest.json`

Single-purpose API exposing exactly one operation upstream (`x-vendor-api-version: 1.0.0`, 1 of 1 operations kept). Audited operation-by-operation and confirmed there is no separate admin/health/telemetry surface to exclude — the sole endpoint is the product's entire business function, so nothing was removed:

- **Query**: `POST /command` — execute a Selector Query Language (S2QL) query and return results plus rendering metadata, for querying network telemetry/observability data (e.g. latency, jitter, packet loss) and violation events.

Two pre-existing vendor spec issues were also cleaned up: a stray top-level `security` block referencing an undefined `apikey` scheme was previously removed (the operation itself already correctly declared `bearerAuth`), and now that redundant per-operation `bearerAuth` override has been consolidated into a single global `security` block at the spec level, since it was the same requirement repeated on every operation.

### `selector_ai_metastore_inventory-1.0.0.json`

Full, unmodified vendor spec for the Metastore/Inventory API (33 operations) — the vendor's complete API surface, preserved as-is. See `selector_ai_metastore_inventory-latest.json` above for the curated subset if you just need common CRUD automation.

### `selector_ai_query-1.0.0.json`

Full, unmodified vendor spec for the Query API (1 operation) — the vendor's complete API surface, preserved as-is. See `selector_ai_query-latest.json` above for the curated subset if you just need common CRUD automation.
