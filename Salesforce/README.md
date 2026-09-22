# Salesforce

Salesforce is a cloud-based CRM platform for managing accounts, contacts, opportunities, cases, leads, and other business objects, plus programmatic and declarative org customization via Apex and metadata.

This project provides two peer OpenAPI specs — the core REST API and the Tooling API — for building automation via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on both.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Scope](#scope)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`salesforce_rest-latest.json`](#salesforce_rest-latestjson)
  - [`salesforce_rest-62.0.json`](#salesforce_rest-620json)
  - [`salesforce_tooling-latest.json`](#salesforce_tooling-latestjson)
  - [`salesforce_tooling-62.0.json`](#salesforce_tooling-620json)
- [Studio Projects](#studio-projects)
  - [Salesforce Project](#salesforce-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Two peer specs — `salesforce_rest-latest.json` (core REST API) and `salesforce_tooling-latest.json` (Tooling/metadata API) — each with a full dated counterpart |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 19 workflows in 5 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Salesforce:latest` Integration Model | Required for the REST API CRUD workflows |
| `Salesforce Tooling:latest` Integration Model | Required for the Tooling API metadata workflows |

## Scope

These specs cover generic CRUD against any object (standard or custom) via the REST API's `sobjects` endpoints, SOQL/SOSL query and search, and the Tooling API's metadata CRUD and anonymous Apex execution. Custom objects and fields aren't represented individually — the generic `sobjects/{sObjectName}` endpoints work against any object name, standard or custom, once you supply your org's own API names.

## Integration Configuration

Import both OpenAPI specs from `OpenAPIs/` as Integration Models in **Admin > Integrations**, then create one integration instance per model, both pointing at the same Salesforce org.

Authentication is OAuth 2.0 (client credentials grant) against a connected app configured for the client credentials flow. The token endpoint is per-org: use `login.salesforce.com` for production, `test.salesforce.com` for sandboxes, or your org's My Domain host.

The instances' `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-connected-app-consumer-key>",
      "client_secret": "<your-connected-app-consumer-secret>",
      "auth_method": "client_secret_post",
      "scope": "",
      "token_url": "https://yourorg.my.salesforce.com/services/oauth2/token",
      "refresh_url": "",
      "token": { "access_token": "" }
    }
  },
  "server": {
    "protocol": "https",
    "host": "yourorg.my.salesforce.com",
    "base_path": ""
  }
}
```

Replace `yourorg.my.salesforce.com` with your org's actual My Domain hostname in both the `token_url` and `server.host` fields — the value baked into the spec's `servers`/`tokenUrl` fields is a placeholder.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`salesforce_rest-latest.json`](./OpenAPIs/salesforce_rest-latest.json) | latest | 11 | Curated REST API subset — see breakdown below |
| [`salesforce_rest-62.0.json`](./OpenAPIs/salesforce_rest-62.0.json) | 62.0 | 21 | Full REST API reference surface |
| [`salesforce_tooling-latest.json`](./OpenAPIs/salesforce_tooling-latest.json) | latest | 8 | Curated Tooling API subset — see breakdown below |
| [`salesforce_tooling-62.0.json`](./OpenAPIs/salesforce_tooling-62.0.json) | 62.0 | 10 | Full Tooling API reference surface |

### `salesforce_rest-latest.json`

Trimmed to 11 of 21 upstream operations covering generic CRUD for automation against any standard or custom object.

Resources included, by category:

- **Objects**: List Available Objects, Get Object Basic Information, Describe Object
- **Records**: Create Record, Get Record, Update Record, Delete Record, Upsert Record by External ID
- **Query**: SOQL Query, SOQL Query All, SOSL Search

### `salesforce_rest-62.0.json`

Full reference surface (21 operations), adding org-introspection and UI-metadata endpoints not typically part of day-to-day CRUD automation: deleted/updated record ID lists, org limits and record counts, page layouts, list views and their results, object quick actions, the app menu, and tabs.

### `salesforce_tooling-latest.json`

Trimmed to 8 of 10 upstream operations covering metadata object CRUD and anonymous Apex execution.

Resources included, by category:

- **Metadata Objects**: List Tooling Objects, Create Metadata Record, Describe Tooling Object, Get Metadata Record, Update Metadata Record, Delete Metadata Record
- **Apex**: Tooling Query, Execute Anonymous Apex

### `salesforce_tooling-62.0.json`

Full reference surface (10 operations), adding Tooling Query All and asynchronous Apex test execution (`runTestsAsynchronous`).

## Studio Projects

### Salesforce Project

Backed by the **`Salesforce:latest`** and **`Salesforce Tooling:latest`** Integration Models (see above). The project contains **19 workflows** organized into **5 folders**, one atomic workflow per curated operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Objects | List Available Objects, Get Object Basic Information, Describe Object | Object discovery and metadata |
| Records | Create, Get, Update, Delete, Upsert by External ID | Record CRUD on any standard or custom object |
| Query | SOQL Query, SOQL Query All, SOSL Search | Querying and searching records |
| Tooling Metadata | List, Create, Describe, Get, Update, Delete | Metadata object CRUD (CustomField, ValidationRule, etc.) |
| Tooling Apex | Tooling Query, Execute Anonymous Apex | Apex execution and metadata querying |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Salesforce:latest` Integration Model | Import from [`salesforce_rest-latest.json`](./OpenAPIs/salesforce_rest-latest.json) before importing the project |
| `Salesforce Tooling:latest` Integration Model | Import from [`salesforce_tooling-latest.json`](./OpenAPIs/salesforce_tooling-latest.json) before importing the project |
| `Salesforce` integration instance | Create in **Admin > Integrations** with the connection properties above. Records/Query/Objects workflows are wired to an integration instance named `Salesforce` — update the `adapter_id` value in each workflow task if yours is named differently |
| `Salesforce Tooling` integration instance | Create in **Admin > Integrations** with the connection properties above. Tooling workflows are wired to an integration instance named `Salesforce Tooling` — update the `adapter_id` value in each workflow task if yours is named differently |
