Microsoft Graph Mail is the Microsoft Graph API surface for sending email on behalf of a user in Microsoft 365 / Exchange Online.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`microsoft_graph_mail-latest.json`](#microsoft_graph_mail-latestjson)
  - [`microsoft_graph_mail-1.0.json`](#microsoft_graph_mail-10json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Microsoft Graph Mail OpenAPI spec — `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Microsoft Graph API | v1.0 |
| Microsoft Graph Mail Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Microsoft Graph tenant.

Authentication is an OAuth2 bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Obtain a token via the OAuth2 client credentials grant: `POST https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token` with `client_id`, `client_secret`, and `scope=https://graph.microsoft.com/.default`.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`microsoft_graph_mail-latest.json`](./OpenAPIs/microsoft_graph_mail-latest.json) | latest (curated) | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`microsoft_graph_mail-1.0.json`](./OpenAPIs/microsoft_graph_mail-1.0.json) | 1.0 | Full spec for Microsoft Graph Mail v1.0. |

### `microsoft_graph_mail-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 1.0`, 1 operation). This spec was hand-scoped to a single Microsoft Graph action — there is no separate admin, health-check, or introspection surface bundled in to exclude, so nothing was removed.

Operations included, by category:

- **Mail sending**: `POST /users/{user-id}/sendMail` — send a message on behalf of a user (optionally saving a copy to Sent Items)

### `microsoft_graph_mail-1.0.json`

Full, unmodified vendor spec for Microsoft Graph Mail v1.0 — the vendor's complete API surface, preserved as-is. See `microsoft_graph_mail-latest.json` above for the curated subset if you just need common CRUD automation.
