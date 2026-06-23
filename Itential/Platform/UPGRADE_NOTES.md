# Itential Platform Configuration Management — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/itential-config-mgmt`  
**Status:** Planning  
**Files to modify:** `Itential/Platform/Projects/Itential Platform Configuration Management.project.json`

---

## Summary

One `AGManager` task in one workflow. Minimal scope — same CLI → `GatewayManager sendConfig` pattern as Arista/Cisco ASA.

---

## Tasks to Migrate

### Workflow: Push Configuration

| # | Task Name | Current App | Pattern |
|---|---|---|---|
| 1 | `itential_cli` | AGManager | CLI config push |

**Incoming variables (current):**
```json
{
  "_groups": "",
  "_hosts": "$var.xxx.deviceList",
  "command": "$var.xxx.configurationList"
}
```

**Change:** Replace with `GatewayManager` `sendConfig`:
```json
{
  "app": "GatewayManager",
  "displayName": "GatewayManager",
  "name": "sendConfig",
  "description": "Send configuration to inventory nodes through a Gateway5 service",
  "variables": {
    "incoming": {
      "clusterId": "cluster-itential",
      "config": "<rendered config template var>",
      "inventory": "<rendered inventory template var>"
    },
    "outgoing": {
      "result": ""
    }
  }
}
```

> **Note:** Trace the `$var.xxx` references from the Push Configuration workflow to identify the correct rendered template var IDs.

---

## Other Workflows (No Changes)

| Workflow | Apps Used | Action |
|---|---|---|
| 5 remaining workflows | ConfigurationManager, TemplateBuilder, MOP | No change |

---

## Other Adapters

`ConfigurationManager`, `TemplateBuilder`, `MOP`, `WorkFlowEngine` — no changes needed.

---

## Reference Template

`Cisco/IOS/Projects/Cisco IOS.project.json` — `sendConfig` task pattern.

---

## Testing

- [ ] Push Configuration workflow deploys config via GatewayManager successfully
