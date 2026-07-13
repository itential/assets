GitHub is a web-based platform for Git version control, code review, issue tracking, and CI/CD via GitHub Actions.

This project provides two complementary ways to automate against GitHub:

- **Studio Project workflows** built on the **GitHub Adapter** — a set of repository CRUD workflows (create a branch, commit a file, get a file, open a pull request).
- **OpenAPI specs** for building new automation directly against GitHub's REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for repository automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | GitHub REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | IAP project containing the repository CRUD workflows |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| GitHub Adapter | Required for the Studio Project workflows below |
| GitHub Integration Model | Required only if building new automation directly against the OpenAPI specs |

## Integration Configuration

### Adapter (Studio Project workflows)

Install the [GitHub Adapter](https://gitlab.com/itentialopensource/adapters/adapter-github) and configure an instance in **Admin > Adapters**, then update the `adapterId` value in each workflow task to match your instance name before importing.

### Integration Model (OpenAPI-based automation)

To build automation directly against the REST API instead, import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your GitHub instance (or `api.github.com` for GitHub.com).

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <your-github-personal-access-token>
```

Generate a Personal Access Token at GitHub Settings → Developer settings → Personal access tokens, or use a GitHub App installation token.

---

## Studio Projects

### GitHub Project

| Folder | Workflows | Scope |
|---|---|---|
| Commit File | Commit File | Create or update a file's contents on a branch |
| Create Branch | Create Branch | Create a new branch from a reference branch |
| (root) | Create Pull Request, Get File | Open a pull request between branches; read a file's contents |

#### Dependencies

| Dependency | Notes |
|---|---|
| [GitHub Adapter](https://gitlab.com/itentialopensource/adapters/adapter-github) | Required. Update `adapterId` in each workflow task to match your instance name. |

---

## Workflow Input Reference

All workflows accept a JSON object when run manually or called as a child workflow.

### Create Pull Request

```json
{
  "adapterId": "GitHub",
  "repoOwner": "my-org",
  "repoName": "my-repo",
  "prTitle": "Add new feature",
  "sourceBranch": "feature/my-change",
  "targetBranch": "main"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `adapterId` | string | Yes | Name of the configured GitHub adapter instance. |
| `repoOwner` | string | Yes | Repository owner (user or organization). |
| `repoName` | string | Yes | Repository name. |
| `prTitle` | string | Yes | Pull request title. |
| `sourceBranch` | string | Yes | Branch containing the changes. |
| `targetBranch` | string | Yes | Branch to merge into. |

### Commit File

```json
{
  "adapterId": "GitHub",
  "repoOwner": "my-org",
  "repoName": "my-repo",
  "filePath": "configs/router1.cfg",
  "branchName": "main",
  "commitMessage": "Update router1 config",
  "fileContent": "hostname router1\n..."
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `adapterId` | string | Yes | Name of the configured GitHub adapter instance. |
| `repoOwner` | string | Yes | Repository owner (user or organization). |
| `repoName` | string | Yes | Repository name. |
| `filePath` | string | Yes | Path of the file to create or update. |
| `branchName` | string | Yes | Branch to commit to. |
| `commitMessage` | string | Yes | Commit message. |
| `fileContent` | string | Yes | New file content. |

### Create Branch

```json
{
  "adapterId": "GitHub",
  "owner": "my-org",
  "repoName": "my-repo",
  "branchName": "feature/my-change",
  "refBranchName": "main"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `adapterId` | string | Yes | Name of the configured GitHub adapter instance. |
| `owner` | string | Yes | Repository owner (user or organization). |
| `repoName` | string | Yes | Repository name. |
| `branchName` | string | Yes | Name for the new branch. |
| `refBranchName` | string | Yes | Existing branch to branch from. |

### Get File

```json
{
  "adapterId": "GitHub",
  "repoOwner": "my-org",
  "repoName": "my-repo",
  "filePath": "configs/router1.cfg",
  "branchName": "main"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `adapterId` | string | Yes | Name of the configured GitHub adapter instance. |
| `repoOwner` | string | Yes | Repository owner (user or organization). |
| `repoName` | string | Yes | Repository name. |
| `filePath` | string | Yes | Path of the file to read. |
| `branchName` | string | Yes | Branch to read from. |

---

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`github_rest_api-latest.json`](./OpenAPIs/github_rest_api-latest.json) | latest (curated) | Trimmed to 320 of 987 upstream operations — see breakdown below |
| [`github_rest_api-1.1.4.json`](./OpenAPIs/github_rest_api-1.1.4.json) | 1.1.4 | Full, unmodified vendor spec |

### `github_rest_api-latest.json`

Actively-maintained spec (`x-vendor-api-version: 3.1.3`). Trimmed to 320 of 987 upstream operations covering common CRUD for repository automation. Excludes GitHub Enterprise admin, security scanning (Dependabot/code/secret scanning), Packages, Pages, and CI status-check APIs. Pull the full spec from [GitHub's official OpenAPI description](https://github.com/github/rest-api-description) if you need one of the excluded areas.

Resources included, by category:

- **Repository content**: Contents (files), Branches, Commits, Compare
- **Collaboration**: Issues, Pull Requests, Comments, Labels, Milestones, Collaborators, Invitations
- **Releases**: Releases, Tags
- **CI/CD**: Actions Workflows, Workflow Runs, Jobs, Artifacts
- **Deployment**: Environments, Deployments
- **Webhooks**: Repository Hooks
- **Organizations**: Org Teams, Members, Public Members, Outside Collaborators, Org Repos
- **User**: Authenticated user profile
