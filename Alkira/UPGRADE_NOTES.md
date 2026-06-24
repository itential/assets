# Alkira — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/alkira`  
**Status:** Complete  
**Files to modify:** `Alkira/Projects/Alkira.project.json`

---

## Summary

Alkira has two distinct gateway migration paths: `AGManager` (CLI/Netmiko) and `AutomationGateway` (device lifecycle). 5 tasks total across 2 workflows.

---

## Tasks to Migrate

### Workflow: Configure Firewall

| # | Task Name | Current App | Pattern |
|---|---|---|---|
| 1 | `itential_netmiko_set_config` | AGManager | CLI config push |
| 2 | `itential_netmiko_set_config` | AGManager | CLI config push |

**Change:** Replace both with `GatewayManager` `sendConfig` tasks.

Incoming variables to remap:
- `_hosts` → `inventory` (rendered inventory template)
- `command` → `config` (rendered config template)
- Add: `clusterId: "cluster-itential"`
- Remove: `_groups`

---

### Workflow: Onboard Device - IAG

| # | Task Name | Current App | Description |
|---|---|---|---|
| 1 | `createDeviceRaw` | AutomationGateway | Creates device record in inventory |
| 2 | `addDeviceToDeviceGroup` | AutomationGateway | Adds device to a group |
| 3 | `connectDevice` | AutomationGateway | Establishes device connectivity |

**Change:** `AutomationGateway` device lifecycle operations need to be replaced with their `GatewayManager` / `InventoryManager` equivalents.

- `createDeviceRaw` → determine equivalent in IAG5 inventory API
- `addDeviceToDeviceGroup` → determine equivalent in IAG5 inventory API
- `connectDevice` → determine equivalent in IAG5 inventory API

> **Note:** These are not simple variable remaps. Review how Cisco IOS and Juniper JUNOS handle device onboarding (`createInventory` workflow tasks) and mirror that pattern.

---

## Other Adapters in This Project

`Alkira`, `Awsec2`, `MOP`, `TemplateBuilder`, `WorkFlowEngine` — no changes needed for these.

---

## Reference Templates

- `Cisco/IOS/Projects/Cisco IOS.project.json` — `sendConfig` task pattern
- `Juniper/JUNOS/Projects/Juniper JUNOS.project.json` — `InventoryManager` / device onboarding pattern

---

## Testing

- [ ] Configure Firewall workflow executes against a test Alkira device
- [ ] Onboard Device workflow creates and connects a device via IAG5 inventory

## Changes Made

### Configure Firewall
- Tasks `9903` and `c06b`: `AGManager/itential_netmiko_set_config` → `GatewayManager/sendConfig`
- `_hosts` → `inventory`: `$var.3509.deviceArray`
- `lines` → `config`: `$var.b9ed.renderedTemplate` (task 9903) / `["commit"]` (task c06b)
- Added `clusterId: "cluster-itential"`
- Removed: `_groups`, `enable_mode`, `end_command`, `parents`, `provider`, `save_command`, `transactions`

### Onboard Device - IAG
- Task `2918`: `AutomationGateway/createDeviceRaw` → `InventoryManager/addNodesToInventory`
  - `inventory_identifier: $var.job.deviceGroup` (device group IS the inventory in IAG5)
  - `nodes: [{name: $var.job.deviceName, variables: $var.29f0.merged_object}]`
- Task `27f0`: Removed (`addDeviceToDeviceGroup` — implicit in `addNodesToInventory` above)
- Task `4d96`: `AutomationGateway/connectDevice` → `InventoryManager/getInventoryByIdentifier`
  - `identifier: $var.job.deviceGroup` (verifies inventory/device is registered)
- Removed `automationGatewayAdapterId` from inputSchema/outputSchema
- Updated transitions: `2918 → 4d96 → end` (27f0 removed from chain)
