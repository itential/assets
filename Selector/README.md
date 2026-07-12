Selector AI is a network observability and AIOps platform that correlates telemetry, logs, and events across network and infrastructure domains to support anomaly detection, root cause analysis, and inventory-driven analytics.

This project provides OpenAPI specs for automating against Selector AI's REST APIs via an Integration Model.

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

### `selector_ai_metastore_inventory-latest.json` (curated)

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 15 of 33 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Inventory**: create, list, get, update, and delete inventory items and item collections
- **Inventory Schema (v2)**: create, list, update, and delete inventory schema definitions

Excluded: legacy v1 schema endpoints (superseded by v2), bulk/CSV import-export utilities, and admin/diagnostic endpoints (health, logs, config, version, opstats). Pull the full spec from the dated file below if you need something not covered here.

### `selector_ai_query-latest.json` (full spec, untouched)

Single-purpose API exposing one operation (`POST /command`) to execute Selector Query Language (S2QL) queries against network telemetry and observability data. Already narrowly scoped, so no operations were trimmed. A pre-existing vendor spec issue — a stray top-level `security` block referencing an undefined `apikey` scheme — was removed since the operation itself already correctly declares `bearerAuth`.

### Full, unmodified specs

| Spec | Description |
|---|---|
| [`selector_ai_metastore_inventory-1.0.0.json`](./OpenAPIs/selector_ai_metastore_inventory-1.0.0.json) | Full spec for Selector AI Metastore Inventory 1.0.0. |
| [`selector_ai_query-1.0.0.json`](./OpenAPIs/selector_ai_query-1.0.0.json) | Full spec for Selector AI Query 1.0.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| Selector AI Integration Model | Import from an OpenAPI spec above to build automation against the REST API. |
