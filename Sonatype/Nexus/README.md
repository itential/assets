Sonatype Nexus Repository Manager is a repository manager for storing, organizing, and distributing software artifacts and components across a wide range of package formats (Maven, npm, Docker, NuGet, PyPI, and more).

This project provides OpenAPI specs for automating against the Nexus Repository Manager REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for repository automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`sonatype_nexus_repository-latest.json`](#sonatype_nexus_repository-latestjson)
  - [`sonatype_nexus_repository-3.69.0-02.json`](#sonatype_nexus_repository-3690-02json)
- [Studio Projects](#studio-projects)
  - [Sonatype Nexus Repository Project](#sonatype-nexus-repository-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Nexus Repository REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Sonatype Nexus Repository](./Studio%20Projects/Sonatype%20Nexus%20Repository.project.json) | 18 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Sonatype Nexus Repository | 3.69.0-02 (see OpenAPIs below) |
| Sonatype Nexus Repository Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Nexus Repository instance.

Authentication is HTTP Basic, using a Nexus administrator (or service) account:

```
Authorization: Basic <base64(username:password)>
```

Configure accounts under **Security → Users** in the Nexus admin UI.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basic": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "example.com:443",
    "base_path": "/service/rest"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`sonatype_nexus_repository-latest.json`](./OpenAPIs/sonatype_nexus_repository-latest.json) | latest (curated) | 146 | Actively-maintained, trimmed to 146 of 241 upstream operations covering common CRUD for automation — see breakdown below |
| [`sonatype_nexus_repository-3.69.0-02.json`](./OpenAPIs/sonatype_nexus_repository-3.69.0-02.json) | 3.69.0-02 | 241 | Full spec for Nexus Repository 3.69.0-02 (241 operations), including blob store, security (users/roles/privileges/LDAP/realms/certificates), email, licensing, scripting, tasks, routing rules, content selectors, Repository Firewall, and lifecycle/read-only administration. |

### `sonatype_nexus_repository-latest.json`

Actively-maintained spec (`x-vendor-api-version: 3.69.0-02`). Trimmed to 146 of 241 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Repository Management**: Create, read, update, and delete hosted, proxy, and group repositories across all supported formats — apt, bower, cocoapods, conan, conda, docker, gitlfs, go, helm, maven, npm, nuget, p2, pypi, r, raw, rubygems, yum — plus repository health-check, invalidate-cache, and rebuild-index actions
- **Components**: List, get, upload, and delete components
- **Assets**: List, get, and delete assets
- **Search**: Search components and assets, and search-and-download an asset
- **Formats**: List supported formats and their component upload field requirements
- **Status**: Health-check endpoints for read/write availability

### `sonatype_nexus_repository-3.69.0-02.json`

Full, unmodified vendor spec for Nexus Repository 3.69.0-02 (241 operations) — the vendor's complete API surface, preserved as-is. See `sonatype_nexus_repository-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Sonatype Nexus Repository Project

Backed by the **`Sonatype Nexus Repository:latest`** Integration Model (see [`sonatype_nexus_repository-latest.json`](./OpenAPIs/sonatype_nexus_repository-latest.json) above). The project contains **18 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec. Repository create/update is scoped to Maven and npm hosted repositories as representative examples — the curated spec covers the same CRUD shape across 17 other formats if you need to extend it.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Repositories | List, Get, Delete Repository, Create/Update Maven Hosted Repository, Create/Update npm Hosted Repository, Invalidate Repository Cache | Repository lifecycle |
| Components | List, Upload, Get, Delete Component | Component CRUD |
| Assets | List, Get, Delete Asset | Asset CRUD |
| Search | Search Components, Search Assets | Component/asset discovery |
| Status | Check System Status | Read/write availability check |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Sonatype Nexus Repository:latest` Integration Model | Import from [`sonatype_nexus_repository-latest.json`](./OpenAPIs/sonatype_nexus_repository-latest.json) before importing the project |
| `Sonatype Nexus Repository` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Sonatype Nexus Repository` — update the `adapter_id` value in each workflow task if yours is named differently |
