Atlassian Confluence Server and Data Center is the self-hosted version of Confluence, a team workspace and wiki for creating, organizing, and collaborating on pages, blog posts, and attachments organized into spaces.

This project provides OpenAPI specs for automating against the Confluence Server/Data Center REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`atlassian_confluence_server_data_center-latest.json`](#atlassian_confluence_server_data_center-latestjson)
  - [`atlassian_confluence_server_data_center-9.0.0.json`](#atlassian_confluence_server_data_center-900json)
- [Studio Projects](#studio-projects)
  - [Atlassian Confluence Server — Data Center Project](#atlassian-confluence-server--data-center-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Confluence Server & Data Center REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Atlassian Confluence Server — Data Center](./Studio%20Projects/Atlassian%20Confluence%20Server%20%E2%80%94%20Data%20Center.project.json) | 22 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Confluence Server / Data Center | 9.0.0 (see OpenAPIs below for the exact spec version available) |
| Confluence Server & Data Center Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Confluence Server or Data Center instance.

Authentication is HTTP Basic — a Confluence username and password, or a personal access token generated under **Profile > Personal Access Tokens** (Confluence 7.9+), Base64-encoded in the `Authorization` header:

```
Authorization: Basic <base64(username:password_or_token)>
```

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
    "host": "example.com:7990",
    "base_path": "/confluence"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`atlassian_confluence_server_data_center-latest.json`](./OpenAPIs/atlassian_confluence_server_data_center-latest.json) | latest (curated) | 74 | Trimmed to 74 of 111 upstream operations — see breakdown below |
| [`atlassian_confluence_server_data_center-9.0.0.json`](./OpenAPIs/atlassian_confluence_server_data_center-9.0.0.json) | 9.0.0 | 111 | Full spec for Confluence Server & Data Center 9.0.0. |

### `atlassian_confluence_server_data_center-latest.json`

Actively-maintained spec (`x-vendor-api-version: 9.0.0`). Trimmed to 74 of 111 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Content**: Get/create/update/delete content (pages, blog posts), search content via CQL, history, versions, children, descendants
- **Content Metadata**: Labels, properties, restrictions, watchers, body representation conversion
- **Attachments**: Get, create, update (binary and non-binary), move, and remove attachments and attachment versions
- **Spaces**: Get/create/update/delete/archive/restore spaces, contents in a space
- **Space Metadata**: Labels, properties, watchers
- **Users & Groups**: Look up users, groups, and group membership; current user info
- **Watch Subscriptions**: Add/remove/check a user's watch on content or a space
- **Search**: Global entity search

Excluded (not part of this curated spec): Confluence administration (user/group create-delete-enable-disable), backup and restore jobs, webhook management, long-running task queue, access mode, and content blueprint publishing. Pull the full spec below if you need one of those areas.

### `atlassian_confluence_server_data_center-9.0.0.json`

Full, unmodified vendor spec for Confluence Server & Data Center 9.0.0 (111 operations) — the vendor's complete API surface, preserved as-is. See `atlassian_confluence_server_data_center-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### Atlassian Confluence Server — Data Center Project

Backed by the **`Atlassian Confluence Server — Data Center:latest`** Integration Model (see [`atlassian_confluence_server_data_center-latest.json`](./OpenAPIs/atlassian_confluence_server_data_center-latest.json) above). The project contains **22 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Content | List, Create, Get, Update, Delete Content | Page/blog post content lifecycle |
| Spaces | List, Create, Get, Update, Delete Space | Space lifecycle |
| Attachments | List, Create, Update, Delete Attachment | Attachment lifecycle |
| Content Labels | List, Add, Delete Label | Content label management |
| Content Properties | List, Create, Get, Update, Delete Property | Content metadata key/value properties |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Atlassian Confluence Server — Data Center:latest` Integration Model | Import from [`atlassian_confluence_server_data_center-latest.json`](./OpenAPIs/atlassian_confluence_server_data_center-latest.json) before importing the project |
| `Atlassian Confluence Server — Data Center` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Atlassian Confluence Server — Data Center` — update the `adapter_id` value in each workflow task if yours is named differently |
