Amazon Elastic Kubernetes Service (EKS) is a managed Kubernetes service for running containerized applications on AWS without managing control plane infrastructure. It handles cluster lifecycle, managed node groups, Fargate profiles, add-ons, and identity provider integration for Kubernetes RBAC.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`amazon_eks-latest.json`](#amazon_eks-latestjson)
  - [`amazon_eks-2017-11-01.json`](#amazon_eks-2017-11-01json)

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

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "hmac": {
      "accessKeyId": "<your-aws-access-key-id>",
      "secretAccessKey": "<your-aws-secret-access-key>",
      "sessionToken": ""
    }
  },
  "server": {
    "protocol": "https",
    "host": "eks.us-east-1.amazonaws.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`amazon_eks-latest.json`](./OpenAPIs/amazon_eks-latest.json) | latest (curated) | 35 | Trimmed to 35 of 56 upstream operations — see breakdown below |
| [`amazon_eks-2017-11-01.json`](./OpenAPIs/amazon_eks-2017-11-01.json) | 2017-11-01 | 56 | Full spec for the Amazon EKS 2017-11-01 API. |

Both specs are converted in-house from **AWS's own official Amazon EKS service model** (`eks-2017-11-01.normal.json`, published by AWS at [`github.com/aws/aws-sdk-js`](https://github.com/aws/aws-sdk-js/blob/master/apis/eks-2017-11-01.normal.json) — the same machine-readable definition AWS uses to generate its own SDKs), not from a third-party OpenAPI conversion. AWS does not publish a ready-made OpenAPI/Swagger document for this service directly.

### `amazon_eks-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2017-11-01`). Trimmed to 35 of 56 upstream operations: every included operation manages an EKS cluster or one of its direct sub-resources (add-ons, managed node groups, Fargate profiles, identity provider configs, updates, tags, connected-cluster registrations). The 21 upstream operations added since this spec was last reviewed — Access Entries, Access Policies, Pod Identity Associations, EKS Anywhere Subscriptions, and cluster Insights — are not yet reviewed for inclusion; see the full spec if you need one of those areas in the meantime.

Operations included, by category:

- **Clusters**: Create, list, describe, delete; update config; list/describe/trigger cluster version updates
- **Encryption Config**: Associate an encryption configuration to a cluster
- **Identity Provider Configs** (Kubernetes RBAC integration): Associate, disassociate, describe, list
- **Add-ons**: Create, list, describe, delete, update; look up supported add-on versions and an add-on's configuration schema
- **Fargate Profiles**: Create, list, describe, delete
- **Managed Node Groups**: Create, list, describe, delete; update config; update Kubernetes/AMI version
- **Connected Cluster Registrations** (EKS Connector for external/on-prem clusters): Register, deregister
- **Tags**: List, add, remove tags on an EKS resource

### `amazon_eks-2017-11-01.json`

Full spec, converted in-house from AWS's official service model, for the Amazon EKS 2017-11-01 API (35 operations) — the entire upstream API surface as AWS defines it. See `amazon_eks-latest.json` above for the curated subset if you just need common CRUD automation.
