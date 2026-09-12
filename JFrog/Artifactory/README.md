# JFrog Artifactory

JFrog Artifactory is a universal binary repository manager that stores, manages, and distributes software packages and artifacts (Maven, npm, Docker, PyPI, and dozens of other package formats) across the build and release lifecycle.

This project provides an OpenAPI spec for automating against Artifactory's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for repository and artifact automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`jfrog_artifactory-latest.json`](#jfrog_artifactory-latestjson)
  - [`jfrog_artifactory-7.161.16.json`](#jfrog_artifactory-7161116json)
- [Studio Projects](#studio-projects)
  - [JFrog Artifactory Project](#jfrog-artifactory-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | JFrog Artifactory REST API OpenAPI spec — curated `-latest` plus the full spec |
| [Studio Projects/JFrog Artifactory](./Studio%20Projects/JFrog%20Artifactory.project.json) | 23 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| JFrog Artifactory | 7.98.x or later (for Bearer access token auth) |
| `JFrog Artifactory:latest` Integration Model | Required to run the Studio Project below |

## Integration Configuration

Import `jfrog_artifactory-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your JFrog Platform instance.

Authentication is a Bearer access token in the `Authorization` header. Artifactory's legacy API key header (`X-JFrog-Art-Api`) was deprecated as of 7.98.x, so access tokens are the supported method going forward:

```
Authorization: Bearer <your-access-token>
```

Generate an access token in the JFrog Platform UI under **Administration > User Management > Access Tokens**, or via the Access REST API.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearer": {
      "token": { "value": "<your-access-token>" }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-instance>.jfrog.io",
    "base_path": "/artifactory"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`jfrog_artifactory-latest.json`](./OpenAPIs/jfrog_artifactory-latest.json) | latest (curated) | 87 | Trimmed to 87 of 174 upstream operations covering common CRUD for automation — see breakdown below |
| [`jfrog_artifactory-7.161.16.json`](./OpenAPIs/jfrog_artifactory-7.161.16.json) | 7.161.16 | 174 | Full spec for the JFrog Artifactory REST API |

Both specs are assembled from JFrog's own officially-published, per-endpoint OpenAPI 3.1 definitions on [docs.jfrog.com](https://docs.jfrog.com/artifactory/reference) (the same source that backs Artifactory's interactive `swagger-ui.html` reference) — JFrog does not publish these as a single combined downloadable file, so each operation's official definition was merged into one spec here. The separate **JFrog Distribution API** and package-type-specific plumbing endpoints documented alongside Artifactory are out of scope for this spec.

### `jfrog_artifactory-latest.json`

Actively-maintained spec (`x-vendor-api-version: 7.161.16`). Trimmed to 87 of 174 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Repositories**: List All Configurations, Get, Create, Update, Delete
- **Artifacts**: Deploy, Retrieve, Delete, Copy, Move
- **Item Properties**: Get Storage Item, Set Properties, Delete Properties
- **Searches**: AQL, Artifact, GAVC
- **Repository Replication**: Get, Set, Update, Delete Configuration
- **Trash Can**: Restore Item, Delete Item, Empty

Not included: package-type-specific metadata/index calculation endpoints (Maven, npm, Debian, Conan, etc.), Federated Repositories, Release Bundles v1, Retention policies, storage/garbage-collection/pruning administration, system replication, signed URLs, and metrics/introspection endpoints. Pull the full spec below if you need one of these.

### `jfrog_artifactory-7.161.16.json`

Full spec assembled from JFrog's official per-endpoint OpenAPI definitions for the Artifactory REST API (174 operations) — the entire Artifactory API surface as JFrog documents it, excluding the separate Distribution API. See `jfrog_artifactory-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### JFrog Artifactory Project

Backed by the **`JFrog Artifactory:latest`** Integration Model (see [`jfrog_artifactory-latest.json`](./OpenAPIs/jfrog_artifactory-latest.json) above). The project contains **23 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Repositories | List Configurations, Get, Create, Update, Delete Repository | Repository configuration CRUD |
| Artifacts | Deploy, Retrieve, Delete, Copy, Move | Artifact lifecycle |
| Item Properties | Get, Set, Delete | Item metadata/properties |
| Searches | AQL, Artifact, GAVC | Repository search |
| Repository Replication | Get, Set, Update, Delete Configuration | Replication configuration CRUD |
| Trash Can | Restore, Delete, Empty | Deleted-item recovery |

#### Dependencies

| Dependency | Notes |
|---|---|
| `JFrog Artifactory:latest` Integration Model | Import from [`jfrog_artifactory-latest.json`](./OpenAPIs/jfrog_artifactory-latest.json) before importing the project |
| `JFrog Artifactory` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `JFrog Artifactory` — update the `adapter_id` value in each workflow task if yours is named differently |
