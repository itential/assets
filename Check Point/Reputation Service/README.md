# Reputation Service

Check Point's ThreatCloud reputation lookup service. Given a URL, IP address, or file hash (md5/sha1/sha256), it returns a classification, risk score, and contextual threat data (categories, malware family, geo location, related files) for SIEM/SOAR enrichment.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Connection Properties](#connection-properties)
- [OpenAPIs](#openapis)
  - [`check_point_reputation_service-latest.json`](#check_point_reputation_service-latestjson)
  - [`check_point_reputation_service-1.0.0.json`](#check_point_reputation_service-100json)
- [Studio Projects](#studio-projects)
  - [Check Point Reputation Service Project](#check-point-reputation-service-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Check Point Reputation Service OpenAPI specs |
| [Studio Projects/Check Point Reputation Service](./Studio%20Projects/Check%20Point%20Reputation%20Service.project.json) | 1 workflow for the resource reputation query |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Check Point Reputation Service API key | Contact Check Point (TCAPI_SUPPORT@checkpoint.com) to request one |
| `Check Point Reputation Service` Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration instance using your Reputation Service API key.

Authentication is a session token, retrieved dynamically via `GET /rep-auth/service/v1.0/request` using the `Client-Key` header and replayed on the `token` header of every subsequent request; the token is valid for 30 minutes and Itential Platform re-retrieves it automatically. The API also requires the `Client-Key` header on every actual query call, not just the token-retrieval call — since dynamic retrieval only auto-injects a single header, `Client-Key` is modeled as a required parameter on the query operation itself rather than in the authentication config, so it must be supplied as a workflow input on every task call (see the Studio Project below).

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "rep.checkpoint.com",
    "base_path": ""
  },
  "authentication": {
    "token": {
      "dynamicRetrieval": {
        "method": "GET",
        "url": "https://rep.checkpoint.com/rep-auth/service/v1.0/request",
        "responsePointer": ""
      },
      "parameters": {
        "Client-Key": "<api-key>"
      }
    }
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`check_point_reputation_service-latest.json`](./OpenAPIs/check_point_reputation_service-latest.json) | latest (curated) | 1 | Resource reputation query — see breakdown below |
| [`check_point_reputation_service-1.0.0.json`](./OpenAPIs/check_point_reputation_service-1.0.0.json) | 1.0.0 (full) | 2 | Full upstream spec, including the session-token endpoint |

### `check_point_reputation_service-latest.json`

The upstream spec has only two operations total: the session-token endpoint and the resource reputation query. The token endpoint is modeled as dynamic-retrieval auth rather than as a callable operation (see Integration Configuration above), leaving the single query operation in `-latest`:

- **Query**: query a URL, IP address, or file hash's reputation, risk score, and context — the resource type is selected via the `service` path parameter (`url` / `ip` / `file`)

### `check_point_reputation_service-1.0.0.json`

The full spec as published on SwaggerHub, including the session-token endpoint.

## Studio Projects

### Check Point Reputation Service Project

Backed by the **`Check Point Reputation Service:latest`** Integration Model (see [`check_point_reputation_service-latest.json`](./OpenAPIs/check_point_reputation_service-latest.json) above). The project contains **1 workflow** in **1 folder**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Query | Query Resource Reputation | Reputation, risk, and context lookup for a URL, IP address, or file hash |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Check Point Reputation Service:latest` Integration Model | Import from [`check_point_reputation_service-latest.json`](./OpenAPIs/check_point_reputation_service-latest.json) before importing the project |
| `Check Point Reputation Service` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Check Point Reputation Service` — update the `adapter_id` value in the workflow task if yours is named differently |
| `clientKey` workflow input | Every run of the query workflow takes the API key as a `clientKey` input, sent on the `Client-Key` header alongside the dynamically-retrieved `token` header |
