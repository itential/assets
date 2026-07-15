# Juniper JUNOS

Juniper JUNOS is the network operating system running Juniper's routers, switches, and security devices — a single FreeBSD-based codebase with a hierarchical, transactional configuration model exposed over NETCONF.

This project provides a NETCONF-based device driver, a Studio Project covering software upgrade, port turn-up, golden configuration compliance, and inventory management, plus golden configuration trees and a configuration parser for JUNOS `set`-format lines — see **Device Drivers**, **Projects**, and **Golden Configurations** below.

**Requirements:** Itential Platform >= 6.4 · Itential Gateway >= 5.4

## Table of Contents

- [Contents](#contents)
- [Inventory Manager Configuration](#inventory-manager-configuration)
  - [Action Configuration](#action-configuration)
  - [Node Attributes](#node-attributes)
- [Device Drivers](#device-drivers)
  - [netconf-python](#netconf-python)
- [Projects](#projects)
  - [Juniper JUNOS](#juniper-junos-1)
- [Configuration Parsers](#configuration-parsers)
  - [juniper-junos-set](#juniper-junos-set)
- [Golden Configurations](#golden-configurations)
  - [Juniper JUNOS set](#juniper-junos-set-1)
  - [Juniper JUNOS text - Jinja2](#juniper-junos-text---jinja2)
  - [Juniper JUNOS text - Simple](#juniper-junos-text---simple)

## Contents

| Asset | Description |
|---|---|
| [device-drivers/netconf-python](./device-drivers/netconf-python/) | IG5 Python NETCONF driver — is-alive, run-command, get-config, send-command, reboot |
| [Projects/Juniper JUNOS](./Projects/Juniper%20JUNOS.project.json) | IG5 project — software upgrade, port turn-up, push configuration, command runner |
| [Configuration Parsers/juniper-junos-set.json](./Configuration%20Parsers/juniper-junos-set.json) | Config Manager parser defining the `juniper-junos-set` device type |
| [Golden Configurations/Juniper JUNOS set](./Golden%20Configurations/Juniper%20JUNOS%20set.json) | Golden config tree using JUNOS `set`-format lines — requires `juniper-junos-set` parser |
| [Golden Configurations/Juniper JUNOS text - Jinja2](./Golden%20Configurations/Juniper%20JUNOS%20text%20-%20Jinja2.json) | Golden config tree using `text`-format lines with Jinja2 templates for flexible value matching |
| [Golden Configurations/Juniper JUNOS text - Simple](./Golden%20Configurations/Juniper%20JUNOS%20text%20-%20Simple.json) | Golden config tree using `text`-format lines with literal matching |

---

## Inventory Manager Configuration

Itential Platform ships with netmiko and scrapli drivers for Juniper JUNOS out of the box.
This repo provides a **NETCONF alternative** — use it when you need operations that survive
a mid-response session restart (software upgrades, reboots) or when you want to retrieve
configuration in a specific format (`xml`, `text`, `set`, `json`).

### Action Configuration

Wire the four broker contracts to their `junos-netconf-*` services when creating or
updating an inventory. Replace `your-cluster-id` with the `clusterId` of your IG5 instance.

```json
{
  "actions": [
    {
      "name": "is-alive",
      "action_type": "iag5-service",
      "action_config": {
        "serviceName": "junos-netconf-is-alive",
        "clusterId": "your-cluster-id"
      },
      "action_parameters": {}
    },
    {
      "name": "run-command",
      "action_type": "iag5-service",
      "action_config": {
        "serviceName": "junos-netconf-run-command",
        "clusterId": "your-cluster-id"
      },
      "action_parameters": {}
    },
    {
      "name": "get-config",
      "action_type": "iag5-service",
      "action_config": {
        "serviceName": "junos-netconf-get-config",
        "clusterId": "your-cluster-id"
      },
      "action_parameters": {}
    },
    {
      "name": "set-config",
      "action_type": "iag5-service",
      "action_config": {
        "serviceName": "junos-netconf-set-config",
        "clusterId": "your-cluster-id"
      },
      "action_parameters": {}
    }
  ]
}
```

The `name` field is the broker contract the platform calls. The `serviceName` is the IG5
service that handles it. They do not need to match — the mapping is the bridge.

### Node Attributes

Devices use NETCONF over SSH (port 830). Set these attributes on each node in Inventory Manager:

```json
{
  "name": "my-junos-device",
  "attributes": {
    "itential_host": "192.0.2.1",
    "itential_user": "netconf-user",
    "itential_password": "changeme",
    "itential_driver_options": {
      "netconf": {
        "port": 830,
        "timeout": 30,
        "command_timeout": 300,
        "config_format": "set",
        "lock_timeout": 60,
        "lock_poll_interval": 2
      }
    }
  }
}
```

| Attribute | Type | Unit | Description |
|---|---|---|---|
| `port` | integer | — | NETCONF SSH port on the device (default: `830`) |
| `timeout` | integer | seconds | Connection handshake timeout for all operations except `run-command` |
| `command_timeout` | integer | seconds | RPC wait timeout for `run-command` only — set high (300–600 s) for long-running commands like `request system software add` |
| `config_format` | string | — | Output format for `get-config`: `xml` (default, NETCONF RPC), `text` (curly-brace), `set` (set-format lines), or `json` |
| `lock_timeout` | integer | seconds | Max time to wait for the candidate datastore lock before `send-command` or `send-config` fails (`0` = fail immediately) |
| `lock_poll_interval` | integer | seconds | Polling interval between lock-acquire retries |

> **Required on the device before use:**
> ```
> set system services netconf ssh
> commit
> ```
> TCP/830 must be reachable from the IG5 host.

---

## Device Drivers

### netconf-python

A native Python NETCONF driver for IG5. Use this for any JUNOS operation that would
drop a CLI/SSH session mid-response — software installs and reboots in particular.

See [device-drivers/netconf-python/README.md](./device-drivers/netconf-python/README.md)
for full documentation including all operations, locking behavior, and local testing.

**Quick start — register services in IG5:**

```bash
iagctl db import device-drivers/netconf-python/import.yaml --force
```

Or copy the `services` and `decorators` blocks from
[import.yaml](./device-drivers/netconf-python/import.yaml) into your own `import.yml`.

**Registered services:**

Four services implement the IG5 device broker input/output contracts and are called
directly by the gateway adapter (is-alive checks, Config Manager remediation, etc.):

| Service | Broker contract | Notes |
|---|---|---|
| `junos-netconf-is-alive` | `is-alive` | Returns bare `true` or `false` — no JSON wrapper |
| `junos-netconf-run-command` | `run-command` | Returns plain text command output |
| `junos-netconf-get-config` | `get-config` | Returns plain text configuration |
| `junos-netconf-set-config` | `set-config` | Accepts Config Manager changes array; returns results array |

Three additional services are workflow-only tasks — the broker never calls them directly.
Use them in workflow tasks to give operators structured, typed inputs:

| Service | Operation |
|---|---|
| `junos-netconf-send-command` | Apply an array of set-style config lines and commit |
| `junos-netconf-send-config` | Apply a multi-line config block string and commit |
| `junos-netconf-reboot` | Schedule reboot via `<request-reboot/>` |

**Dependencies:** `ncclient>=0.6.13`, `lxml>=4.9.0`

---

## Projects

### Juniper JUNOS

An IG5 project for Juniper JUNOS device automation via NETCONF, organized into three folders.

**Software Upgrade**
- **JUNOS Upgrade** — backs up the running config, stages the image, verifies SHA-256, runs pre/post checks, installs, and reboots
- Command templates: Verify Image · Version Check · Pre and Post Checks · Stage Upgrade · Reboot
- Form: Upgrade Form — input for device name, target version, image path, and expected SHA-256

> **Before importing:** The Upgrade Form contains example image paths
> (`/var/tmp/junos-install-vsrx3-x86-64-22.4R2.8.tgz`) and SHA-256 hashes for
> specific vSRX packages. Update the form's `enum` fields under "Image Path on Device"
> and "Expected Image SHA-256" to match the software images staged in your environment.

**Golden Configuration**
- **Run Compliance** — runs a compliance check against a golden config tree
- Form: **Compliance Form** — select the golden config tree name and version to run against

**Inventory Management**
- **Create & Update Inventory from NetBox** — creates or updates an Inventory Manager inventory using NetBox as the source of truth
- **Clear & Delete Inventory** — removes all nodes from an inventory and deletes it

**Port Turn Up**
- **Port Turn Up** — provisions an 802.1Q sub-interface on a Juniper JUNOS device: fetches device details from inventory, runs a pre-check, backs up the running config, renders the sub-interface config via Jinja2, pushes it with `send-config`, and verifies with a post-check
- Command templates: Port Turn Up Pre Check · Port Turn Up Post Check — capture `show configuration interfaces`, `show security zones`, and `show route table inet.0` before and after the change
- Template: **802.1Q Sub Interface** — Jinja2 template generating `set`-format lines for the interface unit, VLAN ID, IP address, and security zone assignment
- Form: **8021.Q Sub Interface Form** — inputs: device, interface, VLAN ID, description, IP address, zone

> **Before running:** Ensure the target interface supports VLAN tagging and the security zone
> already exists on the device. The form's `zone` field must match an existing zone name exactly.

**Dependencies:** `junos-netconf-*` services registered in IG5 (see Device Drivers above)

---

## Configuration Parsers

### juniper-junos-set

Defines the `juniper-junos-set` device type in Config Manager. This parser must be
imported before the **Juniper JUNOS set** golden configuration tree can be created or
used. It tokenizes JUNOS `set`-format lines using the `cisco-ios` lexer template, treating
each line as a sequence of words delimited by whitespace, with `#` comments and
quoted strings handled correctly.

Import via Config Manager → Configuration Parsers → Import.

---

## Golden Configurations

Three golden configuration trees are provided. All ship with no device bindings — bind
each tree to your devices in Config Manager after importing.

### Juniper JUNOS set

Device type: `juniper-junos-set` · Config format: `set`

Baseline configuration using JUNOS `set`-format lines. Suited for environments where
configuration is managed and retrieved in set format. Supports Config Manager remediation
via the `junos-netconf-set-config` service.

> **Before importing:** The `juniper-junos-set` parser must be registered in Config Manager
> first (see Configuration Parsers above). Then update `"devices"` in the root node to
> match your Inventory Manager group name and device name.

**Dependencies:** `juniper-junos-set` parser · Config Manager enabled · `junos-netconf-set-config` registered in IG5

### Juniper JUNOS text - Jinja2

Device type: `juniper-junos` · Config format: `text`

Baseline configuration using `text`-format (curly-brace) lines with Jinja2 template
expressions for flexible value matching. Use this when your environment has multiple
allowed values for a field — for example, permitting two software versions during a
phased upgrade rollout.

### Juniper JUNOS text - Simple

Device type: `juniper-junos` · Config format: `text`

Baseline configuration using `text`-format (curly-brace) lines with literal matching.
Use this as a starting point when all devices in a group are expected to share identical
configuration values with no variation.
