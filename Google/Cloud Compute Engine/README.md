Google Cloud Compute Engine is Google Cloud's infrastructure-as-a-service offering for running virtual machines, persistent disks, images, and the virtual networking (VPC, subnets, firewalls, routes, load-balancing building blocks) that supports them.

This project provides OpenAPI specs for automating against the Compute Engine REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`google_cloud_compute_engine-latest.json`](#google_cloud_compute_engine-latestjson)
  - [`google_cloud_compute_engine-v1.json`](#google_cloud_compute_engine-v1json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Compute Engine REST API OpenAPI specs — curated `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Google Cloud Compute Engine API | v1 |
| Google Cloud Compute Engine Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at `https://compute.googleapis.com/compute/v1`.

Authentication is a Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Use a Google service account access token with Compute Engine permissions (`https://www.googleapis.com/auth/compute` or `https://www.googleapis.com/auth/cloud-platform` scope). Generate one via Google Cloud IAM → Service Accounts.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`google_cloud_compute_engine-latest.json`](./OpenAPIs/google_cloud_compute_engine-latest.json) | latest (curated) | Actively-maintained, curated for common CRUD automation — see breakdown below |
| [`google_cloud_compute_engine-v1.json`](./OpenAPIs/google_cloud_compute_engine-v1.json) | v1 | Full spec for Compute Engine API v1 (694 operations) |

### `google_cloud_compute_engine-latest.json`

Actively-maintained spec (`x-vendor-api-version: v1`). Trimmed to 149 of 694 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Instances**: create, get, list, update, delete, aggregated list, start, stop, reset, suspend, resume, attach/detach disk, set metadata, set labels, set tags, set machine type, set deletion protection, get serial port output
- **Disks & Snapshots**: zonal and regional disks (create, get, list, delete, update, resize, create snapshot, set labels), snapshots (get, list, delete, create, set labels)
- **Images**: create, get, list, delete, patch, deprecate, get from family, set labels
- **Networking**: VPC networks (create, get, list, delete, patch), subnetworks (create, get, list, delete, patch, expand IP CIDR range), firewall rules (create, get, list, delete, patch, update), static addresses — regional and global (create, get, list, delete, set labels), routes (create, get, list, delete), routers (create, get, list, delete, patch, update)
- **Instance Groups & Templates**: managed and unmanaged instance groups — zonal and regional (create, get, list, delete, add/remove instances, list instances, set named ports, resize, create/delete managed instances, set instance template), instance templates (create, get, list, delete), autoscalers — zonal and regional (create, get, list, delete, patch, update)
- **Reference lookups & operations**: zones, regions, machine types, project info (get/list), and zone/region/global operation status polling (get, list, wait)

See the repo README for the full scope and the full spec.

### `google_cloud_compute_engine-v1.json`

Full, unmodified vendor spec for Compute Engine API v1 (694 operations) — the vendor's complete API surface, preserved as-is. See `google_cloud_compute_engine-latest.json` above for the curated subset if you just need common CRUD automation.
