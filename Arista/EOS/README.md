# Arista EOS

Arista EOS is the network operating system running Arista's switches and routers — a single Linux-based image spanning campus, data center, and cloud networking hardware, with a programmatic API (eAPI) and extensible CLI.

This project provides a Studio Project covering software upgrade, port turn-up, golden configuration compliance, and inventory management for Arista EOS devices — see **Projects** below.

**Requirements:** Itential Platform >= 6.4 · Itential Automation Gateway >= 5.0

## Table of Contents

- [Contents](#contents)
- [Inventory Manager Configuration](#inventory-manager-configuration)
  - [Node Attributes](#node-attributes)
- [Projects](#projects)
  - [Arista EOS](#arista-eos-1)

## Contents

| Asset | Description |
|---|---|
| [Studio Projects/Arista EOS](./Studio%20Projects/Arista%20EOS.project.json) | Itential Platform project — software upgrade, port turn-up, compliance, inventory management |

---

## Inventory Manager Configuration

Device targeting uses Itential Platform's native Inventory Manager, not an Automation Gateway Ansible inventory. Each workflow's `device` input is an Inventory Manager identifier in `{inventoryName}::{nodeName}` format (e.g. `Arista Lab::switch-01`) — command-template checks (`MOP.RunCommandTemplate`) and device lookups (`ConfigurationManager.getDevice`) resolve directly against that inventory.

Actual configuration pushes go through an Itential Automation Gateway 5.x cluster via `GatewayManager.sendConfig`, targeting the cluster by ID (the shipped workflows use `cluster-itential` as an example — update this to match your own IAG5 cluster name before importing). Set up the inventory and the IAG5 cluster mapping using the **Inventory Management** workflows below, or directly in Inventory Manager / Admin Essentials.

### Node Attributes

Set these attributes on each node in Inventory Manager — the netmiko driver handles command-template checks and device lookups directly:

```json
{
  "name": "switch-01",
  "attributes": {
    "itential_host": "192.0.2.10",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "arista_eos",
    "itential_user": "username",
    "itential_password": "changeme"
  }
}
```

| Attribute | Type | Description |
|---|---|---|
| `itential_host` | string | Management IP or hostname of the device |
| `itential_port` | integer | SSH port (default: `22`) |
| `itential_driver` | string | Driver to use — must be `netmiko` |
| `itential_platform` | string | Netmiko device type — `arista_eos` for EOS |
| `itential_user` | string | SSH username |
| `itential_password` | string | SSH password |

This covers the read/check side (`MOP.RunCommandTemplate`, `ConfigurationManager.getDevice`). The actual config push (`GatewayManager.sendConfig`) is separate — it targets an IAG5 cluster by `clusterId`, not the node's netmiko attributes directly, so the IAG5 cluster also needs its own device credentials configured independently.

---

## Projects

### Arista EOS

An Itential Platform project covering software upgrade, port turn-up, golden configuration compliance, and inventory management for Arista EOS devices, organized into four folders.

**Software Upgrade**
- **EOS Upgrade** — stages the image, runs pre/post checks, installs, and reloads
- Command templates: File Verification · Pre and Post Checks · Reload · Show Version
- Form: **Upgrade Form** — input for device, target version, and image path on device

**Port Turn Up**
- **Port Turn Up** — configure and activate an interface
- Template: Port Turn Up
- Command templates: Pre Checks · Post Checks
- Form: **Port Turn Up Form** — input for device, interface type, interface ID, description, IP address, and CIDR prefix

> **Note:** The Port Turn Up Form collects the interface ID and CIDR prefix directly (e.g. `1.100`, `30`) rather than separate interface/sub-interface/subnet-mask fields — enter the values pre-combined.

**Golden Configuration**
- **Run Compliance** — runs a compliance check against a golden config tree
- Form: **Compliance Form** — select the golden config tree name and version to run against

> Unlike Cisco IOS, this project doesn't yet ship standalone golden config tree exports under a `Golden Configurations/` folder — **Run Compliance** expects a tree you've already created in Configuration Manager, referenced by name via the form.

**Inventory Management**
- **Create & Update Inventory from NetBox** — creates or updates an Inventory Manager inventory using NetBox as the source of truth
- **Clear & Delete Inventory** — removes all nodes from an inventory and deletes it
