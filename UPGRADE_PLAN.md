# Gateway5 Upgrade Plan

Tracks the upgrade of all POC-Sample assets for compatibility with Gateway 5 (IAG5).

**Base branch:** `feature/platform-6.4-upgrade`  
**Reference assets (already complete):** Cisco IOS, Juniper JUNOS

---

## Asset Branches

| Asset | Branch | Planning Doc | Status |
|---|---|---|---|
| Alkira | `feature/gw5-upgrade/alkira` | [UPGRADE_NOTES.md](Alkira/UPGRADE_NOTES.md) | Complete |
| Arista EOS | `feature/gw5-upgrade/arista-eos` | [UPGRADE_NOTES.md](Arista/EOS/UPGRADE_NOTES.md) | Complete |
| Cisco ASA | `feature/gw5-upgrade/cisco-asa` | [UPGRADE_NOTES.md](Cisco/ASA/UPGRADE_NOTES.md) | Planning |
| F5 BIG-IP | `feature/gw5-upgrade/f5-bigip` | [UPGRADE_NOTES.md](F5/BIG-IP/UPGRADE_NOTES.md) | Planning |
| Itential Platform Config Mgmt | `feature/gw5-upgrade/itential-config-mgmt` | [UPGRADE_NOTES.md](Itential/Platform/UPGRADE_NOTES.md) | Planning |
| Kentik | `feature/gw5-upgrade/kentik` | [UPGRADE_NOTES.md](Kentik/UPGRADE_NOTES.md) | Complete |

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
| Itential Platform Data Manipulation | No app dependencies |
| Itential Platform Email | Email adapter only |
| Itential Platform Regex Operations | No app dependencies |
| Itential Platform Workflow Utilities | AppArtifacts/DBMongo only |
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

### AutomationGateway → GatewayManager (device lifecycle tasks)

F5 BIG-IP and Alkira use `AutomationGateway` for device onboarding and HTTP REST calls.
Migration path for these requires per-task analysis — see individual UPGRADE_NOTES.md.
