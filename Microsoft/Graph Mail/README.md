Microsoft Graph Mail is the Microsoft Graph API surface for reading and sending mail (Outlook / Exchange Online) using application (client credentials) permissions — no signed-in user required.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`microsoft_graph_mail-latest.json`](#microsoft_graph_mail-latestjson)
  - [`microsoft_graph_mail-v1.0.json`](#microsoft_graph_mail-v10json)
- [Studio Projects](#studio-projects)
  - [Microsoft Graph Mail Project](#microsoft-graph-mail-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Microsoft Graph Mail OpenAPI spec — `-latest` plus the full app-only-compatible mail surface |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 12 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Microsoft Graph API | v1.0 |
| Microsoft Graph Mail Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Microsoft Graph tenant.

Authentication is native OAuth2 client credentials:

| Field | Value |
|---|---|
| `client_id` | Application (client) ID from your Azure AD app registration |
| `client_secret` | Client secret from that app registration |
| `token_url` | `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token` (substitute your tenant ID) |
| `scope` | `https://graph.microsoft.com/.default` |

The app registration needs the `Mail.ReadWrite` and `Mail.Send` application permissions (admin-consented), scoped to specific mailboxes via an application access policy if you don't want tenant-wide mail access.

All operations in this spec use the `/users/{user-id}/...` endpoints, not `/me/...` — application permissions have no signed-in user context, so `user-id` (a mailbox's user ID or UPN) must be supplied on every call.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`microsoft_graph_mail-latest.json`](./OpenAPIs/microsoft_graph_mail-latest.json) | latest (curated) | 12 | Read and send mail for network-automation workflows — see breakdown below |
| [`microsoft_graph_mail-v1.0.json`](./OpenAPIs/microsoft_graph_mail-v1.0.json) | v1.0 | 137 | Full application-permission-compatible mail surface for Microsoft Graph v1.0 |

### `microsoft_graph_mail-latest.json`

Trimmed to 12 of the 137 application-permission-compatible upstream mail operations, focused on reading and sending mail from an automation workflow:

- **Send**: `POST /users/{user-id}/sendMail` — send a message, optionally saving a copy to Sent Items
- **Messages**: list, get, update (mark read/flag/etc.), delete, move, and reply to messages
- **Attachments**: list a message's attachments, get a single attachment
- **Mail folders**: list folders, get a folder, list a folder's messages

Excluded from this curated file, and available in the full spec below: message rules, mailbox settings, and Outlook master categories (Outlook-client configuration, not automation targets); nested child folders; copy/permanentDelete/forward/replyAll (redundant with move/delete/reply); the two-step createReply/createForward/createReplyAll draft variants; and OData introspection endpoints (`$count`, `delta()`, `$value`, extensions, `createUploadSession`). Also dropped on every kept operation: the optional OData query parameters (`$select`, `$filter`, `$expand`, `$orderby`, `$top`, `$skip`, `$count`) — every operation works fine without them, returning unfiltered/unshaped results.

### `microsoft_graph_mail-v1.0.json`

Every application-permission-compatible mail operation under `/users/{user-id}/messages`, `/mailFolders`, `/sendMail`, `/mailboxSettings`, and `/outlook/masterCategories` — not the whole Graph API, and not the `/me/...` delegated-user endpoints, which require a signed-in user context that doesn't exist under client-credentials auth. See `microsoft_graph_mail-latest.json` above for the curated subset if you just need read/send mail automation.

## Studio Projects

### Microsoft Graph Mail Project

Backed by the **`Microsoft Graph Mail:latest`** Integration Model (see [`microsoft_graph_mail-latest.json`](./OpenAPIs/microsoft_graph_mail-latest.json) above). The project contains **12 workflows** organized into **4 folders**.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Send | 1 | Send a message |
| Messages | 6 | List, get, update, delete, move, and reply to messages |
| Attachments | 2 | List a message's attachments, get a single attachment |
| Mail Folders | 3 | List folders, get a folder, list a folder's messages |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Microsoft Graph Mail:latest` Integration Model | Import from [`microsoft_graph_mail-latest.json`](./OpenAPIs/microsoft_graph_mail-latest.json) before importing the project |
| `Microsoft Graph Mail` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Microsoft Graph Mail` — update the `adapter_id` value in each workflow task if yours is named differently |
