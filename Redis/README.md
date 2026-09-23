Redis Cloud is Redis Enterprise's fully managed database-as-a-service, providing subscriptions, databases, cloud accounts, access control, and user management for Redis deployments across AWS, Google Cloud, and Azure.

This project provides an OpenAPI spec for automating against the Redis Cloud REST API via an Integration Model, plus a Studio Project of CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`redis_cloud-latest.json`](#redis_cloud-latestjson)
  - [`redis_cloud_api-version_1.json`](#redis_cloud_api-version_1json)
- [Studio Projects](#studio-projects)
  - [Redis Cloud Project](#redis-cloud-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Redis Cloud REST API OpenAPI spec — curated `-latest` plus the full official dated spec it was trimmed from |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing the Subscriptions/Databases/Cloud Accounts/ACL/Users CRUD workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Redis Cloud:latest` Integration Model | Required to run the Studio Project below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to Redis Cloud's REST API.

## Integration Configuration

Import `redis_cloud-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Redis Cloud's API.

Authentication is a pair of API key headers:

```
x-api-key: <your-redis-cloud-account-key>
x-api-secret-key: <your-redis-cloud-secret-key>
```

Generate these at Redis Cloud → Access Management → API Keys.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "x-api-key": { "value": "<your-redis-cloud-account-key>" },
    "x-api-secret-key": { "value": "<your-redis-cloud-secret-key>" }
  },
  "server": {
    "protocol": "https",
    "host": "api.redislabs.com",
    "base_path": "/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`redis_cloud-latest.json`](./OpenAPIs/redis_cloud-latest.json) | latest (curated) | 46 | Trimmed to common CRUD for subscriptions, databases, cloud accounts, ACL, and users — see breakdown below |
| [`redis_cloud_api-version_1.json`](./OpenAPIs/redis_cloud_api-version_1.json) | Version 1 | 158 | Full, unmodified official Redis Cloud API spec |

### `redis_cloud-latest.json`

Trimmed from the official Redis Cloud API spec's 158 operations down to 46, covering:

- **Subscriptions**: List, create, get, update, delete (Pro/flexible plans)
- **Databases**: List, create, get, update, delete (under a Pro/flexible subscription)
- **Fixed Subscriptions**: List, create, get, update, delete (Essentials/fixed plans)
- **Fixed Databases**: List, create, get, update, delete (under a fixed subscription)
- **Cloud Accounts**: List, create, get, update, delete
- **ACL Rules**: List, create, update, delete
- **ACL Roles**: List, create, update, delete
- **ACL Users**: List, create, get, update, delete
- **Account Users**: List, get, update, delete
- **Tasks**: List, get by ID (Redis Cloud's subscription/database operations are asynchronous — poll a task's status here)
- **Reference Data**: Supported regions, supported database modules

### `redis_cloud_api-version_1.json`

Full, unmodified official vendor spec for the Redis Cloud API, `Version 1` — preserved as-is from `api.redislabs.com/v1/cloud-api-docs/capi`.

---

## Studio Projects

### Redis Cloud Project

Backed by the **`Redis Cloud:latest`** Integration Model (see [`redis_cloud-latest.json`](./OpenAPIs/redis_cloud-latest.json) above). The project contains **46 workflows** organized into **11 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Subscriptions | 5 | Pro/flexible subscription CRUD |
| Databases | 5 | Database CRUD under a Pro/flexible subscription |
| Fixed Subscriptions | 5 | Essentials/fixed subscription CRUD |
| Fixed Databases | 5 | Database CRUD under a fixed subscription |
| Cloud Accounts | 5 | Cloud account CRUD |
| ACL Rules | 4 | ACL Redis rule CRUD |
| ACL Roles | 4 | ACL role CRUD |
| ACL Users | 5 | ACL user CRUD |
| Account Users | 4 | Account user CRUD |
| Tasks | 2 | Async task status lookup |
| Reference Data | 2 | Supported regions and database modules |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Redis Cloud:latest` Integration Model | Import from [`redis_cloud-latest.json`](./OpenAPIs/redis_cloud-latest.json) before importing the project |
| `Redis Cloud` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Redis Cloud` — update the `adapter_id` value in each workflow task if yours is named differently |
