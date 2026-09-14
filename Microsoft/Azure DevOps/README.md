# Azure DevOps

Azure DevOps Services is Microsoft's cloud-hosted platform for the software development lifecycle: Git source control, build and release pipelines, work item tracking, and project/team administration, all exposed through the Azure DevOps Services REST API.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`azure_devops-latest.json`](#azure_devops-latestjson)
- [Studio Projects](#studio-projects)
  - [Azure DevOps Project](#azure-devops-project)
    - [Folder Structure](#folder-structure)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Azure DevOps Services REST API OpenAPI spec, curated for automation |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing 55 workflows in 7 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Azure DevOps Services | Cloud SaaS (dev.azure.com) — no on-premises Azure DevOps Server support |
| Personal Access Token (PAT) | Scoped to the resource areas the workflows will call (Code, Build, Work Items, Project and Team) |

## Integration Configuration

Import `azure_devops-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your organization.

Authentication is HTTP Basic, using a blank username and a Personal Access Token as the password:

```
Authorization: Basic <base64(:personal-access-token)>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "",
      "password": "<your-personal-access-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "dev.azure.com",
    "base_path": "/<your-organization>"
  }
}
```

Every operation in the spec requires an `api-version` query parameter; it defaults to `7.1`, the current stable Azure DevOps REST API version.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`azure_devops-latest.json`](./OpenAPIs/azure_devops-latest.json) | latest (curated) | 55 | Curated across Projects & Teams, Git, Build, Pipelines, and Work Item Tracking — see breakdown below |

### `azure_devops-latest.json`

Microsoft does not publish a static OpenAPI/Swagger document for Azure DevOps Services, and there is no live introspection endpoint to generate one from (it's a multi-tenant SaaS). This spec is derived directly from [`microsoft/azure-devops-node-api`](https://github.com/microsoft/azure-devops-node-api) (v17.0.1), Microsoft's own officially-maintained TypeScript client library — its interface files and API client classes define the exact request/response shapes, REST paths, HTTP methods, and API version for every operation.

Curated to 55 of the several hundred operations across the SDK's Git, Build, Pipelines, and Work Item Tracking API areas alone (the full SDK surface also covers Release, Test Plans, Wiki, Service Endpoints, Task Agent pools, Security Roles, and more, none of which are included here).

Resources included, by category:

- **Projects & Teams**: list/create/get/delete projects, list/create/get/update/delete teams
- **Git Repositories**: list/create/get/update/delete repositories, list refs, list commits, get item content, list/create pushes
- **Git Pull Requests**: list/create/get/update pull requests, list/add reviewers, add labels, list/create comment threads
- **Build**: list/queue/get/update/delete builds, get build changes/logs/timeline
- **Build Definitions**: list/create/get/update/delete build (pipeline) definitions
- **Pipelines**: list/create/get pipelines, list/run pipeline runs, get a run
- **Work Item Tracking**: create/get/update/delete work items, list work items by ID, query by WIQL, list/add comments

## Studio Projects

### Azure DevOps Project

Backed by the **`Azure DevOps:latest`** Integration Model (see [`azure_devops-latest.json`](./OpenAPIs/azure_devops-latest.json) above). The project contains **55 workflows** organized into **7 folders**, one workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Projects & Teams | 9 | List/create/get/delete projects; list/create/get/update/delete teams |
| Git Repositories | 10 | Repository CRUD, refs, commits, item content, pushes |
| Git Pull Requests | 9 | Pull request CRUD, reviewers, labels, comment threads |
| Build | 8 | Build CRUD, changes, logs, timeline |
| Build Definitions | 5 | Build (pipeline) definition CRUD |
| Pipelines | 6 | Pipeline CRUD, runs |
| Work Item Tracking | 8 | Work item CRUD, WIQL query, comments |
