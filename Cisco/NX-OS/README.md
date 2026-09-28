# Cisco NX-OS

Cisco NX-OS is the network operating system running Cisco's Nexus switches — a modular, feature-gated CLI platform deployed across data center access, aggregation, and spine-and-leaf fabrics.

This project provides a Studio Project covering software upgrade, port turn-up, golden configuration compliance, and inventory management for Cisco NX-OS devices — see **Projects** below.

**Requirements:** Itential Platform >= 6.4 · Itential Gateway >= 5.0

## Table of Contents

- [Contents](#contents)
- [Inventory Manager Configuration](#inventory-manager-configuration)
  - [Node Attributes](#node-attributes)
- [Projects](#projects)
  - [Cisco NX-OS](#cisco-nx-os-1)
- [Golden Configurations](#golden-configurations)
  - [Cisco NX-OS - Simple](#cisco-nx-os---simple)
  - [Cisco NX-OS - Jinja2](#cisco-nx-os---jinja2)
  - [Cisco NX-OS - Lab](#cisco-nx-os---lab)

## Contents

| Asset | Description |
|---|---|
| [Studio Projects/Cisco NX-OS](./Studio%20Projects/Cisco%20NX-OS.project.json) | Itential Platform project — software upgrade, port turn-up, compliance, inventory management |
| [Golden Configurations/Cisco NX-OS - Simple](./Golden%20Configurations/Cisco%20NX-OS%20-%20Simple.json) | Golden config tree using literal matching |
| [Golden Configurations/Cisco NX-OS - Jinja2](./Golden%20Configurations/Cisco%20NX-OS%20-%20Jinja2.json) | Golden config tree using Jinja2 expressions and a regex version match |
| [Golden Configurations/Cisco NX-OS - Lab](./Golden%20Configurations/Cisco%20NX-OS%20-%20Lab.json) | Golden config tree for lab baseline configuration |

---

## Inventory Manager Configuration

Itential Platform ships with a netmiko driver for Cisco NX-OS. Broker actions (`is-alive`, `run-command`, `get-config`, `set-config`) are wired automatically when the inventory is created with `createBrokerActions: true` — no manual action configuration is required.

### Node Attributes

Set these attributes on each node in Inventory Manager:

```json
{
  "name": "my-nxos-device",
  "attributes": {
    "itential_host": "192.0.2.1",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "cisco_nxos",
    "itential_user": "username",
    "itential_password": "changeme",
    "itential_driver_options": {
      "netmiko": {
        "banner_timeout": 60,
        "conn_timeout": 60,
        "enable_fast_mode": true,
        "global_delay_factor": 3,
        "read_timeout_override": 1800,
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
| `itential_platform` | string | — | Netmiko device type — `cisco_nxos` for NX-OS |
| `itential_user` | string | — | SSH username |
| `itential_password` | string | — | SSH password |
| `banner_timeout` | integer | seconds | Time to wait for the login banner before timing out |
| `conn_timeout` | integer | seconds | TCP connection timeout |
| `enable_fast_mode` | boolean | — | Skip unnecessary delays between commands when `true` |
| `global_delay_factor` | integer | — | Multiplier applied to all internal netmiko delays — increase for slow devices |
| `read_timeout_override` | integer | seconds | Override the default read timeout for command responses |
| `session_timeout` | integer | seconds | Max lifetime of the SSH session |

> **On `read_timeout_override`:** `install all` runs as one long command that can hold the
> session for more than ten minutes before the switch reloads. The `1800` above is sized for
> that; lower it if you don't use **NX-OS Upgrade**.

> **Reaching Configuration Manager:** the workflows reach the switch through Configuration
> Manager. If a node never appears there, add its inventory to the Device Broker adapter's
> `inventories` list and give the node a `cluster_id` attribute naming your Gateway cluster.

---

## Projects

### Cisco NX-OS

An Itential Platform project covering software upgrade, port turn-up, golden configuration compliance, and inventory management for Cisco NX-OS devices, organized into four folders.

**Software Upgrade**
- **NX-OS Upgrade** — runs pre-checks, verifies the staged image, installs it with `install all` (the switch reloads itself), waits for the new version, and runs post-checks
- Command templates: File Verification · Install · Pre and Post Checks · Show Version
- Form: **Upgrade Form** — input for device name, target version, and image path on device

> **Before importing:** The Upgrade Form contains example image paths
> (`bootflash:///nxos64-cs.10.4.5.M.bin`, `bootflash:///nxos64-cs.10.5.3.F.bin`).
> Update the form's `enum` field under "Image Path on Device" to match the software images
> staged in your environment. Enter the target version as `show version` prints it, for
> example `10.5(3)`.

**Port Turn Up**
- **Port Turn Up** — configure and activate a Layer 3 sub-interface
- Template: Port Turn Up
- Command templates: Pre-Checks · Post-Checks
- Form: **Port Turn Up Form** — input for device, interface type, interface, sub-interface, description, IP address, subnet mask, and VLAN

> **On NX-OS interfaces:** the Interface field is a slot/port string (`1/1`). The template
> makes the parent a routed, enabled port first, which NX-OS sub-interfaces need. The
> pre-check stops the run if the sub-interface already exists; it matches the name as NX-OS
> prints it, so pass the type as `Ethernet` or `port-channel`, never an abbreviation.

> **Before importing:** the **Send Config: Port Turn Up** task's `clusterId`
> (`cluster-itential`) is environment-specific — set it to your Gateway cluster name.

**Golden Configuration**
- **Run Compliance** — runs a compliance check against a golden config tree
- Form: **Compliance Form** — select the golden config tree name and version to run against

> **Before importing:** the **Get treeId** task's `clusterId` (`cluster-itential`) is
> environment-specific — set it to your Gateway cluster name.

**Inventory Management**
- **Create & Update Inventory from NetBox** — creates or updates an Inventory Manager inventory using NetBox as the source of truth, filtered to devices whose NetBox platform is `cisco-nxos`
- **Clear & Delete Inventory** — removes all nodes from an inventory and deletes it

> **Before importing:** **Create & Update Inventory from NetBox** uses the `NetBox:latest`
> Integration Model. Import [`NetBox/OpenAPIs/netbox-latest.json`](../../NetBox/OpenAPIs/netbox-latest.json)
> as an Integration Model and create an integration instance from it, then set:
> - the NetBox task's `adapter_id` (`netbox-latest`) — the name of that integration instance
> - the `createInventory` task's `defaultClusterId` (`cluster-itential`) — your Gateway cluster name
> - the `createInventory` task's `groups` (`admins`) — a group with the `inventory:read` and `inventory:update` roles
>
> If your NetBox uses a platform slug other than `cisco-nxos`, change the task's `platform`
> filter and add the slug to the payload's `platform_map` (it already accepts `nxos` and `nx-os`).

---

## Golden Configurations

Three golden configuration trees are provided. All ship with no device bindings — bind each tree to your devices in Config Manager after importing.

> **On the device type:** the trees use `cisco-nx`, the name of Config Manager's NX-OS config
> parser. It is not the NetBox platform slug `cisco-nxos`, and a tree whose device type names
> no parser fails with `No config parser found for the given device type`.

> **On NX-OS defaults:** `show running-config` hides settings left at their default, so the
> trees never require a line that only restates one (`feature ssh`). To forbid a feature that
> is off by default, they mark its enabled form disallowed, as with `feature telnet`.

### Cisco NX-OS - Simple

Device type: `cisco-nx`

Baseline configuration using literal matching. Use this as a starting point when all devices in a group are expected to share identical configuration values with no variation.

### Cisco NX-OS - Jinja2

Device type: `cisco-nx`

Baseline configuration using Jinja2 template expressions and a regex version match for flexible value matching. Use this when your environment has multiple allowed values for a field — the version line matches any `10.4(x)` or `10.5(x)` release, permitting a phased upgrade rollout.

### Cisco NX-OS - Lab

Device type: `cisco-nx`

Lab baseline configuration. Captures a reference configuration for lab devices — useful as a starting point before tailoring to production standards.
