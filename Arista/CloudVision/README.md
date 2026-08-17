Arista CloudVision-as-a-Service (CVaaS) is Arista's cloud-hosted network management platform, providing fleet-wide visibility and configuration management for Arista devices through a state-based, resource-oriented API.

This project provides an OpenAPI spec for automating against CVaaS's modern Workspace/Studio provisioning model via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
- [Studio Projects](#studio-projects)
  - [Arista CloudVision Project](#arista-cloudvision-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Arista CloudVision Workspace/Studio/Change Control OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 15 workflows in 3 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Arista CloudVision:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |
| A CVaaS service account | Required to obtain a bearer token |

## Integration Configuration

Import `arista_cloudvision_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your CVaaS tenant's host.

Authentication is a service-account bearer token: generate one in CVaaS under Settings > Service Accounts, and send it as `Authorization: Bearer <token>` on every request.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearerAuth": {
      "Authorization": "Bearer <your-service-account-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-cvaas-tenant-host>",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`arista_cloudvision_api-latest.json`](./OpenAPIs/arista_cloudvision_api-latest.json) | latest | 15 | Scoped to the Workspace/Studio/Change Control provisioning flow — see breakdown below |

CloudVision's Resource APIs are gRPC-native; this spec describes Arista's own generated REST/JSON gateway over those same services (introduced in CVP 2021.1.0, still actively maintained), converted from the vendor's published Swagger 2.0 documents to OpenAPI 3.0.

Resources included, by category:

- **Workspace**: Create/update (including issuing build, submit, cancel, abandon, or rollback requests), get, delete, get status, get build status, get per-device build detail
- **Studio**: Set/get/delete a studio's input configuration at a path (e.g. push configuration into the Static Configlet Studio), get the resolved input value
- **Change Control**: Create/update (including flagging start/stop/schedule), get configuration, delete, get full status, approve

A typical flow: create a workspace, push configuration into a Studio, request a build (a single call that internally validates, compiles, and checks the change), submit the workspace (which creates a Change Control), then approve and start that Change Control.

Deliberately excludes: every other Studio resource (AssignedTags, AutofillAction, SecretInput, Studio/StudioConfig, StudioSummary) and Change Control's ChangeControlSummary, since they aren't part of this flow; the "list all" and "get several" operations on every resource, since those are long-lived streaming (chunked NDJSON) responses rather than a single JSON object and don't fit a request/response workflow task; and the dozens of other CloudVision resource packages (inventory, tags, image, telemetry, etc.) entirely, since they're outside this workflow. Several nested vendor structures (build diagnostics, change control stages) are preserved as opaque objects rather than fully typed, since they're deep, vendor-internal detail not needed to drive this flow.

## Studio Projects

### Arista CloudVision Project

Backed by the **`Arista CloudVision:latest`** Integration Model (see [`arista_cloudvision_api-latest.json`](./OpenAPIs/arista_cloudvision_api-latest.json) above). The project contains **15 workflows** organized into **3 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Workspace | 6 | Workspace lifecycle, build/submit requests, build status |
| Change Control | 5 | Change Control lifecycle, status, approval |
| Studio | 4 | Studio input configuration |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Arista CloudVision:latest` Integration Model | Import from [`arista_cloudvision_api-latest.json`](./OpenAPIs/arista_cloudvision_api-latest.json) before importing the project |
| `Arista CloudVision` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Arista CloudVision` — update the `adapter_id` value in each workflow task if yours is named differently |
