# EdgeConnect

HPE Aruba Networking EdgeConnect SD-WAN (formerly Silver Peak EdgeConnect) is centrally managed through Orchestrator, which configures and monitors EdgeConnect appliances, Business Intent Overlays, and tunnels across a WAN fabric.

This project provides OpenAPI specs for automating against Orchestrator's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`edgeconnect-latest.json`](#edgeconnect-latestjson)
  - [`edgeconnect-9.5.json`](#edgeconnect-95json)
- [Studio Projects](#studio-projects)
  - [HPE Aruba Networking EdgeConnect Project](#hpe-aruba-networking-edgeconnect-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Orchestrator REST API OpenAPI specs — curated `-latest` plus a full reference spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 26 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Orchestrator | 9.3+ |
| `HPE Aruba Networking EdgeConnect SD-WAN:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Authentication is a static API key sent on the `X-Auth-Token` header. Generate a key as an administrator in Orchestrator (Users & Authentication > API Keys). Session/cookie-based login is deprecated as of Orchestrator 9.3 and is not used by this integration.

Import `edgeconnect-latest.json` as an Integration Model, then create an integration pointing at your Orchestrator server. Orchestrator's REST API is rooted at `/gms/rest` — this must be set in the instance's `server.base_path` field, since the platform builds the request URL from `protocol`/`host`/`port`/`base_path` rather than any path in the OpenAPI spec itself.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiKeyHeader": {
      "value": "<your-orchestrator-api-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-orchestrator-host>",
    "port": "443",
    "base_path": "/gms/rest"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`edgeconnect-latest.json`](./OpenAPIs/edgeconnect-latest.json) | latest (curated) | 26 | Trimmed to 26 of 154 upstream operations covering appliance management, discovery/approval, appliance groups, Business Intent Overlays, tunnel visibility, and template group configuration — see breakdown below |
| [`edgeconnect-9.5.json`](./OpenAPIs/edgeconnect-9.5.json) | 9.5 | 154 | Full reference spec covering Orchestrator's broader configuration and management surface |

### `edgeconnect-latest.json`

Actively-maintained spec (`x-vendor-api-version: 9.5`). Trimmed to 26 of 154 upstream operations covering common CRUD for SD-WAN fabric automation.

Resources included, by category:

- **Appliances**: list/get, modify, delete, move between groups
- **Discovered Appliances**: list discovered/denied appliances, approve, deny
- **Groups**: list, get, create, update, delete
- **Business Intent Overlays**: list, get, create, update, delete
- **Tunnels**: total tunnel count, physical tunnel listing
- **Template Groups**: list, get, create, update, delete, associate to an appliance

### `edgeconnect-9.5.json`

Full reference spec (154 operations) covering appliances and discovery, groups, Business Intent Overlays, tunnels and bonded tunnels, template groups, regions, zones, VRF segmentation, BGP, OSPF, NAT policy, QoS policy, security maps, IP objects, application definitions, interface labels, HA groups, licensing, releases, SNMP, deployment, and API keys. See `edgeconnect-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### HPE Aruba Networking EdgeConnect Project

Backed by the **`HPE Aruba Networking EdgeConnect SD-WAN:latest`** Integration Model (see [`edgeconnect-latest.json`](./OpenAPIs/edgeconnect-latest.json) above). The project contains **26 workflows** organized into **6 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Appliances | 4 | List/get, modify, delete, move to a different group |
| Discovered Appliances | 4 | List discovered, list denied, approve, deny |
| Groups | 5 | List, get, create, update, delete |
| Business Intent Overlays | 5 | List, get, create, update, delete |
| Tunnels | 2 | Total tunnel count, physical tunnel listing |
| Template Groups | 6 | List, get, create, update, delete, associate to an appliance |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `HPE Aruba Networking EdgeConnect SD-WAN:latest` Integration Model | Import from [`edgeconnect-latest.json`](./OpenAPIs/edgeconnect-latest.json) before importing the project |
| `EdgeConnect` integration instance | Create with the connection properties above. Workflows are wired to an integration instance named `EdgeConnect` — update the `adapter_id` value in each workflow task if yours is named differently |
