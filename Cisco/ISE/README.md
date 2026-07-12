Cisco Identity Services Engine (ISE) is a network access control and policy platform that authenticates and authorizes endpoints and users, enforces network access policy, and manages the network devices, certificates, and nodes that make up an ISE deployment.

This product folder provides OpenAPI specs for automating against ISE's REST APIs via Integration Models. Each spec covers one ISE API module (policy, network devices, certificates, deployment, etc.) — import only the ones your automation needs. The `-latest` spec in each module is either the full vendor surface or a curated CRUD subset — see **OpenAPIs** below for which.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | ISE REST API OpenAPI specs, one per module — curated/full `-latest` plus full dated versions |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco ISE | 3.x (API version `1.0.0`, see OpenAPIs below for exact spec versions available) |
| Cisco ISE Integration Model(s) | Required to build automation against the OpenAPI specs — import the module(s) you need |

## Integration Configuration

Import the OpenAPI spec(s) you need from `OpenAPIs/` as Integration Models in **Admin > Integrations**, then create an integration pointing at your ISE deployment (typically the Policy Administration Node).

Authentication is HTTP Basic, using an ISE administrator (or API-only) username and password:

```
Authorization: Basic <base64(username:password)>
```

Enable API access on the ISE node under **Administration > System > Settings > API Settings**, then use the ISE admin credentials as the Basic Auth username/password when configuring the integration.

## OpenAPIs

Every module below shares the same authentication (HTTP Basic) and vendor API version (`1.0.0`). Each has its own `-latest.json` (actively-maintained) and dated `-1.0.0.json` (full, unmodified vendor spec) pair in `OpenAPIs/`.

### `cisco_ise_5g-latest.json`

Full spec, already narrow (16 operations). Covers 5G subscriber and user-equipment CRUD for ISE's 5G network authentication module.

### `cisco_ise_backup_and_restore-latest.json`

Full spec, already narrow (6 operations). Covers configuration backup, restore, and scheduled backup.

### `cisco_ise_certificates-latest.json`

Full spec, already narrow (22 operations). Covers system certificates, certificate signing requests, trusted certificates, and root CA lifecycle management.

### `cisco_ise_custom_attributes-latest.json`

Full spec, already narrow (5 operations). Covers endpoint custom attribute definition CRUD.

### `cisco_ise_data_connect-latest.json`

Full spec, already narrow (5 operations). Covers Data Connect connection settings.

### `cisco_ise_deployment-latest.json`

Full spec, already narrow (24 operations). Covers deployment node and node-group CRUD, PAN high availability, primary/standalone promotion, node sync, node interfaces, SXP interfaces, and node profiles.

### `cisco_ise_duo_identity_sync-latest.json`

Full spec, already narrow (8 operations). Covers Duo identity sync connections and Active Directory source lookups.

### `cisco_ise_endpoint_replication-latest.json`

Full spec, already narrow (2 operations). Covers stopping/checking endpoint data replication.

### `cisco_ise_endpoints-latest.json`

Full spec, already narrow (10 operations). Covers endpoint CRUD, bulk operations, and device-type summaries.

### `cisco_ise_ipsec-latest.json`

Full spec, already narrow (9 operations). Covers IPsec connection CRUD, bulk create, and enable/disable per network device.

### `cisco_ise_licensing-latest.json`

Full spec, already narrow (9 operations). Covers Smart Licensing registration, tier state, and connection type.

### `cisco_ise_lsd_settings-latest.json`

Full spec, already narrow (2 operations). Covers Local Session Directory (LSD) settings.

### `cisco_ise_mfa-latest.json`

Full spec, already narrow (6 operations). Covers Duo MFA connection CRUD and connection testing.

### `cisco_ise_network_device_groups-latest.json`

Full spec, already narrow (8 operations). Covers network device group CRUD via the ERS API.

### `cisco_ise_network_devices-latest.json`

Full spec, already narrow (13 operations). Covers network device CRUD and bulk submission via the ERS API.

### `cisco_ise_nodes-latest.json`

Full spec, already narrow (4 operations). Covers read-only node lookups via the ERS API.

### `cisco_ise_patches-latest.json`

Full spec, already narrow (6 operations). Covers hot patch and patch install/rollback/listing.

### `cisco_ise_policy-latest.json` (curated)

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 86 of 126 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Device Admin Policy**: Policy Sets (with Authentication, Authorization, and Exception rules), Global Exceptions, Conditions, Network Conditions, Time Conditions
- **Network Access Policy**: Policy Sets (with Authentication, Authorization, and Exception rules), Global Exceptions, Conditions, Network Conditions, Time Conditions

Excluded: hit-count reset actions (analytics, not CRUD), dictionary/attribute introspection and custom-dictionary CRUD, and reference-only lookups (identity stores, service names, shell profiles, command sets, authorization profiles, security groups) that have no corresponding write operations in this API. Pull the full spec (`cisco_ise_policy-1.0.0.json`) if you need those.

### `cisco_ise_pxgrid_direct-latest.json`

Full spec, already narrow (7 operations). Covers pxGrid Direct connector configuration CRUD and connection testing.

### `cisco_ise_repository-latest.json`

Full spec, already narrow (6 operations). Covers repository CRUD and file listing.

### `cisco_ise_sgt_reservation-latest.json`

Full spec, already narrow (5 operations). Covers Security Group Tag (SGT) reservation CRUD and range reservation.

### `cisco_ise_system_settings-latest.json`

Full spec, already narrow (4 operations). Covers proxy and telemetry transport gateway settings.

### `cisco_ise_task_service-latest.json`

Full spec, already narrow (2 operations). Covers read-only async task status lookups.

### `cisco_ise_trustsec-latest.json`

Full spec, already narrow (13 operations). Covers SGACL NBAR application CRUD and TrustSec virtual network CRUD with bulk create/update/delete.

### `cisco_ise_upgrade-latest.json`

Full spec, already narrow (8 operations). Covers the upgrade prepare/stage/proceed workflow and status checks.

### Full, unmodified specs

| Spec | Description |
|---|---|
| [`cisco_ise_5g-1.0.0.json`](./OpenAPIs/cisco_ise_5g-1.0.0.json) | Full spec for the 5G module, API version 1.0.0. |
| [`cisco_ise_backup_and_restore-1.0.0.json`](./OpenAPIs/cisco_ise_backup_and_restore-1.0.0.json) | Full spec for the Backup and Restore module, API version 1.0.0. |
| [`cisco_ise_certificates-1.0.0.json`](./OpenAPIs/cisco_ise_certificates-1.0.0.json) | Full spec for the Certificates module, API version 1.0.0. |
| [`cisco_ise_custom_attributes-1.0.0.json`](./OpenAPIs/cisco_ise_custom_attributes-1.0.0.json) | Full spec for the Custom Attributes module, API version 1.0.0. |
| [`cisco_ise_data_connect-1.0.0.json`](./OpenAPIs/cisco_ise_data_connect-1.0.0.json) | Full spec for the Data Connect module, API version 1.0.0. |
| [`cisco_ise_deployment-1.0.0.json`](./OpenAPIs/cisco_ise_deployment-1.0.0.json) | Full spec for the Deployment module, API version 1.0.0. |
| [`cisco_ise_duo_identity_sync-1.0.0.json`](./OpenAPIs/cisco_ise_duo_identity_sync-1.0.0.json) | Full spec for the Duo Identity Sync module, API version 1.0.0. |
| [`cisco_ise_endpoint_replication-1.0.0.json`](./OpenAPIs/cisco_ise_endpoint_replication-1.0.0.json) | Full spec for the Endpoint Replication module, API version 1.0.0. |
| [`cisco_ise_endpoints-1.0.0.json`](./OpenAPIs/cisco_ise_endpoints-1.0.0.json) | Full spec for the Endpoints module, API version 1.0.0. |
| [`cisco_ise_ipsec-1.0.0.json`](./OpenAPIs/cisco_ise_ipsec-1.0.0.json) | Full spec for the IPSec module, API version 1.0.0. |
| [`cisco_ise_licensing-1.0.0.json`](./OpenAPIs/cisco_ise_licensing-1.0.0.json) | Full spec for the Licensing module, API version 1.0.0. |
| [`cisco_ise_lsd_settings-1.0.0.json`](./OpenAPIs/cisco_ise_lsd_settings-1.0.0.json) | Full spec for the LSD Settings module, API version 1.0.0. |
| [`cisco_ise_mfa-1.0.0.json`](./OpenAPIs/cisco_ise_mfa-1.0.0.json) | Full spec for the MFA module, API version 1.0.0. |
| [`cisco_ise_network_device_groups-1.0.0.json`](./OpenAPIs/cisco_ise_network_device_groups-1.0.0.json) | Full spec for the Network Device Groups module, API version 1.0.0. |
| [`cisco_ise_network_devices-1.0.0.json`](./OpenAPIs/cisco_ise_network_devices-1.0.0.json) | Full spec for the Network Devices module, API version 1.0.0. |
| [`cisco_ise_nodes-1.0.0.json`](./OpenAPIs/cisco_ise_nodes-1.0.0.json) | Full spec for the Nodes module, API version 1.0.0. |
| [`cisco_ise_patches-1.0.0.json`](./OpenAPIs/cisco_ise_patches-1.0.0.json) | Full spec for the Patches module, API version 1.0.0. |
| [`cisco_ise_policy-1.0.0.json`](./OpenAPIs/cisco_ise_policy-1.0.0.json) | Full spec for the Policy module (126 operations), API version 1.0.0. |
| [`cisco_ise_pxgrid_direct-1.0.0.json`](./OpenAPIs/cisco_ise_pxgrid_direct-1.0.0.json) | Full spec for the pxGrid Direct module, API version 1.0.0. |
| [`cisco_ise_repository-1.0.0.json`](./OpenAPIs/cisco_ise_repository-1.0.0.json) | Full spec for the Repository module, API version 1.0.0. |
| [`cisco_ise_sgt_reservation-1.0.0.json`](./OpenAPIs/cisco_ise_sgt_reservation-1.0.0.json) | Full spec for the SGT Reservation module, API version 1.0.0. |
| [`cisco_ise_system_settings-1.0.0.json`](./OpenAPIs/cisco_ise_system_settings-1.0.0.json) | Full spec for the System Settings module, API version 1.0.0. |
| [`cisco_ise_task_service-1.0.0.json`](./OpenAPIs/cisco_ise_task_service-1.0.0.json) | Full spec for the Task Service module, API version 1.0.0. |
| [`cisco_ise_trustsec-1.0.0.json`](./OpenAPIs/cisco_ise_trustsec-1.0.0.json) | Full spec for the TrustSec module, API version 1.0.0. |
| [`cisco_ise_upgrade-1.0.0.json`](./OpenAPIs/cisco_ise_upgrade-1.0.0.json) | Full spec for the Upgrade module, API version 1.0.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| Cisco ISE Integration Model(s) | Import from the OpenAPI spec(s) above for the module(s) you need to automate against. |
