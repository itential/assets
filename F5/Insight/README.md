F5 Insight is F5's monitoring and analytics platform for device fleet management, providing unified visibility, software lifecycle management, and centralized configuration across F5 infrastructure.

This project provides OpenAPI specs for automating against F5 Insight's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`f5_insight-latest.json`](#f5_insight-latestjson)
  - [`f5_insight-v1.2.2.json`](#f5_insight-v122json)
- [Studio Projects](#studio-projects)
  - [F5 Insight Project](#f5-insight-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | F5 Insight API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 227 workflows in 27 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `F5 Insight:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `f5_insight-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your F5 Insight instance.

Authentication is HTTP Basic Auth, supported on every operation in this spec.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-f5-insight-host>",
    "base_path": ""
  }
}
```

Note the empty `base_path` — every operation's path already includes the full `/api/...` prefix literally, so a non-empty base path (e.g. `/api`) would double it up.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`f5_insight-latest.json`](./OpenAPIs/f5_insight-latest.json) | latest (curated) | 227 | Curated to device management, software/upgrade lifecycle, and monitoring — see breakdown below |
| [`f5_insight-v1.2.2.json`](./OpenAPIs/f5_insight-v1.2.2.json) | v1.2.2 | 281 | Full spec for the F5 Insight API |

### `f5_insight-latest.json`

Built from F5's own published OpenAPI spec (embedded in their [API documentation site](https://clouddocs.f5.com/products/insight/latest/apis/api.html), extracted from the page's Redoc bundle), curated to the core fleet-management categories.

Resources included, by category:

- **Device Management**: devices, data centers, trust stores, device migration/import tasks
- **Device Templates**: template CRUD, attach/deploy/clone/lock
- **Inventory**, **Infrastructure Discovery**: fleet and discovered-resource inventory
- **Cloud Environments** / **Cloud Providers**: connection and environment configuration (vSphere, etc.)
- **Software Distribution** / **Software Installation** / **Upgrade**: job lifecycle, scheduling, compatibility and flight checks
- **Backup**, **Storage**: backup/restore, storage target configuration
- **Licensing**: license pools, offerings, members
- **Jobs**, **Observability**, **Health and Readiness**, **Audit Console**, **Telemetry Configuration**, **Validation**, **Workflows**, **Tasks**, **VM Tasks**, **Images**, **Schedule**, **Configuration**, **FQDN Configuration**, **Lifecycle**, **Compatibility Matrix**

Excluded: authentication/authorization/identity-provider administration (one-time setup, not routine automation), AI-assistant chat history and insights, feature flags, and other internal admin tooling, plus 5 operations requiring multipart file uploads (image/backup/upgrade-bundle uploads, device migration bundles) — outside this repo's REST/JSON automation scope. Also excluded: OData-style query parameters (`$select`, `$filter`, `$orderby`, `$top`, `$skip`, `$count`) on 2 list operations — both work fine without them (unfiltered list results).

A handful of workflow names (e.g. generic device/job/workflow CRUD) are prefixed with `F5 Insight` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

### `f5_insight-v1.2.2.json`

Full, unmodified vendor spec for the F5 Insight API, version 1.2.2. See `f5_insight-latest.json` above for the curated subset if you just need common fleet-management automation.

## Studio Projects

### F5 Insight Project

Backed by the **`F5 Insight:latest`** Integration Model (see [`f5_insight-latest.json`](./OpenAPIs/f5_insight-latest.json) above). The project contains **227 workflows** organized into **27 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Device Management | 42 | Devices, data centers, trust stores, migration/import tasks |
| Upgrade | 23 | Upgrade scheduling, jobs, rollback, compatibility |
| Licensing | 21 | License pools, offerings, members |
| Software Distribution | 13 | Distribution job lifecycle |
| Device Templates | 12 | Template CRUD, attach/deploy/clone/lock |
| Software Installation | 11 | Installation job lifecycle |
| Storage | 9 | Storage target configuration |
| Backup | 8 | Backup/restore, schedules |
| Infrastructure Discovery | 7 | Discovered resource inventory |
| Observability | 7 | Monitoring data |
| Jobs | 7 | Generic job tracking |
| Configuration | 6 | System configuration |
| Inventory | 6 | Fleet inventory |
| Cloud Environments | 5 | Environment configuration |
| Cloud Providers | 5 | Provider connections (vSphere, etc.) |
| Schedule | 5 | Backup/upgrade scheduling |
| Health and Readiness | 5 | Health checks, readiness runs |
| VM Tasks | 4 | VM provisioning tasks |
| Compatibility Matrix | 4 | Upgrade path compatibility |
| Flight Checks | 4 | Pre/post-flight validation |
| Images | 4 | Image management |
| Validation | 4 | Device/template validation |
| Audit Console | 3 | Audit event querying |
| Lifecycle | 3 | Continuous lifecycle operations |
| Telemetry Configuration | 3 | Telemetry type configuration |
| Tasks | 2 | Generic task tracking |
| Workflows | 2 | Workflow/execution tracking |
| FQDN Configuration | 2 | FQDN-based external auth configuration |

#### Dependencies

| Dependency | Notes |
|---|---|
| `F5 Insight:latest` Integration Model | Import from [`f5_insight-latest.json`](./OpenAPIs/f5_insight-latest.json) before importing the project |
| `F5 Insight` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `F5 Insight` — update the `adapter_id` value in each workflow task if yours is named differently |
