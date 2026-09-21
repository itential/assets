# Support

Cisco Support APIs provide programmatic access to Cisco's support data: bug search, case management, end-of-life/end-of-sale (EoX) status, product information, serial-number-to-coverage lookups, software suggestions, automated software distribution/compliance, and service order returns (RMA).

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_support-latest.json`](#cisco_support-latestjson)
  - [`cisco_support-1.0.json`](#cisco_support-10json)
- [Studio Projects](#studio-projects)
  - [Folder Structure](#folder-structure)
  - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco Support REST API OpenAPI specs — `-latest` plus the full dated version |
| [Studio Projects/Cisco Support API](./Studio%20Projects/Cisco%20Support%20API.project.json) | 40 workflows, one per curated operation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco Support APIs | 1.0 |
| Cisco API Console application | Registered at [apiconsole.cisco.com](https://apiconsole.cisco.com), granted access to the specific Support API modules needed (Bug, Case, EoX, Product Information, Serial Number to Information, Software Suggestion, Automated Software Distribution, Service Order Return) |

## Integration Configuration

Import [`cisco_support-latest.json`](./OpenAPIs/cisco_support-latest.json) as an Integration Model in **Admin > Integrations**, then create an integration pointing at Cisco's API gateway (`apix.cisco.com`).

Authentication is OAuth 2.0 (client credentials grant) against Cisco's identity service. Register an application at [apiconsole.cisco.com](https://apiconsole.cisco.com) to obtain a client ID/secret, and request access to the Support API modules you plan to automate.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-api-console-client-id>",
      "client_secret": "<your-api-console-client-secret>",
      "auth_method": "client_secret_post",
      "token_url": "https://id.cisco.com/oauth2/default/v1/token",
      "refresh_url": "",
      "scope": "",
      "token": { "access_token": "" }
    }
  },
  "server": {
    "protocol": "https",
    "host": "apix.cisco.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_support-latest.json`](./OpenAPIs/cisco_support-latest.json) | latest (curated) | 40 | Reviewed and confirmed already scoped to common automation use — see breakdown below |
| [`cisco_support-1.0.json`](./OpenAPIs/cisco_support-1.0.json) | 1.0 | 40 | Full, unmodified vendor spec |

### `cisco_support-latest.json`

All 40 operations are read (or, for software compliance/distribution, submit) operations against Cisco's support data domains.

| Category | Operations |
|---|---|
| Bug | Get by bug IDs, search by keyword, by base product ID (with/without software releases), by product series/name with affected or fixed-in releases |
| Case | Get by case IDs, get details by case ID, get by contract IDs, get by user IDs |
| EoX | Get by date range, by product ID, by serial number, by software release string |
| Product Information | Get by serial numbers, by product IDs, MDF info by product IDs |
| Serial Number To Information | Coverage status/summary by serial or instance numbers, orderable product IDs, owner coverage status |
| Software Suggestion | Get suggested software/releases by product or MDF IDs, get compatible suggested software |
| Automated Software Distribution | Get software metadata by PID release/image, get image status by names, K9/EULA compliance forms (get/submit), get download URLs |
| Service Order Return | Get returns by RMA numbers or user IDs |

### `cisco_support-1.0.json`

Full, unmodified vendor spec, API version 1.0 (40 operations) — the vendor's complete surface across all eight Support API modules, preserved as-is. See `cisco_support-latest.json` above for the curated version, which is identical in scope.

---

## Studio Projects

Import [`Cisco Support API.project.json`](./Studio%20Projects/Cisco%20Support%20API.project.json) via **Automation Studio > Projects > Import**. It contains 40 workflows — one atomic workflow per curated operation — organized into 8 folders, built on the [`cisco_support-latest.json`](./OpenAPIs/cisco_support-latest.json) Integration Model.

Every workflow's adapter task is wired to an Integration instance named `Cisco Support`. After importing, either name your Integration instance exactly `Cisco Support`, or update the `adapter_id` value in each workflow task to match your own instance name.

Each adapter task's `response` output is the full HTTP response envelope (`{ok, url, status, headers, text, body}`), not just the payload — the actual data is at `response.body`.

### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Bug | Get Bug Details By Bug Ids, Search Bugs By Keyword, Get Bugs By Base Product Id (with/without releases), Search Bugs By Product Series/Name Affected/Fixed-In Releases | Bug search and lookup |
| Case | Get Case Summary By Case Ids, Get Case Details, Get Cases By Contract Ids, Get Cases By User Ids | Case lookup |
| EoX | Get Eox By Dates, By Product Id, By Serial Number, By Software Release String | End-of-life/end-of-sale status |
| Product Information | Get Product Info By Serial Numbers, By Product Ids, Get Product Mdf Info By Product Ids | Product identification |
| Serial Number To Information | Get Coverage Status/Summary By Serial or Instance Numbers, Get Orderable Product Ids, Get Owner Coverage Status | Coverage lookups |
| Software Suggestion | Get Suggested Software/Releases By Product or Mdf Ids, Get Compatible Suggested Software By Product/Mdf Id | Software recommendation |
| Automated Software Distribution | Get Software Metadata By Pid Release/Image, Get Software Status By Image Names, Get/Submit K9 and Eula Compliance Forms, Get Software Download Urls | Software distribution and compliance |
| Service Order Return | Get Return By Rma Number, Get Returns By User Id | RMA lookup |

### Dependencies

| Dependency | Notes |
|---|---|
| `Cisco Support:latest` Integration Model | Import from [`cisco_support-latest.json`](./OpenAPIs/cisco_support-latest.json) before importing the project |
| `Cisco Support` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Cisco Support` — update the `adapter_id` value in each workflow task if yours is named differently |
