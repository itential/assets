GoDaddy is a domain registrar and web hosting provider. This project covers the GoDaddy Domains API — domain registration, availability and suggestion lookups, DNS record management, domain forwarding, transfers, renewals, and privacy — for automating domain lifecycle operations from Itential Platform.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`godaddy_domains-latest.json`](#godaddy_domains-latestjson)
  - [`godaddy_domains-1.0.0.json`](#godaddy_domains-100json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | GoDaddy Domains REST API OpenAPI spec — curated `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| GoDaddy Domains API | 1.0.0 |
| GoDaddy Domains Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the GoDaddy API.

Authentication is an API key pair in the `Authorization` header:

```
Authorization: sso-key <api_key>:<api_secret>
```

Generate an API key pair at https://developer.godaddy.com/keys.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`godaddy_domains-latest.json`](./OpenAPIs/godaddy_domains-latest.json) | latest (curated) | Trimmed to 31 of 42 upstream operations covering common CRUD for domain automation — see breakdown below |
| [`godaddy_domains-1.0.0.json`](./OpenAPIs/godaddy_domains-1.0.0.json) | 1.0.0 | Full spec for the GoDaddy Domains API, version 1.0.0. |

### `godaddy_domains-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 31 of 42 upstream operations covering common CRUD for domain automation.

Resources included, by category:

- **Domains**: List, Get, Update, Cancel, Get (v2 detail), Update Contacts, Transfer In, Transfer Out, Renew, Verify Registrant Email
- **Availability & Discovery**: Check Availability (single and bulk), Suggest, List Supported TLDs, Get Purchase Schema by TLD
- **DNS Records**: Add, Replace (all/by type/by type and name), Get, Delete
- **Domain Forwarding**: Get, Create, Update, Delete
- **Purchase & Contacts**: Purchase, Validate Purchase, Validate Contacts, Get Legal Agreements
- **Privacy**: Purchase Privacy, Cancel Privacy

Notification opt-in/acknowledgement management, domain action/job history, scheduled-maintenance reporting, and domain redemption recovery are not included. Pull the full spec below if you need one of those areas.

### `godaddy_domains-1.0.0.json`

Full, unmodified vendor spec for the GoDaddy Domains API, version 1.0.0 (42 operations) — the vendor's complete API surface, preserved as-is. See `godaddy_domains-latest.json` above for the curated subset if you just need common CRUD automation.
