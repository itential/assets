Cisco Umbrella is a cloud-delivered security service that combines DNS-layer security, secure web gateway, firewall, and cloud access security broker (CASB) functions to protect users and enforce policy both on and off the corporate network.

This project provides OpenAPI specs for automating against Umbrella's Policies and Deployments REST APIs via Integration Models, plus a Studio Project of ready-to-import CRUD workflows built on those models. Each spec covers one Umbrella resource — import only the ones your automation needs. Every module's `-latest` spec is reviewed and curated for common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [Studio Projects](#studio-projects)
  - [Sites](#sites)
  - [Networks](#networks)
  - [Network Devices](#network-devices)
  - [Internal Domains](#internal-domains)
  - [Internal Networks](#internal-networks)
  - [Application Lists](#application-lists)
- [OpenAPIs](#openapis)
  - [`cisco_umbrella_destination_lists-latest.json`](#cisco_umbrella_destination_lists-latestjson)
  - [`cisco_umbrella_destination_lists-2.0.0.json`](#cisco_umbrella_destination_lists-200json)
  - [`cisco_umbrella_application_lists-latest.json`](#cisco_umbrella_application_lists-latestjson)
  - [`cisco_umbrella_application_lists-1.0.1.json`](#cisco_umbrella_application_lists-101json)
  - [`cisco_umbrella_sites-latest.json`](#cisco_umbrella_sites-latestjson)
  - [`cisco_umbrella_sites-2.0.0.json`](#cisco_umbrella_sites-200json)
  - [`cisco_umbrella_networks-latest.json`](#cisco_umbrella_networks-latestjson)
  - [`cisco_umbrella_networks-2.0.0.json`](#cisco_umbrella_networks-200json)
  - [`cisco_umbrella_network_devices-latest.json`](#cisco_umbrella_network_devices-latestjson)
  - [`cisco_umbrella_network_devices-2.0.0.json`](#cisco_umbrella_network_devices-200json)
  - [`cisco_umbrella_internal_domains-latest.json`](#cisco_umbrella_internal_domains-latestjson)
  - [`cisco_umbrella_internal_domains-2.0.0.json`](#cisco_umbrella_internal_domains-200json)
  - [`cisco_umbrella_internal_networks-latest.json`](#cisco_umbrella_internal_networks-latestjson)
  - [`cisco_umbrella_internal_networks-2.0.0.json`](#cisco_umbrella_internal_networks-200json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco Umbrella Policies and Deployments REST API OpenAPI specs — `-latest` plus the full dated version for each module |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing CRUD workflows for every module, organized one folder per resource |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco Umbrella | Destination Lists API v2.0.0, Application Lists API v1.0.1, Sites/Networks/Network Devices/Internal Domains/Internal Networks APIs v2.0.0 |
| Cisco Umbrella Integration Model | Required to build automation against each OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec(s) you need from `OpenAPIs/` as Integration Models in **Admin > Integrations**, then create an integration pointing at your Umbrella tenant for each.

Authentication is OAuth2 Client Credentials:

```
Authorization: Basic <base64(client_key:client_secret)>
```

Obtain a client key and secret from Cisco Umbrella under **Admin > API Keys > Umbrella API**. The token endpoint requires the client credentials as HTTP Basic auth on the Authorization header. On each Integration instance, set the authentication's `auth_method` field to `client_secret_basic` (it defaults to `client_secret_post`) — Itential Platform then builds `Authorization: Basic <base64(client_id:client_secret)>` on the token request automatically from the plain `client_id`/`client_secret` values, with no manual encoding step.

The instance's `authentication`/`server` properties should look like this once configured — every resource spec shares the same `tokenUrl`, but `base_path` differs per spec (e.g. `/policies/v2` for application/destination lists, `/deployments/v2` for sites/networks/devices — see each spec file for its exact path):

```json
{
  "authentication": {
    "oauthFlow": {
      "client_id": "<your-client-id>",
      "client_secret": "<your-client-secret>",
      "auth_method": "client_secret_basic",
      "token_url": "https://api.umbrella.com/auth/v2/token",
      "refresh_url": "",
      "scope": "",
      "token": { "access_token": "" }
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.umbrella.com",
    "base_path": "<resource-base-path-per-spec>"
  }
}
```

---

## Studio Projects

Import [`Cisco Umbrella.project.json`](./Studio%20Projects/Cisco%20Umbrella.project.json) via **Automation Studio > Projects > Import**. It contains one folder per resource, each with a List/Create/Get/Update/Delete workflow (plus a sub-resource lookup where the API has one) built on that resource's `-latest` Integration Model.

Every workflow's adapter task is wired to a specific Integration instance name (e.g. `Cisco Umbrella Sites`, `Cisco Umbrella Networks`). After importing, either name your Integration instances exactly as listed per folder below, or update the `adapter_id` value in each workflow task to match your own instance names.

Each adapter task's `response` output is the full HTTP response envelope (`{ok, url, status, headers, text, body}`), not just the payload — the actual data is at `response.body`.

### Sites

Built on `cisco_umbrella_sites-latest.json`. Integration instance name: `Cisco Umbrella Sites`.

| Workflow | Scope |
|---|---|
| List Sites | List the sites configured in the organization |
| Create Site | Create a new site |
| Get Site | Retrieve a site by ID |
| Update Site | Update a site's name by ID |
| Delete Site | Delete a site by ID |

### Networks

Built on `cisco_umbrella_networks-latest.json`. Integration instance name: `Cisco Umbrella Networks`.

| Workflow | Scope |
|---|---|
| List Networks | List the networks configured in the organization |
| Create Network | Create a new network |
| Get Network | Retrieve a network by ID |
| Update Network | Update a network by ID |
| Delete Network | Delete a network by ID |
| List Network Policies | List the policies applied to a network |

### Network Devices

Built on `cisco_umbrella_network_devices-latest.json`. Integration instance name: `Cisco Umbrella Network Devices`.

| Workflow | Scope |
|---|---|
| List Network Devices | List the network devices configured in the organization |
| Create Network Device | Create a new network device |
| Get Network Device | Retrieve a network device by ID |
| Update Network Device | Update a network device's name by ID |
| Delete Network Device | Delete a network device by ID |
| List Network Device Policies | List the policies applied to a network device |

### Internal Domains

Built on `cisco_umbrella_internal_domains-latest.json`. Integration instance name: `Cisco Umbrella Internal Domains`.

| Workflow | Scope |
|---|---|
| List Internal Domains | List the internal domains configured in the organization |
| Create Internal Domain | Create a new internal domain |
| Get Internal Domain | Retrieve an internal domain by ID |
| Update Internal Domain | Update an internal domain by ID |
| Delete Internal Domain | Delete an internal domain by ID |

### Internal Networks

Built on `cisco_umbrella_internal_networks-latest.json`. Integration instance name: `Cisco Umbrella Internal Networks`.

| Workflow | Scope |
|---|---|
| List Internal Networks | List the internal networks configured in the organization |
| Create Internal Network | Create a new internal network |
| Get Internal Network | Retrieve an internal network by ID |
| Update Internal Network | Update an internal network by ID |
| Delete Internal Network | Delete an internal network by ID |
| List Internal Network Policies | List the policies applied to an internal network |

### Application Lists

Built on `cisco_umbrella_application_lists-latest.json`. Integration instance name: `Cisco Umbrella Application Lists`.

| Workflow | Scope |
|---|---|
| List Application Lists | List the application lists configured in the organization |
| Create Application List | Create a new application list |
| Get Application List | Retrieve an application list by ID |
| Update Application List | Update an application list by ID |
| Delete Application List | Delete an application list by ID |
| Get Application Usage | Get usage information for applications across lists and rules |

## OpenAPIs

Every module below shares the same authentication (OAuth2 Client Credentials). Each has its own `-latest.json` (actively-maintained) and dated `-{version}.json` (full, unmodified vendor spec) pair in `OpenAPIs/`.

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_umbrella_destination_lists-latest.json`](./OpenAPIs/cisco_umbrella_destination_lists-latest.json) | latest (curated) | 8 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_umbrella_application_lists-latest.json`](./OpenAPIs/cisco_umbrella_application_lists-latest.json) | latest (curated) | 6 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_umbrella_sites-latest.json`](./OpenAPIs/cisco_umbrella_sites-latest.json) | latest (curated) | 5 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_umbrella_networks-latest.json`](./OpenAPIs/cisco_umbrella_networks-latest.json) | latest (curated) | 6 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_umbrella_network_devices-latest.json`](./OpenAPIs/cisco_umbrella_network_devices-latest.json) | latest (curated) | 6 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_umbrella_internal_domains-latest.json`](./OpenAPIs/cisco_umbrella_internal_domains-latest.json) | latest (curated) | 5 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_umbrella_internal_networks-latest.json`](./OpenAPIs/cisco_umbrella_internal_networks-latest.json) | latest (curated) | 6 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`cisco_umbrella_destination_lists-2.0.0.json`](./OpenAPIs/cisco_umbrella_destination_lists-2.0.0.json) | 2.0.0 | 8 | Full spec for the Destination Lists module, API version 2.0.0. |
| [`cisco_umbrella_application_lists-1.0.1.json`](./OpenAPIs/cisco_umbrella_application_lists-1.0.1.json) | 1.0.1 | 6 | Full spec for the Application Lists module, API version 1.0.1. |
| [`cisco_umbrella_sites-2.0.0.json`](./OpenAPIs/cisco_umbrella_sites-2.0.0.json) | 2.0.0 | 5 | Full spec for the Sites module, API version 2.0.0. |
| [`cisco_umbrella_networks-2.0.0.json`](./OpenAPIs/cisco_umbrella_networks-2.0.0.json) | 2.0.0 | 6 | Full spec for the Networks module, API version 2.0.0. |
| [`cisco_umbrella_network_devices-2.0.0.json`](./OpenAPIs/cisco_umbrella_network_devices-2.0.0.json) | 2.0.0 | 6 | Full spec for the Network Devices module, API version 2.0.0. |
| [`cisco_umbrella_internal_domains-2.0.0.json`](./OpenAPIs/cisco_umbrella_internal_domains-2.0.0.json) | 2.0.0 | 5 | Full spec for the Internal Domains module, API version 2.0.0. |
| [`cisco_umbrella_internal_networks-2.0.0.json`](./OpenAPIs/cisco_umbrella_internal_networks-2.0.0.json) | 2.0.0 | 6 | Full spec for the Internal Networks module, API version 2.0.0. |

### `cisco_umbrella_destination_lists-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2.0.0`, 8 operations). Every operation is CRUD on the single Destination Lists resource domain — there is no separate health/status, self-introspection, or admin surface to exclude, so nothing was removed.

Operations included, by category:

- **Destination lists**: List (`GET /destinationlists`), create (`POST /destinationlists`), get by ID (`GET /destinationlists/{destinationListId}`), update by ID (`PATCH /destinationlists/{destinationListId}`), delete by ID (`DELETE /destinationlists/{destinationListId}`)
- **Destinations within a list**: List destinations in a list (`GET /destinationlists/{destinationListId}/destinations`), add destinations to a list (`POST /destinationlists/{destinationListId}/destinations`), remove destinations from a list (`DELETE /destinationlists/{destinationListId}/destinations/remove`)

### `cisco_umbrella_destination_lists-2.0.0.json`

Full, unmodified vendor spec for the Destination Lists module, API version 2.0.0 (8 operations) — the vendor's complete API surface, preserved as-is. See `cisco_umbrella_destination_lists-latest.json` above for the curated version if you just need common CRUD automation.

### `cisco_umbrella_application_lists-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 1.0.1`, 6 operations). Every operation is CRUD on application lists or a read-only usage lookup that supports managing them — there is no separate health/status or admin surface to exclude, so nothing was removed.

Operations included, by category:

- **Application lists**: List (`GET /applicationLists`), create (`POST /applicationLists`), get by ID (`GET /applicationLists/{applicationListId}`), update by ID (`PUT /applicationLists/{applicationListId}`), delete by ID (`DELETE /applicationLists/{applicationListId}`)
- **Application usage**: Get usage of applications across lists and rules (`GET /applications/usage`)

### `cisco_umbrella_application_lists-1.0.1.json`

Full, unmodified vendor spec for the Application Lists module, API version 1.0.1 (6 operations) — the vendor's complete API surface, preserved as-is. See `cisco_umbrella_application_lists-latest.json` above for the curated version if you just need common CRUD automation.

### `cisco_umbrella_sites-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2.0.0`, 5 operations). Every operation is CRUD on the single Sites resource domain — there is no separate health/status or admin surface to exclude, so nothing was removed.

Operations included, by category:

- **Sites**: List (`GET /sites`), create (`POST /sites`), get by ID (`GET /sites/{siteId}`), update by ID (`PUT /sites/{siteId}`), delete by ID (`DELETE /sites/{siteId}`)

### `cisco_umbrella_sites-2.0.0.json`

Full, unmodified vendor spec for the Sites module, API version 2.0.0 (5 operations) — the vendor's complete API surface, preserved as-is. See `cisco_umbrella_sites-latest.json` above for the curated version if you just need common CRUD automation.

### `cisco_umbrella_networks-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2.0.0`, 6 operations). Every operation is CRUD on networks or a read-only lookup of a network's associated policies — there is no separate health/status or admin surface to exclude, so nothing was removed.

Operations included, by category:

- **Networks**: List (`GET /networks`), create (`POST /networks`), get by ID (`GET /networks/{networkId}`), update by ID (`PUT /networks/{networkId}`), delete by ID (`DELETE /networks/{networkId}`)
- **Network policies**: List the policies applied to a network (`GET /networks/{networkId}/policies`)

### `cisco_umbrella_networks-2.0.0.json`

Full, unmodified vendor spec for the Networks module, API version 2.0.0 (6 operations) — the vendor's complete API surface, preserved as-is. See `cisco_umbrella_networks-latest.json` above for the curated version if you just need common CRUD automation.

### `cisco_umbrella_network_devices-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2.0.0`, 6 operations). Every operation is CRUD on network devices or a read-only lookup of a device's associated policies — there is no separate health/status or admin surface to exclude, so nothing was removed.

Operations included, by category:

- **Network devices**: List (`GET /networkdevices`), create (`POST /networkdevices`), get by ID (`GET /networkdevices/{originId}`), update by ID (`PATCH /networkdevices/{originId}`), delete by ID (`DELETE /networkdevices/{originId}`)
- **Network device policies**: List the policies applied to a network device (`GET /networkdevices/{originId}/policies`)

### `cisco_umbrella_network_devices-2.0.0.json`

Full, unmodified vendor spec for the Network Devices module, API version 2.0.0 (6 operations) — the vendor's complete API surface, preserved as-is. See `cisco_umbrella_network_devices-latest.json` above for the curated version if you just need common CRUD automation.

### `cisco_umbrella_internal_domains-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2.0.0`, 5 operations). Every operation is CRUD on the single Internal Domains resource domain — there is no separate health/status or admin surface to exclude, so nothing was removed.

Operations included, by category:

- **Internal domains**: List (`GET /internaldomains`), create (`POST /internaldomains`), get by ID (`GET /internaldomains/{internalDomainId}`), update by ID (`PUT /internaldomains/{internalDomainId}`), delete by ID (`DELETE /internaldomains/{internalDomainId}`)

### `cisco_umbrella_internal_domains-2.0.0.json`

Full, unmodified vendor spec for the Internal Domains module, API version 2.0.0 (5 operations) — the vendor's complete API surface, preserved as-is. See `cisco_umbrella_internal_domains-latest.json` above for the curated version if you just need common CRUD automation.

### `cisco_umbrella_internal_networks-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2.0.0`, 6 operations). Every operation is CRUD on internal networks or a read-only lookup of an internal network's associated policies — there is no separate health/status or admin surface to exclude, so nothing was removed.

Operations included, by category:

- **Internal networks**: List (`GET /internalnetworks`), create (`POST /internalnetworks`), get by ID (`GET /internalnetworks/{internalNetworkId}`), update by ID (`PUT /internalnetworks/{internalNetworkId}`), delete by ID (`DELETE /internalnetworks/{internalNetworkId}`)
- **Internal network policies**: List the policies applied to an internal network (`GET /internalnetworks/{internalNetworkId}/policies`)

### `cisco_umbrella_internal_networks-2.0.0.json`

Full, unmodified vendor spec for the Internal Networks module, API version 2.0.0 (6 operations) — the vendor's complete API surface, preserved as-is. See `cisco_umbrella_internal_networks-latest.json` above for the curated version if you just need common CRUD automation.
