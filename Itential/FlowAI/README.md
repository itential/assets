Itential Platform's own FlowAI REST API: agentic-AI project/agent management, LLM provider profile registration, agent session execution, and human-in-the-loop work-item handling. Lets one Itential Platform (or Itential Gateway) automate building, running, and monitoring FlowAI agents -- and the work items they hand off to a human -- against another Itential Platform instance, or itself.

This project provides an OpenAPI spec for automating FlowAI on Itential Platform's own REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`itential_platform_flowai-latest.json`](#itential_platform_flowai-latestjson)
- [Studio Projects](#studio-projects)
  - [Itential Platform - FlowAI Project](#itential-platform---flowai-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Itential Platform - FlowAI OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform - FlowAI project containing all 52 workflows in 10 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Itential Platform - FlowAI:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `itential_platform_flowai-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the target Itential Platform instance — this can be a different Platform instance, or the same one automating itself.

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
| [`itential_platform_flowai-latest.json`](./OpenAPIs/itential_platform_flowai-latest.json) | latest | 52 | FlowAI — see breakdown below |

### `itential_platform_flowai-latest.json`

Hand-authored from Itential's own published per-operation API reference (docs.itential.com/itential-platform/6/6/api-reference and docs.itential.com/itential-platform/6/api-reference), recovered via the docs site's sitemap.xml since no navigable category index page exists. Covers all four FlowAI backend services in full: agent-project-service (FlowAI Projects and Agents CRUD, admin variants, project bundle import/export), agent-session-manager (session lifecycle, synchronous run-agent execution, message history), work-center-service (work-item lifecycle for human-in-the-loop manual work), and model-registry-service (LLM provider/profile management and credential validation). Note: both agent-project-service and model-registry-service expose an LLM-provider-profile read surface; the agent-project-service operations are prefixed aps* (apsGetProfile/apsListProfiles) to avoid an operationId collision with model-registry-service's canonical create/read/update/delete profile CRUD.

- **FlowAI - Projects** (5 ops): Create FlowAI Project, Get FlowAI Project, List FlowAI Projects, Update FlowAI Project, Delete FlowAI Project
- **FlowAI - Agents** (8 ops): Create Agent, Get Agent, Update Agent, Delete Agent, Get Operable Agent, List Operable Agents, ...
- **FlowAI - Profiles** (2 ops): Get LLM Provider Profile (Agent Project Service), List LLM Provider Profiles (Agent Project Service)
- **FlowAI - Admin** (4 ops): List FlowAI Projects (Admin), Update FlowAI Project (Admin), Delete FlowAI Project (Admin), FlowAI Project Service Health Ping
- **FlowAI - Bundles** (2 ops): Export Project Bundle, Import Project Bundle
- **FlowAI - Sessions** (6 ops): Start Agent Session, Get Agent Session, List Agent Sessions, Update Agent Session State, Delete Agent Session, Get Distinct Trigger Source Options
- **FlowAI - Run Agent** (1 op): Run Agent Synchronously
- **FlowAI - Messages** (2 ops): Get Session Messages, Get Raw Session Message
- **FlowAI - Work Items** (12 ops): Assign Work Item, Cancel Work Item, Cancel Work Items for Execution, Claim Work Item, Complete Work Item, Count Pending Work Items, ...
- **FlowAI - Model Registry** (10 ops): Create Provider Profile, Delete Provider Profile, Fetch Models from Provider (Validate Credential), Get Agent Impact of Profile Deletion, Get Provider Profile, Get Provider Definition, ...

## Studio Projects

### Itential Platform - FlowAI Project

Backed by the **`Itential Platform - FlowAI:latest`** Integration Model (see [`itential_platform_flowai-latest.json`](./OpenAPIs/itential_platform_flowai-latest.json) above). The project contains **52 workflows** organized into **10 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| FlowAI - Projects | 5 | Create FlowAI Project, Get FlowAI Project, List FlowAI Projects, Update FlowAI Project, Delete FlowAI Project |
| FlowAI - Agents | 8 | Create Agent, Get Agent, Update Agent, Delete Agent, Get Operable Agent, List Operable Agents, ... |
| FlowAI - Profiles | 2 | Get LLM Provider Profile (Agent Project Service), List LLM Provider Profiles (Agent Project Service) |
| FlowAI - Admin | 4 | List FlowAI Projects (Admin), Update FlowAI Project (Admin), Delete FlowAI Project (Admin), FlowAI Project Service Health Ping |
| FlowAI - Bundles | 2 | Export Project Bundle, Import Project Bundle |
| FlowAI - Sessions | 6 | Start Agent Session, Get Agent Session, List Agent Sessions, Update Agent Session State, Delete Agent Session, Get Distinct Trigger Source Options |
| FlowAI - Run Agent | 1 | Run Agent Synchronously |
| FlowAI - Messages | 2 | Get Session Messages, Get Raw Session Message |
| FlowAI - Work Items | 12 | Assign Work Item, Cancel Work Item, Cancel Work Items for Execution, Claim Work Item, Complete Work Item, Count Pending Work Items, ... |
| FlowAI - Model Registry | 10 | Create Provider Profile, Delete Provider Profile, Fetch Models from Provider (Validate Credential), Get Agent Impact of Profile Deletion, Get Provider Profile, Get Provider Definition, ... |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Itential Platform - FlowAI:latest` Integration Model | Import from [`itential_platform_flowai-latest.json`](./OpenAPIs/itential_platform_flowai-latest.json) before importing the project |
| `Itential Platform - FlowAI` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Itential Platform - FlowAI` — update the `adapter_id` value in each workflow task if yours is named differently |
