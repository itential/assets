# DCNM

Cisco Data Center Network Manager (DCNM) is the management platform for Cisco Nexus data center switching fabrics, covering fabric provisioning, inventory, top-down VRF/network automation, interface configuration, image policy management, and configuration templating.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_dcnm-latest.json`](#cisco_dcnm-latestjson)
  - [`cisco_dcnm-11.5.3.json`](#cisco_dcnm-1153json)
- [Studio Projects](#studio-projects)
  - [Folder Structure](#folder-structure)
  - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco DCNM REST API OpenAPI specs — `-latest` plus the full dated version |
| [Studio Projects/Cisco DCNM](./Studio%20Projects/Cisco%20DCNM.project.json) | 39 workflows, one per curated operation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco DCNM | 11.5(3) |
| DCNM credentials | A username/password with API access, used once to obtain a `Dcnm-Token` |

## Integration Configuration

Import [`cisco_dcnm-latest.json`](./OpenAPIs/cisco_dcnm-latest.json) as an Integration Model in **Admin > Integrations**, then create an integration pointing at your DCNM appliance.

Authentication is a token retrieved dynamically: `POST /rest/logon` with HTTP Basic credentials returns a JSON body containing the token, which is then sent as the `Dcnm-Token` header on every subsequent call. Itential Platform automates the whole exchange — you only need to supply a pre-encoded Basic credential once.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "Dcnm-Token": {
      "value": "",
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://<dcnm-hostname-or-ip>/rest/logon",
        "responsePointer": "/Dcnm-Token"
      },
      "parameters": {
        "Authorization": "Basic <base64(username:password)>"
      }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<dcnm-hostname-or-ip>",
    "base_path": ""
  }
}
```

Substitute your appliance's hostname/IP in both the `dynamicRetrieval.url` and `server.host` fields, and pre-encode your username/password as a standard HTTP Basic credential for the `Authorization` parameter (`base64("username:password")`, prefixed with `Basic `). The platform re-retrieves the token automatically on expiry.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_dcnm-latest.json`](./OpenAPIs/cisco_dcnm-latest.json) | latest (curated) | 39 | Curated fabric, inventory, interface, top-down network/VRF, policy, and template automation — see breakdown below |
| [`cisco_dcnm-11.5.3.json`](./OpenAPIs/cisco_dcnm-11.5.3.json) | 11.5.3 | 364 | Full, unmodified vendor spec |

### `cisco_dcnm-latest.json`

Trimmed to 39 of 364 upstream operations (`x-vendor-api-version: 11.5(3)`). Covers the operations most relevant to fabric and topology automation; drops the long tail of image management/ISSU, RBAC/user administration, template repository browsing, event/alarm/heartbeat monitoring, and other DCNM console-management surfaces not typically driven by automation.

| Category | Operations |
|---|---|
| Fabrics | List, get, create/update by template, config-save, config-deploy |
| Inventory | List switches, fabrics, interfaces |
| Interfaces | Get, add, update, delete, deploy |
| Networks (top-down v2) | List, create, get, update, delete, attachments, deployments |
| VRFs (top-down v2) | List, create, get, update, delete, attachments, deployments |
| Policy Management | List all policies, attach, list attached, detach, delete |
| Templates | List, get, create, validate |

### `cisco_dcnm-11.5.3.json`

Full, unmodified vendor spec for DCNM 11.5(3) (364 operations) — the vendor's complete REST API surface, preserved as-is. See `cisco_dcnm-latest.json` above for the curated version if you just need common fabric automation.

---

## Studio Projects

Import [`Cisco DCNM.project.json`](./Studio%20Projects/Cisco%20DCNM.project.json) via **Automation Studio > Projects > Import**. It contains 39 workflows — one atomic workflow per curated operation — organized into 7 folders, built on the [`cisco_dcnm-latest.json`](./OpenAPIs/cisco_dcnm-latest.json) Integration Model.

Every workflow's adapter task is wired to an Integration instance named `Cisco DCNM`. After importing, either name your Integration instance exactly `Cisco DCNM`, or update the `adapter_id` value in each workflow task to match your own instance name.

Each adapter task's `response` output is the full HTTP response envelope (`{ok, url, status, headers, text, body}`), not just the payload — the actual data is at `response.body`.

### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Fabrics | Get All Fabrics, Get Fabric, Create/Update Fabric With Nv Pairs, Config Deploy, Config Save | Fabric provisioning and config lifecycle |
| Inventory | Get Switches, Get Fabrics2, Get Interface Details | Read-only inventory lookups |
| Interfaces | Get Interface Update Dto, Add, Update, Delete Interface, Deploy | Interface CRUD and deploy |
| Networks | List, Create, Get, Update, Delete Network V2, Get Network Attach Details V2, Attach Networks V2, Deploy Networks1 V2 | Top-down network CRUD, attach, and deploy |
| VRFs | List, Create, Get, Update, Delete Vrf V2, Get Vrf Attach Details V2, Attach Vrfs V2, Deploy Vrfs1 V2 | Top-down VRF CRUD, attach, and deploy |
| Policy Management | Get All Policies, Attach Policy, Get Attached Policies, Delete Policy Mapping, Delete Policy2 | Image policy attach/detach lifecycle |
| Templates | Get All Template, Get Template, Create Template Json2, Validate Template | Config template CRUD and validation |

### Dependencies

| Dependency | Notes |
|---|---|
| `Cisco DCNM:latest` Integration Model | Import from [`cisco_dcnm-latest.json`](./OpenAPIs/cisco_dcnm-latest.json) before importing the project |
| `Cisco DCNM` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Cisco DCNM` — update the `adapter_id` value in each workflow task if yours is named differently |
