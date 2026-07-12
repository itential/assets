Docker Hub is Docker's cloud-based container registry service for storing, distributing, and managing container images, repositories, and organizations.

This project provides OpenAPI specs for automating against the Docker Hub REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Docker Hub REST API OpenAPI specs — curated `-latest` plus full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Docker Hub | API v2 (see OpenAPIs below for exact spec version available) |
| Docker Hub Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at `https://hub.docker.com`.

Authentication is a Bearer JWT in the `Authorization` header:

```
Authorization: Bearer <token>
```

Obtain a token via `POST /v2/users/login` with your Docker Hub username and password.

## OpenAPIs

### `docker_hub-latest.json` (curated)

Actively-maintained spec (`x-vendor-api-version: beta`). Trimmed to 16 of 28 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Access Tokens**: List, create, retrieve, update, and delete personal access tokens
- **Repositories, Images & Tags**: List repository images, image summaries, image tags by digest, repository tags, and individual tag details
- **Namespaces**: Bulk delete images within a namespace/repository
- **Organization Settings**: Retrieve and update organization settings
- **Authentication**: User login to obtain a bearer token

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`docker_hub-beta.json`](./OpenAPIs/docker_hub-beta.json) | Full spec for Docker Hub API (beta). |

## Dependencies

| Dependency | Notes |
|---|---|
| Docker Hub Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
