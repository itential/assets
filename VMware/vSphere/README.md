# vSphere

VMware vSphere is VMware's virtualization platform for datacenter and cloud infrastructure, built on the ESXi hypervisor and vCenter Server. vCenter Server provides centralized management of hosts, clusters, virtual machines, datastores, and networking across an environment, and exposes the vSphere Automation API — a REST interface — for programmatic access to that inventory.

This project provides OpenAPI specs for building automation directly against the vCenter REST API via an Integration Model — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
  - [Session Authentication](#session-authentication)
  - [Generating a Session Token](#generating-a-session-token)
- [OpenAPIs](#openapis)
  - [`vmware_vsphere_vcenter-latest.json`](#vmware_vsphere_vcenter-latestjson)
  - [`vmware_vsphere_vcenter-2.0.0.json`](#vmware_vsphere_vcenter-200json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | vCenter REST API OpenAPI specs — curated `-latest` plus the full generated spec |

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
      "value": "<vcenter-session-token>"
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

vCenter doesn't issue a static, long-lived API key. This spec's `sessionIdAuth` security scheme sends a session token as the `vmware-api-session-id` header on every request. Generate the token yourself (see below) and paste it into `authentication.sessionIdAuth.value` above.

The token expires after ~30 minutes of inactivity by default (server-configurable) — when calls start failing with `401`, regenerate the token and update the integration's Connection Properties with the new value.

### Generating a Session Token

```bash
curl -k -X POST -u '<username>:<password>' \
  https://<vcenter-hostname-or-ip>/rest/com/vmware/cis/session
```

The response is `{"value": "<session-token>"}` — use that token string (without the surrounding JSON) as the `sessionIdAuth.value` above.

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

### `vmware_vsphere_vcenter-2.0.0.json`

Full spec (178 operations), generated directly from a live vCenter 9.1 instance using VMware's [`vmware-openapi-generator`](https://github.com/vmware/vmware-openapi-generator). VMware doesn't publish a static OpenAPI/Swagger file for the vSphere Automation API, so this is captured from a running server's metamodel rather than preserved from an official vendor download — regenerate against your own vCenter if you need an exact match to a different version. See `vmware_vsphere_vcenter-latest.json` above for the curated subset if you just need common CRUD automation.
