CyberArk Privilege Cloud is CyberArk's SaaS privileged access management platform — Safes, privileged Accounts, and CPM-driven password lifecycle actions (verify, change, reconcile, retrieve), part of the Identity Security Platform (ISPSS).

This project provides an OpenAPI spec for automating against Privilege Cloud's REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model. This is a separate CyberArk product from [Conjur](../Conjur/) (open-source, self-hosted secrets management) — the two don't share an API or auth model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cyberark_privilege_cloud-latest.json`](#cyberark_privilege_cloud-latestjson)
- [Studio Projects](#studio-projects)
  - [CyberArk Privilege Cloud Project](#cyberark-privilege-cloud-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | CyberArk Privilege Cloud OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 16 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `CyberArk Privilege Cloud:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `cyberark_privilege_cloud-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Privilege Cloud tenant.

Authentication is native OAuth2 client credentials against your ISPSS Identity tenant: `POST https://<identity-tenant-id>.id.cyberark.cloud/oauth2/platformtoken` with a form-urlencoded `client_id`/`client_secret`, returning a JSON `access_token`. Generate a service user (client ID/secret) for this in the CyberArk Identity Administration portal.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-service-user-client-id>",
      "client_secret": "<your-service-user-client-secret>",
      "token_url": "https://<your-identity-tenant-id>.id.cyberark.cloud/oauth2/platformtoken",
      "refresh_url": "",
      "scope": "",
      "token": { "access_token": "" }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-privilege-cloud-subdomain>.privilegecloud.cyberark.com",
    "base_path": "/PasswordVault/API"
  }
}
```

Substitute your identity tenant ID in `token_url` and your Privilege Cloud subdomain in `server.host`.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cyberark_privilege_cloud-latest.json`](./OpenAPIs/cyberark_privilege_cloud-latest.json) | latest (curated) | 16 | Safes, Accounts, and password lifecycle actions — see breakdown below |

### `cyberark_privilege_cloud-latest.json`

CyberArk doesn't publish a static downloadable OpenAPI/Swagger file for Privilege Cloud — only a live, per-tenant Swagger UI with no stable pinnable URL. This spec is hand-authored from CyberArk's own current, product-separated REST API reference collection (covering Privilege Cloud specifically, current to Privilege Cloud v14.7), scoped to 16 core operations:

- **Safes** (5 ops): list, get, add, update, delete
- **Accounts** (5 ops): list, get, add, update (JSON-Patch), delete
- **Password Actions** (4 ops): verify credentials, change credentials, reconcile credentials, retrieve password value
- **Platforms** (2 ops): list, get details

Excluded from this build: session/PSM connection actions (ad-hoc connect, PSM connect, check-in exclusive accounts — interactive session management, not automation targets), Safe Members, Applications, Users, access-request workflows, LDAP integration, session monitoring/recordings, and onboarding rules.

**Not independently verified against a live CyberArk tenant.** The source reference is current and product-specific, but one auth detail in particular is worth confirming yourself before relying on it in production: CyberArk's own REST API examples send the bearer token without a `Bearer ` prefix for their legacy session-token auth flow. This spec models the modern OAuth2 flow instead (which Itential Platform auto-prefixes as `Bearer <token>` by default) — if your tenant rejects the `Bearer` prefix, that's a one-line fix on the `oauth2ClientCredentials` security scheme (`auth_method`/token-type override), not a structural problem.

## Studio Projects

### CyberArk Privilege Cloud Project

Backed by the **`CyberArk Privilege Cloud:latest`** Integration Model (see [`cyberark_privilege_cloud-latest.json`](./OpenAPIs/cyberark_privilege_cloud-latest.json) above). The project contains **16 workflows** organized into **4 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Accounts | 5 | List, get, add, update, delete privileged accounts |
| Safes | 5 | List, get, add, update, delete Safes |
| Password Actions | 4 | Verify, change, reconcile credentials; retrieve password value |
| Platforms | 2 | List platforms, get platform details |

#### Dependencies

| Dependency | Notes |
|---|---|
| `CyberArk Privilege Cloud:latest` Integration Model | Import from [`cyberark_privilege_cloud-latest.json`](./OpenAPIs/cyberark_privilege_cloud-latest.json) before importing the project |
| `CyberArk Privilege Cloud` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `CyberArk Privilege Cloud` — update the `adapter_id` value in each workflow task if yours is named differently |
