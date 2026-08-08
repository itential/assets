# ARIN

The American Registry for Internet Numbers (ARIN) is the regional internet registry (RIR) responsible for IP address and Autonomous System Number (ASN) allocation in the United States, Canada, and parts of the Caribbean. It publishes two public, read-only REST services for looking up network, ASN, and organization/contact registration data: **RDAP**, the modern IETF-standardized protocol, and **Whois-RWS**, ARIN's older, ARIN-specific web service.

This project provides a Studio Project of workflows covering both services, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below. Both services are public and require no authentication.

## Table of Contents

- [ARIN](#arin)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`arin_rdap-latest.json`](#arin_rdap-latestjson)
    - [`arin_whois_rws-latest.json`](#arin_whois_rws-latestjson)
  - [Studio Projects](#studio-projects)
    - [ARIN Project](#arin-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Two peer specs — `arin_rdap-latest.json` (primary) and `arin_whois_rws-latest.json` (search-only supplement) |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 15 workflows in 2 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| `ARIN RDAP:latest` Integration Model | Required to build automation against the RDAP spec |
| `ARIN Whois-RWS Search:latest` Integration Model | Optional — only needed for the multi-field search operations RDAP doesn't support |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to ARIN's public services.

## Integration Configuration

Import `arin_rdap-latest.json` (and, optionally, `arin_whois_rws-latest.json`) as Integration Models in **Admin > Integrations**, then create an integration for each — no credentials needed.

### Connection Properties

RDAP:
```json
{
  "server": {
    "protocol": "https",
    "host": "rdap.arin.net",
    "base_path": ""
  },
  "authentication": {},
  "tls": {
    "enabled": true,
    "rejectUnauthorized": true
  },
  "variables": {},
  "version": "latest"
}
```

Whois-RWS (if used):
```json
{
  "server": {
    "protocol": "https",
    "host": "whois.arin.net",
    "base_path": ""
  },
  "authentication": {},
  "tls": {
    "enabled": true,
    "rejectUnauthorized": true
  },
  "variables": {},
  "version": "latest"
}
```

Both services are public with no API key or credential of any kind — the `authentication` block is intentionally empty.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`arin_rdap-latest.json`](./OpenAPIs/arin_rdap-latest.json) | latest | 7 | Primary spec. Every get-by-identifier and search operation ARIN's RDAP service implements. |
| [`arin_whois_rws-latest.json`](./OpenAPIs/arin_whois_rws-latest.json) | latest | 8 | Supplement. Multi-field search operations (POC by company/city, org by DBA, etc.) that RDAP's search can't match. |

### `arin_rdap-latest.json`

RDAP (Registration Data Access Protocol, RFC 7480+) is the IETF-standardized successor to legacy WHOIS, implemented consistently across all five regional internet registries (ARIN, RIPE, APNIC, LACNIC, AFRINIC) — a pattern built against ARIN's RDAP service could likely be adapted to the others with minimal changes. Its JSON is clean and native (no XML artifacts), unlike Whois-RWS.

Operations, by resource type:

- **Networks**: get by IP address, get by CIDR block
- **ASNs**: get by number, search by name
- **Entities**: get by handle, search by name — RDAP unifies organizations, points of contact, and customers into a single entity object distinguished by `roles` (registrant, administrative, technical, abuse, etc.)
- **Domains**: get reverse-DNS delegation by zone name (e.g. `252.149.192.in-addr.arpa`) — ARIN's RDAP domain search is not implemented (returns HTTP 501) and is excluded

### `arin_whois_rws-latest.json`

Whois-RWS is ARIN's older, ARIN-specific REST service. Its JSON is a direct XML-to-JSON transliteration (every leaf value wrapped as `{"$": "value"}`, attributes as `@name`) — workable, but far less pleasant to build workflows against than RDAP's clean JSON. Since RDAP already covers every get-by-identifier operation Whois-RWS offers, **this spec is scoped to only the 8 search operations where Whois-RWS is genuinely more capable than RDAP**: searching points of contact by last name, first name, company, or city; organizations by name or DBA; networks by name; and customers by name (a concept RDAP has no direct equivalent for).

Registration/management operations (create, update, delete) are provided by a third ARIN service, **Reg-RWS** — deliberately not included here. See [Generation Method and Caveats](#generation-method-and-caveats).

---

## Studio Projects

### ARIN Project

Backed by both Integration Models above. The project contains **15 workflows** organized into **2 folders** — one workflow per API operation, matching the two OpenAPI specs 1:1. Every workflow was tested against ARIN's live production services and confirmed returning real data before being committed.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| RDAP | 7 | Get Network By IP, Get Network By CIDR, Get ASN, Get Entity, Get Reverse DNS Delegation, Search Entities By Name, Search ASNs By Name |
| Whois-RWS | 8 | Search POCs By Last/First Name/Company/City, Search Organizations By Name/DBA, Search Networks By Name, Search Customers By Name |

#### Dependencies

| Dependency | Notes |
|---|---|
| `ARIN RDAP:latest` Integration Model | Import from [`arin_rdap-latest.json`](./OpenAPIs/arin_rdap-latest.json) before importing the project |
| `ARIN Whois-RWS Search:latest` Integration Model | Import from [`arin_whois_rws-latest.json`](./OpenAPIs/arin_whois_rws-latest.json) before importing the project |
| `ARIN-RDAP` integration instance | Create in **Admin > Integrations** with the RDAP connection properties above. Workflows in the RDAP folder are wired to an instance named `ARIN-RDAP` — update `adapter_id` in each task if yours is named differently |
| `ARIN-Whois` integration instance | Create with the Whois-RWS connection properties above. Workflows in the Whois-RWS folder are wired to an instance named `ARIN-Whois` |

