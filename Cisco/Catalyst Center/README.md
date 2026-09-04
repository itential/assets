Cisco Catalyst Center (formerly DNA Center) is the centralized management platform for Cisco's enterprise campus and branch networks, covering device inventory and onboarding, SD-Access fabric provisioning, configuration templates, software image management, and network-wide compliance and settings.

This project provides OpenAPI specs for automating against Catalyst Center's REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_catalyst_center-latest.json`](#cisco_catalyst_center-latestjson)
  - [`cisco_catalyst_center-3.1.3.json`](#cisco_catalyst_center-313json)
- [Studio Projects](#studio-projects)
  - [Cisco Catalyst Center Project](#cisco-catalyst-center-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco Catalyst Center OpenAPI specs — curated `-latest` plus the full vendor v3.1.3 export |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 382 workflows in 15 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Cisco Catalyst Center:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `cisco_catalyst_center-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Catalyst Center appliance.

Authentication is a token retrieved dynamically: `POST /dna/system/api/v1/auth/token` with HTTP Basic credentials returns a JSON body containing the token, which is then sent as the `X-Auth-Token` header on every subsequent call. Itential Platform automates the whole exchange — you only need to supply a pre-encoded Basic credential once.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "X-Auth-Token": {
      "value": "",
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://<catalyst-center-hostname-or-ip>/dna/system/api/v1/auth/token",
        "responsePointer": "/Token"
      },
      "parameters": {
        "Authorization": "Basic <base64(username:password)>"
      }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<catalyst-center-hostname-or-ip>",
    "base_path": ""
  }
}
```

Substitute your appliance's hostname/IP in both the `dynamicRetrieval.url` and `server.host` fields, and pre-encode your username/password as a standard HTTP Basic credential for the `Authorization` parameter (`base64("username:password")`, prefixed with `Basic `). The platform re-retrieves the token automatically on expiry.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_catalyst_center-latest.json`](./OpenAPIs/cisco_catalyst_center-latest.json) | latest (curated) | 382 | Curated to core network automation — see breakdown below |
| [`cisco_catalyst_center-3.1.3.json`](./OpenAPIs/cisco_catalyst_center-3.1.3.json) | 3.1.3 | 1298 | Full vendor spec, release 3.1.3 |

### `cisco_catalyst_center-latest.json`

Trimmed from the vendor's 962-path (1298-operation) full v3.1.3 export to 382 operations covering core network automation.

Resources included, by category:

- **SDA Fabric** (89 ops): fabric sites/zones, devices, L2/L3 virtual networks, anycast gateways, port assignments, transits, multicast, provisioning
- **Network Settings** (54 ops): site-level AAA, DHCP, DNS, NTP, telemetry, IP address pools, reserve/release
- **Software Image Management (SWIM)** (44 ops): image inventory, distribute/activate, golden tagging, readiness checks
- **Configuration Templates** (33 ops): project + template CRUD, deploy, preview, version management
- **Devices** (32 ops): inventory list/query/CRUD, config reads, interface lookup, site assignment
- **Device Onboarding (PnP)** (28 ops): full PnP device lifecycle — claim, unclaim, reset, site-claim, workflows
- **Tag** (20 ops): tag CRUD plus device/interface membership in bulk
- **Site Design** (20 ops): areas, buildings, sites CRUD
- **Discovery** (16 ops): create/manage discovery jobs, list discovered devices
- **LAN Automation** (14 ops): start/stop sessions, status, port channels
- **Compliance** (9 ops): run compliance, view detail, remediate
- **Task** (9 ops): async task/activity polling
- **Configuration Archive** (5 ops): list/download device config snapshots (masked and unmasked)
- **Topology** (5 ops): L2/L3/physical topology
- **System Settings** (4 ops): global credentials, Smart Account list

Excluded from this curated file, and available in the full spec below: analytics/trend data, the deprecated `business/sda` API (superseded by `/sda/*` in v2.3+), wireless-only endpoints (SSID, FlexConnect, AP management), hardware detail reads (chassis, PoE, line-card, supervisor-card), UI/admin endpoints (autocomplete, resync intervals, user-defined fields), advisory/bug scan data, lifecycle operations (maintenance schedules, RMA, licenses), old paginated APIs superseded by filter-based equivalents, and one internal vendor test-only endpoint with no `operationId`.

### `cisco_catalyst_center-3.1.3.json`

Full, unmodified vendor spec for Catalyst Center release 3.1.3 — the vendor's complete API surface, preserved as-is. See `cisco_catalyst_center-latest.json` above for the curated subset if you just need core network automation.

## Studio Projects

### Cisco Catalyst Center Project

Backed by the **`Cisco Catalyst Center:latest`** Integration Model (see [`cisco_catalyst_center-latest.json`](./OpenAPIs/cisco_catalyst_center-latest.json) above). The project contains **382 workflows** organized into **15 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| SDA | 89 | Fabric sites/zones, devices, virtual networks, provisioning |
| Network Settings | 54 | Site-level AAA/DHCP/DNS/NTP, IP address pools |
| Software Image Management (SWIM) | 44 | Image inventory, distribute/activate, golden tagging |
| Configuration Templates | 33 | Project + template CRUD, deploy, preview |
| Devices | 32 | Inventory, config reads, interface lookup, site assignment |
| Device Onboarding (PnP) | 28 | Full PnP device lifecycle |
| Tag | 20 | Tag CRUD, device/interface membership |
| Site Design | 20 | Areas, buildings, sites CRUD |
| Discovery | 16 | Discovery jobs, discovered device listing |
| LAN Automation | 14 | Session start/stop, status, port channels |
| Compliance | 9 | Run compliance, view detail, remediate |
| Task | 9 | Async task/activity polling |
| Configuration Archive | 5 | Device config snapshot list/download |
| Topology | 5 | L2/L3/physical topology |
| System Settings | 4 | Global credentials, Smart Account list |

A handful of workflow names (Create/Get/Delete/Update Tag, Device, Network, Project, and Delete Image) are prefixed with `Cisco Catalyst Center` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Cisco Catalyst Center:latest` Integration Model | Import from [`cisco_catalyst_center-latest.json`](./OpenAPIs/cisco_catalyst_center-latest.json) before importing the project |
| `Cisco Catalyst Center` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Cisco Catalyst Center` — update the `adapter_id` value in each workflow task if yours is named differently |
