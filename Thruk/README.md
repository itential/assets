# Thruk

Thruk is a web interface and monitoring dashboard for Naemon/Nagios-compatible monitoring cores, providing a REST API over hosts, services, host/service groups, contacts, downtimes, comments, and monitoring core configuration.

This project provides OpenAPI specs for automating against Thruk's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`thruk-latest.json`](#thruk-latestjson)
  - [`thruk-1.json`](#thruk-1json)
- [Studio Projects](#studio-projects)
  - [Thruk Project](#thruk-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Thruk REST API OpenAPI specs — curated `-latest` plus the full documented spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 73 workflows in 12 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Thruk:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `thruk-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Thruk server.

Authentication is a static, user-generated API key sent via the `X-Thruk-Auth-Key` header. A superuser API key can additionally set the acting user via `X-Thruk-Auth-User`. Create a key from the user profile page (if `api_keys_enabled` is set in the Thruk config) or via the `/thruk/api_keys` endpoint.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiKeyAuth": {
      "api_key": "<your-thruk-api-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-thruk-host>",
    "base_path": "/thruk/r"
  }
}
```

If Thruk runs under OMD with a named site, prefix `base_path` with the site name, e.g. `/monitoring/thruk/r`.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`thruk-latest.json`](./OpenAPIs/thruk-latest.json) | latest (curated) | 73 | Curated to hosts/services CRUD and monitoring operations automation — see breakdown below |
| [`thruk-1.json`](./OpenAPIs/thruk-1.json) | 1 | 169 | Full spec covering every endpoint documented in Thruk's REST API reference |

### `thruk-latest.json`

Curated to the core monitoring CRUD and operational categories.

Resources included, by category:

- **Hosts / Services**: list, get, config create/replace/update/delete, external commands (acknowledge, schedule/remove downtime, comments, enable/disable checks and notifications, passive check result submission, etc.), host-to-service lookups, statistics and totals
- **Host groups / Service groups**: list, get, config CRUD, group-level external commands, statistics
- **Contacts / Contact groups**: list, get, config CRUD, notification commands, contact totals
- **Downtimes / Comments**: list, get by ID
- **Commands / Timeperiods**: list, get by name
- **Status listings**: alerts, logs, notifications, process info, check statistics, sites/backends
- **Config lifecycle**: check, save, reload, revert (the required sequence after any config change, per Thruk's own object-configuration workflow)

External-command operations use a single parameterized endpoint per resource (`.../cmd/{command}`) with the real, documented command names as a path-parameter enum. The full list of command names and their specific parameters is in the Thruk REST API commands reference.

### `thruk-1.json`

Full spec covering every endpoint documented in Thruk's REST API reference. See `thruk-latest.json` for the curated subset if you just need common monitoring automation.

## Studio Projects

### Thruk Project

Backed by the **`Thruk:latest`** Integration Model (see [`thruk-latest.json`](./OpenAPIs/thruk-latest.json) above). The project contains **73 workflows** organized into **12 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Hosts | 10 | List, get, config CRUD, external commands, services lookup, statistics, totals |
| Services | 9 | List, get, config CRUD, external commands, statistics, totals |
| Hostgroups | 8 | List, get, config CRUD, external commands, statistics |
| Servicegroups | 8 | List, get, config CRUD, external commands, statistics |
| Contacts | 8 | List, get, config CRUD, external commands, totals |
| Contactgroups | 7 | List, get, config CRUD, external commands |
| Status | 9 | Index, alerts, logs, notifications, process info, check statistics, sites |
| Config | 5 | Check, diff, reload, revert, save |
| Commands | 3 | List, get by name, generic command dispatch (`POST /cmd`) |
| Comments | 2 | List, get by ID |
| Downtimes | 2 | List, get by ID |
| Timeperiods | 2 | List, get by name |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `Thruk:latest` Integration Model | Import from [`thruk-latest.json`](./OpenAPIs/thruk-latest.json) before importing the project |
| `Thruk` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Thruk` — update the `adapter_id` value in each workflow task if yours is named differently |
