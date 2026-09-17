# Forward Networks

Forward Networks builds a continuously updated digital twin of a network from device configuration and state, used for verification, path search, security and compliance checks, and network-wide querying via the Network Query Engine (NQE).

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`forward_networks-latest.json`](#forward_networks-latestjson)
  - [`forward_networks-26.1.json`](#forward_networks-261json)
- [Studio Projects](#studio-projects)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Forward Networks REST API OpenAPI specs — curated `-latest` plus the full dated version |
| [Studio Projects/](./Studio%20Projects/) | One workflow per curated operation, organized by resource category |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Forward Networks Platform | 26.1 (see OpenAPIs below) |
| Forward Networks Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is HTTP Basic auth, using a Forward Networks API access key as the username and its matching secret as the password on every request. Generate an access key/secret pair in Forward Networks under your user account's API access settings, then configure the Integration's basic-auth credentials in Itential Platform's Admin Essentials with the key as the username and the secret as the password.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`forward_networks-latest.json`](./OpenAPIs/forward_networks-latest.json) | latest (curated) | 71 | Trimmed to 71 of 181 upstream operations covering common CRUD for network automation — see breakdown below |
| [`forward_networks-26.1.json`](./OpenAPIs/forward_networks-26.1.json) | 26.1 | 181 | Full spec for Forward Networks 26.1. |

### `forward_networks-latest.json`

Actively-maintained spec (`x-vendor-api-version: 26.1`). Trimmed to 71 of 181 upstream operations covering common CRUD for network automation.

Resources included, by category:

- **Networks**: List, Create, Delete, Update
- **Network Devices**: List Devices, Get Device, List Device Files, Get Device File Content, List Missing Devices
- **Classic Devices**: List, Create, Update (batch), Get, Update (upsert), Delete, Update
- **Network Endpoints**: Endpoint Profiles (List, Get, Delete, Create CLI/HTTP/SNMP, Update CLI/HTTP/SNMP) and Network Endpoints (List, Get, Delete, Create CLI/HTTP/SNMP, Update CLI/HTTP/SNMP)
- **Credentials**: CLI Credentials and HTTP Credentials (List, Create, Batch Create, Get, Delete, Update)
- **Jump Servers**: List, Create, Delete, Update
- **Device Tags**: List, Create, Get, Delete, Update
- **NQE**: Run Query, Diff Query Results, List Queries
- **Checks**: List Predefined Checks, List/Add/Deactivate Checks, Get/Deactivate a Single Check
- **Path Search**: List L7 Applications, Trace a Path, Bulk Path Trace
- **Network Snapshots**: List, Create, Get Latest Processed
- **Vulnerability Analysis**: List Vulnerabilities

### `forward_networks-26.1.json`

Full, unmodified vendor spec for Forward Networks 26.1 (181 operations) — the vendor's complete API surface, preserved as-is. See `forward_networks-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### `Forward Networks.project.json`

One workflow per curated operation from `forward_networks-latest.json`, organized into folders by resource category, wired to the `Forward Networks:latest` Integration Model.

Every workflow's adapter task is wired to the Integration instance name `Forward Networks`. After importing, either name your Integration instance `Forward Networks`, or update the `adapter_id` value in each workflow task to match your own instance name.

| Folder | Workflows |
|---|---|
| Networks | 4 |
| Network Devices | 5 |
| Classic Devices | 7 |
| Network Endpoints | 18 |
| Credentials | 12 |
| Jump Servers | 4 |
| Device Tags | 5 |
| NQE | 3 |
| Checks | 6 |
| Path Search | 3 |
| Network Snapshots | 3 |
| Vulnerability Analysis | 1 |
