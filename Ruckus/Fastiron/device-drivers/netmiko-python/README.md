# fastiron-netmiko — IG5 Python script service

SSH CLI-based driver for Ruckus Fastiron (IronWare OS) switches. Uses
[netmiko](https://github.com/ktbyers/netmiko) for SSH connectivity.

Tested against Ruckus ICX series switches running FastIron OS (SPS 08.0.95r+).

## Table of Contents

- [Why a custom driver](#why-a-custom-driver)
- [Actions](#actions)
- [get-config section filter](#get-config-section-filter)
- [Known incompatible workflow tasks](#known-incompatible-workflow-tasks)
  - [`sendCommand` (GatewayManager)](#sendcommand-gatewaymanager)
- [Invocation model](#invocation-model)
  - [Registered services](#registered-services)
  - [From iagctl](#from-iagctl)
  - [From an Inventory Manager action mapping](#from-an-inventory-manager-action-mapping)
  - [Direct local testing](#direct-local-testing)
- [Inventory attributes](#inventory-attributes)
- [Prerequisites](#prerequisites)
- [Local development](#local-development)

## Why a custom driver

Fastiron devices are legacy switches that advertise `ssh-rsa` host keys and
include `diffie-hellman-group14-sha1` / `diffie-hellman-group1-sha1` in their
SSH KEX list. Both were removed from paramiko 5.0 (May 2026). This driver pins
`paramiko<5` so those algorithms remain available, and passes
`disabled_algorithms={"pubkeys": []}` to re-enable `ssh-rsa` host-key
verification which paramiko 3.3+ disables by default.

## Actions

| Action | Purpose | Notes |
|---|---|---|
| `is-alive` | Verify SSH reachability | Runs `show version`; returns bare `true`/`false` |
| `run-command` | Execute one or more CLI show/exec commands | `--command` is repeatable |
| `get-config` | Retrieve running configuration | Full config or filtered by `--section` |
| `send-command` | Apply config commands and save | Runs `send_config_set()` then `write memory` |
| `set-config` | Config Manager broker entry point | Same as `send-command`; input is a CM changes array |

## get-config section filter

Pass a section string to retrieve a subset of the running config:

```bash
# Full running config (default)
FASTIRON_OP=get-config python main.py --host 10.0.0.1 --user itential --password "$PASS"

# Single interface
FASTIRON_OP=get-config python main.py ... --section "interface ethernet 1/1/1"

# All interfaces
FASTIRON_OP=get-config python main.py ... --section "interface"

# VLAN config
FASTIRON_OP=get-config python main.py ... --section "vlan 100"
```

The `section` value is appended directly to `show running-config`, so any valid
IronWare filter string works.

## Known incompatible workflow tasks

### `sendCommand` (GatewayManager)

**Do not use** `GatewayManager.sendCommand` with this driver. That task routes through netsdk's built-in netmiko driver, which expects a structured `CommandResult` response with timing fields (`start_time`, `end_time`, `elapsed_time`). This driver returns plain text output and does not produce that format, resulting in:

```
"data": "failed to parse start_time for command 0: failed to parse timestamp string '':
parsing time \"\" as \"2006-01-02 15:04:05\": cannot parse \"\" as \"2006\""
```

**Use instead:**
- `GatewayManager.runService` — call the IG5 service directly by name
- `MOP.runCommandTemplate` — brokered device tasks such as MOP command templates

---

## Invocation model

One service per operation — each points at the same `main.py` and sets a
different `FASTIRON_OP` environment variable. Connection parameters come from
the device's Inventory Manager record (piped to stdin as `InventoryInfo` JSON
by gateway5). CLI flags override stdin values for local testing.

### Registered services

| Service name | Operation |
|---|---|
| `fastiron-netmiko-is-alive` | is-alive |
| `fastiron-netmiko-run-command` | run-command |
| `fastiron-netmiko-get-config` | get-config |
| `fastiron-netmiko-send-command` | send-command |
| `fastiron-netmiko-set-config` | set-config (broker) |

### From iagctl

```bash
iagctl run service python-script fastiron-netmiko-is-alive

iagctl run service python-script fastiron-netmiko-run-command \
  --set command="show version"

iagctl run service python-script fastiron-netmiko-run-command \
  --set command="show interfaces brief"

iagctl run service python-script fastiron-netmiko-get-config

iagctl run service python-script fastiron-netmiko-get-config \
  --set section="interface ethernet 1/1/1"

iagctl run service python-script fastiron-netmiko-send-command \
  --set 'commands=["interface ethernet 1/1/1", "port-name uplink", "exit"]'
```

### From an Inventory Manager action mapping

```json
[
  {
    "name": "is-alive",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "fastiron-netmiko-is-alive",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  },
  {
    "name": "run-command",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "fastiron-netmiko-run-command",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  },
  {
    "name": "get-config",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "fastiron-netmiko-get-config",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  },
  {
    "name": "send-command",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "fastiron-netmiko-send-command",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  },
  {
    "name": "set-config",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "fastiron-netmiko-set-config",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  }
]
```

### Direct local testing

```bash
FASTIRON_OP=is-alive python main.py \
  --host 10.0.0.1 --user itential --password "$PASS"

FASTIRON_OP=run-command python main.py \
  --host 10.0.0.1 --user itential --password "$PASS" \
  --command "show version"

FASTIRON_OP=get-config python main.py \
  --host 10.0.0.1 --user itential --password "$PASS" \
  --section "interface ethernet 1/1/1"

FASTIRON_OP=send-command python main.py \
  --host 10.0.0.1 --user itential --password "$PASS" \
  --command "interface ethernet 1/1/1" \
  --command "port-name uplink" \
  --command "exit"
```

## Inventory attributes

Set these on the device record in Inventory Manager:

```json
{
  "name": "fastiron-sw-01",
  "attributes": {
    "itential_host": "10.0.0.1",
    "itential_user": "itential",
    "itential_password": "$SECRET_vault $KEY_fastiron_pass",
    "itential_driver_options": {
      "netmiko": {
        "device_type": "ruckus_fastiron"
      }
    }
  }
}
```

| Attribute | Default | Purpose |
|---|---|---|
| `itential_host` | — | Device management IP (required) |
| `itential_user` | — | SSH username (required) |
| `itential_password` | — | SSH password (required) |
| `device_type` | `ruckus_fastiron` | netmiko device type |
| `disabled_algorithms` | — | Re-enables `ssh-rsa` host keys disabled by default in newer paramiko versions. Required for Fastiron devices. Set to `{"pubkeys": []}` |

> **Note:** Only fields defined in netsdk's `DriverOptions` model are allowed inside `itential_driver_options.netmiko`. Do not add `port`, `timeout`, or other unrecognised fields — IG5 will reject the inventory node with a pydantic validation error.

> **Note:** Fastiron has user EXEC and privileged EXEC modes. If your devices are configured to auto-elevate to privileged mode on SSH login, no enable password is needed. If your devices require a separate enable password, add `"secret": "<enable-password>"` under `itential_driver_options.netmiko` and pass `--secret` when testing locally.

## Prerequisites

- TCP/22 reachable from IG5 to the device
- SSH enabled on the device (`ip ssh`)
- Credentials with sufficient privilege for the required operations

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
FASTIRON_OP=is-alive python main.py --host 10.0.0.1 --user itential --password "$PASS"
```
