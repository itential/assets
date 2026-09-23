Moogsoft Cloud (APEX AIOps Incident Management) is a SaaS AIOps platform that ingests events, deduplicates them into alerts, and correlates related alerts into incidents to reduce operational noise and speed up incident response.

This project provides OpenAPI specs for automating against the Moogsoft Cloud REST API (`api.moogsoft.ai`) via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`moogsoft_cloud-latest.json`](#moogsoft_cloud-latestjson)
  - [`moogsoft_cloud-2026-09-23.json`](#moogsoft_cloud-2026-09-23json)
- [Studio Projects](#studio-projects)
  - [Moogsoft Cloud Project](#moogsoft-cloud-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Moogsoft Cloud REST API OpenAPI specs — curated `-latest` plus the dated reference spec |
| [Studio Projects/Moogsoft Cloud](./Studio%20Projects/Moogsoft%20Cloud.project.json) | 27 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Moogsoft Cloud / APEX AIOps Incident Management | v1 / v2 |
| Moogsoft Cloud Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Moogsoft Cloud instance.

Authentication is a static, instance-generated API key, created under **Settings > API Key Management**, passed on a header named `apiKey`:

```
apiKey: <your-api-key>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiKeyAuth": {
      "value": "<your-api-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.moogsoft.ai",
    "port": "443",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`moogsoft_cloud-latest.json`](./OpenAPIs/moogsoft_cloud-latest.json) | latest (curated) | 27 | Actively-maintained spec covering common CRUD for automation — see breakdown below |
| [`moogsoft_cloud-2026-09-23.json`](./OpenAPIs/moogsoft_cloud-2026-09-23.json) | 2026-09-23 | 27 | Reference spec |

### `moogsoft_cloud-latest.json`

Covers event ingestion, alerts, incidents, catalogs, maintenance windows, correlation definitions, workflows, and collectors.

Resources included, by category:

- **Events**: Send Events
- **Alerts**: Search, Get Details, Update (owner/status)
- **Incidents**: List, Get Details, Update (assignee/status/priority), Add Comment
- **Catalogs**: List, Create, Get Details, Update, Delete
- **Maintenance Windows**: List, Create, Get Details, Update, Delete
- **Correlation Definitions**: List, Create, Get Details, Update, Delete
- **Workflows**: List, Get Details, Update (name/description/enabled)
- **Collectors**: List

### `moogsoft_cloud-2026-09-23.json`

Moogsoft does not publish a downloadable OpenAPI/Swagger file for this API, so this reference spec carries the same 27 operations as `moogsoft_cloud-latest.json` rather than a larger untrimmed surface.

## Studio Projects

### Moogsoft Cloud Project

Backed by the **`Moogsoft Cloud:latest`** Integration Model (see [`moogsoft_cloud-latest.json`](./OpenAPIs/moogsoft_cloud-latest.json) above). The project contains **27 workflows** organized into **8 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Events | Send Events | Event ingestion |
| Alerts | Search, Get Details, Update | Alert lifecycle |
| Incidents | List, Get Details, Update, Add Comment | Incident lifecycle |
| Catalogs | List, Create, Get Details, Update, Delete | Data enrichment catalog CRUD |
| Maintenance Windows | List, Create, Get Details, Update, Delete | Maintenance window CRUD |
| Correlation Definitions | List, Create, Get Details, Update, Delete | Correlation Engine rule CRUD |
| Workflows | List, Get Details, Update | Workflow Engine automation CRUD |
| Collectors | List | Collector agent visibility |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Moogsoft Cloud:latest` Integration Model | Import from [`moogsoft_cloud-latest.json`](./OpenAPIs/moogsoft_cloud-latest.json) before importing the project |
| `Moogsoft Cloud` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Moogsoft Cloud` — update the `adapter_id` value in each workflow task if yours is named differently |
| `alertId` / `incidentId` / `catalogId` / `windowId` / `correlationDefinitionId` / `workflowId` inputs | Most Get/Update/Delete workflows require the ID of the target resource, typically obtained from a prior List/Search call |
