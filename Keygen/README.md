# Keygen

Keygen is an open, source-available software licensing and distribution API for issuing, validating, and managing software licenses, machines, users, and entitlements. Its REST API exposes license, machine, user, policy, product, and entitlement management at `https://api.keygen.sh/v1`, authenticated with a static Bearer token.

## Table of Contents

- [Keygen](#keygen)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`keygen-latest.json`](#keygen-latestjson)
    - [`keygen-1.0.0.json`](#keygen-100json)
  - [Studio Projects](#studio-projects)
    - [Keygen Project](#keygen-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Keygen API OpenAPI specs — curated `-latest` plus the full spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 64 workflows in 7 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Keygen | Current SaaS release |
| `Keygen:latest` Integration Model | Required to build automation against the OpenAPI specs |
| A Keygen Product or Account token | Generate in the Keygen dashboard under your account or product settings — see **Integration Configuration** below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to Keygen.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Keygen account.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "api.keygen.sh",
    "base_path": "/v1"
  },
  "authentication": {
    "BearerToken": "<product-or-account-token>"
  }
}
```

The Keygen API supports a static Bearer token — there's no login call or token refresh involved, the token is sent as-is on every request as an `Authorization: Bearer` header.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`keygen-latest.json`](./OpenAPIs/keygen-latest.json) | latest (curated) | 64 | Actively-maintained, trimmed to 64 of 111 upstream operations covering common CRUD for licensing automation — see breakdown below |
| [`keygen-1.0.0.json`](./OpenAPIs/keygen-1.0.0.json) | 1.0.0 | 111 | Full Keygen API spec |

### `keygen-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 64 of 111 upstream operations, covering common CRUD for software licensing automation.

Resources included, by category:

- **Licenses**: List/get/create/update/delete, validate by key or by ID, check-in, check-out, suspend, reinstate, revoke, renew, increment/decrement/reset usage, attach/detach entitlements, list entitlements, change group, change policy, attach/detach user, list users
- **Machines**: List/get/create (activate)/update/delete (deactivate), check-out, ping, reset heartbeat, change group
- **Users**: List/get/create/update/delete, ban, unban, change group
- **Policies**: List/get/create/update/delete, attach/detach entitlements, list entitlements
- **Products**: List/get/create/update/delete
- **Entitlements**: List/get/create/update/delete
- **Groups**: List/get/create/update/delete

Dropped from the full spec: artifacts, components, release management (releases, release artifacts, release constraints, publish/yank/upgrade), token administration, second-factor management, password reset requests, current-authenticated-resource lookup, and process heartbeat tracking.

### `keygen-1.0.0.json`

Full Keygen API spec (111 operations) as published.

---

## Studio Projects

### Keygen Project

Backed by the **`Keygen:latest`** Integration Model (see [`keygen-latest.json`](./OpenAPIs/keygen-latest.json) above). The project contains **64 workflows** organized into **7 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Licenses | List, Get, Create, Update, Delete, Validate License Key, Validate License, Check In License, Check Out License, Increment/Decrement/Reset License Usage, Suspend License, Reinstate License, Revoke License, Renew License, Attach/Detach License Entitlements, List License Entitlements, Change License Group, Change License Policy, Attach/Detach License User, List License Users | License lifecycle, validation, usage, and relationship management |
| Machines | List, Get, Activate Machine, Update, Deactivate Machine, Check Out Machine, Ping Machine, Reset Machine Heartbeat, Change Machine Group | Machine activation and heartbeat lifecycle |
| Users | List, Get, Create, Update, Delete, Ban User, Unban User, Change User Group | User CRUD and access control |
| Policies | List, Get, Create, Update, Delete, Attach/Detach Policy Entitlements, List Policy Entitlements | Policy CRUD and entitlement assignment |
| Products | List, Get, Create, Update, Delete | Product CRUD |
| Entitlements | List, Get, Create, Update, Delete | Entitlement CRUD |
| Groups | List, Get, Create, Update, Delete | Group CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Keygen:latest` Integration Model | Import from [`keygen-latest.json`](./OpenAPIs/keygen-latest.json) before importing the project |
| `Keygen` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Keygen` — update the `adapter_id` value in each workflow task if yours is named differently |
