# Gateway5 Upgrade Plan

Tracks the upgrade of all POC-Sample assets for compatibility with Gateway 5 (Itential Gateway 5.x).

**Base branch:** `main`
**Reference assets (already complete):** Cisco IOS, Juniper JUNOS

---

## Asset Branches (this PR)

| Asset | Branch | Planning Doc | Status |
|---|---|---|---|
| Cisco ASA | `feature/gw5-upgrade/main-pr` | [UPGRADE_NOTES.md](Cisco/ASA/UPGRADE_NOTES.md) | Complete |
| Kentik | `feature/gw5-upgrade/main-pr` | [UPGRADE_NOTES.md](Kentik/UPGRADE_NOTES.md) | Complete |

---

## Resolved Upstream (no action needed in this PR)

These assets were originally scoped for this upgrade effort, but `main` has since resolved them independently — re-doing the migration here would be redundant or would target files/paths that no longer exist.

| Asset | Reason |
|---|---|
| Alkira | Entire `Alkira/` directory removed from `main` (repo curation pass) — nothing left to migrate. |
| F5 BIG-IP | `main` replaced the old `AutomationGateway`/workflow-task pattern entirely with a native `device-drivers/f5-rest` Itential Gateway 5.x REST driver. The old `Projects`/`Automations` this plan targeted no longer exist. |
| Itential Platform Configuration Management | Entire `Itential/Platform/` directory (including Configuration Management, Data Manipulation, Email, Regex Operations, and Workflow Utilities projects) removed from `main`. |
| Arista EOS | `main`'s `Studio Projects/Arista EOS.project.json` is already fully migrated to `GatewayManager.sendConfig` (`cluster-itential`), matching the intended fix exactly — no `AGManager` references remain. |

---

## Assets — No Changes Required

These assets use native REST/SDK adapters and have no gateway-dependent tasks.

| Asset | Reason |
|---|---|
| Apache Kafka 2.x | Kafka adapter only |
| Atlassian Jira | Jira adapter only |
| AWS EC2 | EC2 adapter only |
| Cisco Meraki | Meraki adapter only |
| Cisco NSO | NSO/NSOManager — own integration path |
| Cisco NX-OS | ConfigurationManager + MOP, no gateway tasks |
| F5 BIG-IQ | F5BigIQ adapter only |
| GitHub | GitHub adapter only |
| GitLab | GitLab adapter only |
| Infoblox NIOS DDI | Infoblox adapter only |
| IP Fabric | IpFabric adapter only |
| Microsoft Teams | Teams adapter only |
| NetBox | NetBox adapter only |
| Palo Alto Panorama | Panorama + MOP only |
| ServiceNow | ServiceNow adapter only |
| Versa Director | VersaDirector adapter only |
| Ruckus Fastiron | Device driver added in latest devel pull |

---

## Change Pattern Reference

### AGManager → GatewayManager (CLI/Netmiko-based tasks)

**Before:**
```json
{
  "app": "AGManager",
  "displayName": "AG Manager",
  "name": "itential_cli",
  "variables": {
    "incoming": {
      "_hosts": "$var.xxx.deviceList",
      "_groups": "",
      "command": "$var.xxx.configurationList"
    }
  }
}
```

**After:**
```json
{
  "app": "GatewayManager",
  "displayName": "GatewayManager",
  "name": "sendConfig",
  "description": "Send configuration to inventory nodes through a Gateway5 service",
  "variables": {
    "incoming": {
      "clusterId": "cluster-itential",
      "config": "$var.xxx.renderedTemplate",
      "inventory": "$var.xxx.renderedTemplate"
    },
    "outgoing": {
      "result": ""
    }
  }
}
```

Don't forget downstream references to the migrated task's old `stdout` output (e.g. a "View Error" task) — update them to `result`.
