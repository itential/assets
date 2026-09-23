# VELOS

F5 VELOS is the chassis-based platform and system-controller layer that hosts BIG-IP tenant instances on shared hardware blades. Its RESTCONF API, served by the chassis's system controller, manages chassis partitions, tenants, tenant software images, and platform/node hardware status.

This project provides an OpenAPI spec for automating against the VELOS system controller's RESTCONF API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`f5_velos-latest.json`](#f5_velos-latestjson)
  - [`f5_velos-1.6.1.json`](#f5_velos-161json)
- [Studio Projects](#studio-projects)
  - [F5 VELOS Project](#f5-velos-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | F5 VELOS RESTCONF API OpenAPI spec — curated `-latest` plus the dated reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 16 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `F5 VELOS:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `f5_velos-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your VELOS chassis's system controller.

Authentication is HTTP Basic, using the username/password of an F5OS-C user with appropriate role permissions:

```
Authorization: Basic <base64(username:password)>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-f5os-username>",
      "password": "<your-f5os-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-velos-system-controller-host>",
    "port": 8888,
    "base_path": "/restconf/data"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`f5_velos-latest.json`](./OpenAPIs/f5_velos-latest.json) | latest (curated) | 16 | Curated to core system-controller CRUD — see breakdown below |
| [`f5_velos-1.6.1.json`](./OpenAPIs/f5_velos-1.6.1.json) | 1.6.1 | 16 | Reference spec for the F5OS-C RESTCONF API, version 1.6.1 |

### `f5_velos-latest.json`

Hand-built from F5's official VELOS/F5OS-C API reference documentation at clouddocs.f5.com, covering the core system-controller resources most VELOS automation actually touches.

Resources included, by category:

- **Chassis Partitions**: list, create, get, update config (e.g. enable/disable), delete
- **Tenants**: list, create, get, update config (e.g. running-state, vCPU/memory/VLAN assignment), delete
- **Tenant Images**: list, get, delete
- **Platform & Node Status**: list hardware/platform components, get a component's status, list blade slots and their partition assignment

### `f5_velos-1.6.1.json`

Reference spec for the F5OS-C RESTCONF API, version 1.6.1. Same operation set as `f5_velos-latest.json` above.

## Studio Projects

### F5 VELOS Project

Backed by the **`F5 VELOS:latest`** Integration Model (see [`f5_velos-latest.json`](./OpenAPIs/f5_velos-latest.json) above). The project contains **16 workflows** organized into **4 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Chassis Partitions | 5 | List, create, get, update config, delete |
| Tenants | 5 | List, create, get, update config, delete |
| Tenant Images | 3 | List, get, delete |
| Platform & Node Status | 3 | List platform components, get a component, list slots |

#### Dependencies

| Dependency | Notes |
|---|---|
| `F5 VELOS:latest` Integration Model | Import from [`f5_velos-latest.json`](./OpenAPIs/f5_velos-latest.json) before importing the project |
| `F5 VELOS` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `F5 VELOS` — update the `adapter_id` value in each workflow task if yours is named differently |
