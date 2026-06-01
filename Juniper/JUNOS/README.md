# Juniper JUNOS

Assets for the Itential Platform — Juniper Junos device automation using NETCONF.

**Requirements:** Itential Platform >= 6.4 · Itential Automation Gateway >= 5.4

## Contents

| Asset | Description |
|---|---|
| [device-drivers/netconf-python](./device-drivers/netconf-python/) | IAG5 Python NETCONF driver — is-alive, run-command, get-config, send-command, reboot |
| [Projects/Juniper JUNOS](./Projects/Juniper%20JUNOS.project.json) | IAG5 project — software upgrade, port turn-up, push configuration, command runner |
| [Golden Configurations/Juniper JUNOS set](./Golden%20Configurations/Juniper%20JUNOS%20set.json) | Golden config tree using Junos `set`-format lines |
| [Golden Configurations/Juniper JUNOS text - Jinja2](./Golden%20Configurations/Juniper%20JUNOS%20text%20-%20Jinja2.json) | Golden config tree using Jinja2 templates for flexible value matching |
| [Golden Configurations/Juniper JUNOS text - Simple](./Golden%20Configurations/Juniper%20JUNOS%20text%20-%20Simple.json) | Golden config tree using literal text matching |

---

## Inventory Manager Configuration

### Action Configuration

Wire the four broker contracts to their `junos-netconf-*` services when creating or
updating an inventory. Replace `your-cluster-id` with the `clusterId` of your IAG5 instance.

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

The `name` field is the broker contract the platform calls. The `serviceName` is the IAG5
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
        "lock_timeout": 60,
        "lock_poll_interval": 2
      }
    }
  }
}
```

> **Required on the device before use:**
> ```
> set system services netconf ssh
> commit
> ```
> TCP/830 must be reachable from the IAG5 host.

`command_timeout` applies only to `run-command` and is used for long-running operations
like `request system software add` (typically 1–3 minutes on a vSRX). All other operations
use `timeout` for the connection handshake.

---

## Device Drivers

### netconf-python

A native Python NETCONF driver for IAG5. Use this for any Junos operation that would
drop a CLI/SSH session mid-response — software installs and reboots in particular.

See [device-drivers/netconf-python/README.md](./device-drivers/netconf-python/README.md)
for full documentation including all operations, locking behavior, and local testing.

**Quick start — register services in IAG5:**

```bash
iagctl db import device-drivers/netconf-python/import.yaml --force
```

Or copy the `services` and `decorators` blocks from
[import.yaml](./device-drivers/netconf-python/import.yaml) into your own `import.yml`.

**Registered services:**

Four services implement the IAG5 device broker input/output contracts and are called
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

An IAG5 project for Juniper Junos device automation via NETCONF, organized into three folders.

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

**Inventory Management**
- **Create & Update Inventory from NetBox** — creates or updates an Inventory Manager inventory using NetBox as the source of truth
- **Clear & Delete Inventory** — removes all nodes from an inventory and deletes it

**Utility**
- **Teams Message** — sends a Microsoft Teams notification with a direct link to the related job

**Dependencies:** `junos-netconf-*` services registered in IAG5 (see Device Drivers above)

---

## Golden Configurations

Three golden configuration trees are provided. All ship with no device bindings — bind
each tree to your devices in Config Manager after importing.

### Juniper JUNOS set

Device type: `juniper-junos-set`

Baseline configuration using Junos `set`-format lines. Suited for environments where
configuration is managed and retrieved in set format. Supports Config Manager remediation
via the `junos-netconf-set-config` service.

> **Before importing:** Update `"devices"` in the root node to match your Inventory
> Manager group name and device name.

**Dependencies:** Config Manager enabled · `junos-netconf-set-config` registered in IAG5

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
