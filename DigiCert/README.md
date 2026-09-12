# DigiCert

DigiCert is a digital trust provider offering certificate lifecycle management for TLS/SSL, PKI, IoT/device identity, and code signing. This project covers the DigiCert ONE platform's Trust Lifecycle Manager service, which manages certificate enrollment, issuance, and lifecycle for users and devices.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`digicert_trust_lifecycle_manager-latest.json`](#digicert_trust_lifecycle_manager-latestjson)
  - [`digicert_trust_lifecycle_manager-1.0.0.json`](#digicert_trust_lifecycle_manager-100json)
- [Studio Projects](#studio-projects)
  - [DigiCert Trust Lifecycle Manager Project](#digicert-trust-lifecycle-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | DigiCert Trust Lifecycle Manager REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/DigiCert Trust Lifecycle Manager](./Studio%20Projects/DigiCert%20Trust%20Lifecycle%20Manager.project.json) | 34 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| DigiCert ONE / Trust Lifecycle Manager | v1 |
| `DigiCert Trust Lifecycle Manager` Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your DigiCert ONE instance.

Authentication is a static API key in the `X-API-Key` header:

```
X-API-Key: <your-digicert-one-api-token>
```

Generate a Service User API token in the DigiCert ONE **Account Manager**, under **Access > Service User**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "ApiKeyAuth": {
      "value": "<your-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "one.digicert.com",
    "base_path": ""
  }
}
```

Replace `one.digicert.com` with your own DigiCert ONE hostname if you're not using the hosted cloud instance.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`digicert_trust_lifecycle_manager-latest.json`](./OpenAPIs/digicert_trust_lifecycle_manager-latest.json) | latest (curated) | 34 | Actively-maintained spec, trimmed to 34 of 161 upstream operations — see breakdown below |
| [`digicert_trust_lifecycle_manager-1.0.0.json`](./OpenAPIs/digicert_trust_lifecycle_manager-1.0.0.json) | 1.0.0 | 161 | Full spec for DigiCert Trust Lifecycle Manager REST API v1 (161 operations) |

### `digicert_trust_lifecycle_manager-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 34 of 161 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Certificates**: Issue, Get, Renew, Revoke, Get Additional Formats
- **Certificate Search**: Search, Get Summary, Get Result
- **Enrollments**: Create, List Details, Get Details, Get By Code, Redeem, Update Status, Get By Certificate
- **Business Units**: List, Create, Get, Delete
- **Seats**: List, Create, Get, Update, Delete, List Seat Types
- **Certificate Profiles**: List, Create, Get, Update
- **Certificate Owners**: List, Create, Get, Update, Delete

### `digicert_trust_lifecycle_manager-1.0.0.json`

Full, unmodified vendor spec for the DigiCert Trust Lifecycle Manager REST API v1 (161 operations) — the vendor's complete API surface, preserved as-is. See `digicert_trust_lifecycle_manager-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### DigiCert Trust Lifecycle Manager Project

Backed by the **`DigiCert Trust Lifecycle Manager:latest`** Integration Model (see [`digicert_trust_lifecycle_manager-latest.json`](./OpenAPIs/digicert_trust_lifecycle_manager-latest.json) above). The project contains **34 workflows** organized into **7 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Certificates | Issue, Get, Renew, Revoke Certificate, Get Additional Formats | Certificate lifecycle |
| Certificate Search | Search Certificates, Get Search Summary, Get Search Result | Certificate lookup |
| Enrollments | Create, List/Get Details, Get By Code, Redeem, Update Status, Get By Certificate | Enrollment lifecycle |
| Business Units | List, Create, Get, Delete Business Unit | Business unit CRUD |
| Seats | List, Create, Get, Update, Delete Seat, List Seat Types | Seat CRUD |
| Certificate Profiles | List, Create, Get, Update Profile | Certificate profile CRUD |
| Certificate Owners | List, Create, Get, Update, Delete Certificate Owner | Certificate owner CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `DigiCert Trust Lifecycle Manager:latest` Integration Model | Import from [`digicert_trust_lifecycle_manager-latest.json`](./OpenAPIs/digicert_trust_lifecycle_manager-latest.json) before importing the project |
| `DigiCert Trust Lifecycle Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `DigiCert Trust Lifecycle Manager` — update the `adapter_id` value in each workflow task if yours is named differently |
