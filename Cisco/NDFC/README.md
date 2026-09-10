Cisco Nexus Dashboard Fabric Controller (NDFC) REST API — fabric lifecycle, VRF and network provisioning, interface configuration, switch inventory and discovery, policy management, image management (ISSU), config templates, and feature manager. Lets Itential Platform automate NDFC-managed data center fabrics end-to-end.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_ndfc-latest.json`](#cisco_ndfc-latestjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco NDFC REST API Integration Model |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco NDFC | 12.x |
| NDFC API key | Generated in NDFC under **Settings > API Tokens** |

## Integration Configuration

Import `cisco_ndfc-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration instance pointing at your Nexus Dashboard host.

Authentication requires two headers on every request: `X-Nd-Apikey` (the API key, used as the primary security scheme) and `X-Nd-Username` (the username associated with the key). Generate an API key in NDFC under **Settings > API Tokens**.

Configure the instance with `X-Nd-Apikey` as the apiKey value. Add `X-Nd-Username` as an additional static header in the instance configuration (or include it in the integration's custom headers, depending on your Itential Platform version).

The instance's `authentication`/`server` properties should look like this once configured:

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
    "base_path": "/appcenter/cisco/ndfc"
  }
}
```

**Note:** No official standalone OpenAPI spec is published by Cisco. This spec was hand-authored from the [`CiscoDevNet/ansible-dcnm`](https://github.com/CiscoDevNet/ansible-dcnm) endpoint class inventory. The live Swagger UI is available in-product at `https://<ndfc-host>/apidocs/` for additional endpoint details.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_ndfc-latest.json`](./OpenAPIs/cisco_ndfc-latest.json) | 12.x | 100 | Cisco NDFC REST API: fabrics, VRFs, networks, interfaces, inventory, policies, image management |

### `cisco_ndfc-latest.json`

Hand-authored from the CiscoDevNet/ansible-dcnm Ep* endpoint class inventory (github.com/CiscoDevNet/ansible-dcnm, `plugins/module_utils/common/api/v1/`) and the `dcnm_network`, `dcnm_vrf`, `dcnm_interface`, `dcnm_policy`, and `dcnm_inventory` module source files. No official standalone OpenAPI spec is published by Cisco — the live Swagger UI is available in-product at `https://<ndfc-host>/apidocs/`.

| Category | Operations |
|---|---|
| Fabrics | List, get, create, update, delete fabrics; config-save, config-deploy, config-preview, freeze mode, access mode, maintenance mode enable/disable/deploy |
| Switches | Fabric switch summary, list all switches, set switch roles |
| Inventory | List/get/remove switches, POAP, discover, rediscover, RMA, serial number swap, credentials |
| VRFs | CRUD, attachments, deploy, bulk create/update, VLAN ID pool |
| Networks | CRUD, attachments, deploy, status, bulk create/update, VLAN ID pool |
| Interfaces | List, get detail, create, update, bulk modify, mark delete, breakout, VPC pair, global interface deploy |
| Policies | Get, create, update, delete, bulk create, deploy, list by switch |
| Resource Manager | Get available VLAN ID, reserve/release resource IDs, fabric resource pool |
| Image Management | Image policies CRUD, attach/detach, stage, validate, upgrade, ISSU status, bootflash |
| Config Templates | List, get |
| Feature Manager | NDFC version, feature list |
