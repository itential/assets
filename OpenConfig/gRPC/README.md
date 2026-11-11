# gRPC

gRPC is the transport behind gNMI and gNOI, the OpenConfig protocols for reading and writing device configuration and state (gNMI) and running operational commands such as reboot, ping and time (gNOI). Any network operating system that exposes a gNMI or gNOI server can be driven the same way, whichever vendor's YANG models it serves.

## Table of Contents

- [gRPC](#grpc)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Inventory Manager Configuration](#inventory-manager-configuration)
    - [Node Attributes](#node-attributes)
  - [Device Drivers](#device-drivers)
    - [gRPC Driver](#grpc-driver)
  - [Projects](#projects)
    - [gRPC Driver Test](#grpc-driver-test)
  - [Configuration Parsers](#configuration-parsers)
    - [gRPC Parser](#grpc-parser)
  - [Golden Configurations](#golden-configurations)
    - [gRPC Golden - Baseline](#grpc-golden---baseline)

## Contents

| Asset | Description |
|---|---|
| [device-drivers/grpc](./device-drivers/grpc/) | IG5 Python gNMI/gNOI driver: is-alive, get-config, set-config, run-command, gNMI Get/Set/Subscribe, gNOI RPCs, reflection |
| [Studio Projects/gRPC Driver Test](./Studio%20Projects/gRPC%20Driver%20Test.project.json) | Studio Project: create an inventory, test the driver, clean up |
| [Configuration Parsers/grpc.json](./Configuration%20Parsers/grpc.json) | Config Manager parser defining the `grpc` device type |
| [Golden Configurations/gRPC Golden - Baseline](./Golden%20Configurations/gRPC%20Golden%20-%20Baseline.json) | Golden config tree for the `grpc` device type |

---

## Inventory Manager Configuration

Wire the four Config Manager broker actions (`is-alive`, `get-config`, `set-config`, `run-command`) to the `grpc-*` services when you create or update an inventory. The mapping is in the [driver README](./device-drivers/grpc/README.md#installing-on-a-gateway-5-server).

### Node Attributes

Set these attributes on each node in Inventory Manager. Replace the host, credentials and `itential_platform` with your device's values:

```json
{
  "name": "my-gnmi-device",
  "attributes": {
    "itential_host": "192.0.2.1",
    "itential_port": 57400,
    "itential_driver": "grpc",
    "itential_platform": "cisco_xr",
    "itential_user": "username",
    "itential_password": "changeme"
  }
}
```

Driver options such as TLS certificates, timeouts and pooling go under `itential_driver_options.grpc`. The [driver README](./device-drivers/grpc/README.md#options) lists every option and its default.

If the same node is also managed over SSH, keep `itential_port` at 22 and set `itential_driver_options.grpc.port` instead. See [Ports](./device-drivers/grpc/README.md#ports-itential_port-and-the-grpc-port).

The gRPC driver doesn't read `itential_platform`. Set it to your device's type, for example `cisco_xr`. Config Manager uses it to match the node to a parser (the `grpc` parser doesn't filter by device type), and netmiko uses it if the node is also managed over SSH.

---

## Device Drivers

### gRPC Driver

A Gateway 5 driver with one `python-script` service per operation (32 in total), selected by the `GRPC_OP` environment variable. It covers:

- **gNMI:** Capabilities, Get, Set and Subscribe.
- **gNOI:** System, Layer2, BGP and Interface RPCs, plus any other gRPC service through server reflection.
- **Config Manager:** the four broker contracts, wired to the services below.

| Inventory Manager action | Service |
|---|---|
| `is-alive` | `grpc-is-alive` |
| `get-config` | `grpc-gnmi-get-config-text` |
| `set-config` | `grpc-gnmi-set-config-text` |
| `run-command` | `grpc-run-command` |

Connection pooling is `off` by default. See the [driver README](./device-drivers/grpc/README.md) for the operations, pool modes, inventory attributes and install steps.

**Large configurations:** use Gateway 5.5.3 or later. From that version, the `config` input of the set-config services is delivered to the driver as a file, so full-device configurations larger than about 128 KB are supported.

**Dependencies:** `pygnmi`, `grpcio`, `grpcio-reflection`, `protobuf` (see `requirements.txt`)

---

## Projects

### gRPC Driver Test

A Studio Project for trying the driver against a gRPC device.

- **gRPC - Create Inventory** builds an Inventory Manager inventory with the actions mapped to the `grpc-*` services, and adds one placeholder node, `my-gnmi-device`. Before you run it, edit the **populateInventory** task to use a real device (see [Node Attributes](#node-attributes)). The inventory's actions point at the Gateway 5 cluster `cluster-itential`; if your cluster has a different name, change the `cluster_id` values in the **createInventory** task.
- **gRPC - Test Driver** runs the driver against the device selected by tag. It makes real changes: a gNMI Set writes a description and an MTU of 9000 on `Ethernet1`, a Config Manager-style `set-config` writes another description, and a gNOI ping targets `10.0.0.1`. Change those interface and address values in the workflow to suit your device, and use a lab device.
- **gRPC - Delete Inventory** removes the nodes and the inventory.
- Command templates: **gRPC - Device Info** · **gRPC - IOS XR Checks** · **gRPC - Expected Failure**, all run through the `run-command` action.

**Dependencies:** the `grpc-*` services registered in IG5 (see Device Drivers above) · a gNMI/gNOI-enabled device

---

## Configuration Parsers

### gRPC Parser

Defines the `grpc` device type so Config Manager can parse configuration retrieved through the driver's `get-config-text` service.

---

## Golden Configurations

### gRPC Golden - Baseline

A golden config tree for the `grpc` device type. It is a starting point built from sample values: the hostname pattern (`grpc-r.*`), the domain name (`lab.itential.io`) and the `Ethernet1` MTU are example data. Edit them to match your devices before running a compliance check.

**Dependencies:** `grpc` parser · Config Manager enabled · `grpc-gnmi-get-config-text` registered in IG5
