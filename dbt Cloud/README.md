# dbt Cloud

dbt Cloud is the managed service for running dbt (data build tool) transformation jobs, orchestrating analytics engineering pipelines, and managing dbt projects, environments, and warehouse connections.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`dbt_cloud-latest.json`](#dbt_cloud-latestjson)
  - [`dbt_cloud-3.0.0.json`](#dbt_cloud-300json)
  - [`dbt_cloud-2.0.0.json`](#dbt_cloud-200json)
- [Studio Projects](#studio-projects)
  - [dbt Cloud Project](#dbt-cloud-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | dbt Cloud API OpenAPI specs — curated `-latest` plus the two full dated specs |
| [Studio Projects/dbt Cloud](./Studio%20Projects/dbt%20Cloud.project.json) | 29 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| dbt Cloud API | v2 2.0.0 / v3 3.0.0 |
| dbt Cloud Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your dbt Cloud account (e.g. `https://cloud.getdbt.com`, or your region-specific host).

Authentication is a Personal Access Token or Service Token in the `Authorization` header, using the non-standard `Token` prefix (not `Bearer`):

```
Authorization: Token <your-dbt-cloud-token>
```

Generate a Personal Access Token under **Account Settings > Personal Tokens**, or a Service Token under **Account Settings > Service Tokens**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "TokenAuth": {
      "value": "Token <your-dbt-cloud-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "cloud.getdbt.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`dbt_cloud-latest.json`](./OpenAPIs/dbt_cloud-latest.json) | latest (curated) | 29 | Actively-maintained spec, trimmed to 29 of 207 upstream operations — see breakdown below |
| [`dbt_cloud-3.0.0.json`](./OpenAPIs/dbt_cloud-3.0.0.json) | 3.0.0 | 155 | Full spec for dbt Cloud API v3 (account/project administration) |
| [`dbt_cloud-2.0.0.json`](./OpenAPIs/dbt_cloud-2.0.0.json) | 2.0.0 | 52 | Full spec for dbt Cloud API v2 (jobs, runs, artifacts) |

### `dbt_cloud-latest.json`

Actively-maintained spec (`x-vendor-api-version: v2 2.0.0 / v3 3.0.0`), combining the two upstream OpenAPI documents dbt Labs publishes into a single Integration Model. Trimmed to 29 of 207 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Jobs** (from API v2): List, Create, Get, Update, Delete, Trigger Job Run, Retry Failed Job
- **Runs** (from API v2): List, Get, List Artifacts, Get Artifact, Cancel, Get Failure Details, Retry
- **Projects** (from API v3): List, Create, Get, Update, Delete
- **Environments** (from API v3): List, Create, Get, Update, Delete
- **Connections** (from API v3): List, Create, Get, Update, Delete

### `dbt_cloud-3.0.0.json`

Full, unmodified vendor spec for dbt Cloud API v3 (155 operations) — account/project administration surface (projects, environments, connections, credentials, repositories, groups, users, webhooks, and more), preserved as-is.

### `dbt_cloud-2.0.0.json`

Full, unmodified vendor spec for dbt Cloud API v2 (52 operations) — job/run execution surface (jobs, runs, artifacts, notifications), preserved as-is.

See `dbt_cloud-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### dbt Cloud Project

Backed by the **`dbt Cloud:latest`** Integration Model (see [`dbt_cloud-latest.json`](./OpenAPIs/dbt_cloud-latest.json) above). The project contains **29 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Jobs | List, Create, Get, Update, Delete Job, Trigger Job Run, Retry Failed Job | Job definition CRUD and execution |
| Runs | List, Get Run, List/Get Run Artifacts, Cancel Run, Get Run Failure Details, Retry Run | Run monitoring and control |
| Projects | List, Create, Get, Update, Delete Project | Project CRUD |
| Environments | List, Create, Get, Update, Delete Environment | Environment CRUD |
| Connections | List, Create, Get, Update, Delete Connection | Warehouse connection CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `dbt Cloud:latest` Integration Model | Import from [`dbt_cloud-latest.json`](./OpenAPIs/dbt_cloud-latest.json) before importing the project |
| `dbt Cloud` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `dbt Cloud` — update the `adapter_id` value in each workflow task if yours is named differently |
| `account_id` / `project_id` | Every workflow requires the numeric dbt Cloud account ID as input; project-scoped workflows (Environments, Connections) also require the `project_id` |
