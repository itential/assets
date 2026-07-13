Jira Cloud is Atlassian's issue tracking and project management product, used to plan, track, and manage software and business work items (issues) through customizable workflows.

This project provides two complementary ways to automate against Jira Cloud:

- **Studio Project workflows** built on the **Jira Adapter** — issue and project creation/transition workflows.
- **OpenAPI specs** for building new automation directly against the Jira Cloud REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for issue and project automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Jira Cloud REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing issue and project workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Jira Adapter | Required for the Studio Project workflows below |
| Jira Cloud Integration Model | Required only if building new automation directly against the OpenAPI specs |

## Integration Configuration

### Adapter (Studio Project workflows)

Install the [Jira Adapter](https://gitlab.com/itentialopensource/adapters/adapter-jira) and configure an instance in **Admin > Adapters**, then update the `adapter_id` value in each workflow task to match your instance name before importing.

### Integration Model (OpenAPI-based automation)

To build automation directly against the REST API instead, import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Jira Cloud site (e.g. `your-domain.atlassian.net`).

Authentication is HTTP Basic — your Atlassian account email as the username and an API token as the password:

```
Authorization: Basic <base64(email:api_token)>
```

Generate an API token at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens).

---

## Studio Projects

### Atlassian Jira Project

| Folder | Workflows | Scope |
|---|---|---|
| Create Project | Create Project | Create a new Jira project from a project type template |
| Create Issue | Create Issue | Build a payload and create a new Jira issue |
| Transition Issue | Get Transitions, Transition Issue | Look up the available transitions for an issue and move it through its workflow |

#### Dependencies

| Dependency | Notes |
|---|---|
| [Jira Adapter](https://gitlab.com/itentialopensource/adapters/adapter-jira) | Required for the Studio Project workflows. Update `adapter_id` in each workflow task to match your instance name. |

---

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`atlassian_jira_cloud-latest.json`](./OpenAPIs/atlassian_jira_cloud-latest.json) | latest (curated) | Actively-maintained spec, trimmed to common CRUD for automation — see breakdown below |
| [`atlassian_jira_cloud-2.0.0.json`](./OpenAPIs/atlassian_jira_cloud-2.0.0.json) | 2.0.0 | Full spec for the Jira Cloud REST API v2 surface (359 operations) |

### `atlassian_jira_cloud-latest.json`

Actively-maintained spec (`x-vendor-api-version: 3.0.0`). Trimmed to 125 of 545 upstream operations covering common CRUD for automation. Excludes Jira administration areas such as dashboards, filters, workflow/screen/permission/notification scheme configuration, custom field configuration, webhooks, groups, avatars, and Forge/Connect app-extension endpoints. Pull the full spec from [Atlassian's official Jira Cloud REST API v3 reference](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) if you need one of the excluded areas.

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
