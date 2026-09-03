Cisco Webex is a cloud collaboration platform providing team messaging, meetings, and calling. This folder covers the Webex REST APIs: administrative resources (audit events, room/space memberships) and the core messaging surface (rooms, messages, people, teams).

This project provides OpenAPI specs for automating against the Webex REST API via an Integration Model. See **OpenAPIs** below for what each spec covers.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cisco_webex-latest.json`](#cisco_webex-latestjson)
  - [`cisco_webex_messaging-latest.json`](#cisco_webex_messaging-latestjson)
  - [`cisco_webex-1.0.json`](#cisco_webex-10json)
  - [`cisco_webex_messaging-1.0.0.json`](#cisco_webex_messaging-100json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco Webex REST API OpenAPI specs — curated `-latest` plus the full dated spec, for both the core and messaging APIs |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco Webex | v1 REST API |
| Cisco Webex / Cisco Webex — Messaging Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at `webexapis.com`.

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <your-webex-token>
```

Generate a bot token or personal access token at [developer.webex.com](https://developer.webex.com/docs/api/v1) (under **My Webex Apps** or the API docs page for a short-lived personal token).

The instance's `authentication`/`server` properties should look like this once configured for `cisco_webex-latest.json`:

```json
{
  "authentication": {
    "httpBearer": "<your-webex-token>"
  },
  "server": {
    "protocol": "https",
    "host": "webexapis.com",
    "base_path": "/v1"
  }
}
```

`cisco_webex_messaging-latest.json` uses the same bearer token value, but under a differently-named scheme key — configure it as `authentication.bearer-key` instead of `authentication.httpBearer` on an instance of that model.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cisco_webex-latest.json`](./OpenAPIs/cisco_webex-latest.json) | latest (curated) | 8 | Actively-maintained spec — see breakdown below |
| [`cisco_webex_messaging-latest.json`](./OpenAPIs/cisco_webex_messaging-latest.json) | latest (curated) | 33 | Actively-maintained spec — see breakdown below |
| [`cisco_webex-1.0.json`](./OpenAPIs/cisco_webex-1.0.json) | 1.0 | 10 | Full spec for the Cisco Webex core API, version 1.0. |
| [`cisco_webex_messaging-1.0.0.json`](./OpenAPIs/cisco_webex_messaging-1.0.0.json) | 1.0.0 | 63 | Full spec for the Cisco Webex Messaging API, version 1.0.0. |

### `cisco_webex-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0`). Trimmed to 8 of 10 upstream operations.

Resources included, by category:

- **Admin Audit Events**: List admin audit events for the organization (`GET /adminAudit/events`) — the Control Hub compliance/security audit trail of admin actions, not server/API telemetry
- **Events**: List organization events and get event details (`GET /events`, `GET /events/{eventId}`) — the compliance-officer feed of user actions (messages/calls created, deleted, etc.) within the org
- **Memberships**: List, create, get, update, and remove room/space memberships (`GET/POST /memberships`, `GET/PUT/DELETE /memberships/{membershipId}`)

Dropped as a non-automatable reference lookup: `GET /licenses` and `GET /licenses/{licenseId}` — a read-only license-tier catalog (this API surface has no write/assign operation for licenses) rather than something to create/update/delete via automation.

### `cisco_webex_messaging-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 33 of 63 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Memberships**: List, create, get, update, and remove space memberships
- **Messages**: List, create, get, update, and delete messages (including direct/1:1 messages)
- **People**: List, create, get, update, and delete people; get the authenticated user (`/people/me`)
- **Rooms**: List, create, get, update, and delete rooms/spaces; get a room's meeting info
- **Teams**: List, create, get, update, and delete teams and team memberships

Dropped as long tails not core to messaging automation: card/attachment actions, room linked folders, the audit event feed (already covered by `cisco_webex-latest.json`), the Hybrid Data Security module (a specialized enterprise deployment feature), room tabs, and webhook management.

### `cisco_webex-1.0.json`

Full, unmodified vendor spec for the Cisco Webex core API, version 1.0 (10 operations) — the vendor's complete API surface, preserved as-is. See `cisco_webex-latest.json` above for the curated subset if you just need common CRUD automation.

### `cisco_webex_messaging-1.0.0.json`

Full, unmodified vendor spec for the Cisco Webex Messaging API, version 1.0.0 (63 operations) — the vendor's complete API surface, preserved as-is. See `cisco_webex_messaging-latest.json` above for the curated subset if you just need common CRUD automation.
