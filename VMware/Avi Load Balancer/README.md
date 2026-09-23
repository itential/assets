# Avi Load Balancer

VMware Avi Load Balancer (formerly NSX Advanced Load Balancer) is a software-defined application delivery controller providing virtual services, server load balancing, SSL/TLS termination, and application and health monitoring across on-prem and cloud environments.

This project provides OpenAPI specs for automating against the Avi Controller's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`vmware_avi_load_balancer-latest.json`](#vmware_avi_load_balancer-latestjson)
  - [`vmware_avi_load_balancer-22.1.1.json`](#vmware_avi_load_balancer-2211json)
- [Studio Projects](#studio-projects)
  - [VMware Avi Load Balancer Project](#vmware-avi-load-balancer-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Avi Controller REST API OpenAPI specs — curated `-latest` plus the full vendor spec |
| [Studio Projects/VMware Avi Load Balancer](./Studio%20Projects/VMware%20Avi%20Load%20Balancer.project.json) | 65 workflows covering core CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Avi Controller | 22.1.x or later |
| `VMware Avi Load Balancer:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

Basic Authentication must be explicitly enabled on the Controller (**Administration > Settings > Access Settings > Allow Basic Authentication**) — it is off by default.

## Integration Configuration

Import `vmware_avi_load_balancer-latest.json` from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Avi Controller. The REST API is rooted at `/api` — this must be set in the instance's `server.base_path` field, since the platform builds the request URL from `protocol`/`host`/`port`/`base_path` rather than any path in the OpenAPI spec itself.

Authentication is HTTP Basic Auth, using an Avi Controller local (or remote) user account.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "BasicAuth": {
      "username": "<your-username>",
      "password": "<your-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<your-avi-controller-host>",
    "port": 443,
    "base_path": "/api"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`vmware_avi_load_balancer-latest.json`](./OpenAPIs/vmware_avi_load_balancer-latest.json) | latest (curated) | 65 | Trimmed to 65 of 1080 upstream operations covering 13 resource types' CRUD — see breakdown below |
| [`vmware_avi_load_balancer-22.1.1.json`](./OpenAPIs/vmware_avi_load_balancer-22.1.1.json) | 22.1.1 | 1080 | Full vendor Avi Controller API spec — 507 paths across 142 resource types |

### `vmware_avi_load_balancer-latest.json`

Trimmed to 65 of 1080 upstream operations covering 13 resource types' CRUD.

Resources included, by category:

- **Virtual Services**: List, Get, Create, Update, Delete
- **Pools**: List, Get, Create, Update, Delete
- **Health Monitors**: List, Get, Create, Update, Delete
- **SSL Certificates**: List, Get, Create, Update, Delete
- **Pool Groups**: List, Get, Create, Update, Delete
- **Application Profiles**: List, Get, Create, Update, Delete
- **Network Profiles**: List, Get, Create, Update, Delete
- **HTTP Policy Sets**: List, Get, Create, Update, Delete
- **PKI Profiles**: List, Get, Create, Update, Delete
- **Service Engine Groups**: List, Get, Create, Update, Delete
- **Network Security Policies**: List, Get, Create, Update, Delete
- **VSVIPs**: List, Get, Create, Update, Delete
- **Tenants**: List, Get, Create, Update, Delete

### `vmware_avi_load_balancer-22.1.1.json`

Full vendor Avi Controller API spec (1080 operations across 507 paths, 142 resource types). See `vmware_avi_load_balancer-latest.json` above for the curated subset if you just need core CRUD automation.

## Studio Projects

### VMware Avi Load Balancer Project

Backed by the **`VMware Avi Load Balancer:latest`** Integration Model (see [`vmware_avi_load_balancer-latest.json`](./OpenAPIs/vmware_avi_load_balancer-latest.json) above). The project contains **65 workflows** organized into **13 folders**, one atomic workflow per curated operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Virtual Services | List, Get, Create, Update, Delete | Virtual service CRUD |
| Pools | List, Get, Create, Update, Delete | Server pool CRUD |
| Health Monitors | List, Get, Create, Update, Delete | Health monitor CRUD |
| SSL Certificates | List, Get, Create, Update, Delete | SSL/TLS key and certificate CRUD |
| Pool Groups | List, Get, Create, Update, Delete | Pool group CRUD |
| Application Profiles | List, Get, Create, Update, Delete | Application profile CRUD |
| Network Profiles | List, Get, Create, Update, Delete | Network profile CRUD |
| HTTP Policy Sets | List, Get, Create, Update, Delete | HTTP policy set CRUD |
| PKI Profiles | List, Get, Create, Update, Delete | PKI profile CRUD |
| Service Engine Groups | List, Get, Create, Update, Delete | Service Engine group CRUD |
| Network Security Policies | List, Get, Create, Update, Delete | Network security policy CRUD |
| VSVIPs | List, Get, Create, Update, Delete | VSVIP CRUD |
| Tenants | List, Get, Create, Update, Delete | Tenant CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `VMware Avi Load Balancer:latest` Integration Model | Import from [`vmware_avi_load_balancer-latest.json`](./OpenAPIs/vmware_avi_load_balancer-latest.json) before importing the project |
| `VMware Avi Load Balancer` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `VMware Avi Load Balancer` — update the `adapter_id` value in each workflow task if yours is named differently |
