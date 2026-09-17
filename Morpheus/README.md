# Morpheus

Morpheus is a cloud management platform for provisioning, monitoring, and deploying applications across public, private, and hybrid clouds, offering a unified control plane for groups, clouds, hosts, instances, apps, and networks.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`morpheus-latest.json`](#morpheus-latestjson)
  - [`morpheus-9.0.2.json`](#morpheus-902json)
- [Studio Projects](#studio-projects)
  - [Morpheus Project](#morpheus-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Morpheus API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Morpheus](./Studio%20Projects/Morpheus.project.json) | 62 workflows covering group, cloud, host, instance, app, and network lifecycle management |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Morpheus | 9.0.2 API |
| `Morpheus` Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Morpheus appliance.

Authentication is OAuth 2.0, authorization code grant. Register an OAuth client on your Morpheus appliance (client ID, client secret, redirect URI), complete the authorization code exchange against `/oauth/authorize` and `/oauth/token`, and configure the resulting client credentials on the integration instance.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`morpheus-latest.json`](./OpenAPIs/morpheus-latest.json) | latest (curated) | 62 | Trimmed to 62 of 1017 upstream operations — see breakdown below |
| [`morpheus-9.0.2.json`](./OpenAPIs/morpheus-9.0.2.json) | 9.0.2 | 1017 | Full spec, bundled from the multi-file source published at `github.com/HewlettPackard/morpheus-openapi` |

### `morpheus-latest.json`

Actively-maintained spec (`x-vendor-api-version: 9.0.2`). Trimmed to 62 of 1017 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Groups**: list, create, get, update, delete
- **Clouds**: list cloud types, list, create, get, update, delete, refresh
- **Hosts**: list host types, list, add (baremetal), get, update, delete, start, stop, restart, resize
- **Instances**: list/get instance types (provisioning), list, create, list service plans, get, update, delete, start, stop, restart, resize, clone, suspend, snapshot create/list/delete
- **Apps**: list, create, get, update, delete, apply state, refresh state, get state
- **Networks**: list network types, list/create/get/update/delete networks, list/create/get/update/delete subnets, list/allocate/get/release floating IPs

Long tails dropped from the upstream surface include: load balancers, security groups, resource pools, blueprints, deployments, containers, service catalog, VDI, backups, image builds, jobs, roles/tenants/users/billing/licensing administration, monitoring/alerting/logging internals, integrations/plugins, wikis/archives, and appliance/system settings.

### `morpheus-9.0.2.json`

Full spec (1017 operations), bundled with the Redocly CLI from the multi-file OpenAPI source Morpheus publishes at `github.com/HewlettPackard/morpheus-openapi` (the same bundling method documented in that repo's own README).

## Studio Projects

### Morpheus Project

Backed by the **`Morpheus:latest`** Integration Model (see [`morpheus-latest.json`](./OpenAPIs/morpheus-latest.json) above). The project contains **62 workflows** organized into **6 folders**, one atomic workflow per API operation.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Groups | Retrieves all Groups, Creates a Group, Retrieves a Specific Group, Updates a Group, Deletes a Group | Group CRUD |
| Clouds | Retrieves all Cloud Types, Retrieves all Clouds, Creates a Cloud, Retrieves a Specific Cloud, Updates a Cloud, Deletes a Cloud, Refreshes a Cloud | Cloud CRUD and refresh |
| Hosts | Host Types, Get All Hosts, Add a Baremetal Host, Get a Specific Host, Updating a Host, Delete a Host, Resize a Host, Restart a Host, Start a Host, Stop a Host | Host CRUD and power lifecycle |
| Instances | Get/Get Specific Instance Types for Provisioning, Get All Instances, Create an Instance, Get Available Service Plans for an Instance, Retrieves a Specific Instance, Updating an Instance, Delete an instance, Clone an Instance, Resize an Instance, Restart an instance, Snapshot an Instance, Get list of snapshots for an Instance, Start an instance, Stop an instance, Suspend an instance, Delete Snapshot of Instance | Instance CRUD, provisioning lookups, power lifecycle, and snapshots |
| Apps | Get All Apps, Create an App, Get a Specific App, Updating an App, Delete an App, Apply State of an App, Refresh State of an App, Get State of an App | App CRUD and state apply/refresh |
| Networks | Network Types, Get All Networks, Create a Network, Get a Specific Network, Update a Network, Delete a Network, Get All Subnets, Create a Subnet, Get a Specific Subnet, Update a Subnet, Delete a Subnet, Get All Floating IPs, Allocate a Floating IP, Get a Specific Floating IP, Release a Floating IP | Network, subnet, and floating IP CRUD |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Morpheus:latest` Integration Model | Import from [`morpheus-latest.json`](./OpenAPIs/morpheus-latest.json) before importing the project |
| `Morpheus` integration instance | Create in **Admin > Integrations** with the OAuth 2.0 connection properties above. Workflows are wired to an integration instance named `Morpheus` — update the `adapter_id` value in each workflow task if yours is named differently |
