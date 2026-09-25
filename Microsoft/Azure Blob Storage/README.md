# Azure Blob Storage

Azure Blob Storage is Microsoft's data-plane object storage service for unstructured data, exposing container and blob resources over a REST API scoped to a single storage account.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`azure_blob_storage-latest.json`](#azure_blob_storage-latestjson)
  - [`azure_blob_storage-2026-10-06.json`](#azure_blob_storage-2026-10-06json)
- [Studio Projects](#studio-projects)
  - [Azure Blob Storage Project](#azure-blob-storage-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Azure Blob Storage REST API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing 12 workflows in 2 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Azure Blob Storage | Data-plane REST API |
| Microsoft Entra ID app registration | Application (client credentials) permissions on the storage account |

## Integration Configuration

Import `azure_blob_storage-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your storage account.

Authentication is native OAuth2 client credentials against Microsoft Entra ID:

| Field | Value |
|---|---|
| `client_id` | Application (client) ID from your Entra ID app registration |
| `client_secret` | Client secret from that app registration |
| `token_url` | `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token` (substitute your tenant ID) |
| `scope` | `https://storage.azure.com/.default` |

The app registration needs an RBAC role assignment on the storage account (or container) covering the operations you automate, e.g. **Storage Blob Data Contributor** for container and blob CRUD.

Azure Blob Storage has no generic hostname — each storage account gets its own blob endpoint, `{account}.blob.core.windows.net`. Since this platform builds `servers[0]` purely from the integration instance's `server.protocol`/`server.host`/`server.port` fields, set `server.host` to your full account-specific hostname (e.g. `mystorageaccount.blob.core.windows.net`), not a placeholder.

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
    "host": "mystorageaccount.blob.core.windows.net"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`azure_blob_storage-latest.json`](./OpenAPIs/azure_blob_storage-latest.json) | latest (curated) | 12 | Common CRUD across containers and blobs — see breakdown below |
| [`azure_blob_storage-2026-10-06.json`](./OpenAPIs/azure_blob_storage-2026-10-06.json) | 2026-10-06 | 71 | Full Microsoft-published data-plane spec |

### `azure_blob_storage-latest.json`

Trimmed to 12 of 71 upstream operations, covering:

- **Containers**: create, get properties, delete, set metadata, list containers, list blobs in a container
- **Blobs**: put (upload), get (download), delete, get properties, set properties (HTTP headers), set metadata

Everything else in the full spec — leases, snapshots, copy operations, tiering, immutability policies, legal holds, tags, the batch/query APIs, page blob and append blob operations, and account/service-level statistics and properties — is out of scope for this curated file.

Authentication is OAuth2 client credentials against Microsoft Entra ID, scope `https://storage.azure.com/.default` — see Integration Configuration above.

### `azure_blob_storage-2026-10-06.json`

The full spec as published by Microsoft in its official [`azure-rest-api-specs`](https://github.com/Azure/azure-rest-api-specs) repository (`specification/storage/data-plane/Microsoft.BlobStorage`), unmodified — Swagger 2.0, with operations addressed by query-string-qualified path keys (e.g. `/{containerName}?restype=container&comp=metadata`) rather than a flat method list. See `azure_blob_storage-latest.json` above for the curated OpenAPI 3.x subset used by the Studio Project.

## Studio Projects

### Azure Blob Storage Project

Backed by the **`Azure Blob Storage:latest`** Integration Model (see [`azure_blob_storage-latest.json`](./OpenAPIs/azure_blob_storage-latest.json) above). The project contains **12 workflows** organized into **2 folders**, one workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Containers | 6 | Create/get properties/delete/set metadata for a container; list containers; list blobs in a container |
| Blobs | 6 | Put (upload)/get (download)/delete a blob; get properties; set properties (HTTP headers); set metadata |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Azure Blob Storage:latest` Integration Model | Import from [`azure_blob_storage-latest.json`](./OpenAPIs/azure_blob_storage-latest.json) before importing the project |
| `Azure Blob Storage` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Azure Blob Storage` — update the `adapter_id` value in each workflow task if yours is named differently |
