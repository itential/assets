Cisco Meraki Dashboard is a cloud-managed networking platform covering wireless, switching, security appliances, and device management across organizations and networks.

This project provides two complementary ways to automate against Meraki:

- **Studio Project workflows** built on the **Meraki Adapter** — network creation and device claim workflows, plus sample use-case workflows.
- **OpenAPI specs** for building new automation directly against the Meraki Dashboard API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for network automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Adapter (Studio Project workflows)](#adapter-studio-project-workflows)
  - [Integration Model (OpenAPI-based automation)](#integration-model-openapi-based-automation)
- [Studio Projects](#studio-projects)
  - [Meraki Project](#meraki-project)
- [Automations](#automations)
- [OpenAPIs](#openapis)
  - [`cisco_meraki_dashboard-latest.json`](#cisco_meraki_dashboard-latestjson)
  - [`cisco_meraki_dashboard-1.48.0.json`](#cisco_meraki_dashboard-1480json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Meraki Dashboard API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing network/device workflows |
| [Automations/](./Automations/) | Standalone exported sample-use-case workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Meraki Adapter | Required for the Studio Project workflows below |
| Meraki Integration Model | Required only if building new automation directly against the OpenAPI specs |

## Integration Configuration

### Adapter (Studio Project workflows)

Install the [Meraki Adapter](https://gitlab.com/itentialopensource/adapters/adapter-meraki) and configure an instance in **Admin > Adapters**, then update the `adapterId` value in each workflow task to match your instance name before importing.

### Integration Model (OpenAPI-based automation)

To build automation directly against the Dashboard API instead, import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Meraki Dashboard API base URL (e.g. `api.meraki.com`).

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <your-meraki-api-key>
```

Generate an API key in the Meraki Dashboard under your user profile → **My Profile** → **API access**.

---

## Studio Projects

### Meraki Project

| Workflows | Scope |
|---|---|
| Create Network | Create a network in an organization |
| Claim Network Devices | Claim devices into a network |
| Create Network and Claim Devices, Create Network and Claim Devices - Reset | Sample use-case workflows chaining the two above |

#### Dependencies

| Dependency | Notes |
|---|---|
| [Meraki Adapter](https://gitlab.com/itentialopensource/adapters/adapter-meraki) | Required for the Studio Project workflows. Update `adapterId` in each workflow task to match your instance name. |

## Automations

- [Create Network and Claim Devices](./Automations/Create%20Network%20and%20Claim%20Devices.json)
- [Create Network and Claim Devices - Reset](./Automations/Create%20Network%20and%20Claim%20Devices%20-%20Reset.json)

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
