Zoom is a cloud unified communications platform for video meetings and webinars, providing programmatic access to meetings, webinars, recordings, users, and accounts through a REST API.

This project provides OpenAPI specs for automating against the Zoom REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for meeting and webinar automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`zoom-latest.json`](#zoom-latestjson)
  - [`zoom-2.0.0.json`](#zoom-200json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Zoom REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Zoom API | 2.0.0 |
| Zoom Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Zoom's API.

Authentication is an API key passed in the `access_token` query parameter:

```
GET https://api.zoom.us/v2/users?access_token=<your-access-token>
```

Generate an access token by creating a Server-to-Server OAuth app at [marketplace.zoom.us](https://marketplace.zoom.us), then exchanging the app's client ID and secret for an access token via `POST https://zoom.us/oauth/token`.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "global": {
      "value": "<your-api-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.zoom.us",
    "base_path": "/v2"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`zoom-latest.json`](./OpenAPIs/zoom-latest.json) | latest (curated) | 49 | Actively-maintained, trimmed to 49 of 155 upstream operations — see breakdown below |
| [`zoom-2.0.0.json`](./OpenAPIs/zoom-2.0.0.json) | 2.0.0 | 155 | Full, unmodified vendor spec |

### `zoom-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.0.0`). Trimmed to 49 of 155 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Meetings**: Retrieve, update, delete a meeting; meeting invitation; meeting status; registrants (list/add) and registrant status; polls (list/create/retrieve/update/delete); recordings (retrieve/delete) and recording settings
- **Webinars**: Retrieve, update, delete a webinar; webinar status; registrants (list/add) and registrant status; polls (list/create/retrieve/update/delete); panelists (list/add/remove)
- **Users**: List/create/retrieve/update/delete a user; check a user's email; update a user's email, password, and status; user settings (retrieve/update); create/list a user's meetings and webinars; list a user's recordings

Excluded: sub-account administration and billing, groups and IM groups/chat, H.323/SIP device management, dashboard metrics, usage/report endpoints, past meeting/webinar instance history, TSP telephony provider configuration, webhook management, tracking fields, and long-tail user administration (assistants, schedulers, PAC accounts, profile pictures, SSO tokens, permissions). See the full spec below for these.

### `zoom-2.0.0.json`

Full, unmodified vendor spec for Zoom API 2.0.0 (155 operations) — the vendor's complete API surface, preserved as-is. See `zoom-latest.json` above for the curated subset if you just need common CRUD automation.
