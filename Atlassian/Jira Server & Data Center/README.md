Atlassian Jira Server and Data Center is Atlassian's self-hosted issue tracking and project management platform for software teams — issues, projects, workflows, and administration for on-premises Jira deployments (distinct from the SaaS Jira Cloud product).

This project provides an OpenAPI spec for automating against the Jira Server/Data Center REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Jira Server & Data Center REST API OpenAPI specs — curated `-latest` plus the full dated spec |

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

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`atlassian_jira_server_data_center-latest.json`](./OpenAPIs/atlassian_jira_server_data_center-latest.json) | latest (curated) | Trimmed to 105 of 430 upstream operations — see breakdown below |
| [`atlassian_jira_server_data_center-10.0.0.json`](./OpenAPIs/atlassian_jira_server_data_center-10.0.0.json) | 10.0.0 | Full spec for Jira Server & Data Center 10.0.0 (430 operations) |

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

## Dependencies

| Dependency | Notes |
|---|---|
| Jira Server & Data Center Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
