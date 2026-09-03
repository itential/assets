New Relic is an observability platform for application performance monitoring (APM), infrastructure, and alerting — applications, hosts, instances, deployments, mobile apps, and alert policies/conditions/notification channels.

This project provides an OpenAPI spec for automating against the New Relic REST API v2 via an Integration Model. The `-latest` spec is the full REST API v2 surface — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`new_relic-latest.json`](#new_relic-latestjson)
  - [`new_relic-v2.json`](#new_relic-v2json)

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

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "APIKeyHeader": {
      "value": "<your-api-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.newrelic.com",
    "base_path": "/v2"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`new_relic-latest.json`](./OpenAPIs/new_relic-latest.json) | latest (curated) | 59 | Actively-maintained spec, reviewed and confirmed already scoped to CRUD, query, and provisioning actions — see breakdown below |
| [`new_relic-v2.json`](./OpenAPIs/new_relic-v2.json) | v2 | 59 | Full, unmodified vendor spec |

### `new_relic-latest.json`

Actively-maintained spec (`x-vendor-api-version: v2`, 59 operations). Every operation in the upstream spec is CRUD, a query, or a provisioning action on New Relic's actual APM/alerting resources — there is no separate health/heartbeat, self-introspection/version-info, or license-lookup surface to exclude, so nothing was removed.

Operations included, by category:

- **GraphQL**: Execute a GraphQL (NerdGraph) query
- **Applications**: List, show, update, delete
- **Application Deployments**: List, create, delete a deployment record for an application
- **Application Hosts**: List, show a host; metric names and metric data for a host
- **Application Instances**: List, show an instance; metric names and metric data for an instance
- **Application Metrics**: Metric names and metric data for an application
- **Key Transactions**: List, show
- **Mobile Applications**: List, show; metric names and metric data
- **Alerts Channels**: List, create, delete notification channels
- **Alerts Policies**: List, create, update, delete
- **Alerts Policy Channels**: Link (update) and unlink (delete) a channel from a policy
- **Alerts Conditions** (APM/Key Transaction, External Service, NRQL, Synthetics, Location Failure): List/create/update/delete conditions per condition type and policy
- **Alerts Entity Conditions**: List conditions on an entity; add/remove a condition to/from an entity
- **Alerts Events, Incidents, Violations**: List events, incidents, and policy violations raised by alerting

Several of the Alerts endpoints above carry vendor deprecation notices pointing users toward NerdGraph, but they remain live, callable REST operations in the current spec, so they are kept rather than excluded.

### `new_relic-v2.json`

Full, unmodified vendor spec for the New Relic REST API v2 — the vendor's complete API surface, preserved as-is. See `new_relic-latest.json` above for the curated subset if you just need common CRUD automation.
