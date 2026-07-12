Amazon Elastic Kubernetes Service (EKS) is a managed Kubernetes service for running containerized applications on AWS without managing control plane infrastructure. It handles cluster lifecycle, managed node groups, Fargate profiles, add-ons, and identity provider integration for Kubernetes RBAC.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Amazon EKS REST API OpenAPI spec — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Amazon EKS | API version 2017-11-01 |
| Amazon EKS Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the EKS regional API endpoint (e.g. `https://eks.<region>.amazonaws.com`).

Authentication uses AWS Signature Version 4 — requests are signed with an AWS access key ID and secret access key rather than a static bearer token or API key header:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/eks/aws4_request, SignedHeaders=..., Signature=<computed-signature>
```

Generate an AWS access key ID and secret access key for an IAM principal with `eks:*` permissions under **IAM > Users/Roles > Security credentials**.

## OpenAPIs

### `amazon_eks-latest.json` (full, unmodified)

Actively-maintained spec (`x-vendor-api-version: 2017-11-01`). This spec already covers a single cohesive product surface — every operation manages an EKS cluster or one of its direct sub-resources (add-ons, managed node groups, Fargate profiles, identity provider configs, updates, tags). There is no vendor-internal tooling, analytics/reporting, or bulk import/export tail to trim, so the full 35-operation spec is kept as-is.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`amazon_eks-2017-11-01.json`](./OpenAPIs/amazon_eks-2017-11-01.json) | Full spec for the Amazon EKS 2017-11-01 API. |

## Dependencies

| Dependency | Notes |
|---|---|
| Amazon EKS Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
