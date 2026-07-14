Okta is a cloud identity platform providing single sign-on, multi-factor authentication, lifecycle management, and identity governance for workforce and customer identities. This project covers Okta's Identity Governance API — entitlements, access grants, resource collections, access certification campaigns, access requests, and continuous security access reviews.

This project provides OpenAPI specs for automating against Okta's Identity Governance REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for governance automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`okta_management-latest.json`](#okta_management-latestjson)
  - [`okta_management-3.2.0.json`](#okta_management-320json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Okta Identity Governance REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Okta Identity Governance | 3.2.0 |
| Okta Management Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Okta org.

Authentication is an API token in the `Authorization` header, using the SSWS token format:

```
Authorization: SSWS <your-okta-api-token>
```

Generate a token in the Okta Admin Console under **Security → API → Tokens**.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`okta_management-latest.json`](./OpenAPIs/okta_management-latest.json) | latest (curated) | Trimmed to 65 of 162 upstream operations — see breakdown below |
| [`okta_management-3.2.0.json`](./OpenAPIs/okta_management-3.2.0.json) | 3.2.0 | Full spec for Okta Identity Governance 3.2.0 (162 operations). |

### `okta_management-latest.json`

Actively-maintained spec (`x-vendor-api-version: 3.2.0`). Trimmed to 65 of 162 upstream operations covering common CRUD for automation. The full upstream spec is Okta's Identity Governance API in its entirety; excluded areas are admin-configuration surfaces (request types, request conditions/sequences/settings, entitlement settings, org and certification settings, resource owners), risk scoring (risk rules and risk-rule assessments), job/task-queue polling, and personal ("my") self-service endpoints that duplicate an equivalent admin-level operation already covered.

Resources included, by category:

- **Entitlements**: Entitlements, Entitlement Values, Entitlement Bundles
- **Grants**: create, list, retrieve, replace, and update access grants
- **Collections**: resource collections, their principal assignments, and their resources
- **Labels**: Labels, and assigning/unassigning Labels to resources
- **Access Certification**: Campaigns (create, list, retrieve, delete, launch, end) and Reviews (list, retrieve, submit bulk review decisions)
- **Access Requests**: browse the default access request catalog, create/list/retrieve requests, and add request messages
- **Security Access Reviews**: create, list, retrieve, update, execute review actions (approve/deny), and add comments
- **Access Revocation**: revoke a principal's access

### `okta_management-3.2.0.json`

Full, unmodified vendor spec for Okta Identity Governance 3.2.0 (162 operations) — the vendor's complete API surface, preserved as-is. See `okta_management-latest.json` above for the curated subset if you just need common CRUD automation.
