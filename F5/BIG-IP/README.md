# F5 BIG-IP

F5 BIG-IP is an application delivery controller providing load balancing, traffic management, and application security for on-premises and cloud environments, configured via TMOS/TMSH or the iControl REST API.

This project provides two ways to automate against BIG-IP: netmiko over SSH/TMSH (the same pattern used for Cisco IOS and Arista EOS), or a custom IG5 device driver over the iControl REST API for HTTP-based access — see **Inventory Manager Configuration** below.

**Requirements:** Itential Platform >= 6.4 · Itential Gateway >= 5.0 (only if using the `f5-rest` device driver)

## Table of Contents

- [Contents](#contents)
- [Inventory Manager Configuration](#inventory-manager-configuration)
  - [Option 1: netmiko (SSH/TMSH)](#option-1-netmiko-sshtmsh)
  - [Option 2: f5-rest (iControl REST over HTTP)](#option-2-f5-rest-icontrol-rest-over-http)
- [Device Drivers](#device-drivers)
  - [f5-rest](#f5-rest)

## Contents

| Asset | Description |
|---|---|
| [device-drivers/f5-rest](./device-drivers/f5-rest/) | IG5 Python iControl REST driver — is-alive, run-command, get-config, set-config, plus a generic REST passthrough |

## Inventory Manager Configuration

BIG-IP devices can be automated two ways. Pick per device based on whether you want CLI (TMSH) or REST (iControl) access — both can coexist across different nodes in the same inventory.

### Option 1: netmiko (SSH/TMSH)

Itential Platform ships with a netmiko driver for F5 BIG-IP out of the box — no additional driver install required. Broker actions (`is-alive`, `run-command`, `get-config`, `set-config`) are wired automatically when the inventory is created with `createBrokerActions: true`, the same as Cisco IOS and Arista EOS.

```json
{
  "name": "my-bigip-device",
  "attributes": {
    "itential_host": "192.0.2.100",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "f5_tmsh",
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
| `itential_platform` | string | Netmiko device type — `f5_tmsh` for the TMSH shell (use `f5_ltm` if your environment is still on the older TMOS shell) |
| `itential_user` | string | SSH username |
| `itential_password` | string | SSH password |

### Option 2: f5-rest (iControl REST over HTTP)

Use this instead of netmiko when you want HTTP-based access to BIG-IP's iControl REST API rather than SSH/TMSH — no SSH access required, all operations go over HTTPS to the management interface. Requires the `f5-rest` device driver registered in Itential Gateway 5.x.

See [device-drivers/f5-rest/README.md](./device-drivers/f5-rest/README.md) for full setup details, authentication options (token, OAuth2 client credentials, Basic, or a static Bearer token), and a generic REST passthrough (`f5-rest-call`) for calling any iControl endpoint directly from a workflow.

**Node attributes:**

```json
{
  "itential_host": "10.0.0.227",
  "itential_port": 8443,
  "itential_driver": "f5-rest",
  "itential_user": "admin",
  "itential_password": "password",
  "itential_driver_options": {
    "f5-rest": {
      "auth_method": "token",
      "get_config_command": "tmsh list all-properties",
      "login_provider": "tmos",
      "save_config": true,
      "timeout": 30,
      "verify_ssl": false
    }
  }
}
```

**Action mapping** — wire the four broker contracts to this driver's IG5 services, replacing `cluster-itential` with your own `cluster_id`:

```json
[
  {
    "name": "is-alive",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "f5-rest-is-alive",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  },
  {
    "name": "run-command",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "f5-rest-run-command",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  },
  {
    "name": "get-config",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "f5-rest-get-config",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  },
  {
    "name": "set-config",
    "action_type": "iag5-service",
    "action_config": {
      "service_name": "f5-rest-set-config",
      "cluster_id": "cluster-itential"
    },
    "action_parameters": {}
  }
]
```

## Device Drivers

### f5-rest

A native Python iControl REST driver for IG5. Use this for HTTP-based BIG-IP automation instead of SSH/TMSH — useful when SSH access to the management interface isn't available, or when you'd rather work directly against iControl REST endpoints from a workflow.

See [device-drivers/f5-rest/README.md](./device-drivers/f5-rest/README.md) for full documentation including all operations, authentication methods, and local testing. That README also has the Inventory Manager action mapping JSON needed to wire the broker contracts (`is-alive`, `run-command`, `get-config`, `set-config`) to this driver's IG5 services.

**Quick start — register services in IG5:**

```bash
iagctl db import device-drivers/f5-rest/import.yaml --force
```

Or copy the `services` and `decorators` blocks from [import.yaml](./device-drivers/f5-rest/import.yaml) into your own `import.yml`.

**Dependencies:** `requests>=2.28.0`
