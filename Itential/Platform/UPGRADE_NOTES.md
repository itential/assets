# Itential Platform Configuration Management — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/itential-config-mgmt`  
**Status:** Complete  
**Files modified:** `Itential/Platform/Projects/Itential Platform Configuration Management.project.json`

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

**Implemented:** Task `ca47` replaced with `GatewayManager sendConfig`:
- `config`: `$var.582e.configurationList`
- `inventory`: `$var.582e.deviceList`
- `clusterId`: `cluster-itential`

Also fixed a stale downstream reference: the "View Error" task (`7a4c`) referenced `$var.ca47.stdout` (the old AGManager output field), which no longer exists now that `ca47` outputs `result`. Updated to `$var.ca47.result`.

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
