Kubernetes is an open-source container orchestration system for automating deployment, scaling, and management of containerized applications — pods, deployments, services, config maps, secrets, namespaces, RBAC, and more.

This project provides OpenAPI specs for automating against the Kubernetes API server via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for cluster automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`kubernetes-latest.json`](#kubernetes-latestjson)
  - [`kubernetes-v1.10.0.json`](#kubernetes-v1100json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Kubernetes API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Kubernetes | 1.10 (see OpenAPIs below for exact spec version available) |
| Kubernetes Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Kubernetes API server.

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <your-kubernetes-token>
```

Use a Kubernetes service account token, a kubeconfig user credential, or a cluster admin token as the value.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "BearerToken": {
      "value": "<your-bearer-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "kubernetes.local",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`kubernetes-latest.json`](./OpenAPIs/kubernetes-latest.json) | latest (curated) | 257 | Actively-maintained, trimmed to 257 of 933 upstream operations — see breakdown below |
| [`kubernetes-v1.10.0.json`](./OpenAPIs/kubernetes-v1.10.0.json) | v1.10.0 | 945 | Full, unmodified vendor spec (945 operations) |

### `kubernetes-latest.json`

Actively-maintained spec (`x-vendor-api-version: v1.10.0`). Trimmed to 257 of 933 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Workloads**: Pods (including logs), Deployments (with scale), ReplicaSets (with scale), StatefulSets (with scale), DaemonSets, ReplicationControllers (with scale), ControllerRevisions
- **Batch**: Jobs, CronJobs
- **Networking**: Services, Endpoints, Ingresses, NetworkPolicies
- **Config & Storage**: ConfigMaps, Secrets, PersistentVolumes, PersistentVolumeClaims, StorageClasses
- **Cluster**: Namespaces, Nodes, ServiceAccounts, ResourceQuotas, LimitRanges, Events, PodDisruptionBudgets
- **Scaling**: HorizontalPodAutoscalers
- **RBAC**: Roles, RoleBindings, ClusterRoles, ClusterRoleBindings

Excludes watch/streaming endpoints, exec/attach/portforward/proxy debug endpoints, deprecated and duplicate API group versions (e.g. `extensions/v1beta1` workloads superseded by `apps/v1`, `apps/v1beta1`/`v1beta2`), webhook and aggregation-layer admin APIs (`admissionregistration.k8s.io`, `apiregistration.k8s.io`, `apiextensions.k8s.io`), and specialized/internal endpoints (TokenReviews, SubjectAccessReviews, CertificateSigningRequests, PodSecurityPolicies, PodPresets, PriorityClasses, ComponentStatuses, raw `/logs/{logpath}`). Pull the full spec if you need one of the excluded areas.

### `kubernetes-v1.10.0.json`

Full, unmodified vendor spec for Kubernetes v1.10.0 (945 operations) — the vendor's complete API surface, preserved as-is. See `kubernetes-latest.json` above for the curated subset if you just need common CRUD automation.
