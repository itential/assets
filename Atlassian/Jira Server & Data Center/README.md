Atlassian Jira Server and Data Center is Atlassian's self-hosted issue tracking and project management platform for software teams — issues, projects, workflows, and administration for on-premises Jira deployments (distinct from the SaaS Jira Cloud product).

This project provides an OpenAPI spec for automating against the Jira Server/Data Center REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`atlassian_jira_server_data_center-latest.json`](#atlassian_jira_server_data_center-latestjson)
  - [`atlassian_jira_server_data_center-10.0.0.json`](#atlassian_jira_server_data_center-1000json)
- [Studio Projects](#studio-projects)
  - [Atlassian Jira Server — Data Center Project](#atlassian-jira-server--data-center-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Jira Server & Data Center REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Atlassian Jira Server — Data Center](./Studio%20Projects/Atlassian%20Jira%20Server%20%E2%80%94%20Data%20Center.project.json) | 29 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Jira Server / Data Center | 10.0.0 (see OpenAPIs below for the exact spec version) |
| Jira Server & Data Center Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Jira Server or Data Center instance.

Authentication is HTTP Basic — a Jira username and password, or (Jira 8.14+) a Personal Access Token used in place of the password:

```
Authorization: Basic <base64(username:password_or_token)>
```

Generate a Personal Access Token in Jira under your user profile → **Personal Access Tokens**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basic": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "http",
    "host": "localhost:8090",
    "base_path": "/jira/rest"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`atlassian_jira_server_data_center-latest.json`](./OpenAPIs/atlassian_jira_server_data_center-latest.json) | latest (curated) | 105 | Trimmed to 105 of 430 upstream operations — see breakdown below |
| [`atlassian_jira_server_data_center-10.0.0.json`](./OpenAPIs/atlassian_jira_server_data_center-10.0.0.json) | 10.0.0 | 430 | Full spec for Jira Server & Data Center 10.0.0 (430 operations) |

### `atlassian_jira_server_data_center-latest.json`

Actively-maintained spec (`x-vendor-api-version: 10.0.0`). Trimmed to 105 of 430 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Issues**: Create, Read, Update, Delete, Bulk create, Create metadata, Comments, Worklogs, Transitions, Attachments (list/get), Remote links, Subtasks, Watchers, Votes, Assignee, Notify
- **Issue Links**: Issue Links, Issue Link Types
- **Projects**: Projects, Components, Versions, Project Roles
- **Search**: JQL Search, Filters
- **Users & Groups**: Users, Groups, Group Membership
- **Reference data**: Priorities, Resolutions, Statuses, Status Categories, Issue Types, Fields
- **Session/Info**: Current user (myself), My Permissions, Permissions, Server Info

Excluded: Jira Software Agile boards/sprints/epics (a separate add-on module), Jira administration (workflows, workflow schemes, permission/notification/security schemes, screens, role administration, application properties, clustering, monitoring, reindexing, license management, email templates), dashboards, avatars, custom field administration, terminology customization, and bulk worklog sync endpoints. Pull the full spec below if you need one of these.

### `atlassian_jira_server_data_center-10.0.0.json`

Full, unmodified vendor spec for Jira Server & Data Center 10.0.0 (430 operations) — the vendor's complete API surface, preserved as-is. See `atlassian_jira_server_data_center-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### Atlassian Jira Server — Data Center Project

Backed by the **`Atlassian Jira Server — Data Center:latest`** Integration Model (see [`atlassian_jira_server_data_center-latest.json`](./OpenAPIs/atlassian_jira_server_data_center-latest.json) above). The project contains **29 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Issues | Create Issue, Get Issue, Update Issue, Delete Issue, Get Transitions, Transition Issue | Issue lifecycle and workflow transitions |
| Comments | List, Add, Get, Update, Delete Comment | Issue comment lifecycle |
| Projects | List, Create, Get, Update, Delete Project | Project lifecycle |
| Issue Worklogs | List, Add, Get, Update, Delete Worklog | Issue worklog lifecycle |
| Project Components | List, Create, Get, Update, Delete Component | Project component lifecycle |
| Project Versions | List Versions, Get Version, Update Version | Project version lookup and update |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Atlassian Jira Server — Data Center:latest` Integration Model | Import from [`atlassian_jira_server_data_center-latest.json`](./OpenAPIs/atlassian_jira_server_data_center-latest.json) before importing the project |
| `Atlassian Jira Server — Data Center` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Atlassian Jira Server — Data Center` — update the `adapter_id` value in each workflow task if yours is named differently |
