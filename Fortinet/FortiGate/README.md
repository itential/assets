# Fortinet FortiGate

FortiGate is Fortinet's network security appliance line, providing firewall, VPN, and routing functionality configured either via CLI (SSH) or the FortiOS REST API.

This project provides two ways to automate against FortiGate: netmiko over SSH/CLI (the same pattern used for Cisco IOS and Arista EOS), or a custom IG5 device driver over the FortiOS REST API for HTTP-based access — see **Inventory Manager Configuration** below.

**Requirements:** Itential Platform >= 6.4 · Itential Gateway >= 5.0 (only if using the `fortigate-rest` device driver)

## Table of Contents

- [Contents](#contents)
- [Inventory Manager Configuration](#inventory-manager-configuration)
  - [Option 1: netmiko (SSH/CLI)](#option-1-netmiko-sshcli)
  - [Option 2: fortigate-rest (FortiOS REST API over HTTP)](#option-2-fortigate-rest-fortios-rest-api-over-http)
- [Device Drivers](#device-drivers)
  - [fortigate-rest](#fortigate-rest)

## Contents

| Asset | Description |
|---|---|
| [device-drivers/fortigate-rest](./device-drivers/fortigate-rest/) | IG5 Python FortiOS REST driver — is-alive, get-config, plus a generic REST passthrough |

## Inventory Manager Configuration

FortiGate devices can be automated two ways. Pick per device based on whether you want CLI (SSH) or REST (FortiOS API) access — both can coexist across different nodes in the same inventory.

### Option 1: netmiko (SSH/CLI)

Itential Platform ships with a netmiko driver for FortiGate out of the box — no additional driver install required. Broker actions (`is-alive`, `run-command`, `get-config`, `set-config`) are wired automatically when the inventory is created with `createBrokerActions: true`, the same as Cisco IOS and Arista EOS.

```json
{
  "name": "my-fortigate-device",
  "attributes": {
    "itential_host": "192.0.2.200",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "fortinet",
    "itential_user": "admin",
    "itential_password": "changeme"
  }
}
```

| Attribute | Type | Description |
|---|---|---|
| `itential_host` | string | Management IP or hostname of the device |
| `itential_port` | integer | SSH port (default: `22`) |
| `itential_driver` | string | Driver to use — must be `netmiko` |
| `itential_platform` | string | Netmiko device type — `fortinet` for FortiOS |
| `itential_user` | string | SSH username |
| `itential_password` | string | SSH password |

### Option 2: fortigate-rest (FortiOS REST API over HTTP)

Use this instead of netmiko when you want HTTP-based access to FortiGate's REST API rather than SSH/CLI — no SSH access required, and all operations go over HTTPS to the management interface. Requires the `fortigate-rest` device driver registered in Itential Gateway 5.x.

See [device-drivers/fortigate-rest/README.md](./device-drivers/fortigate-rest/README.md) for full setup details, the API-token authentication model, and a generic REST passthrough (`fortigate-rest-call`) for calling any FortiOS REST endpoint directly from a workflow.

**Node attributes:**

```json
{
  "name": "fortigate-01",
  "attributes": {
    "itential_host": "192.0.2.200",
    "itential_port": 443,
    "itential_driver": "fortigate-rest",
    "itential_password": "<FortiOS API token>",
    "itential_driver_options": {
      "fortigate-rest": {
        "vdom": "root",
        "verify_ssl": false,
        "timeout": 30,
        "backup_scope": "global"
      }
    }
  }
}
```

**Action mapping** — wire the supported broker contracts to this driver's IG5 services, replacing `cluster-itential` with your own `cluster_id`:

```json
[
  {
    "name": "is-alive",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "fortigate-rest-is-alive",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  },
  {
    "name": "get-config",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "fortigate-rest-get-config",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  }
]
```

## Device Drivers

### fortigate-rest

A native Python FortiOS REST driver for IG5. Use this for HTTP-based FortiGate automation instead of SSH/CLI — useful when SSH access to the management interface isn't available, or when you'd rather work directly against FortiOS REST endpoints from a workflow.

See [device-drivers/fortigate-rest/README.md](./device-drivers/fortigate-rest/README.md) for full documentation including all operations, the API-token authentication model, and local testing. That README also has the Inventory Manager action mapping JSON needed to wire the broker contracts (`is-alive`, `get-config`) to this driver's IG5 services.

**Quick start — register services in IG5:**

```bash
iagctl db import device-drivers/fortigate-rest/import.yaml --force
```

Or copy the `services` and `decorators` blocks from [import.yaml](./device-drivers/fortigate-rest/import.yaml) into your own `import.yml`.

**Dependencies:** `requests>=2.28.0`
