# ADC

NetScaler ADC (formerly Citrix ADC / Citrix NetScaler) is an application delivery controller providing load balancing, content switching, SSL offload, global server load balancing, and high-availability clustering for application traffic. It exposes the **NITRO API**, a REST interface for configuring and monitoring the appliance, at `https://<NSIP>/nitro/v1/config/<resourcetype>`.

This project provides a Studio Project of workflows covering the NITRO API operations most useful for infrastructure automation, plus OpenAPI specs for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [ADC](#adc)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`citrix_netscaler_nitro-latest.json`](#citrix_netscaler_nitro-latestjson)
    - [`citrix_netscaler_nitro-14.1.json`](#citrix_netscaler_nitro-141json)
  - [Studio Projects](#studio-projects)
    - [NetScaler ADC Project](#netscaler-adc-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | NITRO REST API OpenAPI specs — curated `-latest` plus the full generated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 132 workflows in 8 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| NetScaler ADC | 13.0+ (generated from the official `netscaler/adc-nitro-go` SDK targeting 14.1; NITRO's resource model has been stable across 13.x–14.x) |
| `Citrix NetScaler NITRO API:latest` Integration Model | Required to build automation against the OpenAPI specs |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the NITRO API.

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your NetScaler ADC's NSIP (management IP).

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<nsip>",
    "base_path": ""
  },
  "authentication": {
    "nitroUser": {
      "value": "<username>"
    },
    "nitroPass": {
      "value": "<password>"
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

NITRO supports per-request authentication via two static headers (`X-NITRO-USER` / `X-NITRO-PASS`) instead of a session-login-and-cookie flow, so there's no token retrieval/refresh logic involved. Both headers are required on every request; set them to your NetScaler ADC username and password.

**Port:** the connection schema has no separate port field — if your appliance's NITRO API isn't on the default port for its protocol (80 for HTTP, 443 for HTTPS), append the actual port directly to `server.host` (e.g. `"host": "<nsip>:<port>"`). Confirm the real management port with your NetScaler admin rather than assuming — a wrong port produces a connection-level failure (`status: 0`, no response) that looks identical to a network/firewall/DNS problem, and is easy to mistake for one.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`citrix_netscaler_nitro-latest.json`](./OpenAPIs/citrix_netscaler_nitro-latest.json) | latest (curated) | 137 | Curated to 34 resource types covering core load balancing, content switching, SSL, GSLB, high availability, basic network/system config, and responder policies — see breakdown below |
| [`citrix_netscaler_nitro-14.1.json`](./OpenAPIs/citrix_netscaler_nitro-14.1.json) | 14.1 | 6642 | Full spec covering all 1,806 NITRO config resource types |

### `citrix_netscaler_nitro-latest.json`

Curated to 137 operations across 34 resource types covering the NITRO resources most ADC automation actually touches, hand-reviewed for correct HTTP method availability (see [Generation Method and Caveats](#generation-method-and-caveats) — this is the one part of the spec verified by hand rather than inferred by convention).

Resources included, by category:

- **Load Balancing**: `server`, `service`, `servicegroup` (+ member binding), `lbvserver` (+ enable/disable), `lbmonitor`, `lbvserver_service_binding`, `lbvserver_servicegroup_binding`
- **Content Switching**: `csvserver` (+ enable/disable), `cspolicy`, `csaction`, `csvserver_cspolicy_binding`, `csvserver_lbvserver_binding`
- **SSL**: `sslcertkey`, `sslvserver`, `sslvserver_sslcertkey_binding`
- **GSLB**: `gslbvserver` (+ enable/disable), `gslbservice`, `gslbsite`, `gslbvserver_gslbservice_binding`, `gslbvserver_domain_binding`
- **High Availability**: `hanode`, `hafailover` (force-failover action)
- **Network**: `nsip`, `vlan`, `vlan_interface_binding`, `route`, `interface` (read/update only — physical interfaces aren't created or deleted via the API)
- **System**: `nsconfig` (get + save action), `nsversion` (read-only)
- **Responder**: `responderaction`, `responderpolicy`, `responderpolicy_csvserver_binding`, `responderpolicy_lbvserver_binding`

Resources not covered here — AAA, WAF (`appfw`), bot management, VPN, DNS, content inspection, and dozens of other specialized feature modules — are in the full spec.

### `citrix_netscaler_nitro-14.1.json`

Full spec (6,642 operations across all 1,806 NITRO config resource types), generated from the official [`netscaler/adc-nitro-go`](https://github.com/netscaler/adc-nitro-go) Go SDK source rather than a vendor-published OpenAPI document (none exists) or a live-appliance introspection tool. See [Generation Method and Caveats](#generation-method-and-caveats) below before using this spec — HTTP method availability per resource is a structural default, not verified per-resource.

---

## Studio Projects

### NetScaler ADC Project

Backed by the **`Citrix NetScaler NITRO API:latest`** Integration Model (see [`citrix_netscaler_nitro-latest.json`](./OpenAPIs/citrix_netscaler_nitro-latest.json) above). The project contains **132 workflows** organized into **8 folders**, one workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List LB Virtual Servers`, `Enable LB Virtual Server`).

CRUD is only built out where NITRO's REST API actually supports it, and further scoped to the resources that represent genuine day-to-day ADC automation rather than every operation in the curated spec:

- **Full CRUD** (create/read/update/delete): `server`, `service`, `servicegroup`, `lbvserver` (+ enable/disable), `lbmonitor`, `csvserver` (+ enable/disable), `cspolicy`, `csaction`, `sslcertkey`, `gslbvserver` (+ enable/disable), `gslbservice`, `gslbsite`, `nsip`, `vlan`, `route` (create/list/delete — NITRO has no route update), `responderaction`, `responderpolicy`
- **Read/update only**: `sslvserver`, `interface` — property overlays on things that already exist (an SSL-enabled vserver, a physical NIC), not created or deleted independently
- **Bind/unbind** (list/create/delete, no update): the 11 binding resources that support the objects above, e.g. `lbvserver_service_binding`, `csvserver_cspolicy_binding`, `responderpolicy_csvserver_binding`
- **Singleton/action**: `nsconfig` (get + save), `nsversion` (read-only), `hafailover` (force-failover action)

`hanode` (HA node add/remove) is deliberately excluded — adding or removing a node from an HA pair is a rare, high-blast-radius operation, not routine automation, so it's left out of the Studio Project even though it's in the curated OpenAPI spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Load Balancing | 36 | `server`, `service`, `servicegroup` (+ member binding), `lbvserver` (+ bindings, enable/disable), `lbmonitor` |
| Content Switching | 23 | `csvserver` (+ bindings, enable/disable), `cspolicy`, `csaction` |
| SSL | 10 | `sslcertkey`, `sslvserver` (+ cert binding) |
| GSLB | 23 | `gslbvserver` (+ bindings, enable/disable), `gslbservice`, `gslbsite` |
| Network | 20 | `nsip`, `vlan` (+ interface binding), `route`, `interface` |
| Responder | 16 | `responderaction`, `responderpolicy` (+ CS/LB vserver bindings) |
| System | 3 | `nsconfig` (get + save), `nsversion` |
| High Availability | 1 | `hafailover` (force-failover action only) |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Citrix NetScaler NITRO API:latest` Integration Model | Import from [`citrix_netscaler_nitro-latest.json`](./OpenAPIs/citrix_netscaler_nitro-latest.json) before importing the project |
| `NetScaler` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `NetScaler` — update the `adapter_id` value in each workflow task if yours is named differently |
