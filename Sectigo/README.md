# Sectigo

Sectigo is a digital certificate provider offering Sectigo Certificate Manager (SCM), a platform for issuing, renewing, revoking, and tracking SSL/TLS, client, code signing, and device certificates through public and private CAs.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`sectigo_certificate_manager-latest.json`](#sectigo_certificate_manager-latestjson)
  - [`sectigo_certificate_manager-25.11.json`](#sectigo_certificate_manager-2511json)
- [Studio Projects](#studio-projects)
  - [Sectigo Certificate Manager Project](#sectigo-certificate-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Sectigo Certificate Manager REST Enrollment API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Sectigo Certificate Manager](./Studio%20Projects/Sectigo%20Certificate%20Manager.project.json) | 7 workflows covering certificate enrollment and lifecycle automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Sectigo Certificate Manager | REST Enrollment API 25.11 |
| `Sectigo Certificate Manager` Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Sectigo Certificate Manager instance.

Authentication is OAuth 2.0 Client Credentials, backed by Sectigo's Keycloak authorization server:

```
Token URL: https://auth.sso.sectigo.com/auth/realms/apiclients/protocol/openid-connect/token
Grant Type: client_credentials
```

Generate a client ID and secret for your account in Sectigo Certificate Manager, then configure the integration instance's `authentication`/`server` properties like this:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-client-id>",
      "client_secret": "<your-client-secret>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<customer_uri>.enroll.<instance>.sectigo.com",
    "base_path": ""
  }
}
```

Replace `<customer_uri>` and `<instance>` with your assigned customer URI and instance (`enterprise`, `hard`, or `eu`).

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) | latest (curated) | 7 | Actively-maintained spec — see breakdown below |
| [`sectigo_certificate_manager-25.11.json`](./OpenAPIs/sectigo_certificate_manager-25.11.json) | 25.11 | 7 | Full spec for the Sectigo Certificate Manager REST Enrollment API (25.11) |

### `sectigo_certificate_manager-latest.json`

Actively-maintained spec (`x-vendor-api-version: 25.11`). Reviewed against the repo's common-CRUD-for-automation policy: the vendor's full REST Enrollment API surface (7 operations) is already common CRUD for automation, so it's carried through as `-latest` unchanged.

Resources included, by category:

- **Enroll Certificate**: Enroll, Download, Check Status, Initiate DCV Recheck
- **Manage Certificate**: Revoke, Renew, Replace

### `sectigo_certificate_manager-25.11.json`

Full, unmodified vendor spec for the Sectigo Certificate Manager REST Enrollment API (25.11, 7 operations) — the vendor's complete API surface, preserved as-is. See `sectigo_certificate_manager-latest.json` above for the curated (identical) subset.

## Studio Projects

### Sectigo Certificate Manager Project

Backed by the **`Sectigo Certificate Manager:latest`** Integration Model (see [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) above). The project contains **7 workflows** organized into **2 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Enroll Certificate | Enroll, Download, Check Status, Initiate DCV Recheck | Certificate enrollment and lookup |
| Manage Certificate | Revoke, Renew, Replace | Certificate lifecycle management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Sectigo Certificate Manager:latest` Integration Model | Import from [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) before importing the project |
| `Sectigo Certificate Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Sectigo Certificate Manager` — update the `adapter_id` value in each workflow task if yours is named differently |
