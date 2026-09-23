# Cloud on AWS

VMware Cloud on AWS (VMC on AWS) runs a VMware Software-Defined Data Center (SDDC) on dedicated, elastic, bare-metal AWS infrastructure, giving a consistent vSphere-based operating model across on-premises and AWS. The VMware Cloud on AWS API exposes SDDC lifecycle, cluster and host scaling, logical networking, and public IP management over HTTP, with long-running operations tracked as async tasks.

This project provides an OpenAPI spec for automating against the VMware Cloud on AWS API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`vmware_cloud_on_aws-latest.json`](#vmware_cloud_on_aws-latestjson)
  - [`vmware_cloud_on_aws-1.10.json`](#vmware_cloud_on_aws-110json)
- [Studio Projects](#studio-projects)
  - [VMware Cloud on AWS Project](#vmware-cloud-on-aws-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | VMware Cloud on AWS API OpenAPI specs — curated `-latest` plus the dated reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 23 workflows in 7 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| A VMware Cloud on AWS organization, with a CSP API token generated for it | — |
| `VMware Cloud on AWS:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `vmware_cloud_on_aws-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the VMware Cloud on AWS API. The API is rooted at `/vmc/api` — this must be set in the instance's `server.base_path` field, since the platform builds the request URL from `protocol`/`host`/`port`/`base_path` rather than any path in the OpenAPI spec itself.

Authentication exchanges a CSP API token (generated in the VMware Cloud Services Console under My Account > API Tokens) for a short-lived access token, via a form-urlencoded POST to the CSP token-exchange endpoint. Itential Platform performs this exchange automatically and replays the resulting `access_token` on the `csp-auth-token` header of every request, with no prefix, re-retrieving it once it expires.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "vmc.vmware.com",
    "port": "443",
    "base_path": "/vmc/api"
  },
  "authentication": {
    "cspAuthToken": {
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize",
        "responsePointer": "/access_token"
      },
      "parameters": {
        "refresh_token": "<your-csp-api-token>"
      }
    }
  },
  "tls": {
    "enabled": true,
    "rejectUnauthorized": true
  },
  "variables": {},
  "version": "latest"
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`vmware_cloud_on_aws-latest.json`](./OpenAPIs/vmware_cloud_on_aws-latest.json) | latest (curated) | 23 | Curated to SDDC, cluster/host, network, public IP, org, and task CRUD — see breakdown below |
| [`vmware_cloud_on_aws-1.10.json`](./OpenAPIs/vmware_cloud_on_aws-1.10.json) | 1.10 | 35 | Reference spec covering the same resource areas plus core-adjacent read/administrative operations (provision specs, SDDC templates, storage constraints, DNS mode, one-host-to-multi-host conversion) |

### `vmware_cloud_on_aws-latest.json`

Curated to the core CRUD categories.

Resources included, by category:

- **Orgs**: list organizations, get organization details
- **SDDC**: provision, get, list, rename, delete an SDDC
- **Clusters**: add a cluster, delete a cluster, reconfigure a cluster
- **Hosts**: add or remove ESX hosts in an SDDC
- **Public IPs**: allocate, list, get, attach/detach, free a public IP
- **Networks**: create, list, get, update, delete a logical network (segment)
- **Tasks**: list tasks, get task status/details — for polling the async operations above

### `vmware_cloud_on_aws-1.10.json`

Reference spec for VMware Cloud on AWS API 1.10, covering the same resource areas as `-latest` plus core-adjacent operations: SDDC provision specs, one-host-to-multi-host SDDC conversion, DNS mode switching, per-cluster and per-org storage constraints, SDDC configuration templates, and org providers/payment methods. See `vmware_cloud_on_aws-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### VMware Cloud on AWS Project

Backed by the **`VMware Cloud on AWS:latest`** Integration Model (see [`vmware_cloud_on_aws-latest.json`](./OpenAPIs/vmware_cloud_on_aws-latest.json) above). The project contains **23 workflows** organized into **7 folders**, one atomic workflow per API operation.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| SDDC | 5 | List, create, get, rename, delete an SDDC |
| Public IPs | 5 | List, allocate, get, update (attach/detach), delete a public IP |
| Networks | 5 | List, create, get, update, delete a logical network (segment) |
| Clusters | 3 | Create, delete, reconfigure a cluster |
| Tasks | 2 | List tasks, get task |
| Orgs | 2 | Get organizations, get organization |
| Hosts | 1 | Add or remove ESX hosts |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `VMware Cloud on AWS:latest` Integration Model | Import from [`vmware_cloud_on_aws-latest.json`](./OpenAPIs/vmware_cloud_on_aws-latest.json) before importing the project |
| `VMware Cloud on AWS` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `VMware Cloud on AWS` — update the `adapter_id` value in each workflow task if yours is named differently |
