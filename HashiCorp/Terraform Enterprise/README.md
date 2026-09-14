# Terraform Enterprise

HashiCorp Terraform Enterprise (self-hosted) and HCP Terraform (SaaS) share the same v2 API — organizations, workspaces, runs, plans, applies, state versions, variables, and teams for managing Terraform-driven infrastructure as code.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`hashicorp_terraform_enterprise-latest.json`](#hashicorp_terraform_enterprise-latestjson)
  - [`hashicorp_terraform_enterprise-ab4697be.json`](#hashicorp_terraform_enterprise-ab4697bejson)
- [Studio Projects](#studio-projects)
  - [HashiCorp Terraform Enterprise Project](#hashicorp-terraform-enterprise-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Terraform Enterprise / HCP Terraform API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/HashiCorp Terraform Enterprise](./Studio%20Projects/HashiCorp%20Terraform%20Enterprise.project.json) | 35 workflows covering organization/team membership, workspace CRUD, run/plan/apply lifecycle, workspace variables, and state versions |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| HCP Terraform / Terraform Enterprise | v2 API |
| `HashiCorp Terraform Enterprise` Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Terraform Enterprise instance or HCP Terraform.

Authentication is a static bearer token (a user, team, or organization API token) on the `Authorization` header:

```
Authorization: Bearer <your-terraform-api-token>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearerAuth": {
      "value": "<your-terraform-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "app.terraform.io",
    "base_path": "/api/v2"
  }
}
```

Use `app.terraform.io` for HCP Terraform, or your self-hosted Terraform Enterprise hostname.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`hashicorp_terraform_enterprise-latest.json`](./OpenAPIs/hashicorp_terraform_enterprise-latest.json) | latest (curated) | 35 | Trimmed to 35 of 414 upstream operations — see breakdown below |
| [`hashicorp_terraform_enterprise-ab4697be.json`](./OpenAPIs/hashicorp_terraform_enterprise-ab4697be.json) | ab4697be | 414 | Full spec, published directly by HashiCorp at `app.terraform.io/openapi/stable.json` |

### `hashicorp_terraform_enterprise-latest.json`

Actively-maintained spec (`x-vendor-api-version: ab4697be`). Trimmed to 35 of 414 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Organizations**: list, get
- **Organization Memberships**: list, create (invite), get, delete
- **Teams**: list, create, get, update, delete
- **Workspaces**: list, create, get (by ID or name), update, delete, lock, unlock
- **Runs**: create (trigger), get, list (per workspace), apply
- **Plans and Applies**: get plan, get a run's plan, get apply
- **Variables**: list, create, get, update, delete (workspace-scoped)
- **State Versions**: get current, list, get, list outputs

Long tails dropped from the upstream surface include: Stacks (HCP Terraform's newer deployment model), policy sets/policy checks/policy evaluations, SSH keys, agent pools/agents, VCS/OAuth/GitHub App integrations, registry modules, SAML/SCIM/admin settings, audit trails, notification configurations, run triggers, assessments, cost estimates, and configuration version upload/download.

### `hashicorp_terraform_enterprise-ab4697be.json`

Full spec as published by HashiCorp (414 operations). The vendor labels this spec's `info.version` with a build identifier (`ab4697be`) rather than a semantic version, since it's generated continuously from the live API rather than tied to a dated release.

## Studio Projects

### HashiCorp Terraform Enterprise Project

Backed by the **`HashiCorp Terraform Enterprise:latest`** Integration Model (see [`hashicorp_terraform_enterprise-latest.json`](./OpenAPIs/hashicorp_terraform_enterprise-latest.json) above). The project contains **35 workflows** organized into **8 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Organizations | List Organizations, Get Organization | Organization lookup |
| Organization Memberships | List Organization Memberships, Create Organization Membership, Get Organization Membership, Delete Organization Membership | Membership/invite management |
| Teams | List Teams, Create Team, Get Team, Update Team, Delete Team | Team CRUD |
| Workspaces | List Workspaces, Create Workspace, Get Workspace By Name, Get Workspace, Update Workspace, Delete Workspace, Lock Workspace, Unlock Workspace | Workspace CRUD and locking |
| Runs | Create Run, Get Run, List Workspace Runs, Apply Run | Run lifecycle |
| Plans and Applies | Get Plan, Get Run Plan, Get Apply | Plan/apply inspection |
| Variables | List Workspace Variables, Create Workspace Variable, Get Workspace Variable, Update Workspace Variable, Delete Workspace Variable | Workspace variable CRUD |
| State Versions | Get Current State Version, List State Versions, Get State Version, List State Version Outputs | State version reads |

#### Dependencies

| Dependency | Notes |
|---|---|
| `HashiCorp Terraform Enterprise:latest` Integration Model | Import from [`hashicorp_terraform_enterprise-latest.json`](./OpenAPIs/hashicorp_terraform_enterprise-latest.json) before importing the project |
| `HashiCorp Terraform Enterprise` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `HashiCorp Terraform Enterprise` — update the `adapter_id` value in each workflow task if yours is named differently |
