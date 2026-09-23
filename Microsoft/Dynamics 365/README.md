# Dynamics 365

Microsoft Dynamics 365 is Microsoft's business applications suite — Sales, Customer Service, Field Service, and other CRM/ERP applications — built on Dataverse and exposed programmatically through the Dataverse Web API, an OData v4 service.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Scope](#scope)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`microsoft_dynamics_365-latest.json`](#microsoft_dynamics_365-latestjson)
  - [`microsoft_dynamics_365-v9.2.json`](#microsoft_dynamics_365-v92json)
- [Studio Projects](#studio-projects)
  - [Microsoft Dynamics 365 Project](#microsoft-dynamics-365-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Curated `-latest` spec plus a broader dated reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 26 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Dataverse Web API | v9.2 |
| Azure AD application registration | With an associated Dataverse application user, assigned a security role covering the entities being automated |
| `Microsoft Dynamics 365:latest` Integration Model | Required to build automation against the OpenAPI spec |

## Scope

The Dataverse Web API is metadata-driven: every organization's entity set, beyond a common standard core, is generated from that org's own customizations and isn't discoverable from a static spec. These specs cover the standard, org-independent entities documented in Microsoft's Web API Entity Type Reference — accounts, contacts, leads, opportunities, and incidents (cases) — via their entity-set endpoints, plus $batch execution and OData query support ($select, $filter, $expand, $orderby, $top, $count) on list operations. Custom entities aren't represented, since their entity-set names and schemas are unique to each org's customizations.

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Dataverse environment.

Authentication is native OAuth2 client credentials against an Azure AD app registration, using a Dataverse application user (not a licensed interactive user) to control what the client is allowed to do:

| Field | Value |
|---|---|
| `client_id` | Application (client) ID from your Azure AD app registration |
| `client_secret` | Client secret from that app registration |
| `token_url` | `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token` (substitute your tenant ID) |
| `scope` | `https://yourorg.crm.dynamics.com/.default` (substitute your environment's own URL) |

The application user needs a security role granting the appropriate privileges on the entities being automated (Account, Contact, Lead, Opportunity, Incident, and so on).

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-client-id>",
      "client_secret": "<your-client-secret>",
      "token_url": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
      "refresh_url": "",
      "scope": "https://yourorg.crm.dynamics.com/.default",
      "token": {
        "access_token": ""
      }
    }
  },
  "server": {
    "protocol": "https",
    "host": "yourorg.crm.dynamics.com",
    "base_path": "/api/data/v9.2"
  }
}
```

Replace `yourorg.crm.dynamics.com` with your own environment's hostname in the `scope` and `server.host` fields, and set `server.base_path` to your environment's Web API version path (`/api/data/v9.2` for the current release).

Every request also requires the `OData-MaxVersion: 4.0` and `OData-Version: 4.0` headers; both operations in this spec send them as required parameters.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`microsoft_dynamics_365-latest.json`](./OpenAPIs/microsoft_dynamics_365-latest.json) | latest | 26 | Curated CRUD subset — see breakdown below |
| [`microsoft_dynamics_365-v9.2.json`](./OpenAPIs/microsoft_dynamics_365-v9.2.json) | v9.2 | 35 | Broader reference surface |

### `microsoft_dynamics_365-latest.json`

Trimmed to 26 of 35 operations covering create/read/update/delete on Dataverse's core sales and customer-service entities, plus $batch execution.

Resources included, by category:

- **Accounts**: List, Create, Get, Update, Delete
- **Contacts**: List, Create, Get, Update, Delete
- **Leads**: List, Create, Get, Update, Delete
- **Opportunities**: List, Create, Get, Update, Delete
- **Incidents (Cases)**: List, Create, Get, Update, Delete
- **Batch**: Execute Batch

### `microsoft_dynamics_365-v9.2.json`

Broader reference surface (35 operations), adding activity and identity operations Microsoft's Web API reference documents as part of the same standard, org-independent surface: Task (activity) CRUD, read-only System User list/get, the WhoAmI identity function, and the $metadata CSDL document.

## Studio Projects

### Microsoft Dynamics 365 Project

Backed by the **`Microsoft Dynamics 365:latest`** Integration Model (see [`microsoft_dynamics_365-latest.json`](./OpenAPIs/microsoft_dynamics_365-latest.json) above). The project contains **26 workflows** organized into **6 folders**, one workflow per curated operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Accounts | 5 | List, create, get, update, and delete account records |
| Contacts | 5 | List, create, get, update, and delete contact records |
| Leads | 5 | List, create, get, update, and delete lead records |
| Opportunities | 5 | List, create, get, update, and delete opportunity records |
| Incidents (Cases) | 5 | List, create, get, update, and delete incident (case) records |
| Batch | 1 | Execute a $batch request |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Microsoft Dynamics 365:latest` Integration Model | Import from [`microsoft_dynamics_365-latest.json`](./OpenAPIs/microsoft_dynamics_365-latest.json) before importing the project |
| `Microsoft Dynamics 365` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Microsoft Dynamics 365` — update the `adapter_id` value in each workflow task if yours is named differently |
