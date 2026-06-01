# Juniper JUNOS

Assets for the Itential Platform — Juniper Junos device automation using NETCONF.

**Requirements:** Itential Platform >= 6.4 · Itential Automation Gateway >= 5.4

## Contents

| Asset | Description |
|---|---|
| [Device Drivers/netconf-python](./Device%20Drivers/netconf-python/) | IAG5 Python NETCONF driver — is-alive, run-command, get-config, send-command, reboot |
| [Projects/Juniper JUNOS](./Projects/Juniper%20JUNOS.project.json) | IAG5 project — software upgrade, port turn-up, push configuration, command runner |
| [Golden Configurations/Juniper JUNOS set](./Golden%20Configurations/Juniper%20JUNOS%20set.json) | Golden config tree using Junos `set`-format lines |

---

## IAG5 Inventory Configuration

Devices managed by this driver use NETCONF over SSH (port 830). Set these attributes on each
device in Inventory Manager:

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

See [Device Drivers/netconf-python/README.md](./Device%20Drivers/netconf-python/README.md)
for full documentation including all operations, locking behavior, and local testing.

**Quick start — register services in IAG5:**

```bash
# Drop import.yaml into your IAG5 asset repo and run:
iagctl db import Device\ Drivers/netconf-python/import.yaml --force
```

Or copy the `services` and `decorators` blocks from
[import.yaml](./Device%20Drivers/netconf-python/import.yaml) into your own `import.yml`.

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

An IAG5 project covering software upgrade, port turn-up, push configuration, and
command template execution for Juniper Junos devices via NETCONF.

**Workflows included:**
- **Software Upgrade** — stage image, verify SHA-256, install, reboot, and confirm version
- **Port Turn Up** — configure and activate an interface
- **Push Configuration** — apply a set-format config block
- **Command Template Runner** — run operational commands from a template

> **Before importing:** The Software Upgrade form contains example image paths
> (`/var/tmp/junos-install-vsrx3-x86-64-22.4R2.8.tgz`) and SHA-256 hashes for
> specific vSRX packages. Update the form's `enum` fields under "Image Path on Device"
> and "Expected Image SHA-256" to match the software images staged in your environment.

**Dependencies:** `junos-netconf-*` services registered in IAG5 (see Device Drivers above)

---

## Golden Configurations

### Juniper JUNOS set

A golden configuration tree using Junos `set`-format lines (`juniper-junos-set` device
type). Captures baseline configuration for vSRX and tracks per-section nodes for
navigation and compliance.

> **Before importing:** The tree's root node binds to a specific device —
> `"devices": ["Itential Lab JUNOS::aws-lab-junos"]` in the exported JSON. Update this
> to match your Inventory Manager group name and device name before importing.

**Dependencies:** Config Manager enabled · `junos-netconf-set-config` registered in IAG5
