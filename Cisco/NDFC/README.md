Cisco Nexus Dashboard Fabric Controller (NDFC) REST API — LAN fabric lifecycle and SAN fabric management. Lets Itential Platform automate NDFC-managed data center fabrics end-to-end.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_ndfc_lan-latest.json`](#cisco_ndfc_lan-latestjson)
  - [`cisco_ndfc_san-latest.json`](#cisco_ndfc_san-latestjson)
  - [`cisco_ndfc_lan-12.2.2.json`](#cisco_ndfc_lan-1222json)
  - [`cisco_ndfc_san-12.2.2.json`](#cisco_ndfc_san-1222json)

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
| [`cisco_ndfc_lan-latest.json`](./OpenAPIs/cisco_ndfc_lan-latest.json) | latest (curated) | 353 | Curated LAN fabric automation: fabrics, switches, inventory, VRFs, networks, interfaces, policies, templates, resource manager, image/ISSU management |
| [`cisco_ndfc_san-latest.json`](./OpenAPIs/cisco_ndfc_san-latest.json) | latest (curated) | 252 | Curated SAN automation: inventory, discovery, VSAN, zone manager, device alias, portchannels, port monitoring, topology, config archive/drift, image/ISSU management |
| [`cisco_ndfc_lan-12.2.2.json`](./OpenAPIs/cisco_ndfc_lan-12.2.2.json) | 12.2.2 | 840 | Full Cisco NDFC LAN Fabric REST API |
| [`cisco_ndfc_san-12.2.2.json`](./OpenAPIs/cisco_ndfc_san-12.2.2.json) | 12.2.2 | 473 | Full Cisco NDFC SAN REST API |

### `cisco_ndfc_lan-latest.json`

Curated from the official Cisco NDFC LAN Fabric REST API spec (published on [Cisco DevNet](https://developer.cisco.com/docs/nexus-dashboard-fabric-controller/latest/api-reference-lan/), `x-vendor-api-version: 12.2.2`). Covers the operations most relevant to data-center LAN fabric automation.

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

### `cisco_ndfc_san-latest.json`

Curated from the official Cisco NDFC SAN REST API spec (published on [Cisco DevNet](https://developer.cisco.com/docs/nexus-dashboard-fabric-controller/latest/api-reference-san/), `x-vendor-api-version: 12.2.2`). Covers the operations most relevant to SAN fabric automation.

| Category | Operations |
|---|---|
| SAN Inventory | Switch inventory and discovery |
| SAN Discovery Manager | Discovery management |
| SAN VSAN | VSAN create, update, delete, list |
| SAN Zone Manager | Zone and zoneset management |
| SAN Device Alias | Device alias configuration |
| SAN PortChannel | PortChannel management |
| SAN Port Monitoring | Port monitoring policies |
| SAN Topology | Topology discovery and management |
| SAN Credential Management | Switch credential management |
| SAN Config Archive / Config Drift | Config archive and drift detection |
| SAN Image Management | SAN-specific image management |
| ISSU Reports / ISSU Upgrade | In-service software upgrade |
| Stage Management | Image staging |
| Upgrade Management | Upgrade lifecycle |
| Policy Management | Policy CRUD |
| Templates | Config template list and get |
| Features / Switch Features | Feature management |

### `cisco_ndfc_lan-12.2.2.json`

Full official LAN Fabric REST API spec sourced directly from [Cisco DevNet](https://developer.cisco.com/docs/nexus-dashboard-fabric-controller/latest/api-reference-lan/). Covers all 840 operations across all LAN fabric management domains.

### `cisco_ndfc_san-12.2.2.json`

Full official SAN REST API spec sourced directly from [Cisco DevNet](https://developer.cisco.com/docs/nexus-dashboard-fabric-controller/latest/api-reference-san/). Covers all 473 operations for SAN fabric management, including SAN topology, zoning, device alias, VSAN, portchannels, and SAN-specific image management.
