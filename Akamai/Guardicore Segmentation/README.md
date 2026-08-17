Akamai Guardicore Segmentation (formerly Guardicore Centra) is a microsegmentation platform that enforces network policy based on workload identity and labels rather than IP addresses and VLANs.

This project provides an OpenAPI spec for automating against the Guardicore Segmentation management API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
- [Studio Projects](#studio-projects)
  - [Akamai Guardicore Segmentation Project](#akamai-guardicore-segmentation-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Akamai Guardicore Segmentation API OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 55 workflows in 10 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Akamai Guardicore Segmentation API:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |
| A Guardicore Segmentation management console account | Required to obtain an access token |

## Integration Configuration

Import `akamai_guardicore_segmentation_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your management console's hostname.

Authentication is a bearer access token issued by the management console's own login endpoint (not Akamai's EdgeGrid signing used by most other Akamai products):

```
POST {base_url}/api/v3.0/authenticate
{"username": "...", "password": "..."}
```

returns `{"access_token": "...", "refresh_token": "..."}`. Send subsequent requests with `Authorization: Bearer <access_token>`. Access tokens expire — refresh with `POST {base_url}/api/v3.0/authenticate/refresh` sending `Authorization: Bearer <refresh_token>` (no body), which returns a new access token. Accounts with MFA enabled can't use username/password at all and must obtain an access/refresh token pair out of band.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "accessTokenAuth": {
      "Authorization": "Bearer <your-access-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-guardicore-instance-hostname>",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`akamai_guardicore_segmentation_api-latest.json`](./OpenAPIs/akamai_guardicore_segmentation_api-latest.json) | latest | 55 | Covers every resource category the provider manages — see breakdown below |

Built directly from Akamai's official, actively-maintained [`terraform-provider-guardicore-segmentation`](https://github.com/akamai/terraform-provider-guardicore-segmentation) — endpoint paths, HTTP verbs, and field-level request/response schemas were extracted from the provider's Go API client and its Terraform resource schemas.

Resources included, by category:

- **Labels**: Bulk create/update, bulk delete, get, update, delete, update dynamic criteria, list
- **Label Groups**: Create, get, update, delete, list, publish
- **Policy Groups**: Create, list (also used for get-by-id), update, delete, publish
- **Policy Rules**: Create, list, bulk create/update/delete, get, update, delete, publish, bulk move to worksite
- **DNS Security**: Create, list (also used for get-by-id), update, delete, bulk create/update/delete, reset hit count
- **Assets**: List (also used for get-by-id), deactivate, bulk create/update/deactivate
- **Worksites**: Create, update, list, bulk delete, assign entities
- **User Groups**: Create, update, delete, list, publish
- **Incidents**: Create, bulk create, list (also used for get-by-id)
- **Agent Aggregators**: List

Some operations map to the real API honestly rather than inventing symmetric CRUD that doesn't exist: Labels/Policy Groups/DNS Security/Assets/User Groups have no dedicated single-item GET (fetched via list + ID filter), Worksites' update takes the ID in the request body rather than the URL, Incidents are create-only (no update or delete API), Agent Aggregators is list-only (no create/update/delete API), and Assets' "delete" is a soft deactivate rather than permanent removal.

A handful of resource names are prefixed with `Guardicore` (e.g. `Guardicore Get Label`) to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

## Studio Projects

### Akamai Guardicore Segmentation Project

Backed by the **`Akamai Guardicore Segmentation API:latest`** Integration Model (see [`akamai_guardicore_segmentation_api-latest.json`](./OpenAPIs/akamai_guardicore_segmentation_api-latest.json) above). The project contains **55 workflows** organized into **10 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Policy Rules | 10 | Segmentation policy rules and publishing |
| DNS Security | 8 | Blocklists, bulk operations, hit-count reset |
| Labels | 7 | Labels and dynamic criteria |
| Label Groups | 6 | Label groups and publishing |
| Assets | 5 | Asset visibility and lifecycle |
| Worksites | 5 | Worksite management and entity assignment |
| User Groups | 5 | Active Directory-backed user groups |
| Policy Groups | 5 | Policy groups and publishing |
| Incidents | 3 | Incident creation and lookup |
| Agent Aggregators | 1 | Agent/collector visibility |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Akamai Guardicore Segmentation API:latest` Integration Model | Import from [`akamai_guardicore_segmentation_api-latest.json`](./OpenAPIs/akamai_guardicore_segmentation_api-latest.json) before importing the project |
| `Akamai Guardicore` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Akamai Guardicore` — update the `adapter_id` value in each workflow task if yours is named differently |
