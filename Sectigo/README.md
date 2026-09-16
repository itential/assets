# Sectigo

Sectigo is a digital certificate provider offering Sectigo Certificate Manager (SCM), a platform for issuing, renewing, revoking, and tracking SSL/TLS, client, code signing, device, and Mark certificates through public and private CAs, plus account administration (administrators, organizations, domains, persons, ACME accounts, and more).

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`sectigo_certificate_manager-latest.json`](#sectigo_certificate_manager-latestjson)
  - [`sectigo_certificate_manager-25.11.json`](#sectigo_certificate_manager-2511json)
  - [`sectigo_certificate_manager_admin_api-26.7.json`](#sectigo_certificate_manager_admin_api-267json)
- [Studio Projects](#studio-projects)
  - [Sectigo Certificate Manager Project](#sectigo-certificate-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Sectigo Certificate Manager REST Enrollment API and SCM Admin API OpenAPI specs — curated `-latest` plus the full dated specs |
| [Studio Projects/Sectigo Certificate Manager](./Studio%20Projects/Sectigo%20Certificate%20Manager.project.json) | 229 workflows covering certificate enrollment/lifecycle and SCM Admin API automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Sectigo Certificate Manager | REST Enrollment API 25.11; SCM Admin API 26.7 |
| `Sectigo Certificate Manager` Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Sectigo Certificate Manager instance.

Authentication is OAuth 2.0 Client Credentials, backed by Sectigo's Keycloak authorization server (shared by both the REST Enrollment API and the SCM Admin API):

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

The REST Enrollment API and the SCM Admin API sit on genuinely different hosts (`<customer_uri>.enroll.<instance>.sectigo.com` vs. `admin.<instance>.sectigo.com` — the latter has no `customer_uri`), so both server URLs are documented in the spec's `servers` block, but only one can be the active `host` on a given integration instance at a time. To automate against both areas, create two integration instances from the same Integration Model — one with the Enrollment host, one with the Admin host — and point each workflow's `adapter_id` at the matching instance.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) | latest (curated) | 229 | Actively-maintained spec — see breakdown below |
| [`sectigo_certificate_manager-25.11.json`](./OpenAPIs/sectigo_certificate_manager-25.11.json) | 25.11 | 7 | Full spec for the Sectigo Certificate Manager REST Enrollment API (25.11) |
| [`sectigo_certificate_manager_admin_api-26.7.json`](./OpenAPIs/sectigo_certificate_manager_admin_api-26.7.json) | 26.7 | 308 | Full spec for the Sectigo SCM Admin API (26.7) |

### `sectigo_certificate_manager-latest.json`

Actively-maintained spec (`x-vendor-api-version: REST Enrollment API 25.11; SCM Admin API 26.7`), merging both vendor API surfaces behind a single shared `oauth2ClientCredentials` security scheme. Trimmed to 229 of 315 combined upstream operations (7 of 7 REST Enrollment API + 222 of 308 SCM Admin API), reviewed against the repo's common-CRUD-for-automation policy.

Resources included, by category:

- **Enroll Certificate**: Enroll, Download, Check Status, Initiate DCV Recheck (REST Enrollment API)
- **Manage Certificate**: Revoke, Renew, Replace (REST Enrollment API)
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

Excluded (86 of 308 SCM Admin API operations): Network/MS AD/Azure Key Vault discovery-scanning tasks and their agents, discovery operations, assignment rules (dependent on discovery), certificate buckets, the Orchestration Gateway and its keystores/automation endpoints, reports (all types), and usage statistics — these are deep scanning/orchestration-tooling configuration and reporting surfaces rather than core certificate/organization/domain/admin CRUD for automation.

### `sectigo_certificate_manager-25.11.json`

Full, unmodified vendor spec for the Sectigo Certificate Manager REST Enrollment API (25.11, 7 operations) — the vendor's complete API surface for enrollment, preserved as-is.

### `sectigo_certificate_manager_admin_api-26.7.json`

Full, unmodified vendor spec for the Sectigo SCM Admin API (26.7, 308 operations), assembled from Sectigo's per-operation reference documentation at `scm.devx.sectigo.com` (each reference page embeds that operation's OpenAPI definition) — the vendor's complete Admin API surface, preserved as-is. See `sectigo_certificate_manager-latest.json` above for the curated subset merged with the Enrollment API.

## Studio Projects

### Sectigo Certificate Manager Project

Backed by the **`Sectigo Certificate Manager:latest`** Integration Model (see [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) above). The project contains **229 workflows** organized into **24 folders**, one atomic workflow per curated operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Enroll Certificate | 4 | Certificate enrollment and lookup (REST Enrollment API) |
| Manage Certificate | 3 | Certificate lifecycle management (REST Enrollment API) |
| SSL Certificates | 28 | Full SSL certificate lifecycle, locations, profiles, custom fields |
| Client Certificates | 25 | Full client certificate lifecycle, locations, profiles, custom fields |
| Device Certificates | 22 | Full device certificate lifecycle, locations, profiles, custom fields |
| Code Signing Certificates | 2 | Manual revocation |
| Mark Certificates | 10 | Full Mark certificate lifecycle |
| Domains | 12 | Domain CRUD, suspend/activate, CT log monitoring, delegation |
| Domain Control Validation | 18 | TXT/CNAME/HTTP/HTTPS/Email DCV start+submit, status, sync, clear, delete |
| Organizations | 7 | Organization CRUD and lookups |
| Organization Validations | 9 | Organization validation lifecycle |
| Persons | 10 | Person CRUD and lookups |
| Enrollment Endpoints | 9 | Enrollment endpoint CRUD, delegations, configuration |
| Enrollment Endpoint Accounts | 5 | Enrollment endpoint account CRUD, invitations |
| Administrators | 13 | Administrator account CRUD, password/role management |
| IdP Templates | 5 | IdP administrator template CRUD |
| Custom Fields | 5 | Custom field CRUD |
| Notifications | 5 | Notification CRUD |
| Access Control Lists | 5 | ACL entry CRUD |
| Profiles | 2 | Certificate profile lookups |
| DNS Connectors | 3 | DNS connector and provider lookups |
| Azure Accounts | 9 | Azure Key Vault storage account CRUD |
| ACME Public Accounts | 11 | Public ACME server/account/domain/client management |
| ACME Universal Accounts | 7 | Universal ACME account/client management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Sectigo Certificate Manager:latest` Integration Model | Import from [`sectigo_certificate_manager-latest.json`](./OpenAPIs/sectigo_certificate_manager-latest.json) before importing the project |
| `Sectigo Certificate Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Sectigo Certificate Manager` — update the `adapter_id` value in each workflow task if yours is named differently. If you need both the REST Enrollment API and the SCM Admin API, create two integration instances (see Integration Configuration above) and adjust `adapter_id` per folder accordingly. |
