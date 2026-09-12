# Rundeck

Rundeck is a job automation and orchestration platform used to define, schedule, and run operational procedures and ad hoc commands across a node inventory, with centralized logging, access control, and workflow-based execution.

This project provides OpenAPI specs for automating against Rundeck's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for job, project, execution, and node automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`rundeck-latest.json`](#rundeck-latestjson)
  - [`rundeck-59.json`](#rundeck-59json)
- [Studio Projects](#studio-projects)
  - [Rundeck Project](#rundeck-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Rundeck REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Rundeck](./Studio%20Projects/Rundeck.project.json) | 23 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Rundeck REST API | version 59 |
| Rundeck Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Rundeck server.

Authentication is a static API token in the `X-Rundeck-Auth-Token` header (Rundeck also accepts it as an `authtoken` query parameter, but the header is what this spec's security scheme uses). Generate a token from your Rundeck user profile page under **API Tokens**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "rundeckApiToken": {
      "value": "<your-rundeck-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-rundeck-host>",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`rundeck-latest.json`](./OpenAPIs/rundeck-latest.json) | latest (curated) | 23 | Trimmed to 23 of 252 upstream operations covering common CRUD for automation — see breakdown below |
| [`rundeck-59.json`](./OpenAPIs/rundeck-59.json) | 59 | 252 | Full spec for the Rundeck REST API (version 59) |

Both specs are sourced from Rundeck's own official OpenAPI document, published at [`docs.rundeck.com/files/rundeck-api.yml`](https://docs.rundeck.com/docs/api/api-spec.html) and already in OpenAPI 3.0.1 format, so no Swagger-to-OpenAPI conversion was needed. The vendor document defines four security schemes (API token, password session, JWT, and a webhook signing header); this repo keeps only the API token scheme per the one-`securityScheme`-per-spec rule — see **Integration Configuration** above.

### `rundeck-latest.json`

Actively-maintained spec (`x-vendor-api-version: 59`). Trimmed to 23 of 252 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Jobs**: List, Import (create), Get Definition, Get Info, Run, List Executions, Enable, Disable, Delete
- **Projects**: List, Create, Get, Delete
- **Executions**: List, List Running, Get, Get Output, Get State, Abort, Delete
- **Nodes**: List, Get
- **Ad Hoc**: Run Adhoc Command

Not included: cluster/enterprise administration, system configuration, ACL policy management, SCM integration, key storage, local user/role management, runner management, metrics/health checks, webhooks, calendars, and API tokens management. Pull the full spec below if you need one of these.

### `rundeck-59.json`

Full, unmodified vendor spec for the Rundeck REST API (version 59) (252 operations) — the entire upstream API surface as Rundeck publishes it. See `rundeck-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Rundeck Project

Backed by the **`Rundeck:latest`** Integration Model (see [`rundeck-latest.json`](./OpenAPIs/rundeck-latest.json) above). The project contains **23 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the curated spec in full.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Jobs | List, Import, Get Definition, Get Info, Run, List Executions, Enable, Disable, Delete Job | Job lifecycle and execution |
| Projects | List, Create, Get, Delete Project | Project CRUD |
| Executions | List, List Running, Get, Get Output, Get State, Abort, Delete Execution | Execution monitoring and control |
| Nodes | List, Get Node | Node inventory |
| Ad Hoc | Run Adhoc Command | Ad hoc command execution |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Rundeck:latest` Integration Model | Import from [`rundeck-latest.json`](./OpenAPIs/rundeck-latest.json) before importing the project |
| `Rundeck` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Rundeck` — update the `adapter_id` value in each workflow task if yours is named differently |
