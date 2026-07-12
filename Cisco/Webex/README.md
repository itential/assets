Cisco Webex is a cloud collaboration platform providing team messaging, meetings, and calling. This folder covers the Webex REST APIs: administrative resources (audit events, room/space memberships, licenses) and the core messaging surface (rooms, messages, people, teams).

This project provides OpenAPI specs for automating against the Webex REST API via an Integration Model. See **OpenAPIs** below for what each spec covers.

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

## OpenAPIs

### `cisco_webex-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0`). This is the vendor's full published spec for this API surface — it is already narrow and cohesive (admin audit events, room/space memberships, and licenses), so it is included as-is with no trimming.

### `cisco_webex_messaging-latest.json` (curated)

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 33 of 63 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Memberships**: List, create, get, update, and remove space memberships
- **Messages**: List, create, get, update, and delete messages (including direct/1:1 messages)
- **People**: List, create, get, update, and delete people; get the authenticated user (`/people/me`)
- **Rooms**: List, create, get, update, and delete rooms/spaces; get a room's meeting info
- **Teams**: List, create, get, update, and delete teams and team memberships

Dropped as long tails not core to messaging automation: card/attachment actions, room linked folders, the audit event feed (already covered by `cisco_webex-latest.json`), the Hybrid Data Security module (a specialized enterprise deployment feature), room tabs, and webhook management.

### Full, unmodified specs

| Spec | Description |
|---|---|
| [`cisco_webex-1.0.json`](./OpenAPIs/cisco_webex-1.0.json) | Full spec for the Cisco Webex core API, version 1.0. |
| [`cisco_webex_messaging-1.0.0.json`](./OpenAPIs/cisco_webex_messaging-1.0.0.json) | Full spec for the Cisco Webex Messaging API, version 1.0.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| Cisco Webex / Cisco Webex — Messaging Integration Model | Import from an OpenAPI spec above to build automation against the REST API. |
