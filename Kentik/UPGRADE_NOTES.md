# Kentik — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/kentik`  
**Status:** Planning  
**Files to modify:** `Kentik/Projects/Kentik.project.json`

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

> **Note:** The Kentik project has 13 workflows and many adapters. Make the targeted change only in `Push Configuration to Device - IAG`. All other workflows use `KentikV5`, `NetboxV33`, `Servicenow`, `Msteams`, `Awsec2` — leave those untouched.

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

- [ ] Push Configuration to Device - IAG workflow deploys config via GatewayManager
- [ ] All other Kentik workflows unaffected
