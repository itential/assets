# Crosswork Assurance

Cisco Crosswork Assurance (formerly Accedian Skylight, later Cisco Provider Connectivity Assurance) delivers network performance monitoring and service assurance — session analytics, active testing, alerting, and metrics for monitored objects across a provider or enterprise network.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_crosswork_assurance-latest.json`](#cisco_crosswork_assurance-latestjson)
  - [`cisco_crosswork_assurance-25.7.json`](#cisco_crosswork_assurance-257json)
- [Studio Projects](#studio-projects)
  - [Cisco Crosswork Assurance Project](#cisco-crosswork-assurance-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Crosswork Assurance analytics API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Cisco Crosswork Assurance](./Studio%20Projects/Cisco%20Crosswork%20Assurance.project.json) | 97 workflows covering monitored objects, threshold profiles, session filters, alerting, metrics, active testing, data export, time window exclusions, predictions, and connector status |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco Crosswork Assurance | 25.7 analytics API |
| `Cisco Crosswork Assurance` Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your tenant's analytics API.

Authentication is OAuth 2.0 Authorization Code with PKCE, replayed as a Bearer token. Obtain the `AnalyticsUI` client ID from your tenant's IAM console (Applications section, `tenant-admin` role), complete the PKCE authorization_code exchange against your tenant's IAM authority, and configure the resulting access token:

```
Authorization: Bearer <your-access-token>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "OAuth2": {
      "token": "<your-access-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.analytics.accedian.io",
    "base_path": "/api"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_crosswork_assurance-latest.json`](./OpenAPIs/cisco_crosswork_assurance-latest.json) | latest (curated) | 97 | Trimmed to 97 of 253 upstream operations — see breakdown below |
| [`cisco_crosswork_assurance-25.7.json`](./OpenAPIs/cisco_crosswork_assurance-25.7.json) | 25.7 | 253 | Full spec, sourced from the vendor's own rendered API documentation |

### `cisco_crosswork_assurance-latest.json`

Actively-maintained spec (`x-vendor-api-version: 25.7`). Trimmed to 97 of 253 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Monitored Objects**: list, create, get, update, delete, count (filtered), list (filtered), list/count by reporting status, bulk insert/update/patch, summaries, metric baselines
- **Threshold Profiles**: list, create, get, update, delete
- **Session Filter Profiles**: list, create, get, replace, patch, delete
- **Session Filters**: list, create, get, replace, patch, delete
- **Alert Policies**: list, create, get, patch, delete, get default(s), update status
- **Alerts**: list/aggregate/count/group (filtered), create/get/delete active alerts for a monitored object, alert history, alerts for a monitored object
- **Metrics and Reporting**: aggregate/group metrics, aggregate/group derived metrics, instance metric runs, activated dependencies
- **TCP Throughput Tests**: create, list, get/update/delete a report, count/list (filtered)
- **Session Trace**: create, list, get, delete
- **Data Export**: create/list/get/patch/disable/delete a configuration, list/download/delete a report
- **Time Window Exclusions**: create, list, get, patch, replace, delete, list events
- **Predictions**: create, get, delete a prediction profile
- **Connector and Ingestion Status**: list/get connector status, activate connector, list/get connectors, list/create/get operational states, ingestion collector information

Long tails dropped from the upstream surface include: tenant/branding/UI customization (brandings, cards, dashboards, locales), connector configuration templates, data-cleaning history/profiles, duplicate-monitored-object reports, ingestion profile/dictionary administration, metadata mapping/config administration, tenant and IAM administration (tenant CRUD, solution manifests), telemetry agent template/config generation, tech support report generation, internal cache/purge maintenance operations, and distribution downloads.

### `cisco_crosswork_assurance-25.7.json`

Full spec (253 operations), extracted directly from the vendor's own rendered API documentation at `api.accedian.io/session.html`.

## Studio Projects

### Cisco Crosswork Assurance Project

Backed by the **`Cisco Crosswork Assurance:latest`** Integration Model (see [`cisco_crosswork_assurance-latest.json`](./OpenAPIs/cisco_crosswork_assurance-latest.json) above). The project contains **97 workflows** organized into **13 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Scope |
|---|---|
| Monitored Objects | Monitored-object CRUD, bulk operations, summaries, and metric baselines |
| Threshold Profiles | Threshold profile CRUD |
| Session Filter Profiles | Session filter profile CRUD |
| Session Filters | Session filter CRUD |
| Alert Policies | Alert policy CRUD, defaults, and status |
| Alerts | Active alert queries and lifecycle, alert history |
| Metrics and Reporting | Metric and derived-metric aggregation/grouping, instance metric runs, dependencies |
| TCP Throughput Tests | TCP throughput test lifecycle and reports |
| Session Trace | Session trace capture lifecycle |
| Data Export | Export configuration CRUD and report retrieval |
| Time Window Exclusions | Time window exclusion CRUD and events |
| Predictions | Prediction profile CRUD |
| Connector and Ingestion Status | Connector status/activation, operational states, ingestion collector info |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Cisco Crosswork Assurance:latest` Integration Model | Import from [`cisco_crosswork_assurance-latest.json`](./OpenAPIs/cisco_crosswork_assurance-latest.json) before importing the project |
| `Cisco Crosswork Assurance` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Cisco Crosswork Assurance` — update the `adapter_id` value in each workflow task if yours is named differently |
