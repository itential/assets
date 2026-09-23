Jira Service Management is Atlassian's IT service management product, used to run service desks that handle customer requests, incidents, and changes through queues, SLAs, and approval workflows.

This project provides OpenAPI specs for automating against Jira Service Management's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model, organized one folder per resource. Two curated `-latest` specs are provided, covering the same resources but with different authentication — Basic Auth and OAuth 2.0 (3LO) — see **OpenAPIs** below for which to pick and **Integration Configuration** for setup steps.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Basic Auth](#basic-auth)
  - [OAuth 2.0 (3LO)](#oauth-20-3lo)
- [Studio Projects](#studio-projects)
  - [Info](#info)
  - [Knowledge Base](#knowledge-base)
  - [Service Desks](#service-desks)
  - [Request Types](#request-types)
  - [Queues](#queues)
  - [Customers](#customers)
  - [Organizations](#organizations)
  - [Customer Requests](#customer-requests)
  - [Request Transitions](#request-transitions)
  - [Request Comments](#request-comments)
  - [Request Attachments](#request-attachments)
  - [Request Approvals](#request-approvals)
  - [Request Participants](#request-participants)
  - [Request SLAs](#request-slas)
  - [Request Notifications](#request-notifications)
  - [Request Feedback](#request-feedback)
- [OpenAPIs](#openapis)
  - [`atlassian_jira_service_management_basic_auth-latest.json`](#atlassian_jira_service_management_basic_auth-latestjson)
  - [`atlassian_jira_service_management_oauth2_3lo-latest.json`](#atlassian_jira_service_management_oauth2_3lo-latestjson)
  - [`atlassian_jira_service_management-1001.0.0-SNAPSHOT-44cdd07c042959317ed5591bf79dbcd9369f3610.json`](#atlassian_jira_service_management-100100-snapshot-44cdd07c042959317ed5591bf79dbcd9369f3610json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Jira Service Management REST API OpenAPI specs — curated Basic Auth and OAuth 2.0 (3LO) variants, plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing CRUD workflows for service desks, request types, customer requests, queues, SLAs, approvals, organizations, customers, and the knowledge base |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Jira Service Management Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

`atlassian_jira_service_management_basic_auth-latest.json` and `atlassian_jira_service_management_oauth2_3lo-latest.json` share the same `info.title`/`info.version` (`Atlassian Jira Service Management` / `latest`) on purpose, so the Studio Project's workflows work unmodified against whichever one you import — Itential Platform identifies an Integration Model by title and version, not by which spec file created it. Because of that shared identity, **only one of the two can be imported into a given platform at a time**; importing the second while the first is present triggers Itential Platform's normal "model already exists" collision. That's expected — pick the auth method that matches your environment before importing.

### Basic Auth

Create an integration from `atlassian_jira_service_management_basic_auth-latest.json` pointing at your Jira Service Management site (e.g. `your-domain.atlassian.net`).

Authentication is HTTP Basic — your Atlassian account email as the username and an API token as the password:

```
Authorization: Basic <base64(email:api_token)>
```

Generate an API token at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens). The token doesn't expire until manually revoked, so there's no ongoing maintenance once it's configured.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "you@example.com",
      "password": "<api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "your-domain.atlassian.net",
    "base_path": ""
  }
}
```

### OAuth 2.0 (3LO)

Create an integration from `atlassian_jira_service_management_oauth2_3lo-latest.json`. OAuth 2.0 (3LO) needs a bit more setup than Basic Auth, on both the Atlassian and Itential Platform sides — follow the steps below in order. Once set up, the platform refreshes the access token automatically going forward, with no further manual steps.

**Atlassian side:**
1. Register an OAuth 2.0 (3LO) app at [developer.atlassian.com/console/myapps](https://developer.atlassian.com/console/myapps), Resource-level access.
2. Add the Jira Service Management API permission with the scopes your workflows need (e.g. `read:servicedesk-request`, `write:servicedesk-request`, `manage:servicedesk-customer`, `read:jira-user`) and `offline_access` — the last one is mandatory; without it Atlassian never issues a refresh token.
3. Add a callback URL under Authorization (any value works — you'll be reading the authorization code from the browser's address bar after redirect, not hosting anything at that URL).
4. Note the app's Client ID and Client Secret.

**Itential Platform side:**
1. Create the Integration Instance. Set `server.host` to `api.atlassian.com` — not your Jira tenant's own domain; OAuth Bearer calls route through Atlassian's API gateway, Basic Auth calls don't. Set `server.base_path` to `/ex/jira/<cloud-id>`; get the cloud ID with no auth needed via `curl https://<your-site>.atlassian.net/_edge/tenant_info`.
2. **Recommended:** configure the instance for direct/proxy-override routing rather than gateway-routed. This is a direct SaaS connection to Jira Service Management, so a gateway hop typically isn't needed.
3. Skip the built-in Test/Connect button for this integration when using 3LO. Complete the one-time authorization manually:
   - Build the authorize URL with your Client ID, the scopes above, your redirect URI, `response_type=code`, and `prompt=consent`; open it in a browser and accept.
   - Exchange the resulting code immediately (valid ~5 minutes) via `POST https://auth.atlassian.com/oauth/token` with `Content-Type: application/json`.
   - Seed the resulting `access_token`/`refresh_token` into the instance via Itential Platform's integration update API, using the full `properties.properties.properties.{authentication, server, tls, variables, version}` nesting so the values are saved to the location the platform reads at runtime. Include `expires_at` as part of this same payload — compute it yourself as current time plus `expires_in` (in milliseconds, so current epoch ms + 3,600,000 for the standard 1-hour token): `python3 -c "import time; print(int(time.time()*1000) + 3600000)"`. This is a one-time value; the platform recalculates and updates it automatically on every refresh after that.

The instance's `authentication`/`server` properties should look like this once configured (the platform keeps `token` current automatically after this point):

```json
{
  "authentication": {
    "OAuth2": {
      "client_id": "<client-id>",
      "client_secret": "<client-secret>",
      "token_url": "https://auth.atlassian.com/oauth/token",
      "refresh_url": "",
      "scope": "",
      "token": {
        "access_token": "<access-token>",
        "refresh_token": "<refresh-token>",
        "token_type": "Bearer",
        "expires_in": 3600,
        "expires_at": "<epoch-ms-1-hour-from-now>"
      },
      "authorization_url": "https://auth.atlassian.com/authorize"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.atlassian.com",
    "base_path": "/ex/jira/<cloud-id>"
  }
}
```

---

## Studio Projects

Every workflow's adapter task is wired to a specific Integration instance name (`Atlassian Jira Service Management`) — after importing, either name your Integration instance the same, or update the `adapter_id` value in each workflow task to match your own instance name. This works unmodified regardless of which auth variant you imported, since both share the same model identity (see [Integration Configuration](#integration-configuration)).

Create/Update workflows accept the request body as a single pre-built `requestBodyPayload` job variable, rather than individual flat fields — construct the object matching Jira Service Management's REST API shape before starting the job.

### Info

| Workflow | Scope |
|---|---|
| Get Info | Retrieve information about the Jira Service Management instance |

### Knowledge Base

| Workflow | Scope |
|---|---|
| Get Knowledge Base Articles | Search knowledge base articles across all service desks |
| View Knowledge Base Article | View a knowledge base article by page ID |
| Get Service Desk Knowledge Base Articles | Search knowledge base articles for a specific service desk |

### Service Desks

| Workflow | Scope |
|---|---|
| List Service Desks | List all service desks |
| Get Service Desk | Retrieve a service desk by ID |

### Request Types

| Workflow | Scope |
|---|---|
| List All Request Types | List all request types across every service desk |
| List Request Types | List the request types for a service desk |
| Get Request Type | Retrieve a request type by ID |
| Create Request Type | Create a request type on a service desk |
| Delete Request Type | Delete a request type from a service desk |
| Get Request Type Fields | Retrieve the fields for a request type |
| Get Request Type Groups | List the request type groups for a service desk |

### Queues

| Workflow | Scope |
|---|---|
| List Queues | List the queues for a service desk |
| Get Queue | Retrieve a queue by ID |
| Get Issues in Queue | List the issues in a queue |

### Customers

| Workflow | Scope |
|---|---|
| Create Customer | Create a customer account |
| Revoke Portal Only Access | Revoke portal-only access for a customer |
| Get Service Desk Customers | List the customers on a service desk |
| Add Service Desk Customers | Add customers to a service desk |
| Remove Service Desk Customers | Remove customers from a service desk |
| Invite Customer | Invite a customer to a service desk by email |

### Organizations

| Workflow | Scope |
|---|---|
| List Organizations | List all organizations |
| Create Organization | Create an organization |
| Get Organization | Retrieve an organization by ID |
| Delete Organization | Delete an organization |
| Get Organization Users | List the users in an organization |
| Add Organization Users | Add users to an organization |
| Remove Organization Users | Remove users from an organization |
| Get Organization Property Keys | List the entity property keys on an organization |
| Get Organization Property | Retrieve an entity property on an organization |
| Set Organization Property | Create or update an entity property on an organization |
| Delete Organization Property | Delete an entity property from an organization |
| Get Service Desk Organizations | List the organizations associated with a service desk |
| Add Service Desk Organization | Associate an organization with a service desk |
| Remove Service Desk Organization | Remove an organization from a service desk |

### Customer Requests

| Workflow | Scope |
|---|---|
| List Customer Requests | Search customer requests |
| Create Customer Request | Create a customer request |
| Validate Customer Request | Validate a customer request before creating it |
| Get Customer Request | Retrieve a customer request by ID or key |
| Get Customer Request Status | Retrieve the status history of a customer request |

### Request Transitions

| Workflow | Scope |
|---|---|
| Get Customer Transitions | List the transitions available for a customer request |
| Perform Customer Transition | Move a customer request through a transition |

### Request Comments

| Workflow | Scope |
|---|---|
| Get Request Comments | List the comments on a customer request |
| Create Request Comment | Add a comment to a customer request |
| Get Request Comment | Retrieve a single comment by ID |
| Get Comment Attachments | List the attachments on a request comment |

### Request Attachments

| Workflow | Scope |
|---|---|
| Get Request Attachments | List the attachments on a customer request |
| Create Comment with Attachment | Add a comment with attachments to a customer request |
| Get Attachment Content | Retrieve the content of an attachment |
| Attach Temporary File | Upload a temporary file for later attachment to a customer request |

### Request Approvals

| Workflow | Scope |
|---|---|
| Get Approvals | List the approvals on a customer request |
| Get Approval | Retrieve a single approval by ID |
| Answer Approval | Approve or decline an approval on a customer request |

### Request Participants

| Workflow | Scope |
|---|---|
| Get Request Participants | List the participants on a customer request |
| Add Request Participants | Add participants to a customer request |
| Remove Request Participants | Remove participants from a customer request |

### Request SLAs

| Workflow | Scope |
|---|---|
| Get SLA Information | List the SLA metrics on a customer request |
| Get SLA Information by ID | Retrieve a single SLA metric by ID |

### Request Notifications

| Workflow | Scope |
|---|---|
| Get Subscription Status | Get whether the current user is subscribed to a customer request |
| Subscribe | Subscribe the current user to a customer request |
| Unsubscribe | Unsubscribe the current user from a customer request |

### Request Feedback

| Workflow | Scope |
|---|---|
| Get Feedback | Retrieve feedback left on a customer request |
| Post Feedback | Leave feedback on a completed customer request |
| Delete Feedback | Delete feedback from a customer request |

---

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`atlassian_jira_service_management_basic_auth-latest.json`](./OpenAPIs/atlassian_jira_service_management_basic_auth-latest.json) | latest (curated) | 65 | Basic Auth variant — actively-maintained spec, trimmed to common CRUD for automation, see breakdown below |
| [`atlassian_jira_service_management_oauth2_3lo-latest.json`](./OpenAPIs/atlassian_jira_service_management_oauth2_3lo-latest.json) | latest (curated) | 65 | OAuth 2.0 (3LO) variant — same curated operation set as the Basic Auth spec above, different `securityScheme` |
| [`atlassian_jira_service_management-1001.0.0-SNAPSHOT-44cdd07c042959317ed5591bf79dbcd9369f3610.json`](./OpenAPIs/atlassian_jira_service_management-1001.0.0-SNAPSHOT-44cdd07c042959317ed5591bf79dbcd9369f3610.json) | 1001.0.0-SNAPSHOT-44cdd07c042959317ed5591bf79dbcd9369f3610 | 75 | Full spec for the Jira Service Management REST API surface (75 operations) |

### `atlassian_jira_service_management_basic_auth-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1001.0.0-SNAPSHOT-44cdd07c042959317ed5591bf79dbcd9369f3610`). Trimmed to 65 of 75 upstream operations covering common CRUD for automation. Excludes the Assets/Insight workspace lookup endpoints (a separate CMDB product surfaced through the same API), the duplicate permission-bypass customer-creation endpoints, the attachment thumbnail endpoint, and request-type-level entity property administration. Pull the full spec from [Atlassian's official Jira Service Management REST API reference](https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/) if you need one of the excluded areas.

Resources included, by category:

- **Info**: Get info
- **Service Desks**: List, Get by ID
- **Request Types**: List (global and per-service-desk), Get, Create, Delete, Get fields, Get groups
- **Queues**: List, Get, Get issues in queue
- **Customers**: Create, Revoke portal-only access, service-desk customer List/Add/Remove/Invite
- **Organizations**: CRUD, user membership (List/Add/Remove), entity properties (List/Get/Set/Delete), service-desk association (List/Add/Remove)
- **Customer Requests**: List, Create, Validate, Get, Get status
- **Request Transitions**: Get available transitions, Perform transition
- **Request Comments**: List, Create, Get, Get comment attachments
- **Request Attachments**: List, Create comment with attachment, Get content, Attach temporary file
- **Request Approvals**: List, Get, Answer
- **Request Participants**: List, Add, Remove
- **Request SLAs**: List, Get by ID
- **Request Notifications**: Get subscription status, Subscribe, Unsubscribe
- **Request Feedback**: Get, Post, Delete
- **Knowledge Base**: Search articles (global and per-service-desk), View article

### `atlassian_jira_service_management_oauth2_3lo-latest.json`

Identical resource/operation set to `atlassian_jira_service_management_basic_auth-latest.json` above — same 65 operations, same categories — with `securityScheme` replaced by an `oauth2` `authorizationCode` flow instead of `basicAuth`. Shares that spec's `info.title`/`info.version` by design; see [OAuth 2.0 (3LO)](#oauth-20-3lo) under Integration Configuration for why and how that affects importing it.

### `atlassian_jira_service_management-1001.0.0-SNAPSHOT-44cdd07c042959317ed5591bf79dbcd9369f3610.json`

Full, unmodified vendor spec — the vendor's complete API surface, preserved as-is. See `atlassian_jira_service_management_basic_auth-latest.json` above for the curated subset if you just need common CRUD automation.
