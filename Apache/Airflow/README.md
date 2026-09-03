Apache Airflow is an open-source platform for programmatically authoring, scheduling, and monitoring workflows as directed acyclic graphs (DAGs).

This project provides OpenAPI specs for automating against the Airflow stable REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`apache_airflow-latest.json`](#apache_airflow-latestjson)
  - [`apache_airflow-2.5.1.json`](#apache_airflow-251json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Apache Airflow REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Apache Airflow | 2.5.1 |
| Apache Airflow Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Airflow webserver.

Authentication is HTTP Basic — an Airflow username and password:

```
Authorization: Basic <base64(username:password)>
```

Create or manage the account under the Airflow UI's **Admin > Users**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "Basic": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "apache.local",
    "base_path": "/api/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`apache_airflow-latest.json`](./OpenAPIs/apache_airflow-latest.json) | latest (curated) | 50 | Trimmed to 50 of 73 upstream operations — see breakdown below |
| [`apache_airflow-2.5.1.json`](./OpenAPIs/apache_airflow-2.5.1.json) | 2.5.1 | 73 | Full spec for Apache Airflow 2.5.1 (73 operations) |

### `apache_airflow-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.5.1`). Trimmed to 50 of 73 upstream operations covering common CRUD for automation.

Resources included, by category:

- **DAGs**: List, Get, Update (pause/unpause), Delete, Get Source, Get Details, Get Tasks, Get Task, Clear Task Instances, Update Task Instances State
- **DAG Runs**: List, Create, Get, Update, Delete, Clear, Set Note, Batch List
- **Task Instances**: List, Get, Update, Get Links, List Mapped, Get Logs, Set Note, Batch List, XCom Entries (list/get)
- **Connections**: List, Create, Test, Get, Update, Delete
- **Variables**: List, Create, Get, Update, Delete
- **Pools**: List, Create, Get, Update, Delete
- **Monitoring**: Health, Version

Excluded as internal vendor tooling or reporting-only tails: Config, DAG Warnings, Datasets (data-aware scheduling), Event Logs, Import Errors, Permissions, Plugins, Providers, Roles, and Users (RBAC administration).

### `apache_airflow-2.5.1.json`

Full, unmodified vendor spec for Apache Airflow 2.5.1 (73 operations) — the vendor's complete API surface, preserved as-is. See `apache_airflow-latest.json` above for the curated subset if you just need common CRUD automation.

