ServiceNow is an ITSM/ITOM platform used for incident, change, request, and configuration management. This folder covers the Change Management, Table, and Itential Services App REST APIs commonly used to integrate ServiceNow with the Itential Platform.

This project provides two complementary ways to automate against ServiceNow:

- **Studio Project workflows** built on the **ServiceNow Adapter** — a set of ITSM workflows covering change requests, incidents, request items, and the service catalog.
- **OpenAPI specs** for building new automation directly against ServiceNow's REST APIs via an Integration Model. All three specs in this folder are already narrow, single-purpose vendor APIs and are included in full — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Adapter (Studio Project workflows)](#adapter-studio-project-workflows)
  - [Integration Model (OpenAPI-based automation)](#integration-model-openapi-based-automation)
- [Studio Projects](#studio-projects)
  - [ServiceNow Project](#servicenow-project)
- [OpenAPIs](#openapis)
  - [`servicenow_change_management-latest.json`](#servicenow_change_management-latestjson)
  - [`servicenow_table_api-latest.json`](#servicenow_table_api-latestjson)
  - [`servicenow_itential_services_app-latest.json`](#servicenow_itential_services_app-latestjson)
  - [`servicenow_change_management-v1.json`](#servicenow_change_management-v1json)
  - [`servicenow_table_api-v2.json`](#servicenow_table_api-v2json)
  - [`servicenow_itential_services_app-v2.json`](#servicenow_itential_services_app-v2json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | ServiceNow Change Management, Table API, and Itential Services App OpenAPI specs — curated `-latest` plus the full dated spec for each |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing the ITSM workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| ServiceNow Adapter | Required for the Studio Project workflows below |
| ServiceNow Integration Model | Required only if building new automation directly against the OpenAPI specs |

## Integration Configuration

### Adapter (Studio Project workflows)

Install the ServiceNow Adapter and configure an instance in **Admin > Adapters**, then update the `adapterId` value in each workflow task to match your instance name before importing.

### Integration Model (OpenAPI-based automation)

To build automation directly against the REST APIs instead, import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your ServiceNow instance.

Authentication is HTTP Basic for all three specs:

```
Authorization: Basic <base64(username:password)>
```

Use a ServiceNow user/service account with appropriate ACL permissions on the target tables (or, for the Table API, an OAuth2 bearer token in place of Basic auth). For the Itential Services App API, the account must additionally have access to the `x_itent_services_itential` scoped application. Configure REST API access under **System Web Services → REST API Explorer**.

---

## Studio Projects

### ServiceNow Project

| Folder | Workflows | Scope |
|---|---|---|
| Create Change Request | Create Change Request | Create a new change request |
| Update Change Request | Update Change Request | Update an existing change request |
| Approve Change Request | Approve Change Request | Approve a pending change request |
| Close Change Request | Close Change Request | Close a change request |
| Create Incident | Create Incident | Create a new incident |
| Update Incident | Update Incident | Update an existing incident |
| Create Request Item (RITM) | Create Request Item (RITM) | Create a request item from the service catalog |
| Update Request Item | Update Request Item | Update an existing request item |
| Get Service Catalog Inputs | Get Service Catalog Inputs | Retrieve the input variables for a service catalog item |

#### Dependencies

| Dependency | Notes |
|---|---|
| ServiceNow Adapter | Required for the Studio Project workflows. Update `adapterId` in each workflow task to match your instance name. |

---

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`servicenow_change_management-latest.json`](./OpenAPIs/servicenow_change_management-latest.json) | latest (curated) | 42 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`servicenow_table_api-latest.json`](./OpenAPIs/servicenow_table_api-latest.json) | latest (curated) | 6 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`servicenow_itential_services_app-latest.json`](./OpenAPIs/servicenow_itential_services_app-latest.json) | latest (curated) | 1 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
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

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: v3`, 6 operations). The Table API is inherently generic CRUD (list/create/read/update/delete against any table by name) — every operation is a core CRUD verb on the single generic `tableName` resource, so nothing was removed.

Operations included, by category:

- **Table Records**: List/query records in a table, create a record, get a record by `sys_id`, replace a record (PUT), partially update a record (PATCH), delete a record

### `servicenow_itential_services_app-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: v2`, 1 operation). A single-endpoint scoped application API used to relay REST calls between ServiceNow and Itential Platform — there is only one operation in the upstream spec, so nothing was removed.

Operations included, by category:

- **REST Relay**: Make a REST call from ServiceNow to Itential Platform via the scoped app

### `servicenow_change_management-v1.json`

Full, unmodified vendor spec for ServiceNow Change Management v1 (42 operations) — the vendor's complete API surface, preserved as-is. See `servicenow_change_management-latest.json` above, which carries through the same 42 operations since none were trimmed.

### `servicenow_table_api-v2.json`

Full, unmodified vendor spec for ServiceNow Table API v2 (6 operations) — the vendor's complete API surface, preserved as-is. See `servicenow_table_api-latest.json` above, which carries through the same 6 operations since none were trimmed.

### `servicenow_itential_services_app-v2.json`

Full, unmodified vendor spec for the ServiceNow Itential Services App API v2 (1 operation) — the vendor's complete API surface, preserved as-is. See `servicenow_itential_services_app-latest.json` above, which carries through the same operation since none were trimmed.
