# Rancher

Rancher is a multi-cluster Kubernetes management platform from SUSE, providing centralized cluster provisioning, RBAC, and workload management across on-prem and cloud Kubernetes clusters through a management API.

This project provides OpenAPI specs for automating against the Rancher v3 API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for cluster and workload automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`rancher-latest.json`](#rancher-latestjson)
  - [`rancher-2.10.0.json`](#rancher-2100json)
- [Studio Projects](#studio-projects)
  - [`Rancher.project.json`](#rancherprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Rancher v3 API OpenAPI specs — curated `-latest` plus a full dated reference spec |
| [Studio Projects/Rancher.project.json](./Studio%20Projects/Rancher.project.json) | 35 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Rancher | 2.10 (see OpenAPIs below for exact spec version available) |
| Rancher Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Authentication is a bearer token in the `Authorization` header. Generate an API key under **User Avatar > API & Keys** in the Rancher UI — the token is the access key and secret key concatenated with a colon:

```
Authorization: Bearer <access-key>:<secret-key>
```

The base path for every resource is `/v3` — this platform doesn't apply any path in the OpenAPI spec itself, so it must be set explicitly in the instance's `server.base_path` field.

### Connection Properties

```json
{
  "authentication": {
    "tokenAuth": {
      "value": "Bearer <access-key>:<secret-key>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-rancher-host>",
    "port": "443",
    "base_path": "/v3"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`rancher-latest.json`](./OpenAPIs/rancher-latest.json) | latest (curated) | 35 | Trimmed to 35 of 49 upstream operations covering common CRUD for cluster and workload automation — see breakdown below |
| [`rancher-2.10.0.json`](./OpenAPIs/rancher-2.10.0.json) | 2.10.0 | 49 | Full reference spec covering the Rancher v3 management API surface |

### `rancher-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.10.0`). Trimmed to 35 of 49 upstream operations.

Resources included, by category:

- **Clusters**: List, Create, Get, Update, Delete
- **Projects**: List, Create, Get, Update, Delete
- **Namespaces**: List, Create, Get, Update, Delete
- **Workloads**: List, Create, Get, Update, Delete (deployments, stateful sets, daemon sets, jobs, and cron jobs, scoped to a project)
- **Users**: List, Create, Get, Update, Delete
- **Node Templates**: List, Create, Get, Update, Delete
- **Node Pools**: List, Create, Get, Update, Delete

### `rancher-2.10.0.json`

Full reference spec (49 operations) — adds Cluster Role Template Bindings, Project Role Template Bindings, Role Templates, Settings, and Node Drivers on top of everything in `rancher-latest.json`.

## Studio Projects

### `Rancher.project.json`

One folder per resource, each with a List/Create/Get/Update/Delete workflow built on `rancher-latest.json`'s Integration Model.

Every workflow's adapter task is wired to the Integration instance name `Rancher`. After importing, either name your Integration instance `Rancher`, or update the `adapter_id` value in each workflow task to match your own instance name.

**Clusters**

| Workflow | Scope |
|---|---|
| List Clusters | Get a list of cluster objects |
| Create Cluster | Create a cluster object |
| Get Cluster | Get a cluster object by ID |
| Update Cluster | Update a cluster object by ID |
| Delete Cluster | Delete a cluster object by ID |

**Projects**

| Workflow | Scope |
|---|---|
| List Projects | Get a list of project objects |
| Create Project | Create a project object |
| Get Project | Get a project object by ID |
| Update Project | Update a project object by ID |
| Delete Project | Delete a project object by ID |

**Namespaces**

| Workflow | Scope |
|---|---|
| List Namespaces | Get a list of namespace objects |
| Create Namespace | Create a namespace object |
| Get Namespace | Get a namespace object by ID |
| Update Namespace | Update a namespace object by ID |
| Delete Namespace | Delete a namespace object by ID |

**Users**

| Workflow | Scope |
|---|---|
| List Users | Get a list of user objects |
| Create User | Create a user object |
| Get User | Get a user object by ID |
| Update User | Update a user object by ID |
| Delete User | Delete a user object by ID |

**Node Templates**

| Workflow | Scope |
|---|---|
| List Node Templates | Get a list of node template objects |
| Create Node Template | Create a node template object |
| Get Node Template | Get a node template object by ID |
| Update Node Template | Update a node template object by ID |
| Delete Node Template | Delete a node template object by ID |

**Node Pools**

| Workflow | Scope |
|---|---|
| List Node Pools | Get a list of node pool objects |
| Create Node Pool | Create a node pool object |
| Get Node Pool | Get a node pool object by ID |
| Update Node Pool | Update a node pool object by ID |
| Delete Node Pool | Delete a node pool object by ID |

**Workloads**

| Workflow | Scope |
|---|---|
| List Workloads | Get a list of workload objects in a project |
| Create Workload | Create a workload object in a project |
| Get Workload | Get a workload object by ID |
| Update Workload | Update a workload object by ID (e.g. change scale or container image) |
| Delete Workload | Delete a workload object by ID |
