# OWASP ZAP

OWASP ZAP (Zed Attack Proxy) is an open-source web application security scanner maintained by the OWASP Foundation. It combines an intercepting proxy, a traditional link-following spider, an AJAX spider, and an active scanner that probes discovered endpoints for vulnerabilities, all controllable through a local HTTP API.

This project provides OpenAPI specs for automating against ZAP's HTTP API via an Integration Model, plus a Studio Project of ready-to-import workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`owasp_zap-latest.json`](#owasp_zap-latestjson)
  - [`owasp_zap-2.16.1.json`](#owasp_zap-2161json)
- [Studio Projects](#studio-projects)
  - [OWASP ZAP Project](#owasp-zap-project)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | OWASP ZAP API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 33 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| OWASP ZAP | 2.16.x (see OpenAPIs below for exact spec version) |
| `OWASP ZAP:latest` Integration Model | Required to build automation against the OpenAPI specs, and to run the Studio Project below |

## Integration Configuration

Import `owasp_zap-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your ZAP instance's local API.

Authentication is a static API key, configured in ZAP under Tools > Options > API. It's sent as an `X-ZAP-API-Key` header on every request.

### Connection Properties

```json
{
  "authentication": {
    "apiKeyHeader": {
      "value": "<your-zap-api-key>"
    }
  },
  "server": {
    "protocol": "http",
    "host": "127.0.0.1",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`owasp_zap-latest.json`](./OpenAPIs/owasp_zap-latest.json) | latest (curated) | 33 | Curated to spider/active scan job control, alerts, and context/scope and core session automation — see breakdown below |
| [`owasp_zap-2.16.1.json`](./OpenAPIs/owasp_zap-2.16.1.json) | 2.16.1 | 735 | Full spec generated from the ZAP project's own API documentation source |

### `owasp_zap-latest.json`

Curated to the operations a typical automated scan workflow (spider a target, active-scan it, pull back the alerts, and manage scope) actually needs.

Resources included, by category:

- **Spider**: start scan, get status, stop scan, get results, list scans, remove scan
- **Active Scan**: start scan, get status, stop/pause/resume scan, remove scan, list scans, get alert IDs raised by a scan
- **Alerts**: list, get by ID, summary by risk, count, delete by ID, delete all
- **Context**: create, list, get, remove, include/exclude URL regex from scope, get URLs in context
- **Core**: list sites, get URLs, get version, access a URL, new session, save session

### `owasp_zap-2.16.1.json`

Full spec covering every ZAP API component (spider, active scan, passive scan, AJAX spider, context, alerts, alert filters, authentication, authorization, users, sessions, scripts, HUD, GraphQL, WebSocket, breakpoints, replacer, and more), generated from the ZAP project's own API documentation source. See `owasp_zap-latest.json` for the curated subset if you just need common scan automation.

## Studio Projects

### OWASP ZAP Project

Backed by the **`OWASP ZAP:latest`** Integration Model (see [`owasp_zap-latest.json`](./OpenAPIs/owasp_zap-latest.json) above). The project contains **33 workflows** organized into **5 folders**.

**Folder structure:**

| Folder | Workflows | Scope |
|---|---|---|
| Spider | 6 | Start/stop scan, get status/results, list scans, remove scan |
| Active Scan | 8 | Start/stop/pause/resume scan, remove scan, list scans, get status, get alert IDs |
| Alerts | 6 | List, get, summary, count, delete one, delete all |
| Context | 7 | Create, list, get, remove, include/exclude regex, get URLs |
| Core | 6 | List sites, get URLs, get version, access URL, new session, save session |

**Dependencies:**

| Dependency | Notes |
|---|---|
| `OWASP ZAP:latest` Integration Model | Import from [`owasp_zap-latest.json`](./OpenAPIs/owasp_zap-latest.json) before importing the project |
| `OWASP ZAP` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `OWASP ZAP` — update the `adapter_id` value in each workflow task if yours is named differently |
