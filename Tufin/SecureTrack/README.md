# Tufin SecureTrack

Tufin SecureTrack is the network security policy management and visibility component of the Tufin Orchestration Suite. It provides centralized discovery and monitoring of firewalls, routers, and cloud security controls; security rule and policy search across the managed device estate; network object and service inventory; and configuration revision history — all through a REST API authenticated with HTTP Basic auth against a Tufin user account (SecureTrack itself may back that account with local, RADIUS, LDAP, or TACACS+ credentials, but the wire protocol seen by Itential Platform is always Basic).

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`tufin_securetrack-latest.json`](#tufin_securetrack-latestjson)
  - [`tufin_securetrack-25.2.json`](#tufin_securetrack-252json)
- [Studio Projects](#studio-projects)
  - [Tufin SecureTrack Project](#tufin-securetrack-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | SecureTrack REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 66 curated workflows in 8 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Tufin SecureTrack | R25-2 (25.2) |
| `Tufin SecureTrack:latest` Integration Model | Import from `OpenAPIs/tufin_securetrack-latest.json` |

## Integration Configuration

Create an Itential Platform integration instance from the `Tufin SecureTrack:latest` Integration Model, authenticated with a Tufin user's HTTP Basic credentials, pointed at your SecureTrack management server (`https://<securetrack-host>/securetrack/api`). The Studio Project's workflows are wired to an integration instance named **`Tufin SecureTrack`** via `adapter_id` — if your instance uses a different name, update `adapter_id` in each workflow task after importing.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`tufin_securetrack-latest.json`](./OpenAPIs/tufin_securetrack-latest.json) | latest (curated) | 66 | Trimmed from the full 275-operation upstream spec — see breakdown below |
| [`tufin_securetrack-25.2.json`](./OpenAPIs/tufin_securetrack-25.2.json) | 25.2 | 275 | Full spec for SecureTrack R25-2 (275 operations) |

### `tufin_securetrack-latest.json`

Actively-maintained spec (`x-vendor-api-version: 25.2`). Trimmed from the full 275-operation upstream spec down to 66 operations covering common automation CRUD.

Resources included, by category:

- **Monitored Devices**: device add/update/delete (including bulk), license, and status operations
- **Security Rules**: rule search across managed devices
- **Policies and Sub-Policies**: policy and sub-policy listing/search
- **Policy Browser**: rule documentation lookups
- **Network Objects**: object CRUD
- **Services and Ports**: service/port object CRUD
- **NAT Policies**: NAT rule listing
- **Revisions**: device configuration revision history

Excluded as deep admin/analysis plumbing: network topology mapping, network zone manager (zones/subnets/patterns), policy optimization/analysis, unified security policy (violations/exceptions/alerts/zone matrix/cloud tag policy), secure cloud integration, IPsec VPN, device interfaces and zones, internet objects, change windows/authorization, application IDs, domains, LDAP, licenses, time objects, additional policy fields, and general properties.

### `tufin_securetrack-25.2.json`

Full spec for SecureTrack R25-2 (275 operations) — the vendor's complete published API surface, converted from its native Swagger 1.2 documentation format to OpenAPI 3.0. See `tufin_securetrack-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Tufin SecureTrack Project

Backed by the **Tufin SecureTrack** REST API via the `Tufin SecureTrack:latest` Integration Model. The project contains **66 workflows** — one atomic workflow per curated operation — organized into **8 folders** matching the OpenAPI resource categories above.

| Folder | Workflows |
|---|---|
| Monitored Devices | 19 |
| Policies and Sub-Policies | 11 |
| Security Rules | 8 |
| Network Objects | 7 |
| Services and Ports | 7 |
| Policy Browser (formerly Rule Documentation) | 7 |
| NAT Policies | 4 |
| Revisions | 3 |

Each workflow accepts a JSON object of the source operation's path/query parameters (and, for write operations, a `spec` object holding the request body) when run manually or called as a child workflow, and returns the full HTTP response envelope (`{ok, url, status, headers, text, body}`) from the adapter task.
