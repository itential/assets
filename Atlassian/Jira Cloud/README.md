Jira Cloud is Atlassian's issue tracking and project management product, used to plan, track, and manage software and business work items (issues) through customizable workflows.

This project provides OpenAPI specs for automating against Jira Cloud's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model, organized one folder per resource. The `-latest` spec is a curated subset covering common CRUD for issue and project automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [Studio Projects](#studio-projects)
  - [Issues](#issues)
  - [Comments](#comments)
  - [Projects](#projects)
  - [Issue Worklogs](#issue-worklogs)
  - [Project Components](#project-components)
  - [Project Versions](#project-versions)
- [OpenAPIs](#openapis)
  - [`atlassian_jira_cloud-latest.json`](#atlassian_jira_cloud-latestjson)
  - [`atlassian_jira_cloud-2.0.0.json`](#atlassian_jira_cloud-200json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Jira Cloud REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing CRUD workflows for Issues, Comments, Projects, Worklogs, Components, and Versions |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Jira Cloud Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import [`atlassian_jira_cloud-latest.json`](./OpenAPIs/atlassian_jira_cloud-latest.json) as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Jira Cloud site (e.g. `your-domain.atlassian.net`).

Authentication is HTTP Basic — your Atlassian account email as the username and an API token as the password:

```
Authorization: Basic <base64(email:api_token)>
```

Generate an API token at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens).

---

## Studio Projects

Import [`Atlassian Jira.project.json`](./Studio%20Projects/Atlassian%20Jira.project.json) via **Automation Studio > Projects > Import**. Every workflow's adapter task is wired to a specific Integration instance name (`Atlassian Jira Cloud`) — after importing, either name your Integration instance the same, or update the `adapter_id` value in each workflow task to match your own instance name.

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
| [`atlassian_jira_cloud-latest.json`](./OpenAPIs/atlassian_jira_cloud-latest.json) | latest (curated) | 125 | Actively-maintained spec, trimmed to common CRUD for automation — see breakdown below |
| [`atlassian_jira_cloud-2.0.0.json`](./OpenAPIs/atlassian_jira_cloud-2.0.0.json) | 2.0.0 | 541 | Full spec for the Jira Cloud REST API v2 surface (541 operations) |

### `atlassian_jira_cloud-latest.json`

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

### `atlassian_jira_cloud-2.0.0.json`

Full, unmodified vendor spec (2.0.0) — the vendor's complete API surface, preserved as-is. See `atlassian_jira_cloud-latest.json` above for the curated subset if you just need common CRUD automation.
