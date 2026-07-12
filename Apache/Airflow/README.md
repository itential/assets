Apache Airflow is an open-source platform for programmatically authoring, scheduling, and monitoring workflows as directed acyclic graphs (DAGs).

This project provides OpenAPI specs for automating against the Airflow stable REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

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

## OpenAPIs

### `apache_airflow-latest.json` (curated)

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

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`apache_airflow-2.5.1.json`](./OpenAPIs/apache_airflow-2.5.1.json) | Full spec for Apache Airflow 2.5.1 (73 operations). |

## Dependencies

| Dependency | Notes |
|---|---|
| Apache Airflow Integration Model | Import from an OpenAPI spec above to build automation against the REST API. |
