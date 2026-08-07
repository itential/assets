# vSphere

VMware vSphere is VMware's virtualization platform for datacenter and cloud infrastructure, built on the ESXi hypervisor and vCenter Server. vCenter Server provides centralized management of hosts, clusters, virtual machines, datastores, and networking across an environment, and exposes the vSphere Automation API — a REST interface — for programmatic access to that inventory.

This project provides a Studio Project of workflows covering the vCenter REST API operations most useful for infrastructure automation — so you don't have to dig through the full API surface to find them — plus OpenAPI specs for building your own automation via an Integration Model. See **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
  - [Session Authentication](#session-authentication)
  - [Generating the Basic Auth Header](#generating-the-basic-auth-header)
- [OpenAPIs](#openapis)
  - [`vmware_vsphere_vcenter-latest.json`](#vmware_vsphere_vcenter-latestjson)
  - [`vmware_vsphere_vcenter-2.0.0.json`](#vmware_vsphere_vcenter-200json)
- [Studio Projects](#studio-projects)
  - [VMware vSphere vCenter Project](#vmware-vsphere-vcenter-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | vCenter REST API OpenAPI specs — curated `-latest` plus the full generated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 22 workflows in 2 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| VMware vCenter Server | 7.0+ (generated against 9.1; the included VM/host/cluster/datastore operations are stable across 7.0–9.x) |
| `VMware vSphere vCenter:latest` Integration Model | Required to build automation against the OpenAPI specs |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the vCenter REST API.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your vCenter Server.

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

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`vmware_vsphere_vcenter-latest.json`](./OpenAPIs/vmware_vsphere_vcenter-latest.json) | latest (curated) | 91 | Actively-maintained, trimmed to 91 of 178 upstream operations covering common CRUD for infrastructure automation — see breakdown below |
| [`vmware_vsphere_vcenter-2.0.0.json`](./OpenAPIs/vmware_vsphere_vcenter-2.0.0.json) | 2.0.0 | 178 | Full spec generated from a live vCenter instance |

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

**Note on `list` filter parameters**: vSphere's REST API uses dot-notation query parameter names for list filters (e.g. `filter.names`, `filter.clusters`). Itential Platform's task-naming convention doesn't permit dots in parameter names, and there's no way to alias a task's input name independently of the actual wire parameter name — so these optional filter parameters are omitted from every `list` operation. All `list` operations still work and return the full unfiltered result set; filter client-side (e.g. with a transformation task) if you need to narrow results.

### `vmware_vsphere_vcenter-2.0.0.json`

Full spec (178 operations), generated directly from a live vCenter 9.1 instance using VMware's [`vmware-openapi-generator`](https://github.com/vmware/vmware-openapi-generator). VMware doesn't publish a static OpenAPI/Swagger file for the vSphere Automation API, so this is captured from a running server's metamodel rather than preserved from an official vendor download — regenerate against your own vCenter if you need an exact match to a different version. See `vmware_vsphere_vcenter-latest.json` above for the curated subset if you just need common CRUD automation.

The same dot-notation filter parameters described above are omitted here too, for the same reason (Itential Platform naming convention incompatibility).

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
| `vSphere` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `vSphere` — update the `adapter_id` value in each workflow task if yours is named differently |

#### Known Limitations

- **No server-side filtering**: every `List` workflow returns the full unfiltered inventory (see [Note on `list` filter parameters](#vmware_vsphere_vcenter-latestjson) above / PROAD-654). Filter client-side if you need a subset.
- **No cluster/host/resource-pool capacity data**: vCenter's REST API doesn't expose CPU or memory utilization for clusters, hosts, or resource pools — that data lives in the older SOAP-based Performance Manager API, which isn't part of this Integration Model. `Get Datastore` is the only workflow with a real capacity number (`free_space`); there's no equivalent for compute capacity.
- **No built-in error handling**: workflow tasks have a single success transition and no error branch, by design, to keep each workflow's canvas minimal. A failed task will fail the job rather than routing to a graceful error path.
