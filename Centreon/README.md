# Centreon

Centreon is an IT and network monitoring platform for hosts, services, and infrastructure health across on-premise environments.

This project provides OpenAPI specs for automating against Centreon's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for host and service automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`centreon-latest.json`](#centreon-latestjson)
  - [`centreon-25.10.json`](#centreon-2510json)
- [Studio Projects](#studio-projects)
  - [`Centreon.project.json`](#centreonprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Centreon REST API OpenAPI specs — curated `-latest` plus the full spec |
| [Studio Projects/](./Studio%20Projects/) | Configuration CRUD, monitoring status, and downtime/acknowledgement workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Centreon | 25.10+ |
| Centreon Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is a static API token sent on the `X-AUTH-TOKEN` header. Generate a token as an administrator in the Centreon web UI (Administration > Authentication, or a user's Security tab) — unlike a token obtained via `/login`, an admin-generated token does not expire from inactivity.

In Itential Platform's **Admin Essentials**, set the integration's `authentication.tokenAuth.value` field to the token value:

```json
"authentication": {
  "tokenAuth": {
    "value": "<TOKEN>"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`centreon-latest.json`](./OpenAPIs/centreon-latest.json) | latest (curated) | 85 | Trimmed to 85 of 240 upstream operations covering host/service configuration CRUD, monitoring status, and downtime/acknowledgement management — see breakdown below |
| [`centreon-25.10.json`](./OpenAPIs/centreon-25.10.json) | 25.10 | 240 | Full spec, bundled from Centreon's published OpenAPI source. |

### `centreon-latest.json`

Actively-maintained spec (`x-vendor-api-version: 25.10`). Trimmed to 85 of 240 upstream operations covering common CRUD for host and service automation.

Resources included, by category:

- **Host Configuration**: Hosts, Host Categories, Host Groups, Host Severities
- **Service Configuration**: Services, Service Categories, Service Groups, Service Severities
- **Host Monitoring**: real-time host status, host status counts, host checks, host categories/groups
- **Service Monitoring**: real-time service status, service status counts, service checks, service categories/groups/names
- **Severities Monitoring**: real-time host and service severities
- **Acknowledgements**: host, service, and multi-resource acknowledgement create/list/cancel
- **Downtimes**: host, service, and multi-resource downtime scheduling/list/cancel
- **Resources**: the unified host+service resources view, including per-resource detail and checks

### `centreon-25.10.json`

Full spec (240 operations), assembled from Centreon's published OpenAPI source — the vendor splits its reference across many linked YAML files, so this is a dereferenced ("bundled") single-file JSON equivalent to that source, narrowed to a single auth method (`X-AUTH-TOKEN`) and a single server entry per this repo's Integration Model rules. See `centreon-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### `Centreon.project.json`

One folder per resource/category, each with the corresponding CRUD, monitoring, acknowledgement, or downtime workflows built on `centreon-latest.json`'s Integration Model.

Every workflow's adapter task is wired to the Integration instance name `Centreon`. After importing, either name your Integration instance `Centreon`, or update the `adapter_id` value in each workflow task to match your own instance name.

**Hosts (Configuration)**

| Workflow | Scope |
|---|---|
| List Hosts | Find all host configurations |
| Create Host | Create a host configuration |
| Get Host | Get a host configuration by ID |
| Update Host | Partially update a host configuration |
| Delete Host | Delete a host configuration |

**Host Categories (Configuration)**

| Workflow | Scope |
|---|---|
| List Host Categories | List all host categories |
| Create Host Category | Create a host category |
| Get Host Category | Get a host category by ID |
| Update Host Category | Update a host category |
| Delete Host Category | Delete a host category |

**Host Groups (Configuration)**

| Workflow | Scope |
|---|---|
| List Host Groups | List all host groups |
| Create Host Group | Create a host group |
| Get Host Group | Get a host group by ID |
| Update Host Group | Update a host group |
| Delete Host Group | Delete a host group |

**Host Severities (Configuration)**

| Workflow | Scope |
|---|---|
| List Host Severities | List all host severities |
| Create Host Severity | Create a host severity |
| Get Host Severity | Get a host severity by ID |
| Update Host Severity | Update a host severity |
| Delete Host Severity | Delete a host severity |

**Services (Configuration)**

| Workflow | Scope |
|---|---|
| List Services | Find all services |
| Create Service | Create a service |
| Update Service | Partially update a service |
| Delete Service | Delete a service |

**Service Categories (Configuration)**

| Workflow | Scope |
|---|---|
| List Service Categories | List all service categories |
| Create Service Category | Create a service category |
| Delete Service Category | Delete a service category |

**Service Groups (Configuration)**

| Workflow | Scope |
|---|---|
| List Service Groups | List all service groups |
| Create Service Group | Create a service group |
| Delete Service Group | Delete a service group |

**Service Severities (Configuration)**

| Workflow | Scope |
|---|---|
| List Service Severities | List all service severities |
| Create Service Severity | Create a service severity |
| Update Service Severity | Update a service severity |
| Delete Service Severity | Delete a service severity |

**Hosts (Monitoring)**

| Workflow | Scope |
|---|---|
| List Host Status | List real-time host status |
| Get Host Status | Get real-time status for a host |
| Count Host Status | Count hosts by status |
| Check Multiple Hosts | Schedule a forced check on multiple hosts |
| Check Host | Schedule a forced check on a host |

**Host Categories (Monitoring)**

| Workflow | Scope |
|---|---|
| List Real-Time Host Categories | List host categories from real-time monitoring data |

**Host Groups (Monitoring)**

| Workflow | Scope |
|---|---|
| List Real-Time Host Groups | List host groups from real-time monitoring data |
| List Host Groups For Host | List the host groups a given host belongs to |

**Services (Monitoring)**

| Workflow | Scope |
|---|---|
| List Service Status | List real-time service status |
| Get Service Status | Get real-time status for a service |
| List Services For Host | List services attached to a given host |
| Count Service Status | Count services by status |
| Check Multiple Services | Schedule a forced check on multiple services |
| Check Service | Schedule a forced check on a service |

**Service Categories (Monitoring)**

| Workflow | Scope |
|---|---|
| List Real-Time Service Categories | List service categories from real-time monitoring data |

**Service Groups (Monitoring)**

| Workflow | Scope |
|---|---|
| List Real-Time Service Groups | List service groups from real-time monitoring data |
| List Service Groups For Service | List the service groups a given service belongs to |

**Service Names (Monitoring)**

| Workflow | Scope |
|---|---|
| List Real-Time Unique Service Names | List unique service names across real-time monitoring data |

**Severities (Monitoring)**

| Workflow | Scope |
|---|---|
| List Real-Time Host Severities | List host severities from real-time monitoring data |
| List Real-Time Service Severities | List service severities from real-time monitoring data |

**Acknowledgements**

| Workflow | Scope |
|---|---|
| List Acknowledgements | List all acknowledgements |
| Get Acknowledgement | Get a single acknowledgement by ID |
| List Host Acknowledgements | List acknowledgements across all hosts |
| Acknowledge Multiple Hosts | Add an acknowledgement to multiple hosts |
| List Acknowledgements For Host | List acknowledgements for a single host |
| Acknowledge Host | Add an acknowledgement to a single host |
| Cancel Host Acknowledgement | Cancel an acknowledgement on a host |
| List Acknowledgements For Service | List acknowledgements for a single service |
| Acknowledge Service | Add an acknowledgement to a single service |
| Cancel Service Acknowledgement | Cancel an acknowledgement on a service |
| List Service Acknowledgements | List acknowledgements across all services |
| Acknowledge Multiple Services | Add an acknowledgement to multiple services |
| Acknowledge Multiple Resources | Add an acknowledgement to multiple resources (unified host+service view) |
| Remove Multiple Resource Acknowledgements | Remove acknowledgements from multiple resources |

**Downtimes**

| Workflow | Scope |
|---|---|
| List Downtimes | List all downtimes |
| Get Downtime | Get a single downtime by ID |
| Cancel Downtime | Cancel a downtime |
| List Host Downtimes | List downtimes across all hosts |
| Schedule Downtime For Multiple Hosts | Schedule a downtime on multiple hosts |
| List Downtimes For Host | List downtimes for a single host |
| Schedule Host Downtime | Schedule a downtime on a single host |
| List Downtimes For Service | List downtimes for a single service |
| Schedule Service Downtime | Schedule a downtime on a single service |
| List Service Downtimes | List downtimes across all services |
| Schedule Downtime For Multiple Services | Schedule a downtime on multiple services |
| Schedule Downtime For Multiple Resources | Schedule a downtime on multiple resources (unified host+service view) |

**Resources**

| Workflow | Scope |
|---|---|
| List Resources | List resources (unified host+service view) |
| Check Multiple Resources | Schedule a forced check on multiple resources |
| List Resources With Parents | List resources including their parent relationships |
| Get Resource Host Details | Get resource-view details for a host |
| Get Resource Service Details | Get resource-view details for a service |
