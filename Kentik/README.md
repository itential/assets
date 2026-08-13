Kentik is a network observability platform for NetFlow analytics, DDoS detection, and infrastructure monitoring.

This project provides an OpenAPI spec for automating against Kentik's Device and Site APIs via an Integration Model, plus CRUD workflows built on that model. It also retains a set of pre-existing sample-use-case workflows built on the legacy Kentik adapter, demonstrating cross-system orchestration with AWS, ServiceNow, NetBox, and Microsoft Teams.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`kentik_device_site_api-latest.json`](#kentik_device_site_api-latestjson)
  - [`kentik_device_api-v202504beta2.json`](#kentik_device_api-v202504beta2json)
  - [`kentik_site_api-v202509.json`](#kentik_site_api-v202509json)
- [Studio Projects](#studio-projects)
  - [Kentik Project](#kentik-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Kentik Device & Site API OpenAPI spec — curated `-latest` plus the two official dated specs it was combined from |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing the Devices/Sites/Site Markets CRUD workflows and the pre-existing sample-use-case workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Kentik Device & Site API:latest` Integration Model | Required to run the Devices/Sites/Site Markets folders |
| [Kentik 5.x Adapter](https://gitlab.com/itentialopensource/adapters/adapter-kentick_v5) | Required to run the Create Device/Device Flow Test/Sample Use Cases folders (legacy, unmigrated) |

> **Note:** This project does not require Itential Gateway for the Devices/Sites/Site Markets folders. All API calls are made directly from Itential Platform to Kentik's REST API.

## Integration Configuration

Import `kentik_device_site_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Kentik's v6 API gateway.

Authentication is a pair of API key headers:

```
X-CH-Auth-Email: <your-kentik-account-email>
X-CH-Auth-API-Token: <your-kentik-api-token>
```

Generate an API token at Kentik → Settings → My Profile → API Tokens.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "email": { "value": "<your-kentik-account-email>" },
    "token": { "value": "<your-kentik-api-token>" }
  },
  "server": {
    "protocol": "https",
    "host": "grpc.api.kentik.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`kentik_device_site_api-latest.json`](./OpenAPIs/kentik_device_site_api-latest.json) | latest (curated) | 20 | Combines the official Device and Site v6 APIs into one Integration Model — see breakdown below |
| [`kentik_device_api-v202504beta2.json`](./OpenAPIs/kentik_device_api-v202504beta2.json) | v202504beta2 | 10 | Full, unmodified official Device API spec |
| [`kentik_site_api-v202509.json`](./OpenAPIs/kentik_site_api-v202509.json) | v202509 | 10 | Full, unmodified official Site API spec |

### `kentik_device_site_api-latest.json`

**Important context:** Kentik's legacy v5 REST API — the one the [Kentik 5.x Adapter](https://gitlab.com/itentialopensource/adapters/adapter-kentick_v5) targets — was **deprecated in January 2025**, and no official OpenAPI/Swagger spec was ever published for it. Kentik's current, officially-specified, actively-supported API is v6, based on gRPC with an automatic REST/JSON translation layer (gRPC-gateway). This spec targets v6.

Combines two official Kentik v6 specs from [`github.com/kentik/api-schema-public`](https://github.com/kentik/api-schema-public) into a single Integration Model: the Device API (`v202504beta2`, 10 operations) and the Site API (`v202509`, 10 operations). Both are already narrow, single-purpose service APIs — every operation is CRUD against devices, sites, or site markets — so all 20 operations are included in full.

Two endpoints used by the legacy adapter (`/api/ui/companySettings`, `/api/ui/devices/non-cloud-status`) are **not** part of this spec — they're undocumented internal UI-backend endpoints (no official spec, no v6 equivalent found), reverse-engineered from browser traffic rather than sourced from any published API. They remain in use only by the legacy `Device Flow Test` and `Device Onboarding` workflows in the Studio Project below.

Operations included, by category:

- **Devices**: List, create (single or batch), update (single or batch), delete (single or batch), get by ID, get by name, update labels
- **Sites**: List, create, get, update, delete
- **Site Markets**: List, create, get, update, delete

### `kentik_device_api-v202504beta2.json`

Full, unmodified official vendor spec for the Kentik Device API, version `v202504beta2` — preserved as-is from `github.com/kentik/api-schema-public`.

### `kentik_site_api-v202509.json`

Full, unmodified official vendor spec for the Kentik Site API, version `v202509` — preserved as-is from `github.com/kentik/api-schema-public`.

---

## Studio Projects

### Kentik Project

#### Folder Structure

| Folder | Workflows | Scope | Backing |
|---|---|---|---|
| Devices | 10 | Device CRUD (list, create, update, delete, get by ID/name, batch ops, labels) | `Kentik Device & Site API:latest` Integration Model |
| Sites | 5 | Site CRUD | `Kentik Device & Site API:latest` Integration Model |
| Site Markets | 5 | Site Market CRUD | `Kentik Device & Site API:latest` Integration Model |
| Create Device | 1 | Create a device (legacy) | Kentik 5.x Adapter |
| Device Flow Test | 2 | Find devices / raw flow-status check via an undocumented internal endpoint (legacy) | Kentik 5.x Adapter |
| Sample Use Cases | 28 | Cross-system reference workflows: AWS security-group remediation, ServiceNow incident/change tickets, NetBox sync, MS Teams notifications, IOS-XE config push via IAG (legacy, unmigrated — see note below) | Kentik 5.x Adapter, plus AWS EC2, ServiceNow, NetBox, and Microsoft Teams adapters |

A few resource names in the Devices folder are prefixed with `Kentik` (`Create Kentik Device`, `Get Kentik Device`, `Update Kentik Device`) to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

> **Note on Sample Use Cases:** This folder is a multi-vendor reference solution (Kentik + AWS + ServiceNow + NetBox + Microsoft Teams + IAG device config push), not a Kentik-specific CRUD surface. It's left as-is on the legacy Kentik 5.x Adapter — migrating it would mean rewriting orchestration logic that spans several other products' adapters, well beyond the scope of this pass. It also depends on the two undocumented `/api/ui/` endpoints noted above, which have no v6 equivalent.

#### Dependencies

| Dependency | Notes |
|---|---|
| `Kentik Device & Site API:latest` Integration Model | Import from [`kentik_device_site_api-latest.json`](./OpenAPIs/kentik_device_site_api-latest.json) before importing the project. Backs the Devices, Sites, and Site Markets folders. |
| `Kentik` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Kentik` — update the `adapter_id` value in each workflow task if yours is named differently |
| [Kentik 5.x Adapter](https://gitlab.com/itentialopensource/adapters/adapter-kentick_v5) | Required for the Create Device, Device Flow Test, and Sample Use Cases folders (legacy, unmigrated) |

**Testing status:** the 20 Devices/Sites/Site Markets workflows were created and schema-validated against a running Itential Platform instance, using a placeholder integration instance — no Kentik test account was available for this pass, so none have been executed against a live Kentik account.
