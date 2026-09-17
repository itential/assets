# Device42

Device42 is an agentless data center and IT asset discovery, inventory, and dependency mapping platform (CMDB) covering devices, racks, rooms, buildings, IP address management, applications, and vendors.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`device42-latest.json`](#device42-latestjson)
  - [`device42-2.0.json`](#device42-20json)
- [Studio Projects](#studio-projects)
  - [`Device42.project.json`](#device42projectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Device42 REST API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/](./Studio%20Projects/) | CRUD workflows for Devices, Hardware Models, Racks, Rooms, Buildings, IP Address Management, Applications, and Vendors |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Device42 | REST API v2.0 (as published) |
| Device42 Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is HTTP Basic — a Device42 username and password sent as the `Authorization` header on every request.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`device42-latest.json`](./OpenAPIs/device42-latest.json) | latest (curated) | 66 | Trimmed to 66 of 468 upstream operations covering common CRUD for automation — see breakdown below |
| [`device42-2.0.json`](./OpenAPIs/device42-2.0.json) | 2.0 | 468 | Full spec, Swagger 2.0 as published. |

### `device42-latest.json`

Sourced from Device42's own officially-published OpenAPI spec at `api.device42.com/device42.yaml` (Swagger 2.0, converted to OpenAPI 3.0). Trimmed to 66 of 468 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Devices**: Devices, Hardware Models
- **Facilities**: Racks, Rooms, Buildings
- **IP Address Management**: Subnets, IP Addresses, VLANs, MAC Addresses, DNS Zones, DNS Records, IP/Subnet Suggestion
- **Applications**: Application Components, Business Applications, Business Application Elements
- **Vendors**: Vendors

### `device42-2.0.json`

Full, unmodified vendor spec (468 operations, Swagger 2.0 as published) — the entire Device42 REST API surface, including autodiscovery jobs, PDUs/power circuits, patch panels, certificates, secrets, purchasing, license/user administration, and reporting. See `device42-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### `Device42.project.json`

One workflow per curated operation, organized by resource category, built on `device42-latest.json`'s Integration Model.

Every workflow's adapter task is wired to the Integration instance name `Device42`. After importing, either name your Integration instance `Device42`, or update the `adapter_id` value in each workflow task to match your own instance name.

**Devices**

| Workflow | Scope |
|---|---|
| List Devices | Get a list of devices |
| Create Device | Create a device |
| Get Device | Get a device by ID |
| Update Device | Update a device by ID |
| Delete Device | Delete a device by ID |
| Archive Device | Archive a device by ID |

**Hardware Models**

| Workflow | Scope |
|---|---|
| List Hardware Models | Get a list of hardware models |
| Create Hardware Model | Create a hardware model |
| Get Hardware Model | Get a hardware model by ID |
| Delete Hardware Model | Delete a hardware model by ID |

**Racks**

| Workflow | Scope |
|---|---|
| List Racks | Get a list of racks |
| Create Rack | Create a rack |
| Get Rack | Get a rack by ID |
| Delete Rack | Delete a rack by ID |

**Rooms**

| Workflow | Scope |
|---|---|
| List Rooms | Get a list of rooms |
| Create Room | Create a room |
| Get Room | Get a room by ID |
| Update Room | Update a room by ID |
| Delete Room | Delete a room by ID |

**Buildings**

| Workflow | Scope |
|---|---|
| List Buildings | Get a list of buildings |
| Create Building | Create a building |
| Get Building | Get a building by ID |
| Delete Building | Delete a building by ID |

**IP Address Management**

| Workflow | Scope |
|---|---|
| List Subnets | Get a list of subnets |
| Create Subnet | Create a subnet |
| Update Subnet | Update a subnet |
| Get Subnet | Get a subnet by ID |
| Delete Subnet | Delete a subnet by ID |
| List IP Addresses | Get a list of IP addresses |
| Create IP Address | Create an IP address |
| List IP Addresses by Subnet | Get IP addresses within a subnet |
| Delete IP Address | Delete an IP address by ID |
| List VLANs | Get a list of VLANs |
| Create VLAN | Create a VLAN |
| Update VLAN | Update a VLAN |
| Get VLAN | Get a VLAN by ID |
| Update VLAN by ID | Update a VLAN by ID |
| Delete VLAN | Delete a VLAN by ID |
| List MAC Addresses | Get a list of MAC addresses |
| Create MAC Address | Create a MAC address |
| Get MAC Address | Get a MAC address by ID |
| Delete MAC Address | Delete a MAC address by ID |
| List DNS Zones | Get a list of DNS zones |
| Create DNS Zone | Create a DNS zone |
| Delete DNS Zone | Delete a DNS zone by ID |
| List DNS Records | Get a list of DNS records |
| Create DNS Record | Create a DNS record |
| Delete DNS Record | Delete a DNS record by ID |
| Suggest IP Address | Suggest an available IP address |
| Suggest Subnet | Suggest an available child subnet |

**Applications**

| Workflow | Scope |
|---|---|
| List Application Components | Get a list of application components |
| Create Application Component | Create an application component |
| Get Application Component | Get an application component by ID |
| Delete Application Component | Delete an application component by ID |
| List Business Applications | Get a list of business applications |
| Create Business Application | Create a business application |
| Get Business Application | Get a business application by ID |
| Delete Business Application | Delete a business application by ID |
| List Business Application Elements | Get a list of business application elements |
| Create Business Application Element | Associate a device, resource, or application component with a business application |
| Delete Business Application Element | Remove a business application element association by criteria |
| Get Business Application Element | Get a business application element by ID |
| Delete Business Application Element by ID | Delete a business application element by ID |

**Vendors**

| Workflow | Scope |
|---|---|
| List Vendors | Get a list of vendors |
| Create Vendor | Create a vendor |
| Delete Vendor | Delete a vendor by ID |
