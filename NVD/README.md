# NVD

The National Vulnerability Database (NVD) is the U.S. government's public repository of standards-based vulnerability management data, built on the CVE (Common Vulnerabilities and Exposures) and CPE (Common Platform Enumeration) standards. It publishes CVE records, CVE change history, the CPE dictionary, CPE match criteria, and information on the data sources that feed the NVD, all through a small set of public REST APIs.

This project provides an OpenAPI spec covering the full NVD API surface for building automation via an Integration Model, plus a Studio Project of workflows — see **OpenAPIs** and **Studio Projects** below. The API is public; an API key is optional and only raises the request rate limit.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`nvd-latest.json`](#nvd-latestjson)
- [Studio Projects](#studio-projects)
  - [NVD Project](#nvd-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | `nvd-latest.json` — the full NVD API surface (CVE, CVE Change History, CPE, CPE Match Criteria, Source) |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 5 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| NVD API | 2.0 |
| `NVD:latest` Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import `nvd-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at NVD's public service (`https://services.nvd.nist.gov`).

Authentication is an optional API key in the `apiKey` header. Without a key, requests are limited to 5 per rolling 30-second window; with a key, the limit rises to 50 per rolling 30-second window. Request a key at NVD's API key request page.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "ApiKeyAuth": {
      "value": "<your-nvd-api-key-or-leave-blank>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "services.nvd.nist.gov",
    "base_path": ""
  }
}
```

Leaving the API key value blank is a valid configuration — every operation still works unauthenticated, just at the lower public rate limit.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`nvd-latest.json`](./OpenAPIs/nvd-latest.json) | latest | 5 | Full spec covering every NVD 2.0 API |

### `nvd-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0`). All 5 operations are carried through as `-latest` — NVD's public API surface is small and entirely read-only.

Operations, by resource type:

- **CVEs**: List / Get CVEs — full filter set (CVE ID(s), CPE association, CVSS v2/v3/v4 metrics and severity, CWE, CVE tags, KEV/CERT/OVAL flags, keyword search, publish/modified/KEV date ranges, source identifier, CPE version ranges, pagination)
- **CVE Change History**: List CVE change history — by CVE ID(s), change-event type, or change-date range
- **CPEs**: List / Get CPEs — by CPE Name ID, match string, keyword, match criteria ID, last-modified date range, pagination
- **CPE Match Criteria**: List / Get CPE Match Criteria — by CVE ID, match criteria ID, match string search, last-modified date range, pagination
- **Sources**: List sources — the organizations that contribute data to the NVD, by source identifier or last-modified date range

## Studio Projects

### NVD Project

Backed by the **`NVD:latest`** Integration Model (see [`nvd-latest.json`](./OpenAPIs/nvd-latest.json) above). The project contains **5 workflows** organized into **5 folders**, one per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| CVEs | List / Get CVEs | CVE records |
| CVE Change History | List CVE Change History | CVE change events |
| CPEs | List / Get CPEs | CPE dictionary records |
| CPE Match Criteria | List / Get CPE Match Criteria | CPE match strings and match string ranges |
| Sources | List Sources | NVD data-source organizations |

#### Dependencies

| Dependency | Notes |
|---|---|
| `NVD:latest` Integration Model | Import from [`nvd-latest.json`](./OpenAPIs/nvd-latest.json) before importing the project |
| `NVD` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `NVD` — update the `adapter_id` value in each workflow task if yours is named differently |
