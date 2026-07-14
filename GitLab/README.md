GitLab is a web-based DevOps platform for Git version control, code review, issue tracking, and CI/CD pipelines.

This project provides two complementary ways to automate against GitLab:

- **Studio Project workflows** built on the **GitLab Adapter** — project, branch, merge request, and file/commit lifecycle workflows.
- **OpenAPI specs** for building new automation directly against GitLab's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for repository and CI/CD automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Adapter (Studio Project workflows)](#adapter-studio-project-workflows)
  - [Integration Model (OpenAPI-based automation)](#integration-model-openapi-based-automation)
- [Studio Projects](#studio-projects)
  - [GitLab Project](#gitlab-project)
- [OpenAPIs](#openapis)
  - [`gitlab_rest_api-latest.json`](#gitlab_rest_api-latestjson)
  - [`gitlab_rest_api-v4.json`](#gitlab_rest_api-v4json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | GitLab REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing the project/branch/merge-request/file workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| GitLab Adapter | Required for the Studio Project workflows below |
| GitLab Integration Model | Required only if building new automation directly against the OpenAPI specs |

## Integration Configuration

### Adapter (Studio Project workflows)

Install the [GitLab Adapter](https://gitlab.com/itentialopensource/adapters/adapter-gitlab) and configure an instance in **Admin > Adapters**, then update the `adapterId` value (`$var.job.adapterId`) in each workflow task to match your instance name before importing.

### Integration Model (OpenAPI-based automation)

To build automation directly against the REST API instead, import `OpenAPIs/gitlab_rest_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your GitLab instance (or `gitlab.com` for GitLab SaaS).

Authentication is an API key in the `PRIVATE-TOKEN` header:

```
PRIVATE-TOKEN: <your-personal-access-token>
```

Generate a Personal Access Token (or group/project access token) at GitLab → User Settings → Access Tokens.

---

## Studio Projects

### GitLab Project

| Folder | Workflows | Scope |
|---|---|---|
| Create Project | Create Project | Create a new project in a namespace |
| Create Templated Project | Create Templated Project | Create a project from an existing template project |
| Push Commit to Branch | Push Commit to Branch | Read an existing file and push an updated commit to a branch |
| Get Diff for Merge | Get Diff for Merge | Retrieve merge request diff versions |
| (root) | Get Branch, Get File, Create Branch, Create Merge Request, Update Project Variables | Read a branch or file; create a branch or merge request; update a project CI/CD variable |

#### Dependencies

| Dependency | Notes |
|---|---|
| [GitLab Adapter](https://gitlab.com/itentialopensource/adapters/adapter-gitlab) | Required for the Studio Project workflows. Update the `adapterId` in each workflow task to match your instance name. |

---

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`gitlab_rest_api-latest.json`](./OpenAPIs/gitlab_rest_api-latest.json) | latest (curated) | Trimmed to 133 of 1008 upstream operations covering common CRUD for automation — see breakdown below |
| [`gitlab_rest_api-v4.json`](./OpenAPIs/gitlab_rest_api-v4.json) | v4 | Full spec for GitLab REST API v4 (1008 operations) |

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
