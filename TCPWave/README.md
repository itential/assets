# TCPWave

TCPWave IPAM is a DNS-DHCP-IPAM (DDI) management platform, providing unified management of IP address space, DNS zones and resource records, and DHCP scopes across an organization's network infrastructure.

This project provides an OpenAPI spec for automating against the TCPWave IPAM REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`tcpwave_ipam-latest.json`](#tcpwave_ipam-latestjson)
  - [`tcpwave_ipam-11.32P4.json`](#tcpwave_ipam-1132p4json)
- [Studio Projects](#studio-projects)
  - [TCPWave IPAM Project](#tcpwave-ipam-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | TCPWave IPAM REST API OpenAPI spec — curated `-latest` plus the full reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 20 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `TCPWave IPAM:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `tcpwave_ipam-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your TCPWave IPAM appliance.

Authentication is a static API key: a long-lived (default 60-day) session token generated out-of-band from the TCPWave IPAM UI (**Administration > Security Management > Session Token Management**) and replayed on every request as the `TIMS-Session-Token` header. There is no token-exchange call — generate the token once in the UI and paste it into the integration instance.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "TIMSSessionToken": {
      "apiKey": "<your-session-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-tcpwave-host>",
    "port": 7443,
    "base_path": "/tims/rest"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`tcpwave_ipam-latest.json`](./OpenAPIs/tcpwave_ipam-latest.json) | latest (curated) | 20 | Curated to core IPAM/DDI CRUD — see breakdown below |
| [`tcpwave_ipam-11.32P4.json`](./OpenAPIs/tcpwave_ipam-11.32P4.json) | 11.32P4 | 20 | Reference spec for the TCPWave IPAM REST API, version 11.32P4 |

### `tcpwave_ipam-latest.json`

Hand-built from TCPWave's official REST API guide and the request/response shapes published in TCPWave's own [`TIMS-Rest-Client`](https://github.com/TCPWAVE/TIMS-Rest-Client) reference client, covering the core DDI resources most IPAM automation actually touches.

Resources included, by category:

- **Networks**: create, delete, list, get details by IP
- **Subnets**: create, update, delete, get by object IP
- **IP Addresses**: create IP object (host record, optionally with DNS resource records), delete, get next free IP in a subnet, list resource records
- **DNS Zones & Records**: create zone, update zone (including adding/removing resource records), delete zones, list zones, get zone
- **DHCP Scopes**: create, delete, list (paginated)

### `tcpwave_ipam-11.32P4.json`

Reference spec for the TCPWave IPAM REST API, version 11.32P4 (the version documented in TCPWave's official REST API guide at the time of writing). Same operation set as `tcpwave_ipam-latest.json` above — TCPWave's full published API surface (1400+ calls per the vendor) spans far more than DDI automation, so this spec covers the core IPAM/DDI CRUD resources rather than the entire catalog.

## Studio Projects

### TCPWave IPAM Project

Backed by the **`TCPWave IPAM:latest`** Integration Model (see [`tcpwave_ipam-latest.json`](./OpenAPIs/tcpwave_ipam-latest.json) above). The project contains **20 workflows** organized into **5 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Networks | 4 | Create, delete, list, get details by IP |
| Subnets | 4 | Create, update, delete, get by object IP |
| IP Addresses | 4 | Create IP object, delete, get next free IP, list resource records |
| DNS Zones & Records | 5 | Create, update (incl. resource records), delete, list, get |
| DHCP Scopes | 3 | Create, delete, list |

#### Dependencies

| Dependency | Notes |
|---|---|
| `TCPWave IPAM:latest` Integration Model | Import from [`tcpwave_ipam-latest.json`](./OpenAPIs/tcpwave_ipam-latest.json) before importing the project |
| `TCPWave IPAM` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `TCPWave IPAM` — update the `adapter_id` value in each workflow task if yours is named differently |
