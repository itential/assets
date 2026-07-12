New Relic is an observability platform for application performance monitoring (APM), infrastructure, and alerting — applications, hosts, instances, deployments, mobile apps, and alert policies/conditions/notification channels.

This project provides an OpenAPI spec for automating against the New Relic REST API v2 via an Integration Model. The `-latest` spec is the full REST API v2 surface — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | New Relic REST API v2 OpenAPI spec — `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| New Relic REST API | v2 |
| New Relic Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at New Relic.

Authentication is an API key in a header:

```
X-Api-Key: <your-new-relic-api-key>
```

Generate a user or ingest API key in New Relic under **Account Settings > API Keys**.

## OpenAPIs

### `new_relic-latest.json`

Actively-maintained spec (`x-vendor-api-version: v2`). This is the full, untrimmed New Relic REST API v2 spec — it already covers a single cohesive product surface (application performance monitoring and alerting: applications, deployments, hosts, instances, metrics, key transactions, mobile applications, and alert channels/conditions/policies/incidents/violations) with no admin/internal-tooling long tail to cut, so no operations were removed.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`new_relic-v2.json`](./OpenAPIs/new_relic-v2.json) | Full spec for New Relic REST API v2. |

## Dependencies

| Dependency | Notes |
|---|---|
| New Relic Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
