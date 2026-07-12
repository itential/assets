Cisco PSIRT openVuln API provides programmatic access to Cisco security vulnerability information, including CVEs, security advisories, affected products, severity ratings, and remediation details.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco PSIRT openVuln API OpenAPI specs — `-latest` plus full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco PSIRT openVuln API | 2.0.1 |
| Cisco PSIRT openVuln API Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the Cisco PSIRT openVuln API.

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Register an app at https://apiconsole.cisco.com with openVuln API access, then obtain a token via OAuth2 client credentials from `POST https://id.cisco.com/oauth2/default/v1/token`.

## OpenAPIs

### `cisco_psirt_openvuln-latest.json`

Full spec, left untouched — the API is already a narrow, single-purpose read-only vulnerability lookup service (advisories, CVEs, bug IDs, severity, affected products/platforms), so no trimming was needed.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`cisco_psirt_openvuln-2.0.1.json`](./OpenAPIs/cisco_psirt_openvuln-2.0.1.json) | Full spec for Cisco PSIRT openVuln API 2.0.1. |

## Dependencies

| Dependency | Notes |
|---|---|
| Cisco PSIRT openVuln API Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
