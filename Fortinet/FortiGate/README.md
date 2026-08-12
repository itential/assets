# Fortinet FortiGate

FortiGate is Fortinet's network security appliance line, providing firewall, VPN, and routing functionality configured either via CLI (SSH) or the FortiOS REST API.

Itential Platform ships no built-in driver for FortiGate. This project provides a custom IG5 device driver over the FortiOS REST API for HTTP-based access — see **Inventory Manager Configuration** below.

**Requirements:** Itential Platform >= 6.4 · Itential Gateway >= 5.0

## Table of Contents

- [Contents](#contents)
- [Inventory Manager Configuration](#inventory-manager-configuration)
- [Device Drivers](#device-drivers)
  - [fortigate-rest](#fortigate-rest)

## Contents

| Asset | Description |
|---|---|
| [device-drivers/fortigate-rest](./device-drivers/fortigate-rest/) | IG5 Python FortiOS REST driver — is-alive, get-config, plus a generic REST passthrough |

## Inventory Manager Configuration

FortiOS's REST API authenticates with a static API token (Bearer), not a username/password login, and has no CLI passthrough endpoint — so `run-command` and `set-config` aren't implemented by this driver. See [device-drivers/fortigate-rest/README.md](./device-drivers/fortigate-rest/README.md) for the full attribute reference, the reasoning behind the CLI-passthrough gap, and the generic REST passthrough (`fortigate-rest-call`) for calling any FortiOS REST endpoint directly from a workflow.

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

A native Python FortiOS REST driver for IG5. Use this for HTTP-based FortiGate automation — no SSH access to the management interface required.

See [device-drivers/fortigate-rest/README.md](./device-drivers/fortigate-rest/README.md) for full documentation including all operations, the API-token authentication model, and local testing. That README also has the Inventory Manager action mapping JSON needed to wire the broker contracts (`is-alive`, `get-config`) to this driver's IG5 services.

**Quick start — register services in IG5:**

```bash
iagctl db import device-drivers/fortigate-rest/import.yaml --force
```

Or copy the `services` and `decorators` blocks from [import.yaml](./device-drivers/fortigate-rest/import.yaml) into your own `import.yml`.

**Dependencies:** `requests>=2.28.0`
