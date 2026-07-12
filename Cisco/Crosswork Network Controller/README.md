Cisco Crosswork Network Controller (CNC) is a network automation platform for provisioning, monitoring, and optimizing service provider transport and IP networks, combining device inventory/element management with service-level provisioning such as L3VPN.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | CNC OpenAPI specs — Device Management and L3VPN, each with a curated `-latest` plus the full dated version |

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

Paste the JWT as the bearer token. JWTs expire and must be refreshed manually until Cisco resolves IPSO-9866.

## OpenAPIs

### `cisco_crosswork_network_controller_device_management-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (1 operation). The upstream API exposes exactly one endpoint and it is a genuine inventory query with no separate health/metrics/version-info surface to exclude, so nothing was removed.

Operations included, by category:

- **Device inventory**: Get all devices (deep inventory query, including device detail attributes)

### `cisco_crosswork_network_controller_l3vpn-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (4 operations). The upstream API implements the IETF L3VPN NTW model as a single RESTCONF resource with full CRUD; there is no admin, health, or introspection surface to exclude, so nothing was removed.

Operations included, by category:

- **L3VPN service intent**: Get, create/replace (PUT), partially update (PATCH), delete a VPN service by `vpn-service-vpn-id`

### Full, unmodified specs

| Spec | Description |
|---|---|
| [`cisco_crosswork_network_controller_device_management-7.2.0.json`](./OpenAPIs/cisco_crosswork_network_controller_device_management-7.2.0.json) | Full Device Management spec for CNC 7.2.0. |
| [`cisco_crosswork_network_controller_l3vpn-7.2.0.json`](./OpenAPIs/cisco_crosswork_network_controller_l3vpn-7.2.0.json) | Full L3VPN spec for CNC 7.2.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| CNC Integration Model | Import from an OpenAPI spec above to build automation against the REST API. |
