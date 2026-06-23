# Cisco ASA — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/cisco-asa`  
**Status:** Planning  
**Files to modify:** `Cisco/ASA/Projects/Cisco ASA.project.json`

---

## Summary

Three `AGManager` tasks across three workflows. All follow the same CLI config-push pattern, making this a consistent `sendConfig` migration.

---

## Tasks to Migrate

### Workflow: Push Configuration to Device

| # | Task Name | Current App | Pattern |
|---|---|---|---|
| 1 | `itential_cli` | AGManager | CLI config push |

---

### Workflow: Delete ACL Rule

| # | Task Name | Current App | Pattern |
|---|---|---|---|
| 1 | `itential_cli` | AGManager | CLI config push |

---

### Workflow: Add ACL Rule

| # | Task Name | Current App | Pattern |
|---|---|---|---|
| 1 | `itential_cli` | AGManager | CLI config push |

**Incoming variables (same pattern on all three):**
```json
{
  "_groups": "",
  "_hosts": "$var.xxx.deviceList",
  "command": "$var.xxx.configurationList"
}
```

**Change for each:** Replace with `GatewayManager` `sendConfig`:
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

> **Note:** Trace the `$var.xxx` references in each workflow individually — the var IDs will differ between Push Config, Delete ACL, and Add ACL workflows.

---

## Other Workflows (No Changes)

One remaining workflow uses only `WorkFlowEngine`/`MOP` — no changes needed.

---

## Reference Template

`Cisco/IOS/Projects/Cisco IOS.project.json` — same vendor, same CLI pattern. The IOS project's Port Turn Up and IOS Upgrade workflows are the direct reference for the `sendConfig` task shape.

---

## Testing

- [ ] Push Configuration to Device sends config via GatewayManager
- [ ] Add ACL Rule applies rule via GatewayManager
- [ ] Delete ACL Rule removes rule via GatewayManager
