# Salt

Salt is an open-source infrastructure automation and remote execution engine. Its salt-api service exposes the master's execution, runner, and wheel functions over a REST interface (the `rest_cherrypy` netapi module), letting external systems run commands against minions, manage minion authentication keys, and track jobs without a local Salt client.

This project provides a Studio Project of workflows covering the REST API operations most useful for automation, plus an OpenAPI spec for building your own automation via an Integration Model — see **Studio Projects** and **OpenAPIs** below.

## Table of Contents

- [Salt](#salt)
  - [Table of Contents](#table-of-contents)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Integration Configuration](#integration-configuration)
    - [Connection Properties](#connection-properties)
  - [OpenAPIs](#openapis)
    - [`salt-latest.json`](#salt-latestjson)
    - [`salt-3008.1.json`](#salt-30081json)
  - [Studio Projects](#studio-projects)
    - [Salt Project](#salt-project)
      - [Folder Structure](#folder-structure)
      - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Salt `rest_cherrypy` netapi OpenAPI specs — curated `-latest` plus the matching dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 9 workflows in 4 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Salt master with `salt-api` and the `rest_cherrypy` netapi module enabled | Any release exposing `/login`, `/`, `/minions`, `/jobs`, and `/keys` |
| `Salt:latest` Integration Model | Required to build automation against the OpenAPI spec |
| A Salt eauth account (PAM, LDAP, or another configured external auth module) | Used for the session-token login |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to the Salt master.

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Salt master.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<salt-master-host-or-ip>",
    "port": "8000"
  },
  "authentication": {
    "SaltToken": {
      "username": "<eauth-username>",
      "password": "<eauth-password>",
      "eauth": "<eauth-module>"
    }
  }
}
```

Itential Platform logs in against `/login` with these credentials, extracts the session token from the response, and replays it on the `X-Auth-Token` header of every subsequent request.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`salt-latest.json`](./OpenAPIs/salt-latest.json) | latest (curated) | 9 | Actively-maintained spec — see breakdown below |
| [`salt-3008.1.json`](./OpenAPIs/salt-3008.1.json) | 3008.1 | 9 | Dated spec matching the documented `rest_cherrypy` REST surface |

### `salt-latest.json`

Actively-maintained spec (`x-vendor-api-version: 3008.1`). Reviewed against the repo's common-CRUD-for-automation policy: all 9 documented `rest_cherrypy` operations are already in scope, so the full spec is carried through as `-latest`.

Resources included, by category:

- **Execution**: Run a lowstate command against targeted minions (or a runner/wheel/ssh function) and wait for the result; start the same call asynchronously and get back a job ID
- **Minions**: List all minions and their grains, get a single minion's grains
- **Jobs**: List published jobs, get a job's metadata and per-minion results
- **Keys**: List minion authentication keys by status, get a single minion's key fingerprint, generate and auto-accept a new minion keypair

### `salt-3008.1.json`

Dated spec matching the documented `rest_cherrypy` REST surface as of Salt 3008.1.

---

## Studio Projects

### Salt Project

Backed by the **`Salt:latest`** Integration Model (see [`salt-latest.json`](./OpenAPIs/salt-latest.json) above). The project contains **9 workflows** organized into **4 folders**, one atomic workflow per API operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List Minions`, `Get Job`).

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Execution | Run Command, Run Command Async | Lowstate command execution, synchronous and asynchronous |
| Minions | List Minions, Get Minion | Minion inventory and grain data |
| Jobs | List Jobs, Get Job | Published job tracking and results |
| Keys | List Keys, Get Key, Generate Key | Minion authentication key management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Salt:latest` Integration Model | Import from [`salt-latest.json`](./OpenAPIs/salt-latest.json) before importing the project |
| `Salt` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Salt` — update the `adapter_id` value in each workflow task if yours is named differently |
