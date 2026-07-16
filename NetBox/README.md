# NetBox Assets
Assets for the Itential Platform.

## OpenAPIs
- [NetBox 4.1](./OpenAPIs/netbox_4.1.json)

## Projects
### NetBox Project
- Create Prefix
- Delete a Prefix
- Reserve an IP Address
- Delete an IP Address
- Assign Next IP (in Prefix)
- _Sample Use Cases_
    - Onboard Device in Branch

### Netbox Inventory Sync
This project contains workflows for creating inventories and populating them with nodes in Inventory Manager from Netbox
This pulls the netbox inventory through loops using pagination, check and creates a inventory called "Netbox" in inventory manager and adds all the devices to the "Netbox" Inventory. The "platform" for IAG5 is fetched using the "Manufacturer" of the device, i.e if cisco is "cisco-ios", juniper is "junos" and nokia/aclatel is "sros"
- Netbox Inventory Sync
- Get Netbox Inventory 
- Create Inventory And Add Nodes
- Add Device to Inventory

#### Dependencies
- [NetBox 3.x Adapter](https://gitlab.com/itentialopensource/adapters/adapter-netbox_v33)
- NetBox 4.1 Integration
- Netbox Latest Integration
