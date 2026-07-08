# Kentik — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/kentik`  
**Status:** Complete  
**Files modified:** `Kentik/Projects/Kentik.project.json`

---

## Summary

One `AGManager` task in one workflow within a large, multi-adapter project (13 workflows). The gateway change is isolated — the rest of the project uses REST adapters that don't need modification.

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
  "_hosts": "$var.xxx.deviceList",
  "command": "$var.xxx.configurationList"
}
```

**Implemented:** Task `ca47` replaced with `GatewayManager sendConfig`:
- `config`: `$var.4a43.configurationArray`
- `inventory`: `$var.4a43.deviceArray`
- `clusterId`: `cluster-itential`

Also fixed a stale downstream reference: the "View Error" task referenced `$var.ca47.stdout` (the old AGManager output field), which no longer exists now that `ca47` outputs `result`. Updated to `$var.ca47.result`.

All other 12 workflows left untouched.

---

## Other Workflows (No Changes)

12 remaining workflows use Kentik, NetBox, ServiceNow, MS Teams, AWS EC2 adapters. No gateway dependency.

---

## Other Adapters

`KentikV5`, `NetboxV33`, `Servicenow`, `Msteams`, `Awsec2`, `TemplateBuilder`, `MOP`, `WorkFlowEngine` — no changes needed.

---

## Reference Template

`Cisco/IOS/Projects/Cisco IOS.project.json` — `sendConfig` task pattern.

---

## Testing

- [x] Push Configuration to Device - IAG workflow deploys config via GatewayManager
- [x] All other Kentik workflows unaffected
