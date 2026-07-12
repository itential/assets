Datadog is a monitoring and observability platform for infrastructure, applications, and logs, unifying metrics, traces, and logs into dashboards, monitors, and incident workflows.

This project provides OpenAPI specs for automating against Datadog's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for observability automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Datadog REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Datadog Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Datadog site (e.g. `api.datadoghq.com` or `api.datadoghq.eu`).

Authentication is an API key in the `DD-API-KEY` header (and an application key in `DD-APPLICATION-KEY` for endpoints that require one):

```
DD-API-KEY: <your-datadog-api-key>
DD-APPLICATION-KEY: <your-datadog-application-key>
```

Generate both from Datadog under **Organization Settings → API Keys** and **Application Keys**.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`datadog-latest.json`](./OpenAPIs/datadog-latest.json) | latest (curated) | Actively-maintained, curated for common CRUD for observability automation — see breakdown below |
| [`datadog-2.0.json`](./OpenAPIs/datadog-2.0.json) | 2.0 | Full spec for Datadog API v2.0. |
| [`datadog_legacy-1.0.json`](./OpenAPIs/datadog_legacy-1.0.json) | 1.0 | Legacy Datadog API v1.0 spec. |

### `datadog-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0`). Trimmed to 39 of 1198 upstream operations. Datadog's full API surface spans dozens of specialized products (Security Monitoring, Synthetics, RUM, CI Visibility, APM, Cost Management, and more) that are out of scope for general-purpose automation; this spec keeps only the cross-cutting operational primitives. Note that this spec snapshot has no bare Monitor, Dashboard, or SLO CRUD endpoints upstream (only narrow sub-resources like notification rules and report status), so those resources are excluded here rather than partially represented. Pull the full spec from [Datadog's official OpenAPI description](https://github.com/DataDog/datadog-api-client-python/blob/master/.generator/schemas/v2/openapi.yaml) if you need one of the excluded product areas.

Resources included, by category:

- **Incident response**: Downtimes, Maintenance Windows, Incidents (create/get/search)
- **Logs**: Event submission, Event search
- **Metrics**: Active metric listing, Scalar and timeseries queries
- **Tagging**: Tag enrichment rules
- **Access management**: Users, Roles

## Dependencies

| Dependency | Notes |
|---|---|
| Datadog Integration Model | Import from an OpenAPI spec above to build automation against the REST API. |
