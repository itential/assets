# Spirent TestCenter

Spirent TestCenter is a network test and measurement platform for validating device, network, and security performance at scale. The STC REST API exposes its Tcl/Python automation object model — sessions, test objects, chassis connections, and command execution — over HTTP.

This project provides an OpenAPI spec for automating against the STC REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`spirent_testcenter-latest.json`](#spirent_testcenter-latestjson)
  - [`spirent_testcenter-1.0.json`](#spirent_testcenter-10json)
- [Studio Projects](#studio-projects)
  - [Spirent TestCenter Project](#spirent-testcenter-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Spirent TestCenter STC REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 26 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Spirent TestCenter:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

> **Note:** This project does **not** require Itential Gateway. All calls go directly from Itential Platform to a Spirent Lab Server or standalone STC REST daemon.

## Integration Configuration

Import `spirent_testcenter-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Lab Server or REST daemon.

Authentication is a static session token, sent in the `X-STC-API-Session` header — there is no login/token exchange. A session must first be created via the `Create New Session` workflow (`POST /sessions/`), which returns the session ID used to derive that token.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "staticSessionToken": {
      "value": "<your-stc-session-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<labserver-or-daemon-host>",
    "base_path": "/stcapi"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`spirent_testcenter-latest.json`](./OpenAPIs/spirent_testcenter-latest.json) | latest (curated) | 25 | Trimmed from the full 30-operation upstream spec down to 25 operations — see breakdown below |
| [`spirent_testcenter-1.0.json`](./OpenAPIs/spirent_testcenter-1.0.json) | 1.0 | 30 | Full spec for the STC REST API (30 operations) |

### `spirent_testcenter-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0`). Trimmed from the full 30-operation upstream spec down to 25 operations covering session management, the object/attribute model (single and bulk), chassis connections, file management, and test execution (apply/perform/bulk perform) plus system status.

Resources included, by category:

- **Sessions**: List Current Sessions, Create New Session, Get Session Info, End Session
- **Object/Attribute Model**: Create Test Center Object, Configure Test Center Object, Get Attributes Or Object Handles, Delete Object
- **Bulk Object Management**: Create One Or More Automation Objects, Bulk Configure Object Attributes, Get Value Of One Or More Attributes, Bulk Delete Objects
- **Chassis Connections**: Connect To Chassis, Get Connection Status All Chassis, Connect To Specified Chassis, Disconnect From Specified Chassis, Get Specified Chassis Status
- **File Management**: List Session Files, Upload File Post, Download Specified File, Upload File To Session
- **Test Execution & System**: Send Test Configuration (apply), Perform Api Method, Bulk Perform Command, Get System Information

### `spirent_testcenter-1.0.json`

Full, unmodified vendor spec for the STC REST API (30 operations) — the complete API surface including the help browser and log-write utility, preserved as-is. See `spirent_testcenter-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Spirent TestCenter Project

Backed by the **`Spirent TestCenter:latest`** Integration Model (see [`spirent_testcenter-latest.json`](./OpenAPIs/spirent_testcenter-latest.json) above). The project contains **26 workflows** organized into **6 folders**, spanning session lifecycle, the object/attribute model, chassis connections, file management, and test execution.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| SessionManagement | Check Session Existance, Create New Session, End Session, Get Session Info, List Current Sessions | STC REST session lifecycle |
| ObjectManagement | Configure Test Center Object, Create Test Center Object, Delete Object, Get Attributes Or Object Handles | Single-object create/read/update/delete |
| BulkObjectManagement | Bulk Configure Object Attributes, Bulk Delete Objects, Create One Or More Automation Objects, Get Value Of One Or More Attributes | Bulk object/attribute operations |
| ChassisConnections | Connect To Chassis, Connect To Specified Chassis, Disconnect From Specified Chassis, Get Connection Status All Chassis, Get Specified Chassis Status | Chassis connection management |
| FileManagement | Download Specified File, List Session Files, Upload File Post, Upload File To Session | Session file transfer |
| SystemFunctions | Bulk Perform Command, Get System Information, Perform Api Method, Send Test Configuration | Test execution and system status |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Spirent TestCenter:latest` Integration Model | Import from [`spirent_testcenter-latest.json`](./OpenAPIs/spirent_testcenter-latest.json) before importing the project |
| `Spirent TestCenter` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Spirent TestCenter` — update the `adapter_id` value in each workflow task if yours is named differently |
