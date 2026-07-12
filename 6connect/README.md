6connect Provision is an IP address management (IPAM) and network provisioning platform providing resource allocation, DNS management, and automation workflows.

This project provides the OpenAPI spec for automating against the 6connect Provision REST API via an Integration Model. The `-latest` spec is the full, unmodified vendor spec — it is already scoped to a single resource domain, so no trimming was needed.

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

## OpenAPIs

### `6connect_provision-latest.json` (full spec, untouched)

Full, unmodified vendor spec (`x-vendor-api-version: 2.0.0`). This is already a narrow, single-purpose API covering resource provisioning (create/read/update/delete, attributes, links, attachments, and tree/backup operations for provisioned resources) — no operations were removed.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`6connect_provision-2.0.0.json`](./OpenAPIs/6connect_provision-2.0.0.json) | Full spec for 6connect Provision 2.0.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| 6connect Provision Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
