Sonatype Nexus Repository Manager is a repository manager for storing, organizing, and distributing software artifacts and components across a wide range of package formats (Maven, npm, Docker, NuGet, PyPI, and more).

This project provides OpenAPI specs for automating against the Nexus Repository Manager REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for repository automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`sonatype_nexus_repository-latest.json`](#sonatype_nexus_repository-latestjson)
  - [`sonatype_nexus_repository-3.69.0-02.json`](#sonatype_nexus_repository-3690-02json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Nexus Repository REST API OpenAPI specs — curated `-latest` plus the full dated spec |

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

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`sonatype_nexus_repository-latest.json`](./OpenAPIs/sonatype_nexus_repository-latest.json) | latest (curated) | Actively-maintained, trimmed to 146 of 241 upstream operations covering common CRUD for automation — see breakdown below |
| [`sonatype_nexus_repository-3.69.0-02.json`](./OpenAPIs/sonatype_nexus_repository-3.69.0-02.json) | 3.69.0-02 | Full spec for Nexus Repository 3.69.0-02 (241 operations), including blob store, security (users/roles/privileges/LDAP/realms/certificates), email, licensing, scripting, tasks, routing rules, content selectors, Repository Firewall, and lifecycle/read-only administration. |

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
