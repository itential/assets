Microsoft Graph Mail is the Microsoft Graph API surface for sending email on behalf of a user in Microsoft 365 / Exchange Online.

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

### `microsoft_graph_mail-latest.json` (full spec, untouched)

Full, unmodified vendor spec (`x-vendor-api-version: 1.0`, 1 operation). This spec was hand-scoped to a single Microsoft Graph action — there is no separate admin, health-check, or introspection surface bundled in to exclude, so nothing was removed.

Operations included, by category:

- **Mail sending**: `POST /users/{user-id}/sendMail` — send a message on behalf of a user (optionally saving a copy to Sent Items)

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`microsoft_graph_mail-1.0.json`](./OpenAPIs/microsoft_graph_mail-1.0.json) | Full spec for Microsoft Graph Mail v1.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| Microsoft Graph Mail Integration Model | Import from the OpenAPI spec above to build automation against the Send Mail endpoint. |
