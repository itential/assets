RingCentral is a cloud communications platform providing business phone, SMS/MMS, fax, video meetings, and team messaging (RingCentral App) services, exposed through its Connect Platform REST API.

This project provides OpenAPI specs for automating against the RingCentral Connect Platform API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | RingCentral Connect Platform REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| RingCentral Connect Platform API | 1.0.39 |
| `RingCentral` Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at `https://platform.ringcentral.com/`.

Authentication is an OAuth2 bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Obtain an access token via RingCentral's OAuth2 flow (client credentials or JWT flow) using an app registered in your RingCentral Developer account at https://developers.ringcentral.com. The spec's `OAuth2` security scheme points at RingCentral's own `authorizationUrl`/`tokenUrl` endpoints (`https://platform.ringcentral.com/restapi/oauth/authorize` and `.../restapi/oauth/token`).

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`ringcentral-latest.json`](./OpenAPIs/ringcentral-latest.json) | latest (curated) | Trimmed to 153 of 312 upstream operations — see breakdown below |
| [`ringcentral-1.0.39.json`](./OpenAPIs/ringcentral-1.0.39.json) | 1.0.39 | Full spec for RingCentral Connect Platform API 1.0.39 (312 operations). |

### `ringcentral-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.39`). Trimmed to 153 of 312 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Account / Company**: Account info, Business Address, Service Info, Business Hours (account and extension level)
- **Extensions (Users)**: List, Create, Read, Update, Delete extensions; Caller ID, Notification Settings, Presence, Unified Presence
- **Call Logs**: Account and extension call logs, active calls
- **Call Control**: Telephony sessions and call parties (answer, hold, park, transfer, pickup, flip, forward, reject, reply, unhold, supervise), call-out
- **Call Queues / Call Monitoring Groups**: List queues/groups and members
- **Rule Management**: Answering Rules (account and extension level), Call Recording toggle
- **Call Forwarding**: Forwarding numbers
- **Call Blocking**: Blocked phone numbers
- **Devices**: Device read/update, extension device list
- **Contacts**: Internal directory entries and search, external address book contacts
- **Messaging**: SMS, MMS, Fax send
- **RingOut**: Click-to-call (make/read/cancel RingOut calls)
- **Meetings**: RingCentral Video meeting create/read/update/delete/end
- **Message Store**: Read/update/delete voicemail, fax, and SMS messages and attachments
- **Phone Numbers**: Account and extension phone number lookup
- **Call Recordings**: Recording metadata and content retrieval
- **Call Routing**: IVR menus and IVR prompts
- **Team Messaging (RingCentral App)**: Teams, Chats, Conversations, Posts, Calendar Events
- **Subscriptions**: Event notification subscriptions (for event-driven automation)
- **API Info**: Service status/health check

Dropped as long tails: OAuth2 endpoints (handled by the integration's security scheme, not called as workflow tasks), SCIM user provisioning (overlaps with Extension CRUD), Automatic Location Updates / E911 device-address management, Paging Only Groups, Glip compliance data exports and message-store export reports, Glip webhooks and interactive cards, regional-settings reference/lookup dictionaries (country, language, state, timezone), profile images, custom greetings, deprecated duplicate endpoints (`/ringout`, `/glip/groups`), and various bulk-assign administrative endpoints. See the full spec for anything not covered here.
