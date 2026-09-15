# Tufin SecureApp

Tufin SecureApp is the application-centric network security management component of the Tufin Orchestration Suite. It models business applications as collections of servers, connections, and services, and maps that application connectivity to the underlying network security policy — through a REST API authenticated with HTTP Basic auth against a Tufin user account.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`tufin_secureapp-latest.json`](#tufin_secureapp-latestjson)
  - [`tufin_secureapp-25.2.json`](#tufin_secureapp-252json)
- [Studio Projects](#studio-projects)
  - [Tufin SecureApp Project](#tufin-secureapp-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | SecureApp REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 56 curated workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Tufin SecureApp | R25-2 (25.2) |
| `Tufin SecureApp:latest` Integration Model | Import from `OpenAPIs/tufin_secureapp-latest.json` |

## Integration Configuration

Create an Itential Platform integration instance from the `Tufin SecureApp:latest` Integration Model, authenticated with a Tufin user's HTTP Basic credentials, pointed at your SecureApp management server (`https://<secureapp-host>/securechangeworkflow/api`, the same server that hosts SecureChange). The Studio Project's workflows are wired to an integration instance named **`Tufin SecureApp`** via `adapter_id` — if your instance uses a different name, update `adapter_id` in each workflow task after importing.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`tufin_secureapp-latest.json`](./OpenAPIs/tufin_secureapp-latest.json) | latest (curated) | 56 | Trimmed from the full 104-operation upstream spec — see breakdown below |
| [`tufin_secureapp-25.2.json`](./OpenAPIs/tufin_secureapp-25.2.json) | 25.2 | 104 | Full spec for SecureApp R25-2 (104 operations, Swagger 1.2, as published by the vendor) |

### `tufin_secureapp-latest.json`

Actively-maintained spec (`x-vendor-api-version: 25.2`). Trimmed from the full 104-operation upstream spec down to 56 operations covering common automation CRUD.

Resources included, by category:

- **Applications**: application CRUD, history, and bulk import
- **Application Connections**: connection CRUD, extended listing, and repair
- **Application Interfaces**: interface CRUD
- **Application Servers (by application)**: per-application server CRUD, move, and impact analysis
- **Application Services (local)**: application-scoped service CRUD
- **Application Services (global)**: global service CRUD

Excluded as deep admin/config plumbing or niche: application packs (bulk export/import), customers, application migration, access portal, application users, cloud console, the cross-application server registry (duplicate of the per-application server listing), load balancers, application identities, and application pending changes.

### `tufin_secureapp-25.2.json`

Full, unmodified vendor spec for SecureApp R25-2 (104 operations) — Tufin's native Swagger 1.2 documentation, preserved as published. See `tufin_secureapp-latest.json` above for the curated OpenAPI 3.0 subset if you just need common CRUD automation.

## Studio Projects

### Tufin SecureApp Project

Backed by the **Tufin SecureApp** REST API via the `Tufin SecureApp:latest` Integration Model. The project contains **56 workflows** — one atomic workflow per curated operation — organized into **6 folders** matching the OpenAPI resource categories above.

| Folder | Workflows |
|---|---|
| Applications | 14 |
| Application Interfaces | 15 |
| Application Connections | 8 |
| Application Servers (by application) | 8 |
| Application Services (global) | 6 |
| Application Services (local) | 5 |

Each workflow accepts a JSON object of the source operation's path/query parameters (and, for write operations, a `spec` object holding the request body) when run manually or called as a child workflow, and returns the full HTTP response envelope (`{ok, url, status, headers, text, body}`) from the adapter task.
