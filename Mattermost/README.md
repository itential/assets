# Mattermost

Mattermost is an open-source, self-hostable team collaboration and messaging platform, providing channels, direct messaging, and integrations for engineering and IT operations teams.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`mattermost-latest.json`](#mattermost-latestjson)
  - [`mattermost-4.0.0.json`](#mattermost-400json)
- [Studio Projects](#studio-projects)
  - [Mattermost Project](#mattermost-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Mattermost REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Mattermost](./Studio%20Projects/Mattermost.project.json) | 33 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Mattermost REST API | v4 (4.0.0) |
| Mattermost Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Mattermost server (e.g. `https://your-mattermost-url`).

Authentication is a static Personal Access Token in the `Authorization` header — no login call is used:

```
Authorization: Bearer <your-personal-access-token>
```

Generate a Personal Access Token under **Profile > Security > Personal Access Tokens** (must be enabled by a System Admin under **System Console > Integrations > Integration Management**).

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearerAuth": {
      "value": "<your-personal-access-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "your-mattermost-url",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`mattermost-latest.json`](./OpenAPIs/mattermost-latest.json) | latest (curated) | 33 | Actively-maintained spec, trimmed to 33 of 598 upstream operations — see breakdown below |
| [`mattermost-4.0.0.json`](./OpenAPIs/mattermost-4.0.0.json) | 4.0.0 | 598 | Full spec for the Mattermost REST API v4 (598 operations) |

### `mattermost-latest.json`

Actively-maintained spec (`x-vendor-api-version: 4.0.0`). Trimmed to 33 of 598 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Channels**: List, Create, Get, Update, Delete, List Members, Add Member, Remove Member
- **Posts**: Create, Get, Update, Delete, List for Channel, Search
- **Users**: List, Create, Get, Update, Delete, Get by Username, Get by Email, Search, Update Active Status
- **Teams**: List, Create, Get, Update, Delete, List Members, Add Member, Remove Member, Get by Name, List Channels for Team

### `mattermost-4.0.0.json`

Full, unmodified vendor spec for the Mattermost REST API v4 (598 operations) — reconstructed from the vendor's official split-source YAML files (`mattermost/mattermost` repo, `api/v4/source/*.yaml`), concatenated in the same order as the vendor's own build (`api/Makefile`), since the repo does not check in a single pre-built bundle. See `mattermost-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Mattermost Project

Backed by the **`Mattermost:latest`** Integration Model (see [`mattermost-latest.json`](./OpenAPIs/mattermost-latest.json) above). The project contains **33 workflows** organized into **4 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Channels | List, Create, Get, Update, Delete Channel, List/Add/Remove Channel Member | Channel and channel membership CRUD |
| Posts | Create, Get, Update, Delete Post, List Posts for Channel, Search Posts | Post lifecycle and search |
| Users | List, Create, Get, Update, Delete User, Get by Username/Email, Search Users, Update Active Status | User CRUD and lookup |
| Teams | List, Create, Get, Update, Delete Team, List/Add/Remove Team Member, Get by Name, List Channels for Team | Team and team membership CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Mattermost:latest` Integration Model | Import from [`mattermost-latest.json`](./OpenAPIs/mattermost-latest.json) before importing the project |
| `Mattermost` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Mattermost` — update the `adapter_id` value in each workflow task if yours is named differently |
