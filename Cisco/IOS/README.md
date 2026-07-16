# Cisco IOS

Cisco IOS is the network operating system running Cisco's routers and switches — a mature CLI-driven platform (spanning IOS and IOS-XE) widely deployed across enterprise and service provider networks.

This project provides a Studio Project covering software upgrade, port turn-up, golden configuration compliance, and inventory management for Cisco IOS devices — see **Projects** below.

**Requirements:** Itential Platform >= 6.4 · Itential Automation Gateway >= 5.0

## Table of Contents

- [Contents](#contents)
- [Inventory Manager Configuration](#inventory-manager-configuration)
  - [Node Attributes](#node-attributes)
- [Projects](#projects)
  - [Cisco IOS](#cisco-ios-1)
- [Golden Configurations](#golden-configurations)
  - [Cisco IOS - Simple](#cisco-ios---simple)
  - [Cisco IOS - Jinja2](#cisco-ios---jinja2)
  - [Cisco IOS - Lab](#cisco-ios---lab)

## Contents

| Asset | Description |
|---|---|
| [Projects/Cisco IOS](./Projects/Cisco%20IOS.project.json) | Itential Platform project — software upgrade, port turn-up, compliance, inventory management |
| [Golden Configurations/Cisco IOS - Simple](./Golden%20Configurations/Cisco%20IOS%20-%20Simple.json) | Golden config tree using literal matching |
| [Golden Configurations/Cisco IOS - Jinja2](./Golden%20Configurations/Cisco%20IOS%20-%20Jinja2.json) | Golden config tree using Jinja2 expressions for flexible value matching |
| [Golden Configurations/Cisco IOS - Lab](./Golden%20Configurations/Cisco%20IOS%20-%20Lab.json) | Golden config tree for lab baseline configuration |

---

## Inventory Manager Configuration

Itential Platform ships with a netmiko driver for Cisco IOS. Broker actions (`is-alive`, `run-command`, `get-config`, `set-config`) are wired automatically when the inventory is created with `createBrokerActions: true` — no manual action configuration is required.

### Node Attributes

Set these attributes on each node in Inventory Manager:

```json
{
  "name": "my-ios-device",
  "attributes": {
    "itential_host": "192.0.2.1",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "cisco_ios",
    "itential_user": "username",
    "itential_password": "changeme",
    "itential_driver_options": {
      "netmiko": {
        "banner_timeout": 60,
        "conn_timeout": 60,
        "enable_fast_mode": true,
        "global_delay_factor": 3,
        "read_timeout_override": 600,
        "session_timeout": 300
      }
    }
  }
}
```

| Attribute | Type | Unit | Description |
|---|---|---|---|
| `itential_host` | string | — | Management IP or hostname of the device |
| `itential_port` | integer | — | SSH port (default: `22`) |
| `itential_driver` | string | — | Driver to use — must be `netmiko` |
| `itential_platform` | string | — | Netmiko device type — `cisco_ios` for IOS/IOS-XE |
| `itential_user` | string | — | SSH username |
| `itential_password` | string | — | SSH password |
| `banner_timeout` | integer | seconds | Time to wait for the login banner before timing out |
| `conn_timeout` | integer | seconds | TCP connection timeout |
| `enable_fast_mode` | boolean | — | Skip unnecessary delays between commands when `true` |
| `global_delay_factor` | integer | — | Multiplier applied to all internal netmiko delays — increase for slow devices |
| `read_timeout_override` | integer | seconds | Override the default read timeout for command responses |
| `session_timeout` | integer | seconds | Max lifetime of the SSH session |

---

## Projects

### Cisco IOS

An Itential Platform project covering software upgrade, port turn-up, golden configuration compliance, and inventory management for Cisco IOS devices, organized into four folders.

**Software Upgrade**
- **IOS Upgrade** — stages the image, runs pre/post checks, installs, and reloads
- Command templates: File Verification · Pre and Post Checks · Reload · Show Version
- Form: **Upgrade Form** — input for device name, target version, and image path on device

> **Before importing:** The Upgrade Form contains example image paths
> (`bootflash:/c8000v-universalk9.17.15.01a.SPA.bin`, `bootflash:/c8000v-universalk9.17.15.03a.SPA.bin`)
> for specific C8000v images. Update the form's `enum` field under "Image Path on Device"
> to match the software images staged in your environment.

**Port Turn Up**
- **Port Turn Up** — configure and activate an interface
- Template: Port Turn Up
- Command templates: Pre-Checks · Post-Checks
- Form: **Port Turn Up Form** — input for device, interface type, interface, sub-interface, description, IP address, subnet mask, and VLAN

**Golden Configuration**
- **Run Compliance** — runs a compliance check against a golden config tree
- Form: **Compliance Form** — select the golden config tree name and version to run against

**Inventory Management**
- **Create & Update Inventory from NetBox** — creates or updates an Inventory Manager inventory using NetBox as the source of truth
- **Clear & Delete Inventory** — removes all nodes from an inventory and deletes it

---

## Golden Configurations

Three golden configuration trees are provided. All ship with no device bindings — bind each tree to your devices in Config Manager after importing.

### Cisco IOS - Simple

Device type: `cisco-ios`

Baseline configuration using literal matching. Use this as a starting point when all devices in a group are expected to share identical configuration values with no variation.

### Cisco IOS - Jinja2

Device type: `cisco-ios`

Baseline configuration using Jinja2 template expressions for flexible value matching. Use this when your environment has multiple allowed values for a field — for example, permitting two software versions during a phased upgrade rollout.

### Cisco IOS - Lab

Device type: `cisco-ios`

Lab baseline configuration. Captures a reference configuration for lab devices — useful as a starting point before tailoring to production standards.
