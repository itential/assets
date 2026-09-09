Netskope's REST API v2 — events and alerts, datasearch, dataexport iterators, policy, steering and NPA private apps, CASB, SaaS Posture Management, incidents and UBA, profiles, infrastructure, SCIM, reporting, and more. Ships as two specs: a curated Integration Model (`netskope-latest.json`) covering the most-commonly-automated customer-facing operations, and the full Netskope v2 API (`netskope_v2.json`) for complete coverage.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`netskope-latest.json`](#netskope-latestjson)
  - [`netskope_v2.json`](#netskope_v2json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Curated Netskope Integration Model (`netskope-latest.json`) and the full Netskope v2 spec (`netskope_v2.json`) |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Netskope API token | A service account token generated in Settings > Administration > Administrators > Service Account |

## Integration Configuration

Import `netskope-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration instance pointing at your Netskope tenant.

Authentication is a static API token sent as a request header (`Netskope-Api-Token`). Generate a token in **Settings > Administration > Administrators > Service Account**, then configure it in the integration instance.

The Netskope base URL is tenant-specific — replace `<tenant>` with your actual tenant subdomain (e.g., `mycompany.goskope.com`).

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "apiKeyAuth": {
      "value": "<your-netskope-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<tenant>.goskope.com",
    "base_path": "/api/v2"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`netskope-latest.json`](./OpenAPIs/netskope-latest.json) | v2 | 571 | Curated Netskope API: events, alerts, datasearch, policy, steering/NPA, CASB, SaaS Posture Management, incidents, profiles, infrastructure, SCIM, reporting |
| [`netskope_v2.json`](./OpenAPIs/netskope_v2.json) | v2 | 848 | Full Netskope REST API v2 — all operations across all product areas |

### `netskope-latest.json`

Sourced from Netskope's official api-schemas repo published via Postman (postman.com/netskope-tech-alliances/netskope-rest-api). Curated to customer-facing operations across 19 categories — excludes internal UI microservices (`ui`, `echo`, `dem`, `adem`) and niche/specialized services (`nsiq`, `skopilot`, `forwardproxy`, `drm`, `foundation`, `ubadatasvc`):

| Category | Description |
|---|---|
| events | Alerts, application, audit, network, page, transaction logs; dataexport iterators; datasearch |
| policy | URL lists, real-time policy, NPA policy/policygroup, internet access groups/rules, domain fronting |
| steering | NPA private apps and tags, cert-pinned apps, GRE, IPSec tunnel configuration |
| spm | SaaS Posture Management — apps, inventory, policy, reports, posture scores, third-party apps |
| services | DLP data lineage, EDM, mTLS, PKI rotation, traffic classes/rules, CloudTap, TYOC |
| profiles | Destination profiles, network location profiles, HTTP header profiles, service profiles, device intelligence |
| incidents | IMS forensics, malware, incident updates, UBA, TSS |
| infrastructure | NPA publishers, load balancers, upgrade profiles |
| scim | SCIM user/group provisioning |
| casbapi | CASB enforcement, notification, policy, remediation, steward |
| reporting | Advanced Analytics reporting |
| platform | Platform settings, advanced file scan, contracts |
| auth | API token management |
| notifications | Custom images, delivery settings, notification templates |
| rbac | Role-based access control |
| atp | Advanced Threat Protection file scan and reports |
| deviceclassification | Device classification configuration |
| discovery | Log management, web uploader |
| users | User attributes |

### `netskope_v2.json`

Sourced from Netskope's official api-schemas repo published via Postman (postman.com/netskope-tech-alliances/netskope-rest-api). Full Netskope REST API v2 — 848 operations across 571 paths covering all product areas including internal UI microservices and specialized services. Import this spec if you need operations not covered by the curated build.
