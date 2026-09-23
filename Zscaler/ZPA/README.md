Zscaler Private Access (ZPA) is Zscaler's Zero Trust Network Access service — it brokers least-privilege, identity-aware access to private applications without exposing them to the internet or placing users on the corporate network.

This project provides OpenAPI specs for automating against ZPA's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`zscaler_zpa_api-latest.json`](#zscaler_zpa_api-latestjson)
  - [`zscaler_zpa_api-3.8.48.json`](#zscaler_zpa_api-3848json)
- [Studio Projects](#studio-projects)
  - [Zscaler ZPA Project](#zscaler-zpa-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Zscaler ZPA API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 31 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Zscaler Private Access:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |
| Zscaler OneAPI access enabled for your organization | Required — not self-service; contact your Zscaler account team |

## Integration Configuration

Import `zscaler_zpa_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Zscaler's OneAPI host.

Authentication is OAuth2 client-credentials via Zscaler's unified OneAPI platform (brokered through Zidentity) — the same mechanism ZIA uses. Generate a client ID/secret at Admin Portal → API Key Management → OneAPI Credentials.

The token request also requires a fixed `audience=https://api.zscaler.com` parameter alongside `client_id`/`client_secret` — configure this as an extra static token-request parameter on the integration if your platform version supports it.

Every ZPA management-config endpoint is rooted at `/zpa/mgmtconfig/v1/admin/customers/<your-zpa-customer-id>` — your numeric ZPA customer ID (visible in the ZPA Admin Portal under Administration > Company) must be set in the instance's `server.base_path` field, since the platform builds the request URL from `protocol`/`host`/`port`/`base_path` rather than any path in the OpenAPI spec itself.

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
    "base_path": "/zpa/mgmtconfig/v1/admin/customers/<your-zpa-customer-id>"
  }
}
```

Non-production clouds use `api.<cloud>.zsapi.net` instead of `api.zsapi.net`.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`zscaler_zpa_api-latest.json`](./OpenAPIs/zscaler_zpa_api-latest.json) | latest (curated) | 31 | Trimmed to 31 of 74 upstream operations covering common CRUD for automation — see breakdown below |
| [`zscaler_zpa_api-3.8.48.json`](./OpenAPIs/zscaler_zpa_api-3.8.48.json) | 3.8.48 | 74 | Reference spec extracted from Zscaler's official SDK — ZPA's core management-config API surface |

### `zscaler_zpa_api-latest.json`

Both specs in this folder were built directly from Zscaler's official, actively-maintained [`zscaler-sdk-go`](https://github.com/zscaler/zscaler-sdk-go) source — endpoint paths, HTTP verbs, and field-level request/response schemas were extracted from the SDK's typed Go structs and service functions.

Trimmed to 31 of 74 upstream operations covering common CRUD for automation. The full SDK models ZPA's entire management-config surface, including Service Edges/Service Edge Groups, provisioning keys, application servers, SAML/SCIM/IdP configuration, device posture and trusted network reference data, browser access/PRA/inspection/isolation policy types, microtenants, LSS log streaming, and dozens of other specialized areas — none of those are included here.

Resources included, by category:

- **Application Segments**: List, get, create, update, delete
- **Segment Groups**: List, get, create, update, delete
- **Server Groups**: List, get, create, update, delete
- **App Connector Groups**: List, get, create, update, delete
- **App Connectors**: List, get, update, delete (App Connectors self-register during enrollment via a provisioning key — there is no create operation)
- **Access Policy**: Get policy set, list rules, get rule, create rule, update rule, delete rule, reorder rule

### `zscaler_zpa_api-3.8.48.json`

Reference spec extracted from `zscaler-sdk-go` release `v3.8.48` (74 operations) — ZPA's core management-config API surface as implemented in the SDK, preserved as-is. Beyond the curated categories above, it also covers Service Edges, Service Edge Groups, Application Servers, Provisioning Keys, Machine Groups, Posture Profiles, Trusted Networks, and Identity Providers. See `zscaler_zpa_api-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Zscaler ZPA Project

Backed by the **`Zscaler Private Access:latest`** Integration Model (see [`zscaler_zpa_api-latest.json`](./OpenAPIs/zscaler_zpa_api-latest.json) above). The project contains **31 workflows** organized into **6 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Access Policy | 7 | Get policy set, list/get/create/update/delete/reorder rules |
| Application Segments | 5 | List, get, create, update, delete |
| Segment Groups | 5 | List, get, create, update, delete |
| Server Groups | 5 | List, get, create, update, delete |
| App Connector Groups | 5 | List, get, create, update, delete |
| App Connectors | 4 | List, get, update, delete |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Zscaler Private Access:latest` Integration Model | Import from [`zscaler_zpa_api-latest.json`](./OpenAPIs/zscaler_zpa_api-latest.json) before importing the project |
| `Zscaler ZPA` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Zscaler ZPA` — update the `adapter_id` value in each workflow task if yours is named differently |
