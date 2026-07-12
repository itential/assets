ServiceNow is an ITSM/ITOM platform used for incident, change, request, and configuration management. This folder covers the Change Management, Table, and Itential Services App REST APIs commonly used to integrate ServiceNow with the Itential Platform.

This project provides two complementary ways to automate against ServiceNow:

- **Studio Project workflows** built on the **ServiceNow Adapter** — a set of ITSM workflows covering change requests, incidents, request items, and the service catalog.
- **OpenAPI specs** for building new automation directly against ServiceNow's REST APIs via an Integration Model. All three specs in this folder are already narrow, single-purpose vendor APIs and are included in full — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | ServiceNow Change Management, Table API, and Itential Services App OpenAPI specs — curated `-latest` plus the full dated spec for each |
| [Studio Projects/](./Studio%20Projects/) | IAP project containing the ITSM workflows |

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

---

## OpenAPIs

### `servicenow_change_management-latest.json`

Full, untrimmed spec (`x-vendor-api-version: v2`) — this is already a narrow, single-purpose API covering the Change Management module only (change requests, emergency/normal/standard changes, change tasks, approvals, conflicts, scheduling, and CI associations). No operations were removed.

### `servicenow_table_api-latest.json`

Full, untrimmed spec (`x-vendor-api-version: v3`) — the ServiceNow Table API is inherently generic CRUD (list/create/read/update/delete against any table by name), so it is included in full. No operations were removed.

### `servicenow_itential_services_app-latest.json`

Full, untrimmed spec (`x-vendor-api-version: v2`) — a single-endpoint scoped application API used to relay REST calls between ServiceNow and Itential Platform. No operations were removed.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`servicenow_change_management-v1.json`](./OpenAPIs/servicenow_change_management-v1.json) | Full spec for ServiceNow Change Management v1. |
| [`servicenow_table_api-v2.json`](./OpenAPIs/servicenow_table_api-v2.json) | Full spec for ServiceNow Table API v2. |
| [`servicenow_itential_services_app-v2.json`](./OpenAPIs/servicenow_itential_services_app-v2.json) | Full spec for ServiceNow Itential Services App v2. |

## Dependencies

| Dependency | Notes |
|---|---|
| ServiceNow Adapter | Required for the Studio Project workflows. Update `adapterId` in each workflow task to match your instance name. |
| ServiceNow Integration Model | Only needed if building automation directly against the OpenAPI specs above. |
