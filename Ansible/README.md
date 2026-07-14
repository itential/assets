Ansible AWX (the upstream open-source project behind Red Hat Ansible Automation Platform's Controller) is a web UI, REST API, and task engine for Ansible — managing job templates, inventories, credentials, projects, and job/workflow execution.

This project provides OpenAPI specs for automating against the AWX (Tower) REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`ansible_awx_tower-latest.json`](#ansible_awx_tower-latestjson)
  - [`ansible_awx_tower-v2.json`](#ansible_awx_tower-v2json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Ansible AWX (Tower) REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Ansible AWX / Tower | API v2 |
| Ansible AWX (Tower) Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your AWX/Tower instance.

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Generate a token by issuing `POST /api/v2/tokens/` with your AWX username and password.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`ansible_awx_tower-latest.json`](./OpenAPIs/ansible_awx_tower-latest.json) | latest (curated) | Trimmed to 277 of 631 upstream operations — see breakdown below |
| [`ansible_awx_tower-v2.json`](./OpenAPIs/ansible_awx_tower-v2.json) | v2 | Full, unmodified vendor spec |

### `ansible_awx_tower-latest.json`

Actively-maintained spec (`x-vendor-api-version: v2`). Trimmed to 277 of 631 upstream operations covering common CRUD for automation. Pull the full spec from a running AWX instance's `/api/v2/` OpenAPI schema endpoint if you need something not covered here.

Resources included, by category:

- **Organizations, Teams, Users**: core CRUD plus organization-scoped listing of inventories, projects, job templates, workflow job templates, credentials, and execution environments
- **Projects**: CRUD, sync (`update`), project updates (read/cancel/events/stdout), playbooks, schedules
- **Inventories**: CRUD, hosts, groups, variable data, inventory sources, ad hoc commands, tree view
- **Groups & Hosts**: CRUD, host/group membership, variable data, Ansible facts
- **Inventory Sources & Updates**: CRUD, sync (`update`), read/cancel/events/stdout on updates
- **Credentials & Credential Types**: CRUD, credential test
- **Execution Environments**: CRUD
- **Job Templates & Jobs**: CRUD, launch, relaunch, cancel, stdout, job events, job host summaries, labels, schedules, survey spec
- **Ad Hoc Commands**: create/read, cancel, relaunch, events, stdout
- **Workflow Job Templates, Workflow Jobs, Workflow Job Template/Job Nodes**: CRUD, launch, relaunch, cancel, node topology (always/success/failure nodes)
- **Labels, Schedules, Notification Templates & Notifications**: CRUD/read

Excluded as long-tail/admin surface: activity streams, analytics/reporting, bulk operations, instance/instance-group and mesh/receptor infrastructure administration, RBAC role management (`roles`, `role_definitions`, `role_*_assignments`), the `service-index` federation API, system jobs/settings/config administration, workflow approvals, and webhook receiver endpoints (GitHub/GitLab/Bitbucket callback hooks).

### `ansible_awx_tower-v2.json`

Full, unmodified vendor spec (API v2, 631 operations) — the vendor's complete API surface, preserved as-is. See `ansible_awx_tower-latest.json` above for the curated subset if you just need common CRUD automation.
