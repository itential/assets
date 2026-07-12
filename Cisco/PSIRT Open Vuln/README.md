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

### `cisco_psirt_openvuln-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2.0.1`, 30 operations). Every operation is a read-only lookup against Cisco security advisory/CVE/vulnerability data — the product's only business resource — so there is no separate admin, health, or self-introspection surface to exclude. Nothing was removed.

Operations included, by category:

- **All advisories (JSON)**: List all advisories; filter by first-published date range; filter by last-published date range
- **Advisory lookup (JSON)**: Get by advisory ID; get by CVE ID; get by bug ID; get the latest N advisories; get all advisories published in a given year
- **Advisories by severity (JSON)**: Get by severity rating (critical/high/medium/low); filtered by first-published date range; filtered by last-published date range
- **Advisories by product/platform (JSON)**: Get by product name; get by affected network OS type; get by IOS version; get by IOS-XE version; get by ACI version; get by NX-OS version
- **Reference data (network OS/platform versions)**: OS version reference data; platform type reference data; NOS version reference data
- **All advisories (CVRF format)**: List all advisories; filter by first-published date range; filter by last-published date range
- **Advisory lookup (CVRF format)**: Get by advisory ID; get by CVE ID; get by product name; get all advisories published in a given year
- **Advisories by severity (CVRF format)**: Get by severity rating; filtered by first-published date range; filtered by last-published date range

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`cisco_psirt_openvuln-2.0.1.json`](./OpenAPIs/cisco_psirt_openvuln-2.0.1.json) | Full spec for Cisco PSIRT openVuln API 2.0.1. |

## Dependencies

| Dependency | Notes |
|---|---|
| Cisco PSIRT openVuln API Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
