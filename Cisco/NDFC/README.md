Cisco Nexus Dashboard Fabric Controller (NDFC) REST API — fabric lifecycle, VRF and network provisioning, interface configuration, switch inventory and discovery, policy management, image management (ISSU), config templates, and feature manager. Lets Itential Platform automate NDFC-managed data center fabrics end-to-end.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_ndfc-latest.json`](#cisco_ndfc-latestjson)
  - [`cisco_ndfc_lan_v12-2-2.json`](#cisco_ndfc_lan_v12-2-2json)
  - [`cisco_ndfc_san_v12-2-2.json`](#cisco_ndfc_san_v12-2-2json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco NDFC REST API Integration Models |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco NDFC | 12.2.x |
| NDFC API key | Generated in NDFC under **Settings > API Tokens** |

## Integration Configuration

Import the desired spec as an Integration Model in **Admin > Integrations**, then create an integration instance pointing at your Nexus Dashboard host.

Authentication requires two headers on every request: `X-Nd-Apikey` (the API key) and `X-Nd-Username` (the username associated with the key). Generate an API key in NDFC under **Settings > API Tokens**.

Configure the instance with `X-Nd-Apikey` as the `ApiKeyAuth` value and `X-Nd-Username` as the `ApiUsernameAuth` value:

```json
{
  "authentication": {
    "ApiKeyAuth": {
      "value": "<your-ndfc-api-key>"
    },
    "ApiUsernameAuth": {
      "value": "<your-ndfc-username>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<ndfc-host>",
    "base_path": "/appcenter/cisco/ndfc/api/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_ndfc-latest.json`](./OpenAPIs/cisco_ndfc-latest.json) | 12.2.2 | 353 | Curated LAN fabric automation: fabrics, switches, inventory, VRFs, networks, interfaces, links, vPC pairs, policies, templates, resource manager, image/ISSU management, change control, deployment |
| [`cisco_ndfc_lan_v12-2-2.json`](./OpenAPIs/cisco_ndfc_lan_v12-2-2.json) | 12.2.2 | 840 | Full Cisco NDFC LAN Fabric REST API |
| [`cisco_ndfc_san_v12-2-2.json`](./OpenAPIs/cisco_ndfc_san_v12-2-2.json) | 12.2.2 | 473 | Full Cisco NDFC SAN REST API |

### `cisco_ndfc-latest.json`

Curated from the official Cisco NDFC LAN Fabric REST API spec (published on [Cisco DevNet](https://developer.cisco.com/docs/nexus-dashboard-fabric-controller/latest/api-reference-lan/)). Covers the operations most relevant to data-center fabric automation.

| Category | Operations |
|---|---|
| Fabrics | List, get, create, update, delete; config-save, config-deploy, config-preview; access mode, maintenance mode |
| Switches | Fabric switch summary, list all, set roles |
| Inventory | List by fabric, POAP, discover, rediscover, remove, RMA, serial number swap, credentials |
| VRFs | CRUD, attachments, deploy, bulk create/update, VLAN ID pool |
| Networks | CRUD, attachments, deploy, status, bulk create/update, VLAN ID pool |
| Interfaces | List, detail, create, update, bulk modify, mark-delete, breakout, vPC pairs, global interface deploy |
| Links | Fabric link management |
| Policies | Get, create, update, delete, bulk create/deploy |
| Templates | List, get |
| Resource Manager | Get available VLAN ID, reserve/release resource IDs, fabric resource pool |
| Image Management | Image policies CRUD, attach/detach, stage, validate, upgrade, ISSU status, bootflash |
| Change Control | Change control lifecycle |
| Config Deployer | Config deployment operations |
| Deployment | Deployment status and management |
| Fabric Inventory | Fabric-level inventory operations |
| Fabric Backup and Restore | Fabric configuration backup and restore |
| Features | NDFC feature list |

### `cisco_ndfc_lan_v12-2-2.json`

Full official LAN Fabric REST API spec sourced directly from [Cisco DevNet PubHub](https://developer.cisco.com/docs/nexus-dashboard-fabric-controller/latest/api-reference-lan/). Covers all 840 operations across all LAN fabric management domains.

### `cisco_ndfc_san_v12-2-2.json`

Full official SAN REST API spec sourced directly from [Cisco DevNet PubHub](https://developer.cisco.com/docs/nexus-dashboard-fabric-controller/latest/api-reference-san/). Covers all 473 operations for SAN fabric management, including SAN topology, zoning, device alias, VSAN, portchannels, and SAN-specific image management.
