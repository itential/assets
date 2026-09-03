Twilio is a cloud communications platform providing REST APIs for programmable voice calls, SMS/MMS messaging, conferencing, and phone number provisioning and management.

This project provides OpenAPI specs for automating against Twilio's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`twilio-latest.json`](#twilio-latestjson)
  - [`twilio-1.0.0.json`](#twilio-100json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Twilio REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Twilio | REST API `2010-04-01` |
| Twilio Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Twilio's REST API.

Authentication is HTTP Basic, using your Account SID as the username and Auth Token as the password:

```
Authorization: Basic base64(<AccountSid>:<AuthToken>)
```

Both values are available in the Twilio Console at https://console.twilio.com.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "accountSid_authToken": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.twilio.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`twilio-latest.json`](./OpenAPIs/twilio-latest.json) | latest (curated) | 67 | Actively-maintained spec, trimmed to 67 of 197 upstream operations covering common CRUD for automation — see breakdown below |
| [`twilio-1.0.0.json`](./OpenAPIs/twilio-1.0.0.json) | 1.0.0 | 197 | Full spec for the Twilio REST API `2010-04-01`, version `1.0.0` (197 operations) |

### `twilio-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.0.0`). Trimmed to 67 of 197 upstream operations covering common CRUD for automation. Pull the full spec from Twilio's published API reference at https://www.twilio.com/docs/usage/api if you need something not covered here.

Resources included, by category:

- **Account**: Accounts (list, create sub-accounts), Account (get, update)
- **Addresses**: Addresses (list, create, get, update, delete), Dependent Phone Numbers (list)
- **Applications**: TwiML Applications (list, create, get, update, delete)
- **Available Phone Numbers**: Country list, country detail, Local and Toll-Free number search
- **Balance**: Account balance (get)
- **Calls**: Calls (list, create, get, update, delete/hang up), Call Recordings (list, create, get, update, delete)
- **Conferences**: Conferences (list, get, update), Participants (list, create, get, update, delete)
- **Incoming Phone Numbers**: Provisioned numbers (list, create/buy, get, update, delete/release)
- **Messages**: Messages (list, send, get, update/redact, delete), Message Media (list, get, delete)
- **Outgoing Caller IDs**: Verified caller IDs (list, create, get, update, delete)
- **Queues**: Call Queues (list, create, get, update, delete), Queue Members (list, get, update/dequeue)
- **Recordings**: Account-level Recordings (list, get, delete)

### `twilio-1.0.0.json`

Full, unmodified vendor spec for the Twilio REST API `2010-04-01`, version `1.0.0` (197 operations) — the vendor's complete API surface, preserved as-is. See `twilio-latest.json` above for the curated subset if you just need common CRUD automation.
