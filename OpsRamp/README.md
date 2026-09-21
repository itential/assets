# OpsRamp

OpsRamp is a SaaS IT operations management platform providing unified resource/device monitoring, alerting, incident management, and third-party integration management across hybrid IT environments.

This project provides OpenAPI specs for automating against OpsRamp's REST API via an Integration Model, plus a Studio Project of pre-built workflows — see **OpenAPIs** and **Studio Projects** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`opsramp-latest.json`](#opsramp-latestjson)
  - [`opsramp-2.0.0.json`](#opsramp-200json)
- [Studio Projects](#studio-projects)
  - [`OpsRamp.project.json`](#opsrampprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | OpsRamp REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 33 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| OpsRamp | 2.0.0 |
| OpsRamp Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is OAuth 2.0 (client credentials grant). Generate a client key/secret pair for an OpsRamp API client under **Setup > Integrations and Apps > API Management**, then configure the integration's `authentication.oauth2ClientCredentials` fields with those credentials and the token URL (`https://api.opsramp.com/tenancy/auth/oauth/token`).

Every operation is scoped to a tenant by a `clientId` path parameter — this is the OpsRamp tenant/client ID, not part of the integration's static config. Pass it as a job variable (`$var.job.clientId`) on every workflow in the Studio Project, alongside any resource-specific IDs (e.g. `resourceId`, `resourceGroupId`).

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`opsramp-latest.json`](./OpenAPIs/opsramp-latest.json) | latest (curated) | 33 | Trimmed to 33 of 211 upstream operations covering common CRUD for automation — see breakdown below |
| [`opsramp-2.0.0.json`](./OpenAPIs/opsramp-2.0.0.json) | 2.0.0 | 211 | Full spec for OpsRamp 2.0.0. |

### `opsramp-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0.0`). Trimmed to 33 of 211 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Resources/Devices**: Create, Get, Update, Delete, Search, List Minimal, Decommission
- **Device Groups**: Create, Get, Delete, Search (root-level)
- **Sites**: Create, Get, Update, Delete, Search
- **Alerts**: Create, Get Details, Search, Perform Action (acknowledge, resolve, suppress), Get Comments
- **Incidents/Tickets**: Create, Get Details, Update, Search, Perform Action, Add Note
- **Integrations**: Search Installed, Get Installed Details, Update Installed, Uninstall, Search Available, Install

### `opsramp-2.0.0.json`

Full, unmodified vendor spec for OpsRamp 2.0.0 (211 operations) — the vendor's complete API surface, preserved as-is. See `opsramp-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### `OpsRamp.project.json`

One folder per resource category, each with the corresponding CRUD/action workflows built on `opsramp-latest.json`'s Integration Model.

**Resources**

| Workflow | Scope |
|---|---|
| Create Resource | Create a new resource (device) |
| Get Resource | Get a resource by ID |
| Update Resource | Update an existing resource |
| Delete Resource | Delete a resource |
| List Minimal Resources | Get minimal details for resources matching filter criteria |
| Search Resources | Search resources with pagination and filter criteria |
| Decommission Resource | Decommission a resource |

**Device Groups**

| Workflow | Scope |
|---|---|
| Create Device Group | Create or update one or more device groups |
| Get Device Group | Get a device group by ID |
| Delete Device Group | Delete a device group |
| Search Device Groups | Get root-level device groups |

**Sites**

| Workflow | Scope |
|---|---|
| Create Site | Create a new site |
| Get Site | Get a site by ID |
| Update Site | Update an existing site |
| Delete Site | Delete a site |
| Search Sites | Search sites with pagination and filter criteria |

**Alerts**

| Workflow | Scope |
|---|---|
| Create Alerts | Create one or more alerts on resources |
| Get Alert Details | Get details of an alert |
| Search Alerts | Search alerts with pagination and filter criteria |
| Perform Alert Action | Perform an action (e.g. acknowledge, resolve, suppress) on an alert |
| Get Alert Comments | Get comments on an alert |

**Incidents**

| Workflow | Scope |
|---|---|
| Create Incident | Create a new incident or ticket |
| Get Incident Details | Get details of an incident or ticket |
| Update Incident | Update an existing incident or ticket |
| Search Incidents | Search incidents or tickets with pagination and filter criteria |
| Perform Incident Action | Perform an action on an incident or ticket |
| Add Incident Note | Add a note to an incident or ticket |

**Integrations**

| Workflow | Scope |
|---|---|
| Search Installed Integrations | Search installed integrations/apps with pagination and filter criteria |
| Get Installed Integration Details | Get status and details of an installed integration |
| Update Installed Integration | Update an installed integration |
| Uninstall Integration | Uninstall an installed integration |
| Search Available Integrations | Search the catalog of available integrations/apps |
| Install Integration | Install an integration/app |
