6connect Provision is an IP address management (IPAM) and network provisioning platform providing resource allocation, DNS management, and automation workflows.

This project provides the OpenAPI spec for automating against the 6connect Provision REST API via an Integration Model. The `-latest` spec is reviewed and curated for common CRUD automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`6connect_provision-latest.json`](#6connect_provision-latestjson)
  - [`6connect_provision-2.0.0.json`](#6connect_provision-200json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | 6connect Provision REST API OpenAPI spec — `-latest` plus full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| 6connect Provision | 2.0.0 |
| 6connect Provision Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your 6connect Provision instance.

Authentication is HTTP Basic — your 6connect username and password:

```
Authorization: Basic <base64(username:password)>
```

Configure API access in 6connect under **Administration → Users**.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "6connect.com",
    "base_path": "/api/v2"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`6connect_provision-latest.json`](./OpenAPIs/6connect_provision-latest.json) | latest (curated) | 40 | Actively-maintained, curated for common CRUD automation — see breakdown below |
| [`6connect_provision-2.0.0.json`](./OpenAPIs/6connect_provision-2.0.0.json) | 2.0.0 | 40 | Full, unmodified vendor spec |

### `6connect_provision-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2.0.0`, 40 operations). Every operation in the upstream spec is CRUD or a provisioning action on the single `resources` model — there is no separate admin, webhook, or reporting surface to exclude, so nothing was removed.

Operations included, by category:

- **Resources**: List, create, bulk update, query/search, top-of-tree lookup, unassign all IPs
- **Resource (by ID)**: Get, update, delete, clone, get children, get section, get top-of-tree
- **Attributes**: Get, add, update, delete; bulk lookup by section/category
- **Links** (relationships between resources): Get/create/replace/update all links; get/replace/update links by relation; update/delete a specific link
- **Attachments**: List, attach, preview, download, delete
- **Backup**: List backups, trigger a backup
- **Provisioning actions**: Push a resource + poll push status; execute a named action + poll action status

### `6connect_provision-2.0.0.json`

Full, unmodified vendor spec for 6connect Provision 2.0.0 (40 operations) — the vendor's complete API surface, preserved as-is. See `6connect_provision-latest.json` above for the curated subset if you just need common CRUD automation.
