Jira Cloud is Atlassian's issue tracking and project management product, used to plan, track, and manage software and business work items (issues) through customizable workflows.

This project provides OpenAPI specs for automating against Jira Cloud's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model, organized one folder per resource. Two curated `-latest` specs are provided, covering the same resources but with different authentication — Basic Auth and OAuth 2.0 (3LO) — see **OpenAPIs** below for which to pick and **Integration Configuration** for setup steps.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Basic Auth](#basic-auth)
  - [OAuth 2.0 (3LO)](#oauth-20-3lo)
- [Studio Projects](#studio-projects)
  - [Issues](#issues)
  - [Comments](#comments)
  - [Projects](#projects)
  - [Issue Worklogs](#issue-worklogs)
  - [Project Components](#project-components)
  - [Project Versions](#project-versions)
- [OpenAPIs](#openapis)
  - [`atlassian_jira_cloud_basic_auth-latest.json`](#atlassian_jira_cloud_basic_auth-latestjson)
  - [`atlassian_jira_cloud_oauth2_3lo-latest.json`](#atlassian_jira_cloud_oauth2_3lo-latestjson)
  - [`atlassian_jira_cloud-2.0.0.json`](#atlassian_jira_cloud-200json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Jira Cloud REST API OpenAPI specs — curated Basic Auth and OAuth 2.0 (3LO) variants, plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing CRUD workflows for Issues, Comments, Projects, Worklogs, Components, and Versions |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Jira Cloud Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

`atlassian_jira_cloud_basic_auth-latest.json` and `atlassian_jira_cloud_oauth2_3lo-latest.json` share the same `info.title`/`info.version` (`Atlassian Jira Cloud` / `latest`) on purpose, so the Studio Project's workflows work unmodified against whichever one you import — Itential Platform identifies an Integration Model by title and version, not by which spec file created it. Because of that shared identity, **only one of the two can be imported into a given platform at a time**; importing the second while the first is present triggers Itential Platform's normal "model already exists" collision. That's expected — pick the auth method that matches your environment before importing.

### Basic Auth

Create an integration from `atlassian_jira_cloud_basic_auth-latest.json` pointing at your Jira Cloud site (e.g. `your-domain.atlassian.net`).

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

Create an integration from `atlassian_jira_cloud_oauth2_3lo-latest.json`. OAuth 2.0 (3LO) needs a bit more setup than Basic Auth, on both the Atlassian and Itential Platform sides — follow the steps below in order. Once set up, the platform refreshes the access token automatically going forward, with no further manual steps.

**Atlassian side:**
1. Register an OAuth 2.0 (3LO) app at [developer.atlassian.com/console/myapps](https://developer.atlassian.com/console/myapps), Resource-level access.
2. Add the Jira API permission with scopes `read:jira-work`, `write:jira-work`, `read:jira-user`, and `offline_access` — the last one is mandatory; without it Atlassian never issues a refresh token.
3. Add a callback URL under Authorization (any value works — you'll be reading the authorization code from the browser's address bar after redirect, not hosting anything at that URL).
4. Note the app's Client ID and Client Secret.

**Itential Platform side:**
1. Create the Integration Instance. Set `server.host` to `api.atlassian.com` — not your Jira tenant's own domain; OAuth Bearer calls route through Atlassian's API gateway, Basic Auth calls don't. Set `server.base_path` to `/ex/jira/<cloud-id>`; get the cloud ID with no auth needed via `curl https://<your-site>.atlassian.net/_edge/tenant_info`.
2. **Recommended:** configure the instance for direct/proxy-override routing rather than gateway-routed. This is a direct SaaS connection to Jira Cloud, so a gateway hop typically isn't needed.
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

Every workflow's adapter task is wired to a specific Integration instance name (`Atlassian Jira Cloud`) — after importing, either name your Integration instance the same, or update the `adapter_id` value in each workflow task to match your own instance name. This works unmodified regardless of which auth variant you imported, since both share the same model identity (see [Integration Configuration](#integration-configuration)).

Most Create/Update workflows accept the request body as a single pre-built `requestBodyPayload` (or `payload`) job variable, rather than individual flat fields — construct the object matching Jira's REST API shape before starting the job.

### Issues

| Workflow | Scope |
|---|---|
| List Issues | Search for issues using JQL |
| Create Issue | Create a new issue |
| Get Issue | Retrieve an issue by ID or key |
| Update Issue | Update an issue by ID or key |
| Delete Issue | Delete an issue by ID or key |
| Get Transitions | List the available transitions for an issue |
| Transition Issue | Move an issue through its workflow |

### Comments

| Workflow | Scope |
|---|---|
| Get Comments | List the comments on an issue |
| Add Comment | Add a comment to an issue |
| Get Comment | Retrieve a single comment by ID |
| Update Comment | Update a comment by ID |
| Delete Comment | Delete a comment by ID |

### Projects

| Workflow | Scope |
|---|---|
| List Projects | Search for projects |
| Create Project | Create a new project |
| Get Project | Retrieve a project by ID or key |
| Update Project | Update a project by ID or key |
| Delete Project | Delete a project by ID or key |

### Issue Worklogs

| Workflow | Scope |
|---|---|
| List Worklogs | List the worklogs on an issue |
| Add Worklog | Add a worklog to an issue |
| Get Worklog | Retrieve a single worklog by ID |
| Update Worklog | Update a worklog by ID |
| Delete Worklog | Delete a worklog by ID |

### Project Components

| Workflow | Scope |
|---|---|
| List Components | List the components in a project |
| Create Component | Create a component in a project |
| Get Component | Retrieve a component by ID |
| Update Component | Update a component by ID |
| Delete Component | Delete a component by ID |

### Project Versions

| Workflow | Scope |
|---|---|
| List Versions | List the versions in a project |
| Create Version | Create a version in a project |
| Get Version | Retrieve a version by ID |
| Update Version | Update a version by ID |
| Delete Version | Delete a version by ID |

---

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`atlassian_jira_cloud_basic_auth-latest.json`](./OpenAPIs/atlassian_jira_cloud_basic_auth-latest.json) | latest (curated) | 125 | Basic Auth variant — actively-maintained spec, trimmed to common CRUD for automation, see breakdown below |
| [`atlassian_jira_cloud_oauth2_3lo-latest.json`](./OpenAPIs/atlassian_jira_cloud_oauth2_3lo-latest.json) | latest (curated) | 125 | OAuth 2.0 (3LO) variant — same curated operation set as the Basic Auth spec above, different `securityScheme` |
| [`atlassian_jira_cloud-2.0.0.json`](./OpenAPIs/atlassian_jira_cloud-2.0.0.json) | 2.0.0 | 541 | Full spec for the Jira Cloud REST API v2 surface (541 operations) |

### `atlassian_jira_cloud_basic_auth-latest.json`

Actively-maintained spec (`x-vendor-api-version: 3.0.0`). Trimmed to 125 of 541 upstream operations covering common CRUD for automation. Excludes Jira administration areas such as dashboards, filters, workflow/screen/permission/notification scheme configuration, custom field configuration, webhooks, groups, avatars, and Forge/Connect app-extension endpoints. Pull the full spec from [Atlassian's official Jira Cloud REST API v3 reference](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) if you need one of the excluded areas.

Resources included, by category:

- **Issues**: Create, Get, Update, Delete, Bulk Create, Assign, Create-metadata lookup, Edit-metadata, Changelog, Notify
- **Issue Transitions**: Get Transitions, Transition Issue
- **Issue Comments**: List, Add, Get, Update, Delete
- **Issue Attachments**: Settings, Add, Get metadata, Get content, Delete
- **Issue Worklogs**: List, Add, Get, Update, Delete
- **Issue Watchers**: List, Add, Delete
- **Issue Links & Link Types**: Create/Get/Delete Issue Link, CRUD Issue Link Types
- **Issue Remote Links**: List, Create/Update, Get, Delete
- **Issue Search**: Search by JQL (GET/POST), Search Issue IDs, Issue Picker, Check Issues Against JQL
- **Issue Bulk Operations**: Bulk Edit, Bulk Move, Bulk Operation Progress
- **Projects**: List, Create, Search, Get, Update, Delete
- **Project Components**: List, Create, Get, Update, Delete
- **Project Versions**: List, Create, Get, Update, Delete
- **Reference data**: Issue Types, Priorities, Resolutions, Fields, Statuses, Labels
- **Users**: Get, Bulk Get, Email Lookup, current-user (`myself`), full User Search suite (assignable search, picker, by-query, permission search)

### `atlassian_jira_cloud_oauth2_3lo-latest.json`

Identical resource/operation set to `atlassian_jira_cloud_basic_auth-latest.json` above — same 125 operations, same categories — with `securityScheme` replaced by an `oauth2` `authorizationCode` flow instead of `basicAuth`. Shares that spec's `info.title`/`info.version` by design; see [OAuth 2.0 (3LO)](#oauth-20-3lo) under Integration Configuration for why and how that affects importing it.

### `atlassian_jira_cloud-2.0.0.json`

Full, unmodified vendor spec (2.0.0) — the vendor's complete API surface, preserved as-is. See `atlassian_jira_cloud_basic_auth-latest.json` above for the curated subset if you just need common CRUD automation.
