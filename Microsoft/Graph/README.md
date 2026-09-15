# Microsoft Graph

Microsoft Graph is Microsoft's unified API for Microsoft 365 data and services, covering identity, productivity, and collaboration resources such as Mail, Users, Groups, Calendar, Files, and Microsoft Teams.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`microsoft_graph-latest.json`](#microsoft_graph-latestjson)
  - [`microsoft_graph-v1.0.json`](#microsoft_graph-v10json)
- [Studio Projects](#studio-projects)
  - [Microsoft Graph Project](#microsoft-graph-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Microsoft Graph OpenAPI spec — `-latest` plus the extracted Mail/Users/Groups/Calendar/Files/Teams surface |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 53 workflows in 6 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Microsoft Graph API | v1.0 |
| Microsoft Graph Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Microsoft Graph tenant.

Authentication is native OAuth2 client credentials:

| Field | Value |
|---|---|
| `client_id` | Application (client) ID from your Azure AD app registration |
| `client_secret` | Client secret from that app registration |
| `token_url` | `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token` (substitute your tenant ID) |
| `scope` | `https://graph.microsoft.com/.default` |

The app registration needs application permissions matching the resources you automate (e.g. `Mail.ReadWrite`, `Mail.Send`, `User.ReadWrite.All`, `Group.ReadWrite.All`, `Calendars.ReadWrite`, `Files.ReadWrite.All`, `Channel.ReadWrite.All`, `ChannelMessage.Send`), admin-consented for the tenant. For mail automation, application access policies can scope `Mail.*` permissions to specific mailboxes instead of tenant-wide access.

All operations in this spec use application-permission-compatible endpoints (`/users/{user-id}/...`, `/groups/{group-id}/...`, `/teams/{team-id}/...`), not the `/me/...` delegated-user endpoints — application permissions have no signed-in user context.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-client-id>",
      "client_secret": "<your-client-secret>",
      "token_url": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
      "refresh_url": "",
      "scope": "",
      "token": {
        "access_token": ""
      }
    }
  },
  "server": {
    "protocol": "https",
    "host": "graph.microsoft.com",
    "base_path": "/v1.0"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`microsoft_graph-latest.json`](./OpenAPIs/microsoft_graph-latest.json) | latest (curated) | 53 | Common CRUD automation across Mail, Users, Groups, Calendar/Events, Files, and Teams — see breakdown below |
| [`microsoft_graph-v1.0.json`](./OpenAPIs/microsoft_graph-v1.0.json) | v1.0 | 988 | Full extracted Mail/Users/Groups/Calendar/Files/Teams surface for Microsoft Graph v1.0 |

### `microsoft_graph-latest.json`

Trimmed to 53 of 988 upstream operations, focused on common automation across six resource areas:

- **Mail**: send a message; list, get, update (mark read/flag/etc.), delete, move, and reply to messages; list/get a message's attachments; list mail folders, get a folder, list a folder's messages
- **Users**: list, create, get, update, delete
- **Groups**: list, create, get, update, delete; list/add/remove group members
- **Calendar and Events**: list, create, get, update, delete events; accept, decline, cancel an event
- **Files**: get a user's drive, get a drive, get a drive's root folder, list/get/create/update/delete drive items, download/upload drive item content
- **Teams**: get a team; list/create/get/update/delete channels; list/send/get channel messages; reply to a channel message

Excluded from this curated file, and available in the full spec below: message rules, mailbox settings, and Outlook master categories (Outlook-client configuration, not automation targets); nested child mail folders; copy/permanentDelete/forward/replyAll (redundant with move/delete/reply); the two-step createReply/createForward/createReplyAll draft variants; OData introspection endpoints (`$count`, `delta()`, `$value`, `$ref` type-cast variants, extensions, `createUploadSession`); calendar sharing permissions and calendar groups; event attachments, extensions, and recurring-instance expansion; drive item versions, permissions, thumbnails, and sensitivity labels; Teams primary-channel duplicates of the channel surface, channel tabs, shared channels, and message reactions/soft-delete; user/group directory administration (license assignment, password reset, membership checks, sign-in session revocation); and Excel workbook automation under drive items (charts, worksheets, tables, ranges), which is out of scope for this product. Also dropped on every kept operation: the optional OData query parameters (`$select`, `$filter`, `$expand`, `$orderby`, `$top`, `$skip`, `$count`, `$search`) — every operation works fine without them, returning unfiltered/unshaped results.

### `microsoft_graph-v1.0.json`

The application-permission-compatible operations under Mail (`/users/{user-id}/messages`, `/mailFolders`, `/sendMail`, `/mailboxSettings`, `/outlook/masterCategories`), Users, Groups, Calendar/Events, Files (drives/driveItems), and Teams (channels/chat messages), mechanically extracted from Microsoft's official [`msgraph-metadata`](https://github.com/microsoftgraph/msgraph-metadata) v1.0 OpenAPI description (`openapi/v1.0/openapi.yaml`) by selecting operations tagged under those resource areas — not the whole Graph API (which spans over 11,000 paths across every Microsoft 365 workload), and not the `/me/...` delegated-user endpoints. Excel workbook operations under drive items were dropped even from this full extraction, since they're a distinct automation surface (spreadsheet manipulation, not file/drive management) rather than an omission specific to this product. See `microsoft_graph-latest.json` above for the curated subset if you just need common CRUD automation.

## Studio Projects

### Microsoft Graph Project

Backed by the **`Microsoft Graph:latest`** Integration Model (see [`microsoft_graph-latest.json`](./OpenAPIs/microsoft_graph-latest.json) above). The project contains **53 workflows** organized into **6 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Users | 5 | List, create, get, update, and delete users |
| Groups | 8 | List, create, get, update, and delete groups; list, add, and remove group members |
| Calendar and Events | 8 | List, create, get, update, and delete events; accept, decline, and cancel an event |
| Files | 10 | Get a user's drive, get a drive, get a drive's root folder, list/get/create/update/delete drive items, download/upload drive item content |
| Teams | 10 | Get a team; list, create, get, update, and delete channels; list, send, and get channel messages; reply to a channel message |
| Mail | 12 | Send a message; list, get, update, delete, move, and reply to messages; list a message's attachments, get a single attachment; list mail folders, get a folder, list a folder's messages |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Microsoft Graph:latest` Integration Model | Import from [`microsoft_graph-latest.json`](./OpenAPIs/microsoft_graph-latest.json) before importing the project |
| `Microsoft Graph` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Microsoft Graph` — update the `adapter_id` value in each workflow task if yours is named differently |
