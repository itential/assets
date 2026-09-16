# Sectigo

Sectigo is a digital certificate provider offering Sectigo Certificate Manager (SCM), a platform for issuing, renewing, revoking, and tracking SSL/TLS, client, code signing, device, and Mark certificates through public and private CAs, plus account administration (administrators, organizations, domains, persons, ACME accounts, and more). SCM exposes this functionality as two genuinely separate REST APIs on two different hosts: the **REST Enrollment API**, scoped to certificate enrollment/lifecycle actions a customer's own systems perform, and the **SCM Admin API**, scoped to account and access administration plus full certificate management across the org.

This project provides a Studio Project of workflows covering both APIs, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Sectigo](#sectigo)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
  - [OpenAPIs](#openapis)
    - [`sectigo_certificate_manager-latest.json`](#sectigo_certificate_manager-latestjson)
    - [`sectigo_certificate_manager-25.11.json`](#sectigo_certificate_manager-2511json)
    - [`sectigo_scm_admin-latest.json`](#sectigo_scm_admin-latestjson)
    - [`sectigo_scm_admin-26.7.json`](#sectigo_scm_admin-267json)
  - [Studio Projects](#studio-projects)
    - [Sectigo Project](#sectigo-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Two peer specs — `sectigo_certificate_manager-latest.json` (REST Enrollment API) and `sectigo_scm_admin-latest.json` (SCM Admin API) — plus their full dated counterparts |
| [Studio Projects/Sectigo](./Studio%20Projects/Sectigo.project.json) | 229 workflows covering certificate enrollment/lifecycle and SCM Admin API automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Sectigo Certificate Manager | REST Enrollment API 25.11; SCM Admin API 26.7 |
| `Sectigo Certificate Manager:latest` Integration Model | Required to build automation against the REST Enrollment API spec |
| `Sectigo SCM Admin:latest` Integration Model | Required to build automation against the SCM Admin API spec |

## Integration Configuration

Import both OpenAPI specs from `OpenAPIs/` as separate Integration Models in **Admin > Integrations**, then create one integration instance per model — each API lives on its own host, and an Itential Platform integration instance can only ever point at a single host, so a single combined instance cannot serve both.

Authentication is OAuth 2.0 Client Credentials, backed by Sectigo's Keycloak authorization server (shared by both the REST Enrollment API and the SCM Admin API):

```
Token URL: https://auth.sso.sectigo.com/auth/realms/apiclients/protocol/openid-connect/token
Grant Type: client_credentials
```

Generate a client ID and secret for your account in Sectigo Certificate Manager, then configure each integration instance's `authentication`/`server` properties like this:

REST Enrollment API:
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

SCM Admin API:
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
    "host": "admin.<instance>.sectigo.com",
    "base_path": ""
  }
}
```

Replace `<customer_uri>` and `<instance>` with your assigned customer URI and instance (`enterprise`, `hard`, or `eu`) — note the Admin host has no `customer_uri` segment.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) | latest (curated) | 7 | Curated spec for the REST Enrollment API — see breakdown below |
| [`sectigo_certificate_manager-25.11.json`](./OpenAPIs/sectigo_certificate_manager-25.11.json) | 25.11 | 7 | Full spec for the Sectigo Certificate Manager REST Enrollment API (25.11) |
| [`sectigo_scm_admin-latest.json`](./OpenAPIs/sectigo_scm_admin-latest.json) | latest (curated) | 222 | Curated spec for the SCM Admin API — see breakdown below |
| [`sectigo_scm_admin-26.7.json`](./OpenAPIs/sectigo_scm_admin-26.7.json) | 26.7 | 308 | Full spec for the Sectigo SCM Admin API (26.7) |

### `sectigo_certificate_manager-latest.json`

Curated spec (`x-vendor-api-version: REST Enrollment API 25.11`) for the REST Enrollment API — every operation the vendor's Enrollment surface exposes, reviewed against the repo's common-CRUD-for-automation policy (nothing was excluded; the full surface is only 7 operations).

Resources included, by category:

- **Enroll Certificate**: Enroll, Download, Check Status, Initiate DCV Recheck
- **Manage Certificate**: Revoke, Renew, Replace

### `sectigo_certificate_manager-25.11.json`

Full, unmodified vendor spec for the Sectigo Certificate Manager REST Enrollment API (25.11, 7 operations) — the vendor's complete API surface for enrollment, preserved as-is. Identical in content to `sectigo_certificate_manager-latest.json` since no operations were excluded.

### `sectigo_scm_admin-latest.json`

Curated spec (`x-vendor-api-version: SCM Admin API 26.7`) for the SCM Admin API. Trimmed to 222 of 308 upstream operations, reviewed against the repo's common-CRUD-for-automation policy.

Resources included, by category:

- **SSL Certificates** (28): list/get/update/delete, enroll (with and without keygen), collect, decline/approve, revoke (by ID, by serial number, mark-as-revoked), replace, renew (by ID, by renew ID, mark-as-renewed), DCV info/recheck, locations, profiles, custom fields
- **Client Certificates** (25): list/get/update/delete, enroll, collect (by ID, by backend cert ID), list by person (ID or email), revoke (by cert ID, serial number, backend cert ID, by email, mark-as-revoked), renew (by serial number, by backend cert ID), download as P12, locations, profiles, custom fields
- **Device Certificates** (22): list/get/update/delete, enroll, collect, decline/approve, revoke (by serial number, by ID, mark-as-revoked), replace, renew (by serial number, by ID), locations, profiles, custom fields
- **Code Signing Certificates** (2): mark-as-revoked
- **Mark Certificates** (10): get details, enroll, DCV info/recheck, revoke, decline/approve, collect, update, list
- **Domains** (12): list/get/create/delete, suspend/activate, CT log monitoring, delegate/remove delegation
- **Domain Control Validation** (18): start + submit for TXT, CNAME, HTTP, HTTPS, and Email DCV methods; get status, sync, clear, delete, list all
- **Organizations** (7): list/get/create/update/delete, list by certificate type, list by role
- **Organization Validations** (9): get details, list, submit, re-submit, sync, reset-and-remove, external validation assignment
- **Persons** (10): find by ID/email, update, delete, list, create
- **Enrollment Endpoints** (9): list/get/create/update/delete, delegations, configuration
- **Enrollment Endpoint Accounts** (5): list/get/create/update/delete, plus send-invitation
- **Administrators** (13): get/update/delete/list/create, change password, get available roles/privileges, password state, identity providers, email confirmation
- **IdP Templates** (5): list/get/create/update/delete
- **Custom Fields** (5): list/get/create/update/delete
- **Notifications** (5): list/get-types/create/update/delete
- **Access Control Lists** (5): list/get/create/update/delete
- **Profiles** (2): list, get details
- **DNS Connectors** (3): list, get details, list providers
- **Azure Accounts** (9): list/get/create/update/delete, check, vaults, resource groups, delegate organizations
- **ACME Public Accounts** (11): list servers, list/get/create/update/delete accounts, deactivate client, domains (list/add/remove), list clients
- **ACME Universal Accounts** (7): list/get/create/update/delete accounts, deactivate client, list clients

Excluded (86 of 308 operations): network/MS AD/Azure Key Vault discovery-scanning tasks and their agents, discovery operations, assignment rules (dependent on discovery), certificate buckets, the Orchestration Gateway and its keystores/automation endpoints, reports (all types), and usage statistics — these are deep scanning/orchestration-tooling configuration and reporting surfaces rather than core certificate/organization/domain/admin CRUD for automation.

### `sectigo_scm_admin-26.7.json`

Full, unmodified vendor spec for the Sectigo SCM Admin API (26.7, 308 operations), assembled from Sectigo's per-operation reference documentation at `scm.devx.sectigo.com` (each reference page embeds that operation's OpenAPI definition) — the vendor's complete Admin API surface, preserved as-is. See `sectigo_scm_admin-latest.json` above for the curated subset.

## Studio Projects

### Sectigo Project

Backed by both Integration Models above — enrollment/lifecycle workflows use **`Sectigo Certificate Manager:latest`**, all other workflows use **`Sectigo SCM Admin:latest`** (see [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) and [`sectigo_scm_admin-latest.json`](./OpenAPIs/sectigo_scm_admin-latest.json) above). The project contains **229 workflows** organized into **24 folders**, one atomic workflow per curated operation.

#### Folder Structure

| Folder | Workflows | Model | Scope |
|---|---|---|---|
| Enroll Certificate | 4 | Sectigo Certificate Manager | Certificate enrollment and lookup |
| Manage Certificate | 3 | Sectigo Certificate Manager | Certificate lifecycle management |
| SSL Certificates | 28 | Sectigo SCM Admin | Full SSL certificate lifecycle, locations, profiles, custom fields |
| Client Certificates | 25 | Sectigo SCM Admin | Full client certificate lifecycle, locations, profiles, custom fields |
| Device Certificates | 22 | Sectigo SCM Admin | Full device certificate lifecycle, locations, profiles, custom fields |
| Code Signing Certificates | 2 | Sectigo SCM Admin | Manual revocation |
| Mark Certificates | 10 | Sectigo SCM Admin | Full Mark certificate lifecycle |
| Domains | 12 | Sectigo SCM Admin | Domain CRUD, suspend/activate, CT log monitoring, delegation |
| Domain Control Validation | 18 | Sectigo SCM Admin | TXT/CNAME/HTTP/HTTPS/Email DCV start+submit, status, sync, clear, delete |
| Organizations | 7 | Sectigo SCM Admin | Organization CRUD and lookups |
| Organization Validations | 9 | Sectigo SCM Admin | Organization validation lifecycle |
| Persons | 10 | Sectigo SCM Admin | Person CRUD and lookups |
| Enrollment Endpoints | 9 | Sectigo SCM Admin | Enrollment endpoint CRUD, delegations, configuration |
| Enrollment Endpoint Accounts | 5 | Sectigo SCM Admin | Enrollment endpoint account CRUD, invitations |
| Administrators | 13 | Sectigo SCM Admin | Administrator account CRUD, password/role management |
| IdP Templates | 5 | Sectigo SCM Admin | IdP administrator template CRUD |
| Custom Fields | 5 | Sectigo SCM Admin | Custom field CRUD |
| Notifications | 5 | Sectigo SCM Admin | Notification CRUD |
| Access Control Lists | 5 | Sectigo SCM Admin | ACL entry CRUD |
| Profiles | 2 | Sectigo SCM Admin | Certificate profile lookups |
| DNS Connectors | 3 | Sectigo SCM Admin | DNS connector and provider lookups |
| Azure Accounts | 9 | Sectigo SCM Admin | Azure Key Vault storage account CRUD |
| ACME Public Accounts | 11 | Sectigo SCM Admin | Public ACME server/account/domain/client management |
| ACME Universal Accounts | 7 | Sectigo SCM Admin | Universal ACME account/client management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Sectigo Certificate Manager:latest` Integration Model | Import from [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) before importing the project |
| `Sectigo SCM Admin:latest` Integration Model | Import from [`sectigo_scm_admin-latest.json`](./OpenAPIs/sectigo_scm_admin-latest.json) before importing the project |
| `Sectigo Certificate Manager` integration instance | Create in **Admin > Integrations** with the REST Enrollment API connection properties above. Workflows in the Enroll Certificate and Manage Certificate folders are wired to an instance named `Sectigo Certificate Manager` — update `adapter_id` in each task if yours is named differently |
| `Sectigo SCM Admin` integration instance | Create with the SCM Admin API connection properties above. All other workflows are wired to an instance named `Sectigo SCM Admin` — update `adapter_id` in each task if yours is named differently |
