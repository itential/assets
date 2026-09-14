# Jenkins

Jenkins is an open source automation server used to build, test, and deploy software through user-defined jobs and pipelines, run on a controller with optional distributed build agents.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`jenkins-latest.json`](#jenkins-latestjson)
  - [`jenkins-2026-09-14.json`](#jenkins-20260914json)
- [Studio Projects](#studio-projects)
  - [Jenkins Project](#jenkins-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Jenkins remote access API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Jenkins](./Studio%20Projects/Jenkins.project.json) | 21 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Jenkins | LTS (remote access API is stable across recent LTS lines) |
| `Jenkins:latest` Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Jenkins controller.

Authentication is HTTP Basic using your Jenkins username and an API token (not your account password). Generate a token from your Jenkins user profile under **Configure > API Token**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "jenkins_auth": {
      "username": "<your-jenkins-username>",
      "password": "<your-jenkins-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "jenkins.example.com",
    "base_path": ""
  }
}
```

Replace `jenkins.example.com` with your own Jenkins controller hostname.

## OpenAPIs

Jenkins itself publishes no official OpenAPI/Swagger spec or automated REST API documentation. Both specs here are derived from [`swaggy-jenkins`](https://github.com/oapicf/swaggy-jenkins), a community-maintained OpenAPI description of Jenkins' remote access API under the OpenAPI Generator Community Foundation.

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`jenkins-latest.json`](./OpenAPIs/jenkins-latest.json) | latest (curated) | 21 | Actively-maintained spec, trimmed to 21 of 58 upstream operations — see breakdown below |
| [`jenkins-2026-09-14.json`](./OpenAPIs/jenkins-2026-09-14.json) | 2026-09-14 | 58 | Full spec, including the Blue Ocean REST API (58 operations) |

### `jenkins-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2026-09-14`). Trimmed to 21 of 58 upstream operations covering common CRUD for automation.

Resources included, by category:

- **System**: Get Headers, Get Details, Get CSRF Crumb
- **Nodes and Agents**: Get Computer / Agent Status
- **Jobs**: Get, Create, Get Configuration, Update Configuration, Delete, Disable, Enable
- **Builds**: Trigger, Get Last Build, Stop Last Build, Get Console Output
- **Queue**: Get Queue, Get Queue Item
- **Views**: Create, Get, Get Configuration, Update Configuration

### `jenkins-2026-09-14.json`

Full spec (58 operations) — the complete `swaggy-jenkins` surface, including Blue Ocean, captured 2026-09-14. See `jenkins-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Jenkins Project

Backed by the **`Jenkins:latest`** Integration Model (see [`jenkins-latest.json`](./OpenAPIs/jenkins-latest.json) above). The project contains **21 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| System | Get Jenkins Headers, Get Jenkins Details, Get CSRF Crumb | Instance-level info and CSRF crumb retrieval |
| Nodes and Agents | Get Computer / Agent Status | Agent/node status |
| Jobs | Get, Create, Get Configuration, Update Configuration, Delete, Disable, Enable Job | Job CRUD |
| Builds | Trigger, Get Last Build, Stop Last Build, Get Console Output | Build lifecycle |
| Queue | Get Queue, Get Queue Item | Build queue |
| Views | Create, Get, Get Configuration, Update Configuration View | View CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Jenkins:latest` Integration Model | Import from [`jenkins-latest.json`](./OpenAPIs/jenkins-latest.json) before importing the project |
| `Jenkins` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Jenkins` — update the `adapter_id` value in each workflow task if yours is named differently |
