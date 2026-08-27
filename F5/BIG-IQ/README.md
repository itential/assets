F5 BIG-IQ is F5's centralized management platform for BIG-IP devices — device discovery and onboarding, licensing, and template-based provisioning.

This project provides an OpenAPI spec for automating against BIG-IQ's REST API via an Integration Model, plus a Studio Project of workflows built on that model. It also retains a set of pre-existing workflows built on the legacy F5 BIG-IQ Adapter.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`f5_bigiq_api-latest.json`](#f5_bigiq_api-latestjson)
- [Studio Projects](#studio-projects)
  - [F5 BIG-IQ Project](#f5-big-iq-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | F5 BIG-IQ API OpenAPI spec, hand-built from F5's official API reference documentation |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing the new Integration Model workflows plus the pre-existing legacy adapter workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `F5 BIG-IQ API:latest` Integration Model | Required to run the Device Discovery & Trust/Device Groups & IP Pools/Device Reference & Machine ID/Device Templates/Global Templates & Config Sets/Licensing folders |
| [F5 BIG-IQ Adapter](https://gitlab.com/itentialopensource/adapters/adapter-f5_bigiq) | Required to run the Run Script/Sample Use Cases folders (legacy, unmigrated) |

> **Note:** This project does not require Itential Gateway for the Integration Model-backed folders. All API calls are made directly from Itential Platform to BIG-IQ's REST API.

## Integration Configuration

Import `f5_bigiq_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your BIG-IQ instance.

Authentication is HTTP Basic:

```
Authorization: Basic <base64(username:password)>
```

Use a BIG-IQ user account with appropriate role permissions for the resources you're automating.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-bigiq-username>",
      "password": "<your-bigiq-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-bigiq-instance>",
    "base_path": "/mgmt"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`f5_bigiq_api-latest.json`](./OpenAPIs/f5_bigiq_api-latest.json) | latest (curated) | 68 | Hand-built and independently verified against F5's official documentation — see breakdown below |

### `f5_bigiq_api-latest.json`

F5 does not publish a downloadable OpenAPI/Swagger spec for BIG-IQ, and no live instance self-generates one either. This spec was hand-built from F5's official per-endpoint API reference documentation at [clouddocs.f5.com](https://clouddocs.f5.com/products/big-iq/mgmt-api/latest/ApiReferences/bigiq_public_api_ref/) — every operation's path, HTTP verb, and request/response fields were independently verified against that documentation before inclusion.

Scoped to BIG-IQ's own fleet-management capabilities — device discovery/trust/import, device and service-catalog templates, device management IP pools, and license management (purchased-pool and RegKey licensing, utility billing). Excludes BIG-IP device configuration reached through BIG-IQ's working-config and rest-proxy mechanisms (LTM pools, virtual servers, nodes, network interfaces, etc.) — that's BIG-IP's own configuration surface; see [F5/BIG-IP](../BIG-IP/) for direct BIG-IP device management.

Resources included, by category:

- **Device Discovery & Trust**: Discover, trust, import, and remove devices (including a combined discover+import task)
- **Device Groups & IP Pools**: Device management IP pools — list, create, get, update, delete
- **Device Reference & Machine ID**: Resolve a device reference or machine ID from a hostname/address
- **Device Templates**: Device onboarding templates — create, get, update, delete
- **Global Templates & Config Sets**: Service catalog templates and template-based application config deployment
- **Licensing**: Purchased-pool licenses, RegKey pools and offerings, license assignment by address, utility billing reports

## Studio Projects

### F5 BIG-IQ Project

Backed by the **`F5 BIG-IQ API:latest`** Integration Model (see [`f5_bigiq_api-latest.json`](./OpenAPIs/f5_bigiq_api-latest.json) above) for the new folders, plus the pre-existing legacy adapter folders.

#### Folder Structure

| Folder | Workflows | Scope | Backing |
|---|---|---|---|
| Device Discovery & Trust | 16 | Discovery, trust, import, and removal lifecycle | `F5 BIG-IQ API:latest` Integration Model |
| Device Groups & IP Pools | 5 | Device management IP pool CRUD | `F5 BIG-IQ API:latest` Integration Model |
| Device Reference & Machine ID | 3 | Device/machine-ID lookup helpers | `F5 BIG-IQ API:latest` Integration Model |
| Device Templates | 4 | Device onboarding template CRUD | `F5 BIG-IQ API:latest` Integration Model |
| Global Templates & Config Sets | 7 | Service catalog templates, apply-template, config sets | `F5 BIG-IQ API:latest` Integration Model |
| Licensing | 33 | Purchased-pool and RegKey license management, utility billing | `F5 BIG-IQ API:latest` Integration Model |
| Run Script | 1 | Run a script on a BIG-IP device (legacy) | F5 BIG-IQ Adapter |
| Sample Use Cases | 18 | Full BIG-IP upgrade lifecycle: iHealth, backup, upgrade, reboot, rollback (legacy) | F5 BIG-IQ Adapter |

#### Dependencies

| Dependency | Notes |
|---|---|
| `F5 BIG-IQ API:latest` Integration Model | Import from [`f5_bigiq_api-latest.json`](./OpenAPIs/f5_bigiq_api-latest.json) before importing the project. Backs the Device Discovery & Trust, Device Groups & IP Pools, Device Reference & Machine ID, Device Templates, Global Templates & Config Sets, and Licensing folders. |
| `F5 BIG-IQ` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `F5 BIG-IQ` — update the `adapter_id` value in each workflow task if yours is named differently |
| [F5 BIG-IQ Adapter](https://gitlab.com/itentialopensource/adapters/adapter-f5_bigiq) | Required for the Run Script and Sample Use Cases folders (legacy, unmigrated) |

**Testing status:** all 68 new workflows were created and schema-validated against a running Itential Platform instance. No BIG-IQ test instance was available for this pass, so none have been executed against a live account.
