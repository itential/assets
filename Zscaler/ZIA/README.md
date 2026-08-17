Zscaler Internet Access (ZIA) is Zscaler's cloud-delivered secure web gateway — firewall, URL filtering, DLP, and cloud app control enforced at the cloud edge.

This project provides OpenAPI specs for automating against ZIA's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`zscaler_zia_api-latest.json`](#zscaler_zia_api-latestjson)
  - [`zscaler_zia_api-v3.8.46.json`](#zscaler_zia_api-v3846json)
- [Studio Projects](#studio-projects)
  - [Zscaler ZIA Project](#zscaler-zia-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Zscaler ZIA API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 111 workflows in 9 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Zscaler Internet Access:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |
| Zscaler OneAPI access enabled for your organization | Required — not self-service; contact your Zscaler account team |

## Integration Configuration

Import `zscaler_zia_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Zscaler's OneAPI host.

Authentication is OAuth2 client-credentials via Zscaler's unified OneAPI platform (brokered through Zidentity). Generate a client ID/secret at Admin Portal → API Key Management → OneAPI Credentials.

The token request also requires a fixed `audience=https://api.zscaler.com` parameter alongside `client_id`/`client_secret` — configure this as an extra static token-request parameter on the integration if your platform version supports it.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oneApiOAuth2": {
      "client_id": "<your-client-id>",
      "client_secret": "<your-client-secret>",
      "token_url": "https://<your-vanity-domain>.zslogin.net/oauth2/v1/token"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.zsapi.net",
    "base_path": ""
  }
}
```

Non-production clouds use `api.<cloud>.zsapi.net` instead of `api.zsapi.net`.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`zscaler_zia_api-latest.json`](./OpenAPIs/zscaler_zia_api-latest.json) | latest (curated) | 111 | Trimmed to 111 of 479 upstream operations covering common CRUD for automation — see breakdown below |
| [`zscaler_zia_api-v3.8.46.json`](./OpenAPIs/zscaler_zia_api-v3.8.46.json) | v3.8.46 | 479 | Full spec extracted from Zscaler's official SDK — the vendor's complete ZIA API surface |

### `zscaler_zia_api-latest.json`

Both specs in this folder were built directly from Zscaler's official, actively-maintained [`zscaler-sdk-go`](https://github.com/zscaler/zscaler-sdk-go) source — endpoint paths, HTTP verbs, and field-level request/response schemas (including per-field doc comments) were extracted from the SDK's typed Go structs and service functions.

Trimmed to 111 of 479 upstream operations covering common CRUD for automation. The full SDK models ZIA's entire API surface, including DNS control, forwarding control, IPS/NAT control, SSL inspection, sandbox, traffic forwarding/GRE, NSS feeds, malware protection, bandwidth control, endpoint DLP, SaaS security, admin/role management, and dozens of other specialized areas — none of those are included here.

Resources included, by category:

- **Firewall Policies**: Filtering rules, network services/service groups, network applications/application groups, IP source/destination groups, time windows, app services/service groups
- **URL Filtering**: Rules, advanced URL filter & cloud app settings
- **URL Categories**: List, get, create, update, delete
- **Cloud App Control**: Web application rules by type
- **DLP**: Dictionaries, engines, web rules, notification templates, ICAP servers
- **File Type Control**: Rules, categories, custom file types
- **Locations**: Locations, sub-locations, location groups
- **Rule Labels**: List, get, create, update, delete
- **User Management**: Users, groups, departments

A handful of resource names are prefixed with `Zscaler` (`Zscaler Group`/`Zscaler User` workflows) to avoid colliding with identically-named workflows already published for other products — workflow names are unique across the whole Itential Platform instance, not scoped per-project.

### `zscaler_zia_api-v3.8.46.json`

Full spec extracted from `zscaler-sdk-go` release `v3.8.46` (479 operations) — the vendor's complete ZIA API surface as implemented in the SDK, preserved as-is. See `zscaler_zia_api-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Zscaler ZIA Project

Backed by the **`Zscaler Internet Access:latest`** Integration Model (see [`zscaler_zia_api-latest.json`](./OpenAPIs/zscaler_zia_api-latest.json) above). The project contains **111 workflows** organized into **9 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Firewall Policies | 35 | Filtering rules and their supporting objects |
| DLP | 23 | Dictionaries, engines, web rules, notification templates, ICAP servers |
| User Management | 15 | Users, groups, departments |
| Locations | 8 | Locations, sub-locations, location groups |
| URL Filtering | 7 | Rules, advanced URL filter & cloud app settings |
| File Type Control | 7 | Rules, categories, custom file types |
| Cloud App Control | 6 | Web application rules by type |
| URL Categories | 5 | List, get, create, update, delete |
| Rule Labels | 5 | List, get, create, update, delete |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Zscaler Internet Access:latest` Integration Model | Import from [`zscaler_zia_api-latest.json`](./OpenAPIs/zscaler_zia_api-latest.json) before importing the project |
| `Zscaler` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Zscaler` — update the `adapter_id` value in each workflow task if yours is named differently |
