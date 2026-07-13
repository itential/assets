Docker Engine is the core container runtime and daemon behind Docker — it manages the container, image, network, and volume lifecycle on a host via a REST API exposed over a Unix socket or TCP (optionally TLS-secured).

This project provides OpenAPI specs for automating against the Docker Engine REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for container automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Docker Engine REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Docker Engine | API version 1.33 (Docker 17.06+) |
| Docker Engine Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Docker daemon's exposed API endpoint.

Authentication is HTTP Basic, used for TLS-enabled remote Docker daemons:

```
Authorization: Basic <base64(username:password)>
```

Local socket access typically requires no authentication. For remote/production access, expose the Docker daemon over TCP with TLS certificates configured (`dockerd --tlsverify ...`) and supply credentials enforced by your TLS/proxy layer, since the Docker Engine API itself has no native user database.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`docker_engine-latest.json`](./OpenAPIs/docker_engine-latest.json) | latest (curated) | Actively-maintained spec, trimmed to 52 of 105 upstream operations covering common CRUD for automation — see breakdown below |
| [`docker_engine-1.33.json`](./OpenAPIs/docker_engine-1.33.json) | 1.33 | Full spec for Docker Engine API 1.33 (105 operations) |

### `docker_engine-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.33`). Trimmed to 52 of 105 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Containers**: Create, List, Inspect, Start, Stop, Restart, Kill, Pause/Unpause, Rename, Update, Remove, Prune, Logs, Stats, Top, Changes, Wait, Export, Copy files to/from (archive), Exec (create/start/resize/inspect)
- **Images**: Pull (create), List, Inspect, History, Search, Tag, Push, Remove, Prune
- **Networks**: Create, List, Inspect, Remove, Prune, Connect, Disconnect
- **Volumes**: Create, List, Inspect, Remove, Prune
- **Distribution**: Inspect a remote image manifest without pulling it
- **System**: Ping, Version, Info

Excluded as out of scope for this curated spec: Swarm mode and its orchestration objects (Swarm, Service, Task, Node, Secret, Config), plugin management, the experimental BuildKit session endpoint, Dockerfile-based image builds (`/build`, `/commit`), tar-based bulk image import/export, interactive container attach (stdin/stdout hijack), and admin/reporting-only endpoints (`/auth`, `/events`, `/system/df`). See the full spec below for these.
