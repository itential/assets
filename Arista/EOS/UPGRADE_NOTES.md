# Arista EOS — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/arista-eos`  
**Status:** Complete  
**Files modified:** `Arista/EOS/Projects/Arista EOS.project.json`

---

## Summary

One `AGManager` task in one workflow. Straightforward CLI → `GatewayManager sendConfig` migration.

---

## Tasks to Migrate

### Workflow: Push Configuration to Device - IAG

| # | Task Name | Current App | Pattern |
|---|---|---|---|
| 1 | `itential_cli` | AGManager | CLI config push |

**Incoming variables (current):**
```json
{
  "_groups": "",
  "_hosts": "$var.582e.deviceList",
  "command": "$var.582e.configurationList"
}
```

**Implemented:** `GatewayManager` `sendConfig` task (task key `ca47`):
```json
{
  "app": "GatewayManager",
  "displayName": "GatewayManager",
  "name": "sendConfig",
  "description": "Send configuration to inventory nodes through a Gateway5 service",
  "variables": {
    "incoming": {
      "clusterId": "cluster-itential",
      "config": "$var.582e.configurationList",
      "inventory": "$var.582e.deviceList"
    },
    "outgoing": {
      "result": ""
    }
  }
}
```

Both `config` and `inventory` come from the `582e` transformation task, which processes the rendered Jinja template (`b9ed`) and device input (`$var.job.device`) into CLI-ready `configurationList` and `deviceList` outputs.

---

## Other Workflows (No Changes)

| Workflow | Apps Used | Action |
|---|---|---|
| Port Turn Up | MOP, WorkFlowEngine | No change |
| Create VLAN | MOP, WorkFlowEngine | No change |
| Command Template Runner | MOP, WorkFlowEngine | No change |
| Software Upgrade | MOP, WorkFlowEngine | No change |
| File Transfer | WorkFlowEngine | No change |
| Command Template Runner_v2 | MOP, WorkFlowEngine | No change |

---

## Other Adapters

`MOP`, `TemplateBuilder`, `WorkFlowEngine` — no changes needed.

---

## Reference Template

`Cisco/IOS/Projects/Cisco IOS.project.json` — `sendConfig` task pattern in Port Turn Up and IOS Upgrade workflows.

---

## Testing

- [x] Push Configuration to Device - IAG workflow pushes config successfully via GatewayManager
