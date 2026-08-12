GitHub is a web-based platform for Git version control, code review, issue tracking, and CI/CD via GitHub Actions.

This project provides OpenAPI specs for automating against GitHub's REST API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`github_rest_api-latest.json`](#github_rest_api-latestjson)
  - [`github_rest_api-1.1.4.json`](#github_rest_api-114json)
- [Studio Projects](#studio-projects)
  - [GitHub Project](#github-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | GitHub REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 251 workflows in 16 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `GitHub REST API:latest` Integration Model | Required to build automation against the OpenAPI specs, and to run the Studio Project below |

> **Note:** This project does not require Itential Gateway. All API calls are made directly from Itential Platform to GitHub's REST API.

## Integration Configuration

Import `github_rest_api-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your GitHub instance (`api.github.com` for GitHub.com, or your GitHub Enterprise Server hostname with `base_path: /api/v3`).

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <your-github-personal-access-token>
```

Generate a Personal Access Token (or GitHub App installation token) at GitHub Settings → Developer settings → Personal access tokens.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearerAuth": "<your-github-personal-access-token>"
  },
  "server": {
    "protocol": "https",
    "host": "api.github.com",
    "base_path": ""
  }
}
```

For GitHub Enterprise Server, set `host` to your instance's hostname and `base_path` to `/api/v3`.

> **Note:** The OpenAPI spec's `servers` entry is a static placeholder (`https://HOSTNAME/api/v3`) rather than the vendor's templated Enterprise Server URL — Itential Platform Integration Models require a static server URL, so the actual protocol/host/base_path are configured per-instance as shown above, same as GitLab's self-hosted-vs-SaaS split.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`github_rest_api-latest.json`](./OpenAPIs/github_rest_api-latest.json) | latest (curated) | 248 | Trimmed to 248 of 987 upstream operations covering common CRUD for automation — see breakdown below |
| [`github_rest_api-1.1.4.json`](./OpenAPIs/github_rest_api-1.1.4.json) | 1.1.4 | 1186 | Full, unmodified vendor spec |

### `github_rest_api-latest.json`

Actively-maintained spec (`x-vendor-api-version: 3.1.3`). Trimmed to 248 of 987 upstream operations covering common CRUD for repository automation. Beyond the exclusions already carried over from the prior curation pass (GitHub Enterprise admin, security scanning, Packages, Pages), this pass additionally dropped:

- **Legacy team endpoints** (`/teams/{team_id}/...`) — superseded by the org-scoped `/orgs/{org}/teams/{team_slug}/...` equivalents, which are included.
- **Emoji reactions** — a thin long tail of list/create/delete endpoints scattered across six different resource types (issues, comments, pull request review comments, releases, team discussions). Low automation value.
- **The most granular branch-protection sub-resources** — `enforce_admins`, `required_signatures`, and `restrictions` scoped by app/team/user individually. Core protection CRUD (get/update/delete on branch protection, PR review protection, status check protection and contexts, and access restrictions as a whole) is retained.

Pull the full spec from [GitHub's official OpenAPI description](https://github.com/github/rest-api-description) if you need one of the excluded areas.

Resources included, by category:

- **Organizations**: Get, Update, Delete, Members, Outside Collaborators, Public Members, Org Repositories
- **Teams**: List, Create, Get, Update, Delete (org-scoped), Discussions, Discussion Comments, External Groups, Members, Membership, Team Projects, Team Repositories
- **Repositories**: Get, Update, Delete, Collaborators, Invitations
- **Branches**: List, Get, Rename, Branch Protection, PR Review Protection, Status Check Protection/Contexts, Access Restrictions
- **Commits**: List, Get, Compare, Commit Comments, Commit Status
- **Checks**: Check Runs, Check Suites (list)
- **Repository Contents**: Get, Create/Update, Delete file contents
- **Actions**: Artifacts, Workflows, Workflow Runs, Workflow Jobs, Environment Secrets, Environment Variables
- **Issues**: List, Create, Get, Update, Comments, Events, Assignees, Labels, Lock, Milestones
- **Pull Requests**: List, Create, Get, Update, Comments, Requested Reviewers, Reviews
- **Releases**: List, Create, Get, Update, Delete, Release Assets
- **Deployments**: List, Create, Get, Delete, Deployment Status
- **Environments**: List, Create, Get, Update, Delete, Deployment Branch Policies, Deployment Protection Rules
- **Webhooks**: List, Create, Get, Update, Delete, Config, Deliveries
- **Tags**: List, Tag Protection
- **Users**: Authenticated user profile (get/update)

### `github_rest_api-1.1.4.json`

Full, unmodified vendor spec (1.1.4) — the vendor's complete API surface, preserved as-is. See `github_rest_api-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### GitHub Project

Backed by the **`GitHub REST API:latest`** Integration Model (see [`github_rest_api-latest.json`](./OpenAPIs/github_rest_api-latest.json) above). The project contains **251 workflows** organized into **16 folders**, one workflow per curated operation. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List Pull Requests`, `Merge Pull Request`).

Several resource names are prefixed with `GitHub` (`GitHub Organization`, `GitHub Branch`, `GitHub Commit`, `GitHub Commit Comment`, `GitHub Repository File`, `GitHub Release`, `GitHub Deployment`, `GitHub Environment`, `GitHub Tag`) — these are generic terms that would otherwise collide with identically-named workflows already published for other products (Meraki's `Organization`, GitLab's `Branch`/`Commit`/`Release`/`Deployment`/`Environment`/`Tag`/etc.), since workflow names are unique across the whole Itential Platform instance, not scoped per-project.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Organizations | 15 | GitHub Organization, Organization Member, Outside Collaborator, Public Member, Organization Repository |
| Teams | 31 | Team, Team Discussion, Team Discussion Comment, Team External Group, Team Member, Team Membership, Team Project, Team Repository |
| Repositories | 11 | Repository, Collaborator, Repository Invitation |
| Branches | 18 | GitHub Branch, Branch Protection, PR Review Protection, Status Check Protection/Context, Access Restrictions |
| Commits | 13 | GitHub Commit, GitHub Commit Comment, Commit Status |
| Checks | 2 | Check Run, Check Suite (list only) |
| Repository Contents | 4 | GitHub Repository File |
| Actions | 42 | Artifact, Workflow, Workflow Run, Workflow Job, Environment Secret, Environment Variable |
| Issues | 35 | Issue, Issue Comment, Issue Event, Issue Assignee, Issue Label, Issue Lock, Label, Milestone |
| Pull Requests | 27 | Pull Request, Pull Request Comment, Requested Reviewer, Pull Request Review |
| Releases | 13 | GitHub Release, Release Asset |
| Deployments | 7 | GitHub Deployment, Deployment Status |
| Environments | 15 | GitHub Environment, Deployment Branch Policy, Deployment Protection Rule |
| Webhooks | 12 | Webhook, Webhook Config, Webhook Delivery |
| Tags | 4 | GitHub Tag, Tag Protection |
| Users | 2 | Authenticated User |

#### Dependencies

| Dependency | Notes |
|---|---|
| `GitHub REST API:latest` Integration Model | Import from [`github_rest_api-latest.json`](./OpenAPIs/github_rest_api-latest.json) before importing the project |
| `GitHub` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `GitHub` — update the `adapter_id` value in each workflow task if yours is named differently |

**Testing status:** all 251 workflows were created and schema-validated against a running Itential Platform instance. `Get Authenticated User` and `List Organization Members` were executed against a real GitHub account and confirmed returning live data. The remaining workflows have not been individually executed.
