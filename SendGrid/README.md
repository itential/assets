SendGrid is Twilio's cloud-based email delivery platform for sending transactional and marketing email at scale, with tooling for dynamic templates, contact/list management, suppression handling, and delivery analytics.

This project provides an OpenAPI spec for automating against SendGrid's v3 REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for email-sending automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`sendgrid-latest.json`](#sendgrid-latestjson)
  - [`sendgrid-1.0.0-rc.13.json`](#sendgrid-100-rc13json)
- [Studio Projects](#studio-projects)
  - [SendGrid Project](#sendgrid-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | SendGrid v3 REST API OpenAPI spec — curated `-latest` plus the full spec |
| [Studio Projects/SendGrid](./Studio%20Projects/SendGrid.project.json) | 26 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| SendGrid v3 REST API | 1.0.0-rc.13 |
| `SendGrid:latest` Integration Model | Required to run the Studio Project below |

## Integration Configuration

Import `sendgrid-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at SendGrid's API (`https://api.sendgrid.com`, or `https://api.eu.sendgrid.com` for EU regional subusers).

Authentication is a static API key sent as a Bearer token in the `Authorization` header:

```
Authorization: Bearer <your-sendgrid-api-key>
```

Generate an API key in the SendGrid UI under **Settings > API Keys**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearer": {
      "token": { "value": "<your-sendgrid-api-key>" }
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.sendgrid.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`sendgrid-latest.json`](./OpenAPIs/sendgrid-latest.json) | latest (curated) | 83 | Trimmed to 83 of 391 upstream operations covering common CRUD for automation — see breakdown below |
| [`sendgrid-1.0.0-rc.13.json`](./OpenAPIs/sendgrid-1.0.0-rc.13.json) | 1.0.0-rc.13 | 391 | Full spec for the SendGrid v3 REST API |

Both specs are assembled from Twilio SendGrid's own officially-published OpenAPI 3.1 definitions at [`github.com/twilio/sendgrid-oai`](https://github.com/twilio/sendgrid-oai) (the repository's newer home — it was formerly published at `sendgrid/sendgrid-oai`). SendGrid publishes this as 46 separate per-resource files rather than one combined document, so all 46 were merged into the specs here.

### `sendgrid-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0-rc.13`). Trimmed to 83 of 391 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Mail**: Send Mail, Create/Get Mail Batch
- **Templates**: List, Create, Duplicate, Get, Update, Delete, Versions (Create, Get, Update, Delete, Activate)
- **API Keys**: List, Create, Get, Update (name and full), Delete
- **Suppressions**: Unsubscribe Groups (list/create/get/update/delete + group suppressions), global suppressions, bounces, blocks, invalid emails, spam reports (list/get/delete)
- **Marketing Contacts**: List, Get, Upsert, Delete, batch/search/export/import
- **Marketing Lists**: List, Create, Get, Update, Delete, contact removal/count
- **Verified Senders**: Create, List, Update, Delete, resend/verify, domains, steps completed

Not included: the legacy Contact Database (`contactdb`) and Legacy Marketing Campaigns endpoints (superseded by Marketing Contacts/Lists), IP address/pool/warmup management, subusers, teammates/SSO/scopes (user and permission administration), account provisioning/partner reseller endpoints, stats/logs/email-activity reporting, webhooks and tracking/mail settings configuration, domain authentication and link branding, and alerts. Pull the full spec below if you need one of these.

### `sendgrid-1.0.0-rc.13.json`

Full spec assembled from all 46 of Twilio SendGrid's official per-resource OpenAPI definitions (391 operations) — the entire SendGrid v3 API surface as SendGrid documents it. See `sendgrid-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### SendGrid Project

Backed by the **`SendGrid:latest`** Integration Model (see [`sendgrid-latest.json`](./OpenAPIs/sendgrid-latest.json) above). The project contains **26 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Mail | Send Mail, Create/Get Mail Batch | Transactional email sending |
| Templates | List, Create, Get, Update, Delete | Dynamic template CRUD |
| API Keys | List, Create, Get, Update, Delete | API key management |
| Contacts | List, Get, Upsert, Delete | Marketing contact CRUD |
| Lists | List, Create, Get, Update, Delete | Marketing list CRUD |
| Suppressions | List/Delete Bounces, List/Delete Blocks | Suppression list management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `SendGrid:latest` Integration Model | Import from [`sendgrid-latest.json`](./OpenAPIs/sendgrid-latest.json) before importing the project |
| `SendGrid` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `SendGrid` — update the `adapter_id` value in each workflow task if yours is named differently |
