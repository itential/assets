# NetTerrain

NetTerrain is a data center infrastructure management (DCIM) and network documentation platform by Graphical Networks, covering racks, devices, connections, circuits, and diagram hierarchy for physical and logical network layouts.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`netterrain-latest.json`](#netterrain-latestjson)
  - [`netterrain-1.json`](#netterrain-1json)
- [Studio Projects](#studio-projects)
  - [`NetTerrain.project.json`](#netterrainprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | NetTerrain RESTful API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/](./Studio%20Projects/) | CRUD workflows for Nodes, Devices, Racks, Links, Circuits, Node/Device/Rack Types, Vendors, Hierarchy, and Search |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| NetTerrain | RESTful API v1 (as published) |
| NetTerrain Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is HTTP Basic — a NetTerrain username and password sent as the `Authorization` header on every request.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`netterrain-latest.json`](./OpenAPIs/netterrain-latest.json) | latest (curated) | 52 | Trimmed to 52 of 261 upstream operations covering common CRUD for automation — see breakdown below |
| [`netterrain-1.json`](./OpenAPIs/netterrain-1.json) | 1 | 261 | Full spec, OpenAPI 3.0 as published. |

### `netterrain-latest.json`

Trimmed to 52 of 261 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Diagram Objects**: Nodes, Devices, Racks
- **Connections**: Links, Circuits
- **Type Catalog**: Node Types, Device Types, Rack Types, Vendors
- **Navigation**: Hierarchy, Search

### `netterrain-1.json`

Full, unmodified vendor spec (261 operations, OpenAPI 3.0 as published) — the entire NetTerrain RESTful API surface, including cards, ports, slots, port/slot representations and mappings, free text objects, groups, link/node property values and overrides, work orders, users, roles, and rack container designs. See `netterrain-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### `NetTerrain.project.json`

One workflow per curated operation, organized by resource category, built on `netterrain-latest.json`'s Integration Model.

Every workflow's adapter task is wired to the Integration instance name `netterrain`. After importing, either name your Integration instance `netterrain`, or update the `adapter_id` value in each workflow task to match your own instance name.

Create and update workflows take the full NetTerrain JSON body (including nested `href` references to related objects, e.g. `node_type`, `parent_diagram`, `rack_type`, `vendor`) as a single object-typed job input.

**Nodes**

| Workflow | Scope |
|---|---|
| List Nodes | Get a list of nodes |
| Update Node | Update a node identified by its `href` in the request body |
| Create Node | Create a node |
| Get Node | Get a node by ID |
| Update Node by ID | Update a node by ID |
| Delete Node | Delete a node by ID |

**Devices**

| Workflow | Scope |
|---|---|
| List Devices | Get a list of devices |
| Create Device | Create a device |
| Get Device | Get a device by ID |
| Update Device | Update a device by ID |
| Delete Device | Delete a device by ID |

**Racks**

| Workflow | Scope |
|---|---|
| List Racks | Get a list of racks |
| Create Rack | Create a rack |
| Get Rack | Get a rack by ID |
| Update Rack | Update a rack by ID |
| Delete Rack | Delete a rack by ID |

**Links**

| Workflow | Scope |
|---|---|
| List Links | Get a list of links |
| Update Link | Update a link identified by its `href` in the request body |
| Create Link | Create a link |
| Get Link | Get a link by ID |
| Update Link by ID | Update a link by ID |
| Delete Link | Delete a link by ID |

**Circuits**

| Workflow | Scope |
|---|---|
| List Circuits | Get a list of circuits |
| Create Circuit | Create a circuit |
| Get Circuit | Get a circuit by ID |
| Delete Circuit | Delete a circuit by ID |

**Node Types**

| Workflow | Scope |
|---|---|
| List Node Types | Get a list of node types |
| Update Node Type | Update a node type identified by its `href` in the request body |
| Create Node Type | Create a node type |
| Get Node Type | Get a node type by ID |
| Update Node Type by ID | Update a node type by ID |
| Delete Node Type | Delete a node type by ID |

**Device Types**

| Workflow | Scope |
|---|---|
| List Device Types | Get a list of device types |
| Update Device Type | Update a device type identified by its `href` in the request body |
| Create Device Type | Create a device type |
| Get Device Type | Get a device type by ID |
| Update Device Type by ID | Update a device type by ID |
| Delete Device Type | Delete a device type by ID |

**Rack Types**

| Workflow | Scope |
|---|---|
| List Rack Types | Get a list of rack types |
| Update Rack Type | Update a rack type identified by its `href` in the request body |
| Create Rack Type | Create a rack type |
| Get Rack Type | Get a rack type by ID |
| Update Rack Type by ID | Update a rack type by ID |
| Delete Rack Type | Delete a rack type by ID |

**Vendors**

| Workflow | Scope |
|---|---|
| List Vendors | Get a list of vendors |
| Update Vendor | Update a vendor identified by its `href` in the request body |
| Create Vendor | Create a vendor |
| Get Vendor | Get a vendor by ID |
| Update Vendor by ID | Update a vendor by ID |
| Delete Vendor | Delete a vendor by ID |

**Hierarchy**

| Workflow | Scope |
|---|---|
| Get Hierarchy Tree | Get the diagram hierarchy tree |

**Search**

| Workflow | Scope |
|---|---|
| Search | Search nodes and diagrams by name, type, or parent diagram |
