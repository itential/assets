Cisco Catalyst SD-WAN Manager (formerly vManage) is the centralized management console for Cisco's SD-WAN overlay network, providing device onboarding, template-based configuration, certificate management, monitoring, and centralized policy control across the fabric.

This project provides OpenAPI specs for automating against Catalyst SD-WAN Manager's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_catalyst_sdwan_manager-latest.json`](#cisco_catalyst_sdwan_manager-latestjson)
  - [`cisco_catalyst_sdwan_manager-20.15.json`](#cisco_catalyst_sdwan_manager-2015json)
  - [`cisco_catalyst_sdwan_manager-20.12.json`](#cisco_catalyst_sdwan_manager-2012json)
- [Studio Projects](#studio-projects)
  - [Cisco Catalyst SD-WAN Manager Project](#cisco-catalyst-sd-wan-manager-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco Catalyst SD-WAN Manager API OpenAPI specs — curated `-latest` plus two full vendor releases |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 289 workflows in 11 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Cisco Catalyst SD-WAN Manager:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `cisco_catalyst_sdwan_manager-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Catalyst SD-WAN Manager instance.

Authentication is session-cookie based, not a header/bearer token, and it's a two-step handshake vManage requires directly from the client:

1. `POST /j_security_check` with form-encoded `j_username`/`j_password` — the response's `Set-Cookie` header contains the `JSESSIONID` session cookie.
2. `GET /client/token` (using that cookie) returns an `X-XSRF-TOKEN` value that must be sent as a header on every state-changing (`POST`/`PUT`/`DELETE`) request for the remainder of the session.

Itential Platform's dynamic-retrieval mechanism for API-key security schemes can only extract a token from a JSON response body field, not a response header, so it cannot perform step 1 automatically. Both values need to be obtained out-of-band (manually, or via an external scheduled script) and kept current on the integration instance and in each mutating workflow's `X-XSRF-TOKEN` input — sessions expire after 30 minutes of inactivity or 24 hours total.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "sessionCookieAuth": {
      "JSESSIONID": "<session-cookie-value-from-step-1>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-vmanage-host>",
    "base_path": "/dataservice"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_catalyst_sdwan_manager-latest.json`](./OpenAPIs/cisco_catalyst_sdwan_manager-latest.json) | latest (curated) | 289 | Curated to device management, certificates, monitoring, administration, and centralized policy — see breakdown below |
| [`cisco_catalyst_sdwan_manager-20.15.json`](./OpenAPIs/cisco_catalyst_sdwan_manager-20.15.json) | 20.15 | 3815 | Full vendor spec, release 20.15 |
| [`cisco_catalyst_sdwan_manager-20.12.json`](./OpenAPIs/cisco_catalyst_sdwan_manager-20.12.json) | 20.12 | 3445 | Full vendor spec, release 20.12 (Cisco's official DevNet-published export) |

### `cisco_catalyst_sdwan_manager-latest.json`

Built from Cisco's 20.15 OpenAPI export, curated to the operations most commonly automated against Catalyst SD-WAN Manager.

Resources included, by category:

- **Device Inventory**: onboarding, bootstrap config, claiming, discovery
- **Device Actions**: reboot, upgrade, partition management, LXC container lifecycle
- **Device Templates** / **Feature Templates**: template CRUD, attach/detach to devices
- **Certificate Management**: CSR generation, install, root/enterprise cert lifecycle for controllers and edge devices
- **Alarms** and **Device Monitoring**: alarm querying and device state/statistics
- **User and Group Administration**: local users, groups, AAA/RADIUS/TACACS config
- **Centralized Policy**: data-prefix and FQDN list objects (used by centralized data policies for local breakout / traffic steering), plus vSmart centralized policy CRUD, activation, deactivation, and push/connectivity status

Excluded: the Feature Profile (SDWAN/NFVirtual/Mobility) configuration-groups model, which the vendor spec ships with hundreds of broken internal `$ref` pointers (a known, Cisco-acknowledged defect in their OpenAPI export tooling), plus the long tail of narrow per-protocol control-policy definition builders, voice/security template builders, and other niche policy-parcel categories not needed for device and centralized-data-policy automation.

A handful of workflow names (e.g. user/group and device management) are prefixed with `Cisco SD-WAN` to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

### `cisco_catalyst_sdwan_manager-20.15.json`

Full, unmodified vendor spec for Catalyst SD-WAN Manager release 20.15. The vendor's `info.version` field (an internal API-schema revision, not the software release) is preserved in `x-vendor-api-version`; `info.version` here is set to `"20.15"` so the two vendor releases below are distinguishable by filename and in the Itential Platform GUI. Includes the Feature Profile categories and their upstream broken `$ref`s — see `cisco_catalyst_sdwan_manager-latest.json` above for the curated, working subset.

### `cisco_catalyst_sdwan_manager-20.12.json`

Full, unmodified vendor spec for Catalyst SD-WAN Manager release 20.12, as officially published by Cisco on DevNet. Kept alongside the 20.15 export above as a second reference point — the two releases' automatable surface (everything in `-latest`) is highly consistent between them.

## Studio Projects

### Cisco Catalyst SD-WAN Manager Project

Backed by the **`Cisco Catalyst SD-WAN Manager:latest`** Integration Model (see [`cisco_catalyst_sdwan_manager-latest.json`](./OpenAPIs/cisco_catalyst_sdwan_manager-latest.json) above). The project contains **289 workflows** organized into **11 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Device Actions | 40 | Reboot, upgrade, partition management, LXC container lifecycle |
| User and Group Administration | 37 | Local users, groups, AAA/RADIUS/TACACS configuration |
| Certificate Management | 37 | CSR generation, install, root/enterprise certificate lifecycle |
| Device Monitoring | 37 | Device state, statistics, TLOC and hardware health |
| Alarms | 36 | Alarm querying, severity, acknowledgement |
| Device Inventory | 33 | Onboarding, bootstrap config, claiming, discovery |
| Device Templates | 20 | Device template attach/detach, CLI and cloud-init templates |
| Feature Templates | 20 | Feature (general) template CRUD |
| Centralized Policy - vSmart Policy | 11 | Centralized policy CRUD, activation, deactivation, push status |
| Centralized Policy - Data Prefix Lists | 9 | Data-prefix list objects used by centralized data policies |
| Centralized Policy - Data Prefix and FQDN Lists | 9 | Data-prefix and FQDN list objects (e.g. app/domain-based local breakout) |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Cisco Catalyst SD-WAN Manager:latest` Integration Model | Import from [`cisco_catalyst_sdwan_manager-latest.json`](./OpenAPIs/cisco_catalyst_sdwan_manager-latest.json) before importing the project |
| `Cisco Catalyst SD-WAN Manager` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Cisco Catalyst SD-WAN Manager` — update the `adapter_id` value in each workflow task if yours is named differently |
| `X-XSRF-TOKEN` workflow input | Every state-changing workflow requires a current XSRF token as a job input, obtained per the handshake described above — this can't be supplied as a static instance property since it isn't part of the security scheme |
