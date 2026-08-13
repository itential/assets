ServiceNow is an ITSM/ITOM platform used for incident, change, request, and configuration management. This folder covers the Change Management and Table REST APIs commonly used to integrate ServiceNow with the Itential Platform.

This project provides OpenAPI specs for automating against ServiceNow's REST APIs via Integration Models, plus a Studio Project of ready-to-import CRUD workflows built on those models.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`servicenow_change_management-latest.json`](#servicenow_change_management-latestjson)
  - [`servicenow_table_api-latest.json`](#servicenow_table_api-latestjson)
  - [`servicenow_itential_services_app-latest.json`](#servicenow_itential_services_app-latestjson)
  - [`servicenow_change_management-v1.json`](#servicenow_change_management-v1json)
  - [`servicenow_table_api-v2.json`](#servicenow_table_api-v2json)
  - [`servicenow_itential_services_app-v2.json`](#servicenow_itential_services_app-v2json)
- [Studio Projects](#studio-projects)
  - [ServiceNow Project](#servicenow-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | ServiceNow Change Management, Table API, and Itential Services App OpenAPI specs — curated `-latest` plus the full dated spec for each |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 48 workflows in 8 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `ServiceNow Change Management:latest` Integration Model | Required to run the Change Requests/Emergency Changes/Normal Changes/Standard Changes/Change Tasks/Change CIs & Conflicts/Change Scheduling folders |
| `ServiceNow Table API:latest` Integration Model | Required to run the Table Records folder |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to ServiceNow's REST APIs.

## Integration Configuration

Import `servicenow_change_management-latest.json` and `servicenow_table_api-latest.json` as Integration Models in **Admin > Integrations**, then create an integration for each pointing at your ServiceNow instance.

Authentication is HTTP Basic for both specs:

```
Authorization: Basic <base64(username:password)>
```

Use a ServiceNow user/service account with appropriate ACL permissions on the target tables (or, for the Table API, an OAuth2 bearer token in place of Basic auth). Configure REST API access under **System Web Services → REST API Explorer**.

The instances' `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "Basic": {
      "username": "<your-servicenow-username>",
      "password": "<your-servicenow-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-instance>.service-now.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`servicenow_change_management-latest.json`](./OpenAPIs/servicenow_change_management-latest.json) | latest (curated) | 42 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`servicenow_table_api-latest.json`](./OpenAPIs/servicenow_table_api-latest.json) | latest (curated) | 6 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`servicenow_itential_services_app-latest.json`](./OpenAPIs/servicenow_itential_services_app-latest.json) | latest (curated) | 1 | Reviewed and confirmed already scoped to common CRUD for automation — not built into the Studio Project below, see note |
| [`servicenow_change_management-v1.json`](./OpenAPIs/servicenow_change_management-v1.json) | v1 | 42 | Full spec for ServiceNow Change Management v1. |
| [`servicenow_table_api-v2.json`](./OpenAPIs/servicenow_table_api-v2.json) | v2 | 6 | Full spec for ServiceNow Table API v2. |
| [`servicenow_itential_services_app-v2.json`](./OpenAPIs/servicenow_itential_services_app-v2.json) | v2 | 1 | Full spec for ServiceNow Itential Services App v2. |

### `servicenow_change_management-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: v2`, 42 operations). Already a narrow, single-purpose API covering the Change Management module only. Every operation reads or writes an actual change-management business object (change requests, tasks, CIs, conflicts, schedule, risk, approvals) — there is no separate health/metrics/self-introspection surface to exclude, so nothing was removed.

Operations included, by category:

- **Change Requests (any type)**: List, create, get, update, delete; update approvals; update risk assessment; get valid next workflow states
- **Emergency Changes**: List, create, get, update, delete
- **Normal Changes**: List, create, get, update, delete
- **Standard Changes**: List, get, update, delete; create from a standard change template
- **Standard Change Templates**: List, get
- **Change Models**: List, get
- **Change Tasks**: List, create, get, update, delete (implementation tasks under a change)
- **Affected CIs**: List CIs affected by a change; add a CI to a change
- **Conflict Detection**: Get detected conflicts; run conflict detection; clear conflicts
- **Scheduling**: Get CI change schedule; get change schedule; set change to first available slot
- **Impacted Services**: Refresh the impacted business services list for a change
- **Background Worker**: Get the status of a background worker process tied to a change operation

### `servicenow_table_api-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: v3`, 6 operations). The Table API is inherently generic CRUD (list/create/read/update/delete against any table by name) — every operation is a core CRUD verb on the single generic `tableName` resource, so nothing was removed. The vendor spec was missing `operationId` on every operation; this pass added conventional camelCase IDs (e.g. `getApiNowTableTablename`) derived from verb + path, matching the convention used elsewhere in this repo — the dated `-v2.json` spec is left unmodified.

Operations included, by category:

- **Table Records**: List/query records in a table, create a record, get a record by `sys_id`, replace a record (PUT), partially update a record (PATCH), delete a record

### `servicenow_itential_services_app-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: v2`, 1 operation). A single-endpoint scoped application API used to relay REST calls between ServiceNow and Itential Platform — there is only one operation in the upstream spec, so nothing was removed. Same `operationId` gap and fix as the Table API spec above.

Not built into the Studio Project below — this is a relay endpoint for a specific integration pattern rather than a general-purpose CRUD resource, and is out of scope for this pass.

Operations included, by category:

- **REST Relay**: Make a REST call from ServiceNow to Itential Platform via the scoped app

### `servicenow_change_management-v1.json`

Full, unmodified vendor spec for ServiceNow Change Management v1 (42 operations) — the vendor's complete API surface, preserved as-is. See `servicenow_change_management-latest.json` above, which carries through the same 42 operations since none were trimmed.

### `servicenow_table_api-v2.json`

Full, unmodified vendor spec for ServiceNow Table API v2 (6 operations) — the vendor's complete API surface, preserved as-is. See `servicenow_table_api-latest.json` above, which carries through the same 6 operations since none were trimmed.

### `servicenow_itential_services_app-v2.json`

Full, unmodified vendor spec for the ServiceNow Itential Services App API v2 (1 operation) — the vendor's complete API surface, preserved as-is. See `servicenow_itential_services_app-latest.json` above, which carries through the same operation since none were trimmed.

---

## Studio Projects

### ServiceNow Project

Backed by the **`ServiceNow Change Management:latest`** and **`ServiceNow Table API:latest`** Integration Models (see OpenAPIs above). The project contains **48 workflows** organized into **8 folders**, one workflow per curated operation.

#### Folder Structure

| Folder | Workflows | Scope | Integration Model |
|---|---|---|---|
| Change Requests | 10 | Change Request (any type) — CRUD, approvals, risk, next states, impacted services, worker status | Change Management |
| Emergency Changes | 5 | Emergency Change — CRUD | Change Management |
| Normal Changes | 5 | Normal Change — CRUD | Change Management |
| Standard Changes | 9 | Standard Change — list/get/update/delete, create from template, templates, change models | Change Management |
| Change Tasks | 5 | Change Task — CRUD | Change Management |
| Change CIs & Conflicts | 5 | Affected CIs, conflict detection | Change Management |
| Change Scheduling | 3 | CI schedule, change schedule, first available slot | Change Management |
| Table Records | 6 | Generic table CRUD by table name | Table API |

#### Dependencies

| Dependency | Notes |
|---|---|
| `ServiceNow Change Management:latest` Integration Model | Import from [`servicenow_change_management-latest.json`](./OpenAPIs/servicenow_change_management-latest.json) before importing the project |
| `ServiceNow Table API:latest` Integration Model | Import from [`servicenow_table_api-latest.json`](./OpenAPIs/servicenow_table_api-latest.json) before importing the project |
| `ServiceNow Change` integration instance | Backs the Change Management folders. Update the `adapter_id` value in each of those workflow tasks if yours is named differently |
| `ServiceNow Table` integration instance | Backs the Table Records folder. Update the `adapter_id` value in each of those workflow tasks if yours is named differently |

**Testing status:** all 48 workflows were created and schema-validated against a running Itential Platform instance. `List Change Requests` and `List Table Records` were executed against a real ServiceNow instance and confirmed returning live data. The remaining workflows have not been individually executed.
