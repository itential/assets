# Micetro

Micetro (by Men and Mice) is a DDI (DNS-DHCP-IPAM) management platform, providing unified management of DNS zones and records, DHCP scopes, reservations, and address pools, and IP address space across on-prem and cloud networks.

This project provides OpenAPI specs for automating against Micetro's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`micetro-latest.json`](#micetro-latestjson)
  - [`micetro-2.0.json`](#micetro-20json)
- [Studio Projects](#studio-projects)
  - [Micetro Project](#micetro-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Micetro REST API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 96 workflows in 3 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Micetro:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `micetro-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Micetro server.

Authentication is HTTP Basic Auth, using the login name/password of a Micetro user. The REST API also supports Bearer session tokens, NTLM, and Kerberos, but Basic Auth is used here since it needs no separate session-login call.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "BasicAuth": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-micetro-host>",
    "base_path": "/mmws/api/v2"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`micetro-latest.json`](./OpenAPIs/micetro-latest.json) | latest (curated) | 96 | Curated to DNS, DHCP, and IPAM CRUD — see breakdown below |
| [`micetro-2.0.json`](./OpenAPIs/micetro-2.0.json) | 2.0 | 511 | Full spec for the Micetro REST API, version 2.0 |

### `micetro-latest.json`

Built directly from Micetro's own official OpenAPI 3.0 spec, curated to the core DDI categories.

Resources included, by category:

- **DNS**: zones, records (including related-record lookups), servers, views
- **DHCP**: scopes, reservations, servers, superscopes, address pools, exclusions, groups, leases, failover relationships
- **IPAM**: organizations, IP address ranges (including address blocks and subranges), IP address records (including ping and next-free-address lookups)

Excluded: Active Directory sites/forests/site links, appliances, change requests, cloud service accounts/networks, connectable devices/interfaces, folders, metrics, reports, roles, and user/group administration — all outside DDI CRUD automation scope. Within the kept categories, per-object access control lists, event history, and custom property definition administration were also dropped as administrative long tail, not CRUD automation. The deprecated `addressSpaces` endpoints were replaced with their `organizations` successor.

### `micetro-2.0.json`

Full, unmodified vendor spec for the Micetro REST API, version 2.0 — the vendor's complete API surface, preserved as-is. See `micetro-latest.json` above for the curated subset if you just need common DDI automation.

## Studio Projects

### Micetro Project

Backed by the **`Micetro:latest`** Integration Model (see [`micetro-latest.json`](./OpenAPIs/micetro-latest.json) above). The project contains **96 workflows** organized into **3 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| DHCP | 50 | Scopes, reservations, servers, superscopes, address pools, exclusions, groups, leases, failover relationships |
| DNS | 24 | Zones, records, servers, views |
| IPAM | 22 | Organizations, IP address ranges, IP address records |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `Micetro:latest` Integration Model | Import from [`micetro-latest.json`](./OpenAPIs/micetro-latest.json) before importing the project |
| `Micetro` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Micetro` — update the `adapter_id` value in each workflow task if yours is named differently |
