1Password is a password manager and secrets management platform. 1Password Connect is its self-hosted REST API server, providing programmatic access to 1Password vaults for retrieving, creating, and managing secrets and items from automated systems.

This project provides an OpenAPI spec for automating against the 1Password Connect REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for secrets automation — see **OpenAPIs** below.

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

| Spec | Version | Description |
|---|---|---|
| [`1password_connect-latest.json`](./OpenAPIs/1password_connect-latest.json) | latest (curated) | Actively-maintained spec, trimmed to 12 of 16 upstream operations — see breakdown below |
| [`1password_connect-1.5.7.json`](./OpenAPIs/1password_connect-1.5.7.json) | 1.5.7 | Full, unmodified vendor spec |

### `1password_connect-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.5.7`). Trimmed to 12 of 16 upstream operations covering common CRUD for secrets automation. Excludes server activity/health/heartbeat/metrics endpoints (operational monitoring, not secrets automation). Also consolidated a redundant per-operation auth override into a single global `security` block.

Resources included, by category:

- **Vaults**: List, get
- **Items**: List, create, get, update, delete
- **Item Files**: List, get, get content

## Dependencies

| Dependency | Notes |
|---|---|
| 1Password Connect Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
| 1Password Connect server | Self-hosted Connect server deployment required to serve the API; see 1Password documentation. |
