# vSphere

VMware vSphere is VMware's virtualization platform for datacenter and cloud infrastructure, built on the ESXi hypervisor and vCenter Server. vCenter Server provides centralized management of hosts, clusters, virtual machines, datastores, and networking across an environment, and exposes two generations of REST API for programmatic access to that inventory: the legacy `/rest` API (vSphere 6.5+) and the modern `/api`-based **vSphere Automation API** (7.0 U2+, Broadcom's current official name and recommended direction — `/rest` is deprecated, though still functional). This repo provides both, as two independent Integration Models and Studio Projects — see **Choosing /rest vs /api** below.

This project provides Studio Projects of workflows covering the vCenter REST API operations most useful for infrastructure automation — so you don't have to dig through the full API surface to find them — plus OpenAPI specs for building your own automation via an Integration Model. See **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [vSphere](#vsphere)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Choosing /rest vs /api](#choosing-rest-vs-api)
  - [Integration Configuration — VMware vSphere vCenter (/rest)](#integration-configuration--vmware-vsphere-vcenter-rest)
    - [Connection Properties](#connection-properties)
    - [Session Authentication](#session-authentication)
    - [Generating the Basic Auth Header](#generating-the-basic-auth-header)
  - [Integration Configuration — VMware vSphere Automation (/api)](#integration-configuration--vmware-vsphere-automation-api)
    - [Connection Properties](#connection-properties-1)
  - [OpenAPIs](#openapis)
    - [`vmware_vsphere_vcenter-latest.json`](#vmware_vsphere_vcenter-latestjson)
    - [`vmware_vsphere_vcenter-2.0.0.json`](#vmware_vsphere_vcenter-200json)
    - [`vmware_vsphere_automation-latest.json`](#vmware_vsphere_automation-latestjson)
    - [`vmware_vsphere_automation-9.1.0.0.json`](#vmware_vsphere_automation-9100json)
  - [Studio Projects](#studio-projects)
    - [VMware vSphere vCenter Project](#vmware-vsphere-vcenter-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)
    - [VMware vSphere Automation Project](#vmware-vsphere-automation-project)
      - [Folder Structure](#folder-structure-1)
      - [Dependencies](#dependencies-1)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Two independent pairs of specs — curated `-latest` plus the full spec, for both the `/rest` and `/api` generations |
| [Studio Projects/VMware vSphere vCenter](./Studio%20Projects/VMware%20vSphere%20vCenter.project.json) | 22 workflows on the legacy `/rest` API |
| [Studio Projects/VMware vSphere Automation](./Studio%20Projects/VMware%20vSphere%20Automation.project.json) | The same 22 workflows, rebuilt on the modern `/api` surface |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| VMware vCenter Server | 6.5+ for `/rest` (7.0 U2+ if you want `/api` instead — see below) |
| `VMware vSphere vCenter:latest` Integration Model | Required for the `/rest`-based project |
| `VMware vSphere Automation:latest` Integration Model | Required for the `/api`-based project |

## Choosing /rest vs /api

Both projects cover the identical 22 workflows (inventory listing, VM lifecycle, hardware CRUD) — same automation, same scope, different transport underneath. Pick based on your vCenter version:

- **Use `VMware vSphere vCenter` (`/rest`)** if your vCenter is older than 7.0 U2, or you just need the proven, already-validated option.
- **Use `VMware vSphere Automation` (`/api`)** if your vCenter is 7.0 U2+ — it's Broadcom's current recommended direction (`/rest` is deprecated, though not yet removed), and gives access to a much larger operation surface (1300+ operations in the full spec) beyond what's curated into this project's 22 workflows, if you need to extend it yourself.

**Run both in parallel** if you manage vCenters on different versions, or want both available: import both Integration Models and create two separate integration instances — `vSphere vCenter` and `vSphere Automation` — each project's workflows are wired to its own instance name, so they don't collide. The two API generations use genuinely different operations under the hood (not just different auth on the same calls), so there's no single project or instance that works interchangeably against either — you need the matching project for whichever model(s) you have imported.

## Integration Configuration — VMware vSphere vCenter (/rest)

Import `vmware_vsphere_vcenter-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your vCenter Server.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<vcenter-hostname-or-ip>",
    "base_path": ""
  },
  "authentication": {
    "sessionIdAuth": {
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://<vcenter-hostname-or-ip>/rest/com/vmware/cis/session",
        "responsePointer": "/value"
      },
      "parameters": {
        "Authorization": "Basic <base64(username:password)>"
      }
    }
  },
  "tls": {
    "enabled": true,
    "rejectUnauthorized": false
  },
  "variables": {},
  "version": "latest"
}
```

### Session Authentication

vCenter doesn't issue a static, long-lived API key. This spec's `sessionIdAuth` security scheme uses Itential Platform's dynamic API key retrieval: Itential calls vCenter's session-creation endpoint itself (using the `Authorization` credential under `parameters` above), extracts the returned token, and sends it back as the `vmware-api-session-id` header on every request. If a request comes back `401` (e.g. because the session hit its idle timeout — 30 minutes by default, server-configurable), Itential automatically re-fetches a new token and retries once, so there's no need to script your own re-login logic.

Two things to fill in above:
1. Replace `<vcenter-hostname-or-ip>` in `dynamicRetrieval.url` with your actual vCenter address (it's pre-filled as a placeholder matching the `server.host` value, but must be set explicitly here too).
2. Set `parameters.Authorization` to a Basic auth header value — see below.

### Generating the Basic Auth Header

```bash
echo -n '<username>:<password>' | base64
```

Prefix the output with `Basic ` (e.g. `Basic dXNlcjpwYXNz`) and use that full string as `parameters.Authorization` above.

## Integration Configuration — VMware vSphere Automation (/api)

Import `vmware_vsphere_automation-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your vCenter Server.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<vcenter-hostname-or-ip>",
    "base_path": "/api"
  },
  "authentication": {
    "sessionIdAuth": {
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://<vcenter-hostname-or-ip>/rest/com/vmware/cis/session",
        "responsePointer": "/value"
      },
      "parameters": {
        "Authorization": "Basic <base64(username:password)>"
      }
    }
  },
  "tls": {
    "enabled": true,
    "rejectUnauthorized": false
  },
  "variables": {},
  "version": "latest"
}
```

Same session-based dynamic retrieval as the `/rest` project (see **Session Authentication** above — the idle timeout, auto-refresh-on-401, and Basic-header generation steps are identical), with two differences specific to `/api`:

1. **`server.base_path` must be `/api`**, not empty. This spec's `servers.url` template (`https://{host}/api`) doesn't cleanly split into Itential Platform's `host`/`base_path` fields on its own — `host` should be the bare hostname, and `/api` goes in `base_path` explicitly, or business calls will 404 on the missing prefix.
2. **`dynamicRetrieval.url` targets the legacy `/rest` session endpoint**, not `/api/session` — `vmware-api-session-id` is a single, unified session token shared by both API generations, so a token minted via `/rest` works identically against `/api/*` endpoints.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`vmware_vsphere_vcenter-latest.json`](./OpenAPIs/vmware_vsphere_vcenter-latest.json) | latest (curated) | 91 | Actively-maintained, trimmed to 91 of 178 upstream `/rest` operations covering common CRUD for infrastructure automation — see breakdown below |
| [`vmware_vsphere_vcenter-2.0.0.json`](./OpenAPIs/vmware_vsphere_vcenter-2.0.0.json) | 2.0.0 | 178 | Full `/rest` spec generated from a live vCenter instance |
| [`vmware_vsphere_automation-latest.json`](./OpenAPIs/vmware_vsphere_automation-latest.json) | latest (curated) | 89 | Actively-maintained, trimmed to 89 of 1363 upstream `/api` operations — matches the `/rest` curated spec's scope 1:1 wherever `/api` has an equivalent, see breakdown below |
| [`vmware_vsphere_automation-9.1.0.0.json`](./OpenAPIs/vmware_vsphere_automation-9.1.0.0.json) | 9.1.0.0 | 1363 | Full `/api` spec, officially published by Broadcom |

### `vmware_vsphere_vcenter-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0.0`). Trimmed to 91 of 178 upstream operations covering common CRUD for vSphere infrastructure automation. The full upstream spec also covers vCenter appliance self-administration (deployment/upgrade bootstrap, TLS/certificate management, vCenter High Availability setup, SSO topology, internal vCenter services, CEIP/PSC configuration) and long-tail legacy peripheral hardware (floppy, parallel, serial ports) — none of those are included here.

Resources included, by category:

- **Inventory**: Datacenters, Clusters, Hosts, Datastores, Networks, Folders, Resource Pools
- **Virtual Machines**: Create/list/get/delete, power operations (power on/off/suspend/reset), guest OS power operations (shutdown/reboot/standby), guest identity
- **VM Hardware**: CPU, memory, boot/boot device, disks, SCSI/SATA adapters, CD-ROM, Ethernet adapters
- **Templates & OVF**: Deploy VMs from templates and OVF library items, create library items from existing VMs
- **ISO**: Mount/unmount ISO images from a content library onto a VM
- **Storage Policies**: List policies, read/assign a VM's storage policy, compliance checks
- **Guest Customization**: List guest customization specs

### `vmware_vsphere_vcenter-2.0.0.json`

Full spec (178 operations), generated directly from a live vCenter 9.1 instance using VMware's [`vmware-openapi-generator`](https://github.com/vmware/vmware-openapi-generator), which only picked up `/rest`-style bindings on this instance despite it being well past the `/api` cutover — see `vmware_vsphere_automation-9.1.0.0.json` below for the modern surface, which turned out to have an official published source instead of needing generation. Regenerate against your own vCenter if you need an exact `/rest` match to a different version. See `vmware_vsphere_vcenter-latest.json` above for the curated subset if you just need common CRUD automation.

vSphere's `/rest` API uses dot-notation query parameter names for list filters (e.g. `filter.names`, `filter.clusters`) — these optional filter parameters are omitted here too; list operations still return the full unfiltered set.

### `vmware_vsphere_automation-latest.json`

Actively-maintained spec (`x-vendor-api-version: 9.1.0.0`). Trimmed to 89 of 1363 upstream `/api` operations, deliberately matching the `/rest` curated spec's scope 1:1 wherever the modern `/api` surface has an equivalent — same automation coverage, modern transport. Two `/rest` operations (inventory datastore/network "find" queries) have no `/api` equivalent and are excluded. The full upstream spec covers vastly more: ESX host lifecycle/settings management, Content Library, Appliance self-administration, Supervisor/Namespace Management (Kubernetes), vAPI introspection, and CIS session/task management, none of which are included here — see `vmware_vsphere_automation-9.1.0.0.json` below if you need any of that.

Resources included, by category:

- **Inventory**: Datacenters, Clusters, Hosts, Datastores, Networks, Folders, Resource Pools, Storage Policies
- **Virtual Machines**: Create/list/get/delete, power operations (start/stop/reset/suspend), guest OS power operations (shutdown/reboot/standby), guest identity
- **VM Hardware**: CPU, memory, boot/boot device, disks, SCSI/SATA adapters, CD-ROM, Ethernet adapters, hardware version upgrade
- **Templates & OVF**: Deploy VMs from templates and OVF library items
- **ISO**: Mount/unmount ISO images onto a VM
- **Storage Policies**: List policies, read/assign a VM's storage policy, compliance checks
- **Guest Customization**: List guest customization specs

Every operation follows the same incoming-field pattern Itential Platform generates for OpenAPI operations: path parameters as flat fields, JSON request bodies as a `requestBodyPayload`/`bodyContentType` pair.

### `vmware_vsphere_automation-9.1.0.0.json`

Full spec (1363 operations), sourced directly from Broadcom's official [`vmware/vcf-api-specs`](https://github.com/vmware/vcf-api-specs) GitHub repository (`specifications/vsphere/openapi/automation/vcenter.yaml`) — unlike the `/rest` spec above, this one has a genuine vendor-published source, not something generated from a live instance. Preserved as published except for the `sessionIdAuth` security scheme, which was adapted from the vendor's three alternative auth methods (`basic_auth`, `api_key_auth`, `federated_identity_auth`) down to one dynamic-retrieval scheme targeting the legacy `/rest` session endpoint (see **Connection Properties** above) — `basic_auth` only works for session bootstrap, not general business endpoints, and federated/SSO auth isn't expressible as an Itential securityScheme. The one operation that structurally required `federated_identity_auth` (`Vcenter.Authentication.Token_issue`) and the `/session` path itself (absorbed into the security scheme) are excluded from both this file and the curated one, for the same reason.

---

## Studio Projects

### VMware vSphere vCenter Project

Backed by the **`VMware vSphere vCenter:latest`** Integration Model (see [`vmware_vsphere_vcenter-latest.json`](./OpenAPIs/vmware_vsphere_vcenter-latest.json) above). The project contains **22 workflows** organized into **2 folders**, one atomic workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List Clusters`, `Update Virtual Machine CPU`).

CRUD is only built out where vCenter's REST API actually supports it. Inventory objects (clusters, hosts, datastores, networks, folders, resource pools) are read-only in the API — they're pre-provisioned infrastructure, not something automation typically creates or deletes — so the Inventory folder only has List/Get workflows. Virtual machines are the one resource vCenter exposes full lifecycle management for, so the Virtual Machines folder covers create, read, hardware update (CPU, memory, disk, network adapter), power, and delete.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Inventory | List Clusters, List Hosts, List Datastores, List Networks, List Folders, List Resource Pools, List Datacenters, Get Datastore | Read-only inventory lookups |
| Virtual Machines | List Virtual Machines, Get Virtual Machine, Create Virtual Machine (from Template), Update Virtual Machine CPU, Update Virtual Machine Memory, Add/Update/Delete Virtual Machine Disk, Add/Update/Delete Virtual Machine Network Adapter, Power On/Off Virtual Machine, Delete Virtual Machine | Full VM lifecycle |

#### Dependencies

| Dependency | Notes |
|---|---|
| `VMware vSphere vCenter:latest` Integration Model | Import from [`vmware_vsphere_vcenter-latest.json`](./OpenAPIs/vmware_vsphere_vcenter-latest.json) before importing the project |
| `vSphere vCenter` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `vSphere vCenter` — update the `adapter_id` value in each workflow task if yours is named differently. Named to distinguish it from the `/api` project's `vSphere Automation` instance if running both in parallel — see **Choosing /rest vs /api** above |

### VMware vSphere Automation Project

Backed by the **`VMware vSphere Automation:latest`** Integration Model (see [`vmware_vsphere_automation-latest.json`](./OpenAPIs/vmware_vsphere_automation-latest.json) above). The project contains the same **22 workflows** in the same **2 folders** as the `/rest` project above, rebuilt on the modern `/api` operations — same names, same subset of the curated spec, same `<Operation> <Resource>` convention, so migrating between the two (or running both side by side) doesn't change how you think about the automation, only which Integration Model and instance backs it.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Inventory | List Clusters, List Hosts, List Datastores, List Networks, List Folders, List Resource Pools, List Datacenters, Get Datastore | Read-only inventory lookups |
| Virtual Machines | List Virtual Machines, Get Virtual Machine, Create Virtual Machine (from Template), Update Virtual Machine CPU, Update Virtual Machine Memory, Add/Update/Delete Virtual Machine Disk, Add/Update/Delete Virtual Machine Network Adapter, Power On/Off Virtual Machine, Delete Virtual Machine | Full VM lifecycle |

#### Dependencies

| Dependency | Notes |
|---|---|
| `VMware vSphere Automation:latest` Integration Model | Import from [`vmware_vsphere_automation-latest.json`](./OpenAPIs/vmware_vsphere_automation-latest.json) before importing the project |
| `vSphere Automation` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `vSphere Automation` — update the `adapter_id` value in each workflow task if yours is named differently. Named to run in parallel alongside the `/rest` project's `vSphere vCenter` instance without colliding |
