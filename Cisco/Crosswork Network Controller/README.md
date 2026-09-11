Cisco Crosswork Network Controller (CNC) is a network automation platform for provisioning, monitoring, and optimizing service provider transport and IP networks, combining device inventory/element management with service-level provisioning such as L3VPN.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_crosswork_network_controller_device_management-latest.json`](#cisco_crosswork_network_controller_device_management-latestjson)
  - [`cisco_crosswork_network_controller_l3vpn-latest.json`](#cisco_crosswork_network_controller_l3vpn-latestjson)
  - [`cisco_crosswork_network_controller_device_management-7.2.0.json`](#cisco_crosswork_network_controller_device_management-720json)
  - [`cisco_crosswork_network_controller_l3vpn-7.2.0.json`](#cisco_crosswork_network_controller_l3vpn-720json)
- [Studio Projects](#studio-projects)
  - [Cisco Crosswork Network Controller Project](#cisco-crosswork-network-controller-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | CNC OpenAPI specs — Device Management and L3VPN, each with a curated `-latest` plus the full dated version |
| [Studio Projects/Cisco Crosswork Network Controller](./Studio%20Projects/Cisco%20Crosswork%20Network%20Controller.project.json) | 5 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco Crosswork Network Controller | 7.2.0 (see OpenAPIs below for exact spec versions available) |
| CNC Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your CNC instance.

Authentication is a Bearer JWT, obtained via a two-step CAS exchange:

1. `POST /crosswork/sso/v1/tickets` with credentials to obtain a TGT.
2. `POST` the returned TGT URL with `service=https://<cnc-host>/app-dashboard` to receive the JWT.

```
Authorization: Bearer <jwt>
```

Paste the JWT as the bearer token. JWTs expire and must be refreshed manually.

The instance's `authentication`/`server` properties should look like this once configured — `base_path` differs per spec (`/crosswork/inventory/v1` for device management, `/crosswork/proxy/nso/restconf` for L3VPN):

```json
{
  "authentication": {
    "bearerAuth": "<jwt>"
  },
  "server": {
    "protocol": "https",
    "host": "<cnc-host>:<cnc-port>",
    "base_path": "/crosswork/inventory/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_crosswork_network_controller_device_management-latest.json`](./OpenAPIs/cisco_crosswork_network_controller_device_management-latest.json) | latest (curated) | 1 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_crosswork_network_controller_l3vpn-latest.json`](./OpenAPIs/cisco_crosswork_network_controller_l3vpn-latest.json) | latest (curated) | 4 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_crosswork_network_controller_device_management-7.2.0.json`](./OpenAPIs/cisco_crosswork_network_controller_device_management-7.2.0.json) | 7.2.0 | 1 | Full Device Management spec for CNC 7.2.0. |
| [`cisco_crosswork_network_controller_l3vpn-7.2.0.json`](./OpenAPIs/cisco_crosswork_network_controller_l3vpn-7.2.0.json) | 7.2.0 | 4 | Full L3VPN spec for CNC 7.2.0. |

### `cisco_crosswork_network_controller_device_management-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (1 operation). The upstream API exposes exactly one endpoint and it is a genuine inventory query with no separate health/metrics/version-info surface to exclude, so nothing was removed.

Operations included, by category:

- **Device inventory**: Get all devices (deep inventory query, including device detail attributes)

### `cisco_crosswork_network_controller_l3vpn-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (4 operations). The upstream API implements the IETF L3VPN NTW model as a single RESTCONF resource with full CRUD; there is no admin, health, or introspection surface to exclude, so nothing was removed.

Operations included, by category:

- **L3VPN service intent**: Get, create/replace (PUT), partially update (PATCH), delete a VPN service by `vpn-service-vpn-id`

### `cisco_crosswork_network_controller_device_management-7.2.0.json`

Full, unmodified vendor spec for Device Management on CNC 7.2.0 (1 operation) — the vendor's complete API surface, preserved as-is. See `cisco_crosswork_network_controller_device_management-latest.json` above for the curated version if you just need common CRUD automation.

### `cisco_crosswork_network_controller_l3vpn-7.2.0.json`

Full, unmodified vendor spec for L3VPN on CNC 7.2.0 (4 operations) — the vendor's complete API surface, preserved as-is. See `cisco_crosswork_network_controller_l3vpn-latest.json` above for the curated version if you just need common CRUD automation.

---

## Studio Projects

### Cisco Crosswork Network Controller Project

Backed by the **`Cisco Crosswork Network Controller — Device Management:latest`** and **`Cisco Crosswork Network Controller — L3VPN:latest`** Integration Models (see the OpenAPIs above). The project contains **5 workflows** organized into **2 folders**, one atomic workflow per API operation, covering every operation in both curated specs.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Device Management | List Devices | Device inventory query |
| L3VPN | Get, Create or Replace, Update, Delete VPN Service | L3VPN service intent CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Cisco Crosswork Network Controller — Device Management:latest` Integration Model | Import from [`cisco_crosswork_network_controller_device_management-latest.json`](./OpenAPIs/cisco_crosswork_network_controller_device_management-latest.json) before importing the project |
| `Cisco Crosswork Network Controller — L3VPN:latest` Integration Model | Import from [`cisco_crosswork_network_controller_l3vpn-latest.json`](./OpenAPIs/cisco_crosswork_network_controller_l3vpn-latest.json) before importing the project |
| `Cisco Crosswork Network Controller — Device Management` and `Cisco Crosswork Network Controller — L3VPN` integration instances | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to integration instances named `Cisco Crosswork Network Controller — Device Management` and `Cisco Crosswork Network Controller — L3VPN` — update the `adapter_id` value in each workflow task if yours are named differently |
