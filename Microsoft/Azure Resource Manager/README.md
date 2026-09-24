# Azure Resource Manager

Azure Resource Manager is the deployment and management layer for Azure, exposing resource groups, generic resources, resource providers, tags, deployments, and subscriptions through the Azure Resource Manager REST API.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`azure_resource_manager-latest.json`](#azure_resource_manager-latestjson)
  - [`azure_resource_manager_resources-2022-09-01.json`](#azure_resource_manager_resources-2022-09-01json)
  - [`azure_resource_manager_deployments-2022-09-01.json`](#azure_resource_manager_deployments-2022-09-01json)
  - [`azure_resource_manager_subscriptions-2022-12-01.json`](#azure_resource_manager_subscriptions-2022-12-01json)
- [Studio Projects](#studio-projects)
  - [Azure Resource Manager Project](#azure-resource-manager-project)
    - [Folder Structure](#folder-structure)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Azure Resource Manager OpenAPI specs — curated `-latest` plus the full Resources, Deployments, and Subscriptions specs it was drawn from |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing 32 workflows in 7 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Azure Resource Manager | `management.azure.com` (Azure Public Cloud) |
| Microsoft Entra ID app registration | Client credentials grant with a role assignment (e.g. Contributor) scoped to the subscriptions/resource groups being automated |

## Integration Configuration

Import `azure_resource_manager-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Azure Resource Manager.

Authentication is native OAuth2 client credentials against Microsoft Entra ID:

| Field | Value |
|---|---|
| `client_id` | Application (client) ID from your Microsoft Entra app registration |
| `client_secret` | Client secret from that app registration |
| `token_url` | `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token` (substitute your tenant ID) |
| `scope` | `https://management.azure.com/.default` |

The app registration needs a role assignment (e.g. Contributor, or a narrower custom role) on the subscriptions or resource groups the workflows will manage.

Every operation takes an `api-version` query parameter; the spec sets it per operation to the upstream API version it was drawn from (`2022-09-01` for resource groups, resources, providers, tags, and deployments; `2022-12-01` for subscriptions and tenants) — no need to add it yourself.

Azure Resource Manager's own paths already carry their full absolute route (some start with `/subscriptions/...`, others with `/providers/...`, `/tenants`, or `/{resourceId}` directly) — there's no single common prefix to factor out, so `base_path` stays empty. The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "azureADClientCredentials": {
      "client_id": "<your-client-id>",
      "client_secret": "<your-client-secret>",
      "token_url": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
      "refresh_url": "",
      "scope": "https://management.azure.com/.default",
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

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`azure_resource_manager-latest.json`](./OpenAPIs/azure_resource_manager-latest.json) | latest (curated) | 32 | Common CRUD automation across Resource Groups, Resources, Providers, Tags, Deployments, and Subscriptions — see breakdown below |
| [`azure_resource_manager_resources-2022-09-01.json`](./OpenAPIs/azure_resource_manager_resources-2022-09-01.json) | 2022-09-01 | 40 | Full upstream Resource Manager spec (resource groups, generic resources, providers, tags) |
| [`azure_resource_manager_deployments-2022-09-01.json`](./OpenAPIs/azure_resource_manager_deployments-2022-09-01.json) | 2022-09-01 | 55 | Full upstream Deployments spec (tenant/management-group/subscription/resource-group-scoped deployments and deployment operations) |
| [`azure_resource_manager_subscriptions-2022-12-01.json`](./OpenAPIs/azure_resource_manager_subscriptions-2022-12-01.json) | 2022-12-01 | 7 | Full upstream Subscriptions spec (subscriptions, locations, tenants) |

### `azure_resource_manager-latest.json`

Trimmed to 32 of the several hundred upstream operations across Microsoft's official Resource Manager, Deployments, and Subscriptions specs, focused on common automation:

- **Resource Groups**: list, get, create/update, update, delete
- **Resources**: list by resource group, list by subscription, get/create-or-update/update/delete by resource ID
- **Providers**: list, get, register, unregister
- **Tags**: get, create/update, update, and delete tags at a scope (subscription, resource group, or resource)
- **Deployments**: list by resource group, get, create/update, delete, cancel, validate, export template
- **Deployment Operations**: list, get
- **Subscriptions and Tenants**: list subscriptions, get a subscription, list subscription locations, list tenants

Converted from Swagger 2.0 to OpenAPI 3.0. Consolidated into a single `azureADClientCredentials` security scheme and a single `https://management.azure.com` server entry (the upstream specs already define an empty `basePath`, so nothing was discarded in that conversion).

### `azure_resource_manager_resources-2022-09-01.json`

Microsoft's official `ResourceManagementClient` spec (Swagger 2.0, as published), covering resource groups, generic resources, resource providers, and tags in full, including tenant/management-group scope variants and the classic tag-name/tag-value model not carried into the curated file.

### `azure_resource_manager_deployments-2022-09-01.json`

Microsoft's official `DeploymentsClient` spec (Swagger 2.0, as published), covering deployments and deployment operations at tenant, management group, subscription, and resource group scope, including `whatIf` and `calculateTemplateHash`, neither of which are carried into the curated file.

### `azure_resource_manager_subscriptions-2022-12-01.json`

Microsoft's official `SubscriptionClient` spec (Swagger 2.0, as published), covering subscriptions, locations, tenants, and a couple of subscription-level checks (`checkResourceName`, `checkZonePeers`) not carried into the curated file.

## Studio Projects

### Azure Resource Manager Project

Backed by the **`Azure Resource Manager:latest`** Integration Model (see [`azure_resource_manager-latest.json`](./OpenAPIs/azure_resource_manager-latest.json) above). The project contains **32 workflows** organized into **7 folders**, one workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Resource Groups | 5 | List, get, create/update, update, delete |
| Resources | 6 | List by resource group, list by subscription, get/create-or-update/update/delete by resource ID |
| Providers | 4 | List, get, register, unregister |
| Tags | 4 | Get, create/update, update, delete tags at a scope |
| Deployments | 7 | List, get, create/update, delete, cancel, validate, export template |
| Deployment Operations | 2 | List, get |
| Subscriptions and Tenants | 4 | List subscriptions, get a subscription, list locations, list tenants |
