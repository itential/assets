# OP5 Monitor

OP5 Monitor, by ITRS Group, is a Naemon/Nagios-core network and infrastructure monitoring platform. It exposes hosts, services, host/service groups, contacts, and timeperiods through a configuration REST API, live status data through a livestatus-based filter query language, and operational actions (acknowledgements, downtimes, comments, notification/check toggles) through an external-command API.

This project provides OpenAPI specs for automating against OP5 Monitor's REST API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`op5_monitor-latest.json`](#op5_monitor-latestjson)
  - [`op5_monitor-10.json`](#op5_monitor-10json)
- [Studio Projects](#studio-projects)
  - [OP5 Monitor Project](#op5-monitor-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | OP5 Monitor REST API OpenAPI specs — curated `-latest` plus the full documented reference |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 41 workflows in 10 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `OP5 Monitor:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `op5_monitor-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your OP5 Monitor server.

Authentication is HTTP Basic against an OP5 Monitor user account. To authenticate against a non-default authentication module (e.g. LDAP), append `$<module>` to the username, e.g. `user$LDAP`.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-op5-username>",
      "password": "<your-op5-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-op5-host>",
    "base_path": "/api"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`op5_monitor-latest.json`](./OpenAPIs/op5_monitor-latest.json) | latest (curated) | 41 | Curated to config CRUD, filter queries, and external commands automation — see breakdown below |
| [`op5_monitor-10.json`](./OpenAPIs/op5_monitor-10.json) | 10 | 67 | Full reference spec covering every endpoint documented in OP5 Monitor's REST API reference |

### `op5_monitor-latest.json`

Curated to the core monitoring configuration and operational categories.

Resources included, by category:

- **Hosts / Services**: list, get, config create/update/delete
- **Host groups / Service groups**: list, get, config create/update/delete
- **Contacts / Contact groups**: list, get, config create/update/delete
- **Timeperiods**: list, get, config create/update/delete
- **Config**: list pending changes, save changes, revert pending changes
- **Filter**: livestatus-style query and count against hosts, services, groups, downtimes, comments, and log data
- **Command**: submit an external command (acknowledge, schedule/remove downtime, comments, enable/disable checks and notifications, forced re-check) by name, with the documented Naemon/Nagios command names as a path-parameter enum

### `op5_monitor-10.json`

Full reference spec covering every endpoint documented in OP5 Monitor's REST API reference, including host/service templates, check command definitions, the report API, and the autodiscovery (Magellan) and export (Nachos) APIs. See `op5_monitor-latest.json` for the curated subset if you just need common monitoring automation.

## Studio Projects

### OP5 Monitor Project

Backed by the **`OP5 Monitor:latest`** Integration Model (see [`op5_monitor-latest.json`](./OpenAPIs/op5_monitor-latest.json) above). The project contains **41 workflows** organized into **10 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Hosts | 5 | List, get, config create/update/delete |
| Services | 5 | List, get, config create/update/delete |
| Hostgroups | 5 | List, get, config create/update/delete |
| Servicegroups | 5 | List, get, config create/update/delete |
| Contacts | 5 | List, get, config create/update/delete |
| Contactgroups | 5 | List, get, config create/update/delete |
| Timeperiods | 5 | List, get, config create/update/delete |
| Config | 3 | List pending changes, save changes, revert pending changes |
| Filter | 2 | Query, count |
| Command | 1 | Generic external command dispatch (`POST /command/{command}`) |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `OP5 Monitor:latest` Integration Model | Import from [`op5_monitor-latest.json`](./OpenAPIs/op5_monitor-latest.json) before importing the project |
| `OP5` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `OP5` — update the `adapter_id` value in each workflow task if yours is named differently |
