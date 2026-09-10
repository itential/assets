RingCentral is a cloud communications platform providing business phone, SMS/MMS, fax, video meetings, and team messaging (RingCentral App) services, exposed through its Connect Platform REST API.

This project provides OpenAPI specs for automating against the RingCentral Connect Platform API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`ringcentral-latest.json`](#ringcentral-latestjson)
  - [`ringcentral-1.0.39.json`](#ringcentral-1039json)
- [Studio Projects](#studio-projects)
  - [RingCentral Project](#ringcentral-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | RingCentral Connect Platform REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/RingCentral](./Studio%20Projects/RingCentral.project.json) | 22 workflows covering common CRUD automation |

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

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "OAuth2": {
      "client_id": "<your-client-id>",
      "client_secret": "<your-client-secret>",
      "token_url": "https://platform.ringcentral.com/restapi/oauth/token",
      "refresh_url": "",
      "scope": "",
      "token": {
        "access_token": ""
      },
      "authorization_url": "https://platform.ringcentral.com/restapi/oauth/authorize"
    }
  },
  "server": {
    "protocol": "https",
    "host": "platform.ringcentral.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`ringcentral-latest.json`](./OpenAPIs/ringcentral-latest.json) | latest (curated) | 153 | Trimmed to 153 of 312 upstream operations — see breakdown below |
| [`ringcentral-1.0.39.json`](./OpenAPIs/ringcentral-1.0.39.json) | 1.0.39 | 312 | Full spec for RingCentral Connect Platform API 1.0.39 (312 operations). |

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

### `ringcentral-1.0.39.json`

Full, unmodified vendor spec for RingCentral Connect Platform API 1.0.39 (312 operations) — the vendor's complete API surface, preserved as-is. See `ringcentral-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### RingCentral Project

Backed by the **`RingCentral:latest`** Integration Model (see [`ringcentral-latest.json`](./OpenAPIs/ringcentral-latest.json) above). The project contains **22 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Calls | Create Call-Out, Get, Delete Call Session, Hold, Transfer Call Party | Telephony session and call party control |
| Messages | List, Get, Update, Delete Message, Create SMS Message | Message store and SMS |
| Extensions | List, Create, Get, Update, Delete Extension | Extension (user) lifecycle |
| Meetings | List, Create, Get, Update, Delete Meeting | RingCentral Video meeting lifecycle |
| Presence | Get, Update User Presence | Extension presence status |

#### Dependencies

| Dependency | Notes |
|---|---|
| `RingCentral:latest` Integration Model | Import from [`ringcentral-latest.json`](./OpenAPIs/ringcentral-latest.json) before importing the project |
| `RingCentral` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `RingCentral` — update the `adapter_id` value in each workflow task if yours is named differently |
