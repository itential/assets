Itential Platform's own REST API — Integration Models, integration instances, and Automation Studio workflows/projects. Lets one Itential Platform (or Itential Gateway) automate the configuration of another Itential Platform instance, or even itself.

This project provides an OpenAPI spec for automating against Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform-latest.json`](#itential_platform-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform Project](#itential-platform-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 12 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

Authentication is a token retrieved dynamically: `POST /login` with a `username`/`password` body returns the token as the raw response body (no JSON envelope), which is then sent as the `token` query parameter on every subsequent call. Itential Platform automates the whole exchange, including re-retrieval on expiry.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiKeyAuth": {
      "value": "",
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://<target-platform-host>/login"
      },
      "parameters": {
        "username": "<your-username>",
        "password": "<your-password>"
      }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<target-platform-host>",
    "base_path": ""
  }
}
```

**Pointing this at the same Platform instance running the integration itself:** if the target is genuinely the same Platform, use the internal host/port the Platform container/process actually listens on, not any externally-mapped port — e.g. in a single-container Docker deployment mapping host port 3001 to the container's internal port 3000, use `localhost:3000` (the internal port), not `localhost:3001` (the host-mapped port), since the outbound call executes from inside that same container.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`itential_platform-latest.json`](./OpenAPIs/itential_platform-latest.json) | latest (curated) | 12 | Integration Models, integration instances, and Automation Studio workflows/projects — see breakdown below |

### `itential_platform-latest.json`

Hand-authored from direct, first-hand use of these exact endpoints — Itential Platform doesn't publish this as a downloadable spec at a stable URL. Scoped to 12 operations covering the core build/automate loop:

- **Integration Models** (3 ops): list, import, delete
- **Integration Instances** (3 ops): list, create, delete
- **Task Schemas** (1 op): fetch the incoming/outgoing variable schema for one or more Integration Model operations
- **Workflows** (2 ops): create a workflow, delete a workflow by name (the delete-by-name endpoint is undocumented anywhere except platform source)
- **Studio Projects** (3 ops): create, get, export (export returns each component's full inline document — the shape needed to save/version a project as a standalone file, unlike the plain get)

Excluded: device inventory, Configuration Manager, job/task execution and monitoring, user/role administration, and everything else in the platform's much larger overall API surface — this build is scoped specifically to Integration-Model-based build/deploy automation, not general platform administration.

## Studio Projects

### Itential Platform Project

Backed by the **`Itential Platform:latest`** Integration Model (see [`itential_platform-latest.json`](./OpenAPIs/itential_platform-latest.json) above). The project contains **12 workflows** organized into **5 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Integration Models | 3 | List, import, delete Integration Models |
| Integration Instances | 3 | List, create, delete integration instances |
| Task Schemas | 1 | Fetch task input/output schemas ahead of building a workflow |
| Workflows | 2 | Create a workflow, delete a workflow by name |
| Studio Projects | 3 | Create, get, export a Studio Project |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform:latest` Integration Model | Import from [`itential_platform-latest.json`](./OpenAPIs/itential_platform-latest.json) before importing the project |
| `Itential Platform` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform` — update the `adapter_id` value in each workflow task if yours is named differently |
