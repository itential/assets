# Tufin SecureChange

Tufin SecureChange is the network security change automation and workflow component of the Tufin Orchestration Suite. It manages the full lifecycle of firewall/network change tickets — submission, multi-step approval and design tasks, rule mapping, and closure — through a REST API authenticated with HTTP Basic auth against a Tufin user account.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`tufin_securechange-latest.json`](#tufin_securechange-latestjson)
  - [`tufin_securechange-25.2.json`](#tufin_securechange-252json)
- [Studio Projects](#studio-projects)
  - [Tufin SecureChange Project](#tufin-securechange-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | SecureChange REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 70 curated workflows in 7 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Tufin SecureChange | R25-2 (25.2) |
| `Tufin SecureChange:latest` Integration Model | Import from `OpenAPIs/tufin_securechange-latest.json` |

## Integration Configuration

Create an Itential Platform integration instance from the `Tufin SecureChange:latest` Integration Model, authenticated with a Tufin user's HTTP Basic credentials, pointed at your SecureChange management server (`https://<securechange-host>/securechangeworkflow/api`). The Studio Project's workflows are wired to an integration instance named **`Tufin SecureChange`** via `adapter_id` — if your instance uses a different name, update `adapter_id` in each workflow task after importing.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`tufin_securechange-latest.json`](./OpenAPIs/tufin_securechange-latest.json) | latest (curated) | 70 | Trimmed from the full 101-operation upstream spec — see breakdown below |
| [`tufin_securechange-25.2.json`](./OpenAPIs/tufin_securechange-25.2.json) | 25.2 | 101 | Full spec for SecureChange R25-2 (101 operations, Swagger 1.2, as published by the vendor) |

### `tufin_securechange-latest.json`

Actively-maintained spec (`x-vendor-api-version: 25.2`). Trimmed from the full 101-operation upstream spec down to 70 operations covering common automation CRUD.

Resources included, by category:

- **Tickets**: ticket submission, read, export, and step/task/field read and update
- **Ticket Lifecycle**: confirm/reject/cancel a ticket, reassign/redo a task, designer commit/update actions, rule mapping, ticket history
- **Search**: non-deprecated ticket search by details, free text, group, or saved query
- **Queries**: saved-query CRUD
- **Requests**: request search and cancel
- **SecureChange Devices**: target device lookup and suggestion for access requests
- **Workflows**: active workflow listing

Excluded as deprecated, deep admin/config plumbing, or niche: the deprecated free-text/parameter ticket search endpoints, system users, system configuration, roles, triggers, domains, attachments, change audit, extensions, external provider integration, rule recertification, and network object decommissioning.

### `tufin_securechange-25.2.json`

Full, unmodified vendor spec for SecureChange R25-2 (101 operations, Swagger 1.2, as published by Tufin) — the vendor's complete API surface, preserved as-is. Tufin publishes SecureChange's API documentation as a Swagger 1.2 resource listing plus one declaration document per resource category (fetched from `forum.tufin.com`, shared with SecureApp under the `securechangeworkflow` API path); this file consolidates the SecureChange-specific resource listing entries and declarations into a single document without altering their structure, field names, or values. See `tufin_securechange-latest.json` above for the curated subset, converted to OpenAPI 3.0, if you just need common CRUD automation.

## Studio Projects

### Tufin SecureChange Project

Backed by the **Tufin SecureChange** REST API via the `Tufin SecureChange:latest` Integration Model. The project contains **70 workflows** — one atomic workflow per curated operation — organized into **7 folders** matching the OpenAPI resource categories above.

| Folder | Workflows |
|---|---|
| Tickets | 39 |
| Ticket Lifecycle | 15 |
| Search | 4 |
| SecureChange Devices | 4 |
| Queries | 5 |
| Requests | 2 |
| Workflows | 1 |

Each workflow accepts a JSON object of the source operation's path/query parameters (and, for write operations, a `spec` object holding the request body) when run manually or called as a child workflow, and returns the full HTTP response envelope (`{ok, url, status, headers, text, body}`) from the adapter task.
