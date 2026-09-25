# Azure Kubernetes Service

Azure Kubernetes Service (AKS) is Microsoft's managed Kubernetes offering on Azure, handling control plane operations, node pool scaling, and cluster lifecycle so workloads can run on Kubernetes without operating the underlying control plane.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`azure_kubernetes_service-latest.json`](#azure_kubernetes_service-latestjson)
  - [`azure_kubernetes_service-2026-06-01.json`](#azure_kubernetes_service-2026-06-01json)
- [Studio Projects](#studio-projects)
  - [Azure Kubernetes Service Project](#azure-kubernetes-service-project)
    - [Folder Structure](#folder-structure)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Azure Kubernetes Service management API OpenAPI specs — curated `-latest` plus the full vendor-published spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing 15 workflows in 2 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Azure Kubernetes Service API | 2026-06-01 |
| Microsoft Entra ID app registration | Application permissions (client credentials) with an Azure role assignment over the target subscription/resource group |

## Integration Configuration

Import `azure_kubernetes_service-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Azure Resource Manager.

Authentication is native OAuth2 client credentials against Microsoft Entra ID:

| Field | Value |
|---|---|
| `client_id` | Application (client) ID from your Entra ID app registration |
| `client_secret` | Client secret from that app registration |
| `token_url` | `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token` (substitute your tenant ID) |
| `scope` | `https://management.azure.com/.default` |

The app registration's service principal needs an Azure role assignment (e.g. Azure Kubernetes Service Contributor Role, Azure Kubernetes Service Cluster Admin/User Role, or Contributor) scoped to the subscriptions/resource groups the workflows will operate against.

Every operation's path in the spec already includes the full `/subscriptions/{subscriptionId}/...` resource path, so the integration instance needs no `base_path` — leave it empty.

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
    "host": "management.azure.com",
    "base_path": ""
  }
}
```

Every operation requires an `api-version` query parameter; it defaults to `2026-06-01`, the API version this spec was built from.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`azure_kubernetes_service-latest.json`](./OpenAPIs/azure_kubernetes_service-latest.json) | latest (curated) | 15 | Managed Cluster CRUD/lifecycle, cluster credential retrieval, and Agent Pool CRUD — see breakdown below |
| [`azure_kubernetes_service-2026-06-01.json`](./OpenAPIs/azure_kubernetes_service-2026-06-01.json) | 2026-06-01 | 69 | Full vendor-published Managed Clusters API surface |

### `azure_kubernetes_service-latest.json`

Trimmed to 15 of the upstream spec's 69 operations. Resources included, by category:

- **Managed Clusters**: list by subscription, list by resource group, get, create/update, update tags, delete, start, stop
- **Cluster Credentials**: list cluster admin credential, list cluster user credential, list cluster monitoring user credential
- **Agent Pools**: list, get, create/update, delete

### `azure_kubernetes_service-2026-06-01.json`

Full Managed Clusters API surface as published by Microsoft in the [`azure-rest-api-specs`](https://github.com/Azure/azure-rest-api-specs) repo (`specification/containerservice/resource-manager/Microsoft.ContainerService/aks/stable/2026-06-01/managedClusters.json`), preserved as originally published (Swagger 2.0). Beyond the curated 15, this includes maintenance configurations, managed namespaces, node image/upgrade profiles, private endpoint connections and private link resources, trusted access role bindings, identity bindings, snapshots, machines, service mesh/mesh revision profiles, run-command, certificate/service-account-key rotation, service principal/AAD profile resets, and outbound network dependency endpoints.

## Studio Projects

### Azure Kubernetes Service Project

Backed by the **`Azure Kubernetes Service:latest`** Integration Model (see [`azure_kubernetes_service-latest.json`](./OpenAPIs/azure_kubernetes_service-latest.json) above). The project contains **15 workflows** organized into **2 folders**, one workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Managed Clusters | 11 | Cluster list/get/create-update/update-tags/delete, start, stop; list admin/user/monitoring-user credentials |
| Agent Pools | 4 | Agent pool list/get/create-update/delete |
