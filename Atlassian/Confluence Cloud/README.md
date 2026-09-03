Confluence Cloud is Atlassian's team workspace and content collaboration product — pages, blog posts, spaces, comments, labels, and attachments for documenting and organizing team knowledge.

This project provides OpenAPI specs for automating against Confluence Cloud's REST API v2 via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`atlassian_confluence_cloud-latest.json`](#atlassian_confluence_cloud-latestjson)
  - [`atlassian_confluence_cloud-1.0.0.json`](#atlassian_confluence_cloud-100json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Confluence Cloud REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Confluence Cloud | REST API v2 (`x-vendor-api-version: 2.0.0`) |
| Confluence Cloud Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Confluence Cloud site (`https://<your-site>.atlassian.net/wiki/api/v2`).

Authentication is HTTP Basic, using your Atlassian account email as the username and an API token as the password:

```
Authorization: Basic base64(<your-email>:<your-api-token>)
```

Generate an API token at https://id.atlassian.com/manage-profile/security/api-tokens.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "no-default",
    "base_path": "/wiki/api/v2"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`atlassian_confluence_cloud-latest.json`](./OpenAPIs/atlassian_confluence_cloud-latest.json) | latest (curated) | 104 | Actively-maintained spec, trimmed to 104 of 172 upstream operations covering common CRUD for automation — see breakdown below |
| [`atlassian_confluence_cloud-1.0.0.json`](./OpenAPIs/atlassian_confluence_cloud-1.0.0.json) | 1.0.0 | 174 | Full spec for Confluence Cloud REST API v1 |

### `atlassian_confluence_cloud-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0.0`). Trimmed to 104 of 172 upstream operations covering common CRUD for automation. Pull the full v2 spec from Atlassian's [Confluence Cloud REST API v2 docs](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/) if you need something not covered here.

Resources included, by category:

- **Content**: Pages, Blog Posts, Custom Content — create/read/update/delete, children, ancestors, attachments, versions
- **Attachments**: List, get, delete, versions
- **Comments**: Footer Comments, Inline Comments — create/read/update/delete, children, versions
- **Labels**: List labels, and labels for attachments, blog posts, pages, and spaces
- **Spaces**: List, get, and list a space's pages, blog posts, custom content, and labels
- **Content Properties**: Metadata key/value properties on pages, blog posts, attachments, custom content, spaces, and comments
- **Tasks**: List, get, update

Also removed 104 redundant per-operation `security` overrides that all duplicated the single `basicAuth` scheme, and promoted that scheme to a single top-level `security` block.

### `atlassian_confluence_cloud-1.0.0.json`

Full, unmodified vendor spec for Confluence Cloud REST API v1 (174 operations) — the vendor's complete API surface, preserved as-is. See `atlassian_confluence_cloud-latest.json` above for the curated v2 subset if you just need common CRUD automation.
