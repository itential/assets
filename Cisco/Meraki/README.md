Cisco Meraki Dashboard is a cloud-managed networking platform covering wireless, switching, security appliances, and device management across organizations and networks.

This project provides a Studio Project of workflows covering the Dashboard API operations most useful for network automation, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_meraki_dashboard-latest.json`](#cisco_meraki_dashboard-latestjson)
  - [`cisco_meraki_dashboard-1.48.0.json`](#cisco_meraki_dashboard-1480json)
- [Studio Projects](#studio-projects)
  - [Cisco Meraki Project](#cisco-meraki-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Meraki Dashboard API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 162 workflows in 8 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Cisco Meraki Dashboard:latest` Integration Model | Required to build automation against the OpenAPI specs, and to run the Studio Project below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the Meraki Dashboard API.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the Meraki Dashboard API (`api.meraki.com`).

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <your-meraki-api-key>
```

Generate an API key in the Meraki Dashboard under your user profile → **My Profile** → **API access**.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_meraki_dashboard-latest.json`](./OpenAPIs/cisco_meraki_dashboard-latest.json) | latest (curated) | 357 | Actively-maintained, trimmed to 357 of 729 upstream operations covering common CRUD for network automation — see breakdown below |
| [`cisco_meraki_dashboard-1.48.0.json`](./OpenAPIs/cisco_meraki_dashboard-1.48.0.json) | 1.48.0 | 729 | Full, unmodified vendor spec |

### `cisco_meraki_dashboard-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.48.0`). Trimmed to 357 of 729 upstream operations covering common CRUD for network automation. The full upstream spec also covers Systems Manager (MDM), cameras, sensors, cellular gateways, Insight, adaptive policy, licensing, branding, and SAML — none of those are included here. Pull the full spec from [Meraki's official OpenAPI spec](https://developer.cisco.com/meraki/api-v1/) if you need one of the excluded areas.

Resources included, by category:

- **Organizations**: Organizations, Admins, Config Templates, Action Batches, Inventory, Claim
- **Networks**: Networks, Clients, Alerts, Webhooks, Settings, Config Template Bind/Unbind/Split
- **Wireless**: SSIDs and wireless network configuration
- **Appliance**: VLANs, firewall rules, VPN, and MX appliance configuration
- **Switch**: Switch ports, VLANs, and switch configuration
- **VLAN Profiles & Group Policies**: Network-wide VLAN profiles and group policies
- **Firmware**: Firmware upgrade scheduling
- **Devices**: Claim/inventory, management interface, reboot, blink LEDs, clients

### `cisco_meraki_dashboard-1.48.0.json`

Full, unmodified vendor spec for the Meraki Dashboard API (729 operations) — the vendor's complete API surface, preserved as-is. See `cisco_meraki_dashboard-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### Cisco Meraki Project

Backed by the **`Cisco Meraki Dashboard:latest`** Integration Model (see [`cisco_meraki_dashboard-latest.json`](./OpenAPIs/cisco_meraki_dashboard-latest.json) above). The project contains **162 workflows** organized into **8 folders**, one workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List RF Profiles`, `Update Wireless Settings`).

Scoped to core configuration CRUD rather than every operation in the curated spec — read/write settings, policy objects, and device/network lifecycle actions someone would realistically automate. Pure telemetry, history, and analytics endpoints (client usage history, connection/latency stats, device status overviews, etc.) are left out, since they're read-only reporting data rather than something a workflow drives.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Organizations | 25 | Organization, Admin, Config Template, Action Batch, Inventory Device (+ claim/release), Network create/list |
| Networks | 20 | Network, Network Device (+ claim/remove), Network Settings, Alert Settings, Group Policy, Webhook HTTP Server |
| Wireless | 24 | SSID, RF Profile, Wireless Settings, Air Marshal Rule, SSID Identity PSK, Ethernet Ports Profile |
| Appliance | 36 | VLAN (+ settings), L3/L7 Firewall Rules, Firewalled Service, Port Forwarding, 1:1/1:Many NAT, Site-to-Site VPN, Static Route, Appliance Port, Content Filtering, Traffic Shaping Rules, Warm Spare (+ swap) |
| Switch | 32 | Access Policy, Access Control Lists, Switch Stack, Link Aggregation, Port Schedule, QoS Rule, STP, Storm Control, DHCP Server Policy, Switch Settings |
| VLAN Profiles & Group Policies | 5 | VLAN Profile |
| Firmware | 14 | Firmware Upgrades (+ rollback), Staged Upgrade Group/Stages/Events (+ defer) |
| Devices | 6 | Device (+ reboot, blink LEDs), Device Management Interface |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Cisco Meraki Dashboard:latest` Integration Model | Import from [`cisco_meraki_dashboard-latest.json`](./OpenAPIs/cisco_meraki_dashboard-latest.json) before importing the project |
| `Meraki` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Meraki` — update the `adapter_id` value in each workflow task if yours is named differently |

**Testing status:** all 162 workflows were created and schema-validated against a running Itential Platform instance. A representative sample — `List Organizations`, `List Networks`, and `List Inventory Devices` — was executed against a real Meraki Dashboard organization and confirmed returning live data. The remaining workflows have not been individually executed against a real organization.
