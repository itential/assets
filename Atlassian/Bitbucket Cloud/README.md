Bitbucket Cloud is Atlassian's hosted Git repository management service, providing source control, pull requests, branch permissions, and workspace/project organization for teams.

This project provides OpenAPI specs for automating against the Bitbucket Cloud REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`atlassian_bitbucket_cloud-latest.json`](#atlassian_bitbucket_cloud-latestjson)
  - [`atlassian_bitbucket_cloud-2.0.json`](#atlassian_bitbucket_cloud-20json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Bitbucket Cloud REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Bitbucket Cloud | REST API 2.0 |
| Bitbucket Cloud Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at `api.bitbucket.org`.

Authentication is HTTP Basic auth using a Bitbucket App Password:

```
Authorization: Basic <base64(username:app_password)>
```

Generate an App Password in Bitbucket under **Personal Settings > App passwords**.

> **Note:** The upstream spec also defines OAuth2 and a deprecated account API key scheme. Itential Platform supports a single authentication method per integration instance, so this spec is consolidated to the Basic/App Password scheme, which is the standard non-interactive credential for automation.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`atlassian_bitbucket_cloud-latest.json`](./OpenAPIs/atlassian_bitbucket_cloud-latest.json) | latest (curated) | 91 | Trimmed to 91 of 318 upstream operations — see breakdown below |
| [`atlassian_bitbucket_cloud-2.0.json`](./OpenAPIs/atlassian_bitbucket_cloud-2.0.json) | 2.0 | 318 | Full spec for Bitbucket Cloud REST API 2.0 (Swagger 2.0, as published by the vendor) |

### `atlassian_bitbucket_cloud-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0`). Trimmed to 91 of 318 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Workspaces**: List Workspaces, Get Workspace, List Members, Get Member
- **Projects**: Create, Read, Update, Delete; Default Reviewers (list, get, set, remove)
- **Repositories**: Create, Read, Update, Delete; List by Workspace/All; Forks (list, create)
- **Branches & Tags**: List Refs, Branches (list, create, get, delete), Tags (list, create, get, delete)
- **Branch Restrictions**: List, Create, Get, Update, Delete
- **Default Reviewers** (repository-level): List, Get, Set, Remove
- **Deploy Keys**: List, Create, Get, Update, Delete
- **Commits**: Get, Approve/Unapprove, Comments (list, create, get, update, delete), Build Statuses (list, create, get, update), List Pull Requests for a Commit
- **Pull Requests**: Create, Read, Update, List/Activity, Approve/Unapprove, Request/Remove Changes, Comments (list, create, get, update, delete, resolve), List Commits, Decline, Diff, Diffstat, Merge, Merge Task Status, Statuses, Tasks (list, create, get, update, delete)
- **User**: Get Current User

Not included: the legacy Issue Tracker, Snippets, Pipelines/CI-CD (config, variables, caches, schedules, SSH keys, deployments, environments), webhooks, add-ons, code search, SSH keys, properties, and permissions/administration endpoints. Pull the full spec above if you need one of these.

### `atlassian_bitbucket_cloud-2.0.json`

Full, unmodified vendor spec for Bitbucket Cloud REST API 2.0 (Swagger 2.0, as published by the vendor) — the vendor's complete API surface, preserved as-is. See `atlassian_bitbucket_cloud-latest.json` above for the curated subset if you just need common CRUD automation.
