# TigerConnect

TigerConnect is a clinical communication and collaboration platform used by healthcare organizations for secure, HIPAA-compliant messaging between care team members, patients, and connected systems. Its REST API manages users, groups, organizations, messages, roster entries, and entity metadata.

## Table of Contents

- [TigerConnect](#tigerconnect)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`tigerconnect-latest.json`](#tigerconnect-latestjson)
    - [`tigerconnect-2.json`](#tigerconnect-2json)
  - [Studio Projects](#studio-projects)
    - [TigerConnect Project](#tigerconnect-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | TigerConnect REST API OpenAPI specs — curated `-latest` plus the full spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 31 workflows in 7 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| TigerConnect | Any account with API access enabled |
| `TigerConnect:latest` Integration Model | Required to build automation against the OpenAPI specs |
| A TigerConnect API Key and API Secret | Used as the HTTP Basic Auth username/password — see **Integration Configuration** below |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration using the API Key as the username and the API Secret as the password.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "developer.tigertext.me",
    "port": "443"
  },
  "authentication": {
    "BasicAuth": {
      "username": "<API Key>",
      "password": "<API Secret>"
    }
  }
}
```

TigerConnect accepts a static `Authorization: Basic` header built from the API Key and API Secret. There's no login call or token refresh involved — the credentials are sent as-is on every request.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`tigerconnect-latest.json`](./OpenAPIs/tigerconnect-latest.json) | latest (curated) | 31 | Actively-maintained, trimmed to 31 of 47 upstream operations covering common CRUD for automation — see breakdown below |
| [`tigerconnect-2.json`](./OpenAPIs/tigerconnect-2.json) | 2 | 47 | Full spec across Users, Groups, Organizations, Messages, Roster, Metadata, Search, and the Roles Scheduler integration |

### `tigerconnect-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2`). Trimmed to 31 of 47 upstream operations, covering common CRUD for automation.

Resources included, by category:

- **Users**: Create/update, get, and lookup users; add/remove a user's organization membership; get, assign, and remove a user's organization roles
- **Groups**: Create/get/update/delete groups; add/remove group members
- **Organizations**: Create/get/update/delete organizations; create security groups (custom directories)
- **Messages**: Send, get, and delete messages; get a message's attachment; set and get message delivery/read status
- **Roster**: Add/get/remove entries on a user's recent conversation list
- **Metadata**: Set and get key/value metadata on a user or group
- **Search**: Search accounts, groups, and distribution lists

### `tigerconnect-2.json`

Full spec (47 operations) across Users, Groups, Organizations, Messages, Roster, Metadata, Search, plus the Roles Scheduler integration (config, ID mapping, and webhook management) and message typing indicators and unread-count lookups.

---

## Studio Projects

### TigerConnect Project

Backed by the **`TigerConnect:latest`** Integration Model (see [`tigerconnect-latest.json`](./OpenAPIs/tigerconnect-latest.json) above). The project contains **31 workflows** organized into **7 folders**, one atomic workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `Get Group`, `Send Message`).

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Users | Create Or Update, Get, Lookup, Add To Organization, Remove From Organization, Get Roles, Assign Role, Remove Role | User and role administration |
| Groups | Create, Get, Update, Delete, Add Members, Remove Members | Group CRUD and membership |
| Organizations | Create, Get, Update, Delete, Create Security Groups | Organization CRUD |
| Messages | Send, Get, Delete, Get Attachment, Set Status, Get Status | Messaging lifecycle |
| Roster | Add Entry, Get, Remove Entry | Recent conversation list management |
| Metadata | Set, Get | Entity metadata management |
| Search | Search | Directory search |

#### Dependencies

| Dependency | Notes |
|---|---|
| `TigerConnect:latest` Integration Model | Import from [`tigerconnect-latest.json`](./OpenAPIs/tigerconnect-latest.json) before importing the project |
| `TigerConnect` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `TigerConnect` — update the `adapter_id` value in each workflow task if yours is named differently |
