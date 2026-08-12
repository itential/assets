GitLab is a web-based DevOps platform for Git version control, code review, issue tracking, and CI/CD pipelines.

This project provides OpenAPI specs for automating against GitLab's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`gitlab_rest_api-latest.json`](#gitlab_rest_api-latestjson)
  - [`gitlab_rest_api-v4.json`](#gitlab_rest_api-v4json)
- [Studio Projects](#studio-projects)
  - [GitLab Project](#gitlab-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | GitLab REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 133 workflows in 21 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `GitLab REST API:latest` Integration Model | Required to build automation against the OpenAPI specs, and to run the Studio Project below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to GitLab's REST API.

## Integration Configuration

Import `gitlab_rest_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your GitLab instance (or `gitlab.com` for GitLab SaaS).

Authentication is an API key in the `PRIVATE-TOKEN` header:

```
PRIVATE-TOKEN: <your-personal-access-token>
```

Generate a Personal Access Token (or group/project access token) at GitLab → User Settings → Access Tokens.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "access_token_header": {
      "value": "<your-personal-access-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "gitlab.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`gitlab_rest_api-latest.json`](./OpenAPIs/gitlab_rest_api-latest.json) | latest (curated) | 133 | Trimmed to 133 of 1008 upstream operations covering common CRUD for automation — see breakdown below |
| [`gitlab_rest_api-v4.json`](./OpenAPIs/gitlab_rest_api-v4.json) | v4 | 1008 | Full spec for GitLab REST API v4 (1008 operations) |

### `gitlab_rest_api-latest.json`

Actively-maintained spec (`x-vendor-api-version: v4`). Trimmed to 133 of 1008 upstream operations covering common CRUD for automation. The full upstream spec models the entire GitLab REST API surface, including package registries (npm, Maven, PyPI, NuGet, Conan, Composer, Debian, RPM, Helm, Go proxy, generic packages, Terraform module registry), container registry, third-party service integrations, webhooks, instance/user/permission administration, Kubernetes cluster agents, feature flags, error tracking, wikis, snippets, badges, and bulk import/export — none of those are included here. Pull the full spec from [GitLab's official REST API docs](https://docs.gitlab.com/ee/api/rest/) if you need one of the excluded areas.

Resources included, by category:

- **Projects**: List, Create, Get, Update, Delete, Archive, Unarchive, Fork
- **Groups**: List, Create, Get, Update, Delete, List Projects, List Subgroups
- **Members**: Group and Project members (List, Add, Get, Update, Remove)
- **Branches**: List, Create, Get, Delete, Protect, Unprotect
- **Protected Branches**: List, Create, Get, Update, Delete
- **Repository Files**: Get, Get Raw, Create, Update, Delete
- **Repository Browse**: Tree, Compare
- **Commits**: List, Create, Get, Diff, Comments (List/Create)
- **Tags**: List, Create, Get, Delete (git tags and protected tags)
- **Merge Requests**: List, Create, Get, Update, Delete, Merge, Commits, Diffs, Versions
- **Pipelines**: Create (trigger), List, Get Latest, Get, Delete, Cancel, Retry, Jobs, Variables
- **Pipeline Schedules**: List, Create, Get, Update, Delete
- **Jobs**: List, Get, Trace, Cancel, Retry, Play
- **CI/CD Variables**: Group and Project level (List, Create, Get, Update, Delete)
- **Releases**: List, Create, Get, Update, Delete
- **Environments**: List, Create, Get, Update, Delete, Stop
- **Deployments**: List, Create, Get, Update, Delete
- **Deploy Keys**: List, Create, Get, Update, Delete
- **Deploy Tokens**: Group and Project level (List, Create, Get, Delete)
- **Runners**: Project-level List, Register, Delete
- **Users**: List, Get (read-only reference lookup)

### `gitlab_rest_api-v4.json`

Full, unmodified vendor spec for GitLab REST API v4 (1008 operations) — the vendor's complete API surface, preserved as-is. See `gitlab_rest_api-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### GitLab Project

Backed by the **`GitLab REST API:latest`** Integration Model (see [`gitlab_rest_api-latest.json`](./OpenAPIs/gitlab_rest_api-latest.json) above). The project contains **133 workflows** organized into **21 folders**, one workflow per curated operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List Merge Requests`, `Trigger Pipeline`).

Note the `CI-CD Variables` folder name uses a hyphen rather than a slash — Itential Platform's project folder paths use `/` as a path separator, so a literal `/` in a folder name would be parsed as nested folders instead of one folder name.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Groups | 7 | Group (+ list projects, list subgroups) |
| Members | 10 | Group Member, Project Member |
| Deploy Tokens | 8 | Group Deploy Token, Project Deploy Token |
| CI-CD Variables | 10 | Group Variable, Project Variable |
| Projects | 10 | Project (+ archive/unarchive/fork/delete-fork), Project Fork (list) |
| Jobs | 6 | Job (+ cancel/retry/play/trace) |
| Merge Requests | 10 | Merge Request (+ commits/diffs/merge/versions) |
| Pipelines | 9 | Pipeline (+ trigger/latest/cancel/retry/jobs/variables) |
| Pipeline Schedules | 5 | Pipeline Schedule |
| Protected Branches | 5 | Protected Branch |
| Tags | 8 | Tag, Protected Tag |
| Releases | 5 | Release |
| Environments | 6 | Environment (+ stop) |
| Deployments | 5 | Deployment |
| Deploy Keys | 5 | Deploy Key |
| Runners | 3 | Project Runner (list, enable, disable) |
| Branches | 6 | Branch (+ protect/unprotect) |
| Repository Files | 5 | Repository File (+ get raw) |
| Repository Browse | 2 | Repository Tree, Repository Comparison |
| Commits | 6 | Commit (+ diff, comments) |
| Users | 2 | User |

#### Dependencies

| Dependency | Notes |
|---|---|
| `GitLab REST API:latest` Integration Model | Import from [`gitlab_rest_api-latest.json`](./OpenAPIs/gitlab_rest_api-latest.json) before importing the project |
| `GitLab` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `GitLab` — update the `adapter_id` value in each workflow task if yours is named differently |

**Testing status:** all 133 workflows were created and schema-validated against a running Itential Platform instance. `List Projects` and `List Groups` were executed against a real GitLab.com account and confirmed returning live data. `Get Project` for a specific project outside the token's granted scope failed with `insufficient_granular_scope` — GitLab's fine-grained personal access tokens can restrict `Project`/`Group` read access to a limited set of resources (e.g. "personal projects only"), independent of this Integration Model; a token with broader scope resolves this. The remaining workflows have not been individually executed.
