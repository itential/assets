1Password is a password manager and secrets management platform. 1Password Connect is its self-hosted REST API server, providing programmatic access to 1Password vaults for retrieving, creating, and managing secrets and items from automated systems.

This project provides an OpenAPI spec for automating against the 1Password Connect REST API via an Integration Model. The `-latest` spec is the full vendor spec — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | 1Password Connect REST API OpenAPI spec — curated `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| 1Password Connect | 1.5.7 |
| 1Password Connect Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your 1Password Connect server.

Authentication is an API key (bearer token) in the `Authorization` header:

```
Authorization: Bearer <token>
```

Generate a 1Password Connect token when deploying a Connect server. See https://developer.1password.com/docs/connect for details.

## OpenAPIs

### `1password_connect-latest.json` (full spec)

Actively-maintained spec (`x-vendor-api-version: 1.5.7`). This is 1Password Connect's complete API surface, already scoped to a single purpose — vault and secret management — so it is carried through untrimmed. It covers vaults, items, item files, and server health/activity endpoints.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`1password_connect-1.5.7.json`](./OpenAPIs/1password_connect-1.5.7.json) | Full spec for 1Password Connect 1.5.7. |

## Dependencies

| Dependency | Notes |
|---|---|
| 1Password Connect Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
| 1Password Connect server | Self-hosted Connect server deployment required to serve the API; see 1Password documentation. |
