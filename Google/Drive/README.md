Google Drive is a cloud file storage and collaboration service — files and folders, Shared Drives, permissions/sharing, comments, and revision history, accessible over a REST API.

This project provides OpenAPI specs for automating against the Google Drive REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`google_drive-latest.json`](#google_drive-latestjson)
  - [`google_drive-v3.json`](#google_drive-v3json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Google Drive REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Google Drive API | v3 |
| Google Drive Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at `https://www.googleapis.com/drive/v3`.

Authentication is a Google OAuth2 access token, sent as a Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Obtain an access token via the Google Cloud Console → **Service Accounts**, granted a Drive API OAuth scope (e.g. `https://www.googleapis.com/auth/drive`), using the `client_credentials` flow for a service account or a delegated-user OAuth2 authorization-code flow.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`google_drive-latest.json`](./OpenAPIs/google_drive-latest.json) | latest (curated) | Actively-maintained spec, trimmed to 35 of 48 upstream operations — see breakdown below |
| [`google_drive-v3.json`](./OpenAPIs/google_drive-v3.json) | v3 | Full spec for the Google Drive v3 API (48 operations) |

### `google_drive-latest.json`

Actively-maintained spec (`x-vendor-api-version: v3`). Trimmed to 35 of 48 upstream operations covering common CRUD for automation.

Resources included, by category:

- **About**: Get user/storage info
- **Files**: List, Create, Get, Update, Delete, Copy, Export, Empty Trash
- **Shared Drives**: List, Create, Get, Update, Delete, Hide, Unhide
- **Permissions**: List, Create, Get, Update, Delete
- **Comments**: List, Create, Get, Update, Delete
- **Replies**: List, Create, Get, Update, Delete
- **Revisions**: List, Get, Update, Delete

Not included: change/activity polling and push-notification channels (`changes`, `channels` — sync-client tooling), the legacy `teamdrives` resource (superseded by `drives`), file ID pre-generation (`files.generateIds`), file watch/push notifications (`files.watch`), and the Drive Labels endpoints (`files.listLabels`, `files.modifyLabels` — a separate, optional Google Workspace add-on).

### `google_drive-v3.json`

Full, unmodified vendor spec for the Google Drive v3 API (48 operations) — the vendor's complete API surface, preserved as-is. See `google_drive-latest.json` above for the curated subset if you just need common CRUD automation.
