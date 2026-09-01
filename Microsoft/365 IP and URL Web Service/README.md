The Microsoft 365 IP Address and URL web service is Microsoft's public REST service for the current IP address ranges and URLs used by Microsoft 365, plus version tracking and change history — used to configure firewalls, proxy servers, and PAC files.

This project provides an OpenAPI spec for automating against the web service via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`m365_ip_url_web_service-latest.json`](#m365_ip_url_web_service-latestjson)
- [Studio Projects](#studio-projects)
  - [Microsoft 365 IP and URL Web Service Project](#microsoft-365-ip-and-url-web-service-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Microsoft 365 IP Address and URL web service OpenAPI spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 4 workflows in 3 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Microsoft 365 IP Address and URL Web Service:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `m365_ip_url_web_service-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the public service — no credentials required.

The instance's `server` properties should look like this once configured:

```json
{
  "server": {
    "protocol": "https",
    "host": "endpoints.office.com",
    "base_path": ""
  }
}
```

Every operation requires a `clientRequestId` — a GUID you generate yourself and reuse across calls (don't generate a new one per request; Microsoft may block frequently-rotated GUIDs). Generate one once and pass it as a workflow input each time.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`m365_ip_url_web_service-latest.json`](./OpenAPIs/m365_ip_url_web_service-latest.json) | latest | 4 | All 4 documented web methods — see breakdown below |

### `m365_ip_url_web_service-latest.json`

Hand-authored from [Microsoft's own documentation](https://aka.ms/ipurlws) — no vendor-published OpenAPI/Swagger spec exists for this service. All 4 documented web methods are included; this is the service's complete surface.

Resources included:

- **Version**: get the latest published version for all instances, or for a single instance (with optional full version history)
- **Endpoints**: get the current IP address ranges and URLs for an instance, optionally filtered by service area (Common/Exchange/SharePoint/Skype), tenant name, or IPv6 exclusion
- **Changes**: get the changes published since a given version, for building diff-based update workflows

The `instance` enum (`Worldwide`, `China`, `USGovDoD`, `USGovGCCHigh`, `France`, `Germany`) reflects the live service's actual response as of this writing — two more instances (France, Germany) than the 4 currently documented on the Microsoft Learn page.

## Studio Projects

### Microsoft 365 IP and URL Web Service Project

Backed by the **`Microsoft 365 IP Address and URL Web Service:latest`** Integration Model (see [`m365_ip_url_web_service-latest.json`](./OpenAPIs/m365_ip_url_web_service-latest.json) above). The project contains **4 workflows** organized into **3 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Version | 2 | Latest version for all instances, or for one instance |
| Endpoints | 1 | Current IP address ranges and URLs for an instance |
| Changes | 1 | Changes published since a given version |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Microsoft 365 IP Address and URL Web Service:latest` Integration Model | Import from [`m365_ip_url_web_service-latest.json`](./OpenAPIs/m365_ip_url_web_service-latest.json) before importing the project |
| `Microsoft 365 IP and URL Web Service` integration instance | Create in **Admin > Integrations** with the connection properties above — no credentials needed. Workflows are wired to an integration instance named `Microsoft 365 IP and URL Web Service` — update the `adapter_id` value in each workflow task if yours is named differently |
