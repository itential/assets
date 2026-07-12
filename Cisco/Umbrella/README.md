Cisco Umbrella is a cloud-delivered DNS-layer security service that blocks malicious domains, IPs, and URLs before a connection is ever established. The Destination Lists API manages the allow and block lists used by Umbrella's DNS-layer security policies.

This project provides an OpenAPI spec for automating against the Umbrella Destination Lists API via an Integration Model. See **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Cisco Umbrella Destination Lists REST API OpenAPI spec — `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cisco Umbrella | Destination Lists API v2.0.0 |
| Cisco Umbrella Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Umbrella tenant.

Authentication is OAuth2 Client Credentials:

```
Authorization: Basic <base64(client_key:client_secret)>
```

Obtain a client key and secret from Cisco Umbrella under **Admin > API Keys > Umbrella API**. The token endpoint requires the client credentials as HTTP Basic auth on the Authorization header.

## OpenAPIs

### `cisco_umbrella_destination_lists-latest.json`

Full, unmodified upstream spec (`x-vendor-api-version: 2.0.0`) — already a narrow, single-purpose API covering the complete Destination Lists resource (create/list/get/update/delete destination lists, and add/remove destinations within a list), so no trimming was applied.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`cisco_umbrella_destination_lists-2.0.0.json`](./OpenAPIs/cisco_umbrella_destination_lists-2.0.0.json) | Full spec for Cisco Umbrella Destination Lists API v2.0.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| Cisco Umbrella Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
