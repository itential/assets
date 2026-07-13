Slack is a business messaging platform for team communication, offering channels, direct messages, file sharing, and an extensible app/bot platform. The Slack Web API is Slack's primary HTTP API for interacting with a workspace programmatically — sending messages, managing channels, looking up users, and more.

This project provides OpenAPI specs for automating against the Slack Web API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Slack Web API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Slack Web API | 1.7.0 (see OpenAPIs below for exact spec versions available) |
| Slack Web API Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Slack workspace.

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <your-slack-token>
```

Use a Slack bot token (`xoxb-*`) for bot operations, or a user token (`xoxp-*`) for user-delegated actions. Generate one from your Slack app configuration at https://api.slack.com/apps.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`slack_web_api-latest.json`](./OpenAPIs/slack_web_api-latest.json) | latest (curated) | Trimmed to 61 of 174 upstream operations — see breakdown below |
| [`slack_web_api-1.7.0.json`](./OpenAPIs/slack_web_api-1.7.0.json) | 1.7.0 | Full spec for the Slack Web API, version 1.7.0. |

### `slack_web_api-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.7.0`). Trimmed to 61 of 174 upstream operations covering common CRUD for automation. The full upstream spec includes workspace admin tooling (`admin.*`, `apps.*`), app-development/UI features (`views.*`, `dialog.open`), the legacy Calls, Do Not Disturb, Stars, and Workflow Steps modules, OAuth flows, and other niche or internal-tooling endpoints — none of those are included here. Pull the full spec below if you need one of the excluded areas.

Resources included, by category:

- **Messaging**: Post, update, delete, and schedule messages; retrieve permalinks; post ephemeral/"me" messages (`chat.*`)
- **Conversations**: Create, list, get info/history/replies/members, invite, kick, join, leave, archive/unarchive, rename, set purpose/topic, open/close, mark read (`conversations.*`)
- **Users**: List, get info, look up by email, list a user's conversations, presence, identity, and profile get/set (`users.*`)
- **Files**: Upload, list, get info, and delete (`files.*`)
- **Reactions**: Add, remove, get, and list emoji reactions (`reactions.*`)
- **Pins**: Add, remove, and list pinned items (`pins.*`)
- **User Groups**: Create, list, update, enable/disable, and manage membership (`usergroups.*`)
- **Reminders**: Add, complete, delete, get info, and list (`reminders.*`)
- **Team & Auth**: Basic team info (`team.info`) and token validation (`auth.test`)

This pass also removed 61 per-operation `security` overrides that were exact duplicates of the spec's global `security` block (`botToken`), so `securitySchemes` now has a single, unambiguous global auth definition.
