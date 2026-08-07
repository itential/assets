# ADC

NetScaler ADC (formerly Citrix ADC / Citrix NetScaler) is an application delivery controller providing load balancing, content switching, SSL offload, global server load balancing, and high-availability clustering for application traffic. It exposes the **NITRO API**, a REST interface for configuring and monitoring the appliance, at `https://<NSIP>/nitro/v1/config/<resourcetype>`.

This project provides OpenAPI specs for building automation directly against the NITRO API via an Integration Model — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`citrix_netscaler_nitro-latest.json`](#citrix_netscaler_nitro-latestjson)
  - [`citrix_netscaler_nitro-14.1.json`](#citrix_netscaler_nitro-141json)
- [Generation Method and Caveats](#generation-method-and-caveats)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | NITRO REST API OpenAPI specs — curated `-latest` plus the full generated spec |

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

NITRO supports per-request authentication via two static headers (`X-NITRO-USER` / `X-NITRO-PASS`) instead of the session-login-and-cookie flow — this spec uses that mechanism since it needs no token retrieval/refresh logic, unlike session-based APIs (e.g. vSphere's `vmware-api-session-id`). Both headers are required on every request; set them to your NetScaler ADC username and password.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`citrix_netscaler_nitro-latest.json`](./OpenAPIs/citrix_netscaler_nitro-latest.json) | latest (curated) | 121 | Curated to 30 resource types covering core load balancing, content switching, SSL, GSLB, high availability, and basic network/system config — see breakdown below |
| [`citrix_netscaler_nitro-14.1.json`](./OpenAPIs/citrix_netscaler_nitro-14.1.json) | 14.1 | 6642 | Full spec covering all 1,806 NITRO config resource types |

### `citrix_netscaler_nitro-latest.json`

Curated to 121 operations across 30 resource types covering the NITRO resources most ADC automation actually touches, hand-reviewed for correct HTTP method availability (see [Generation Method and Caveats](#generation-method-and-caveats) — this is the one part of the spec verified by hand rather than inferred by convention).

Resources included, by category:

- **Load Balancing**: `server`, `service`, `servicegroup` (+ member binding), `lbvserver` (+ enable/disable), `lbmonitor`, `lbvserver_service_binding`, `lbvserver_servicegroup_binding`
- **Content Switching**: `csvserver` (+ enable/disable), `cspolicy`, `csaction`, `csvserver_cspolicy_binding`, `csvserver_lbvserver_binding`
- **SSL**: `sslcertkey`, `sslvserver`, `sslvserver_sslcertkey_binding`
- **GSLB**: `gslbvserver` (+ enable/disable), `gslbservice`, `gslbsite`, `gslbvserver_gslbservice_binding`, `gslbvserver_domain_binding`
- **High Availability**: `hanode`, `hafailover` (force-failover action)
- **Network**: `nsip`, `vlan`, `vlan_interface_binding`, `route`, `interface` (read/update only — physical interfaces aren't created or deleted via the API)
- **System**: `nsconfig` (get + save action), `nsversion` (read-only)

Resources not covered here — AAA, WAF (`appfw`), bot management, VPN, DNS, content inspection, and dozens of other specialized feature modules — are in the full spec.

### `citrix_netscaler_nitro-14.1.json`

Full spec (6,642 operations across all 1,806 NITRO config resource types), generated from the official [`netscaler/adc-nitro-go`](https://github.com/netscaler/adc-nitro-go) Go SDK source rather than a vendor-published OpenAPI document (none exists) or a live-appliance introspection tool. See [Generation Method and Caveats](#generation-method-and-caveats) below before using this spec — HTTP method availability per resource is a structural default, not verified per-resource.

## Generation Method and Caveats

Unlike some other Integration Models in this repo, no vendor-published OpenAPI/Swagger spec exists for the NITRO API (NetScaler's official API reference is HTML-only), and there's no live-instance generator tool analogous to `vmware-openapi-generator`. Both specs here were instead generated by parsing the Go struct definitions (fields, JSON tags, doc comments) in the official `netscaler/adc-nitro-go` SDK and mapping NITRO's well-documented, uniform REST conventions (`GET/POST/PUT/DELETE` on `/nitro/v1/config/{resourcetype}[/{name}]`, with resources wrapped in a `{"<resourcetype>": {...}}` JSON envelope) onto them.

This means:

- **Both specs are validated but untested against a live appliance.** Every operation passed OpenAPI 3.0 schema validation, Itential Platform's own integration-model validation endpoint, and successful task creation in Automation Studio for a representative sample (full CRUD, an action, a binding, and a singleton resource) — but none have been executed against a real NetScaler ADC. Verify against your own appliance before relying on this in production, and please contribute fixes back if you find discrepancies.
- **HTTP method availability in the full spec is inferred by convention, not verified per-resource.** The Go SDK is a generic REST client — it doesn't encode which of GET/POST/PUT/DELETE each of the 1,806 resource types actually supports (that's enforced by NetScaler firmware at runtime, not the SDK). The full spec defaults every non-binding resource to full CRUD and every `_binding` resource to list/create/delete (no update); some resources will legitimately reject some of these (e.g., read-only status/statistics objects, action-only resources like `reboot` or `shutdown`, and appliance-wide singletons like `nsversion` and `nshardware` that have no per-name lookup). The curated `-latest.json` was hand-reviewed to correct this for its 30 resources — treat the full spec's method list as a starting point to confirm against the [official NITRO API reference](https://developer-docs.netscaler.com/en-us/adc-nitro-api/current-release.html) or your own appliance, not as ground truth.
- **Binding resource semantics are approximate.** NITRO bindings are scoped to a parent resource's name (e.g., `GET /nitro/v1/config/lbvserver_service_binding/{name}` lists services bound to the lbvserver named `{name}`), and removing one specific binding among several often requires an additional `args` query parameter to disambiguate. Both specs model the basic list/create/delete pattern; the disambiguation query parameter isn't included and may need to be added manually for `DELETE` calls against resources with multiple bindings.
- **Field descriptions are truncated in the full spec** (first sentence only) to keep file size manageable across 1,806 resource types and roughly 14,000 fields. The curated spec keeps full vendor doc-comment text for its 30 resources.
