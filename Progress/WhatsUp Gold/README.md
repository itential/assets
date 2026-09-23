# WhatsUp Gold

Progress WhatsUp Gold is a network, server, and application monitoring platform, covering device discovery, polling, and monitoring, with credential, device group, device role, and monitor management.

This project provides OpenAPI specs for automating against WhatsUp Gold's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`whatsup_gold-latest.json`](#whatsup_gold-latestjson)
  - [`whatsup_gold-v1.json`](#whatsup_gold-v1json)
- [Studio Projects](#studio-projects)
  - [WhatsUp Gold Project](#whatsup-gold-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | WhatsUp Gold REST API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 85 workflows in 10 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `WhatsUp Gold:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `whatsup_gold-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your WhatsUp Gold server.

Authentication is a token retrieved dynamically: `POST /api/v1/token`, form-urlencoded, with `grant_type=password` plus a username/password, returns a JSON body containing `access_token`, which is then sent as the `Authorization` header on every subsequent call. Itential Platform automates the whole exchange — you only need to supply your username and password once.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "dynamicToken": {
      "value": "",
      "dynamicRetrieval": {
        "method": "POST",
        "url": "https://<whatsup-gold-host>:9644/api/v1/token",
        "responsePointer": "/access_token"
      },
      "parameters": {
        "grant_type": "password",
        "username": "<your-username>",
        "password": "<your-password>"
      }
    }
  },
  "server": {
    "protocol": "https",
    "host": "<whatsup-gold-host>",
    "port": "9644",
    "base_path": "/api/v1"
  }
}
```

Substitute your WhatsUp Gold server's hostname/IP and REST API port in both the `dynamicRetrieval.url` and `server` fields. The platform re-retrieves the token automatically on expiry.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`whatsup_gold-latest.json`](./OpenAPIs/whatsup_gold-latest.json) | latest (curated) | 85 | Curated to core device, group, credential, role, and monitor CRUD — see breakdown below |
| [`whatsup_gold-v1.json`](./OpenAPIs/whatsup_gold-v1.json) | v1 | 100 | Full vendor spec for the WhatsUp Gold v1 REST API |

### `whatsup_gold-latest.json`

Trimmed from the vendor's 100-operation full v1 export to 85 operations covering core monitoring automation.

Resources included, by category:

- **Devices** (46 ops): device CRUD, bulk operations, properties, polling and maintenance configuration, custom attributes, credential and role assignment, status, and monitoring reports (CPU, disk, memory, interface, ping, state-change)
- **Device Groups** (18 ops): group lookup, child-group and device listing, credential listing, poll-now, aggregate status, and the same monitoring report set scoped to a group
- **Credentials** (8 ops): credential CRUD and device-assignment lookup/removal
- **Device Roles** (8 ops): role CRUD, enable/disable, restore to defaults, and device-assignment listing
- **Monitors** (2 ops): monitor listing and lookup by ID
- **Product** (3 ops): API version, product version, and authenticated-user identity

### `whatsup_gold-v1.json`

Full, unmodified vendor spec for the WhatsUp Gold v1 REST API — the vendor's complete API surface, preserved as-is. See `whatsup_gold-latest.json` above for the curated subset if you just need core monitoring automation.

## Studio Projects

### WhatsUp Gold Project

Backed by the **`WhatsUp Gold:latest`** Integration Model (see [`whatsup_gold-latest.json`](./OpenAPIs/whatsup_gold-latest.json) above). The project contains **85 workflows** organized into **10 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Devices | 18 | Bulk operations, device CRUD, properties, polling and maintenance configuration, status |
| Devices - Attributes | 7 | Custom attribute CRUD on a device |
| Devices - Credentials | 4 | Credential assignment/unassignment on a device |
| Devices - Roles | 6 | Role assignment/unassignment on a device |
| Devices - Reports | 11 | CPU, disk, memory, interface, ping, and state-change reports for a device |
| Device Groups | 18 | Group lookup, child-group/device listing, poll-now, aggregate status, group-scoped reports |
| Device Roles | 8 | Role CRUD, enable/disable, restore to defaults, device-assignment listing |
| Credentials | 8 | Credential CRUD, device-assignment lookup/removal |
| Monitors | 2 | Monitor listing and lookup by ID |
| Product | 3 | API version, product version, authenticated-user identity |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `WhatsUp Gold:latest` Integration Model | Import from [`whatsup_gold-latest.json`](./OpenAPIs/whatsup_gold-latest.json) before importing the project |
| `WhatsUp Gold` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `WhatsUp Gold` — update the `adapter_id` value in each workflow task if yours is named differently |
