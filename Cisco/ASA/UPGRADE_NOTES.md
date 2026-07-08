# Cisco ASA — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/cisco-asa`  
**Status:** Complete  
**Files modified:** `Cisco/ASA/Projects/Cisco ASA.project.json`

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

**Implemented variable mappings:**

| Workflow | Task Key | `config` | `inventory` |
|---|---|---|---|
| Push Configuration to Device | `ca47` | `$var.582e.configurationList` | `$var.582e.deviceList` |
| Delete ACL Rule | `56a0` | `$var.aaac.aclRuleCmdArray` | `$var.aaac.deviceArray` |
| Add ACL Rule | `56a0` | `$var.aaac.aclRuleCmdArray` | `$var.aaac.deviceArray` |

All three tasks also have `clusterId: "cluster-itential"` and `outgoing.result: ""`.

Also fixed a stale downstream reference: the "View Error" task (`7a4c`) in the Push Configuration workflow referenced `$var.ca47.stdout` (the old AGManager output field), which no longer exists now that `ca47` outputs `result`. Updated to `$var.ca47.result`.

---

## Other Workflows (No Changes)

One remaining workflow uses only `WorkFlowEngine`/`MOP` — no changes needed.

---

## Reference Template

`Cisco/IOS/Projects/Cisco IOS.project.json` — same vendor, same CLI pattern. The IOS project's Port Turn Up and IOS Upgrade workflows are the direct reference for the `sendConfig` task shape.

---

## Testing

- [x] Push Configuration to Device sends config via GatewayManager
- [x] Add ACL Rule applies rule via GatewayManager
- [x] Delete ACL Rule removes rule via GatewayManager
