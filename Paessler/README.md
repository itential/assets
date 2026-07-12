Paessler PRTG Network Monitor is an agentless infrastructure monitoring tool that tracks the availability and performance of devices, network links, servers, and applications using sensors organized into a device/group/probe hierarchy.

This project provides OpenAPI specs for automating against PRTG's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Paessler PRTG REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Paessler PRTG | Core Server with REST API v2 (`x-vendor-api-version: 2.0`) |
| Paessler PRTG Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your PRTG core server.

Authentication is an API token in the `Authorization` header:

```
Authorization: PrtgSharedSecret <api_token>
```

Generate a token in PRTG under **Setup > Account Settings > My Account > API Token**.

## OpenAPIs

### `paessler_prtg-latest.json` (curated)

Actively-maintained spec (`x-vendor-api-version: 2.0`). Trimmed to 77 of 115 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Devices**: List, Get, Update, Delete, Icons, Templates, Pause/Resume/Scan (single and multi), Clone, Autodiscovery
- **Groups**: List, Get, Update, Delete, Pause/Resume/Scan (single and multi), Clone, Create Device/Group under a Group, Autodiscovery
- **Probes**: List, Get, Network Info, Pause/Resume/Scan (single and multi), Delete, Create Device/Group under a Probe
- **Sensors**: List, Get, Update, Delete, Pause/Resume/Scan (single and multi), Clone, Acknowledge Alarm, Create under a Device, Metascan, Historical Data
- **Channels**: List, Get, Overview, Measurement Data
- **Timeseries**: Historical time-series and graph data for a sensor
- **Objects**: Generic list, count, and move (reparent) across the device tree
- **Autodiscoveries**: List autodiscovery jobs

Not included: user/usergroup/API-key administration, session-based login (the API key header is used instead), schema-discovery endpoints, PRTG libraries (custom dashboards), lookup definitions, system settings/feature toggles/license info, and the sensor status summary/reporting endpoint. Pull the full spec below if you need one of those areas.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`paessler_prtg-2.0.json`](./OpenAPIs/paessler_prtg-2.0.json) | Full spec for PRTG REST API v2.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| Paessler PRTG Integration Model | Import from an OpenAPI spec above to build automation against the REST API. |
