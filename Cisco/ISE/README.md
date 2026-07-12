Cisco Identity Services Engine (ISE) is a network access control and policy platform that authenticates and authorizes endpoints and users, enforces network access policy, and manages the network devices, certificates, and nodes that make up an ISE deployment.

This product folder provides OpenAPI specs for automating against ISE's REST APIs via Integration Models. Each spec covers one ISE API module (policy, network devices, certificates, deployment, etc.) — import only the ones your automation needs. Every module's `-latest` spec is reviewed and curated for common CRUD for automation — some needed operations trimmed, others were already in scope as-is — see **OpenAPIs** below.

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

### `cisco_ise_5g-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (16 operations). Every operation is CRUD on the 5G module's two business resources — there is no separate admin/reporting surface to exclude.

Operations included, by category:

- **Subscribers**: List, create, bulk create/update/delete, get by ID, get by IMSI, update, delete
- **User Equipment**: List, create, bulk create/update/delete, create from CSV, get by ID, get by IMEI, get all for a subscriber, update, delete

### `cisco_ise_backup_and_restore-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (6 operations). Every operation is a genuine backup/restore action or the status check for a job the same API triggers — no generic health/telemetry surface to exclude.

Operations included, by category:

- **Backup actions**: Trigger on-demand backup, cancel a running backup, get last backup status
- **Restore actions**: Trigger a restore from a named backup
- **Scheduled backup**: Create/update the recurring backup schedule

### `cisco_ise_certificates-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (22 operations). Every operation is CRUD or a provisioning action on certificates/CSRs — no self-introspection or housekeeping surface to exclude.

Operations included, by category:

- **Certificate Signing Requests**: List, generate (standard and intermediate-CA), export, get by ID, delete
- **System Certificates**: List by node, get by ID, update, delete, export, import, generate self-signed
- **Trusted Certificates**: List, get by ID, import, update, delete, export
- **Certificate lifecycle actions**: Regenerate the internal root CA chain, renew OCSP/messaging-service certificates, bind a CA-signed certificate

### `cisco_ise_custom_attributes-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (5 operations). Covers endpoint custom attribute definition CRUD.

Operations included, by category:

- **Custom attribute CRUD**: List, create, get by name, rename, delete by name

### `cisco_ise_data_connect-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (5 operations). Covers Data Connect configuration, not runtime health/telemetry — the "settings" endpoints read/write the feature's enabled state, not a health check.

Operations included, by category:

- **Connection details**: Get ODBC connection details
- **Feature settings**: Get/update whether the Data Connect feature is enabled, update the Data Connect user password, update password expiry (in days)

### `cisco_ise_deployment-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (24 operations). Every operation is CRUD or a provisioning action on deployment nodes/node-groups — no self-introspection or reporting-only surface to exclude.

Operations included, by category:

- **Nodes**: List, register a standalone node, get by hostname, update, deregister
- **Node groups**: List, create, get by name, update, delete, add node, list nodes in a group, remove node
- **High availability**: Get/update PAN HA configuration, promote standalone to primary, promote secondary to primary, demote primary to standalone
- **Node sync**: Trigger manual synchronization of a node
- **Node interfaces**: List interfaces on a node, get/configure the SXP interface
- **Profiler**: Get/update the profiler probe configuration of a PSN

### `cisco_ise_duo_identity_sync-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (8 operations). Covers Duo identity sync connections and Active Directory source lookups.

Operations included, by category:

- **Active Directory sources**: List configured Active Directories, list AD groups for a given Active Directory
- **Identity sync configs**: List, create, get by name, update, delete
- **Sync action**: Trigger a sync between an Active Directory and its MFA provider

### `cisco_ise_endpoint_replication-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (2 operations). This is a control switch (get/set whether endpoint replication is stopped), not a health check — kept as-is.

Operations included, by category:

- **Replication control**: Get/update the stop-replication status

### `cisco_ise_endpoints-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (10 operations). Covers endpoint CRUD, bulk operations, and device-type summaries.

Operations included, by category:

- **Endpoint CRUD**: List, create, get by ID/MAC, update, delete
- **Bulk operations**: Bulk create, bulk update, bulk delete, create an endpoint task
- **Reporting**: Aggregate summary by device type

### `cisco_ise_ipsec-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (9 operations). Covers IPsec connection CRUD, bulk create, and enable/disable per network device.

Operations included, by category:

- **IPsec connections**: List all nodes, create, update, get by hostname + NAD IP, delete
- **Bulk operations**: Create/update/enable/disable/remove connections in bulk
- **Enable/disable actions**: Enable/disable a connection on a node
- **Certificates**: List certificates associated with the IPsec role

### `cisco_ise_licensing-latest.json` (curated)

Trimmed to 8 of 9 upstream operations covering Smart Licensing registration, tier enable/disable, connection-type/state lookups, and eval-license status.

Operations included, by category:

- **Registration**: Get/set Smart Licensing registration information
- **Smart license state**: Get/set smart-licensing state (enabled/disabled) and connection type (direct, proxy, on-prem SSM, transport gateway)
- **Tier state**: Get/set whether a given license tier (Essential/Advantage/Premier/Device Admin) is enabled
- **Reference lookups**: Eval-license days remaining, current connection type

Excludes the static feature-to-tier reference mapping lookup (`GET /api/v1/license/system/feature-to-tier-mapping`) — a read-only catalog of which ISE features are gated behind which license tier, with no corresponding write operation in this API. Pull the full spec (`cisco_ise_licensing-1.0.0.json`) if you need it.

### `cisco_ise_lsd_settings-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (2 operations). Covers Local Session Directory (LSD) settings.

Operations included, by category:

- **LSD settings**: Get/update the endpoint-ownership and random-changing-MAC (RCM) settings

### `cisco_ise_mfa-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (6 operations). Covers Duo MFA connection CRUD and connection testing.

Operations included, by category:

- **Duo MFA connection CRUD**: List, create, get by name, update, delete
- **Connection test**: Verify the Auth/Admin API keys of the Duo host

### `cisco_ise_network_device_groups-latest.json` (curated)

Trimmed to 7 of 8 operations. Covers network device group CRUD via the ERS API. Excludes the ERS API self-introspection `versioninfo` endpoint.

### `cisco_ise_network_devices-latest.json` (curated)

Trimmed to 12 of 13 operations. Covers network device CRUD and bulk submission via the ERS API. Excludes the ERS API self-introspection `versioninfo` endpoint.

### `cisco_ise_nodes-latest.json` (curated)

Trimmed to 3 of 4 operations. Covers read-only node lookups via the ERS API. Excludes the ERS API self-introspection `versioninfo` endpoint.

### `cisco_ise_patches-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (6 operations). Covers hot patch and patch install/rollback/listing.

Operations included, by category:

- **Hot patches**: List installed hot patches, install, rollback
- **Patches**: List installed patches, install, rollback

### `cisco_ise_policy-latest.json` (curated)

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 86 of 126 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Device Admin Policy**: Policy Sets (with Authentication, Authorization, and Exception rules), Global Exceptions, Conditions, Network Conditions, Time Conditions
- **Network Access Policy**: Policy Sets (with Authentication, Authorization, and Exception rules), Global Exceptions, Conditions, Network Conditions, Time Conditions

Excluded: hit-count reset actions (analytics, not CRUD), dictionary/attribute introspection and custom-dictionary CRUD, and reference-only lookups (identity stores, service names, shell profiles, command sets, authorization profiles, security groups) that have no corresponding write operations in this API. Pull the full spec (`cisco_ise_policy-1.0.0.json`) if you need those.

### `cisco_ise_pxgrid_direct-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (7 operations). The dictionary-references lookup reflects live per-connector state (which dictionaries a configured connector references), not a static vendor catalog, so it was kept alongside the connector CRUD and connection test.

Operations included, by category:

- **Connector config CRUD**: List, create, get by name, update, delete
- **Dictionary references**: Get the map of dictionaries referenced by configured connectors
- **Connection test**: Test a connector's connection

### `cisco_ise_repository-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (6 operations). Covers repository CRUD and file listing.

Operations included, by category:

- **Repository CRUD**: List, create, get by name, update, delete
- **Files**: List files in a repository

### `cisco_ise_sgt_reservation-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (5 operations). Covers Security Group Tag (SGT) reservation CRUD and range reservation.

Operations included, by category:

- **SGT reservation CRUD**: List, get by client ID, update, delete
- **Range reservation**: Reserve a contiguous range of SGTs for a client

### `cisco_ise_system_settings-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (4 operations). Covers proxy and telemetry transport gateway settings.

Operations included, by category:

- **Proxy settings**: Get/update ISE's outbound proxy connection settings
- **Transport gateway settings**: Get/update the telemetry transport gateway settings

### `cisco_ise_task_service-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (2 operations). Read-only, but it's the shared status-polling surface that backup/restore, upgrade, patch, and certificate-regeneration operations across the other ISE modules point to for tracking the async job they just triggered — normal automation, not generic housekeeping, so nothing was removed.

Operations included, by category:

- **Task status lookups**: List all task statuses, get a task's status by ID

### `cisco_ise_trustsec-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (13 operations). Covers SGACL NBAR application CRUD and TrustSec virtual network CRUD with bulk create/update/delete.

Operations included, by category:

- **NBAR applications**: List, create, get by ID, update, delete
- **Virtual networks**: List, create, get by ID, update, delete
- **Virtual network bulk operations**: Bulk create, bulk update, bulk delete

### `cisco_ise_upgrade-latest.json` (curated)

Reviewed and confirmed already scoped to common CRUD for automation (8 operations). Covers the upgrade prepare/stage/proceed workflow and status checks.

Operations included, by category:

- **Pre-checks**: Initiate pre-checks on the primary PAN, get pre-check status
- **Staging**: Start staging, cancel staging, get staging status
- **Proceed (execute upgrade)**: Initiate the upgrade, get upgrade-proceed status
- **Summary**: Get the overall upgrade process summary status

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
