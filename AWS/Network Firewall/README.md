AWS Network Firewall is a managed, stateful network firewall and intrusion detection/prevention service for Amazon VPCs — it provides firewall policies, stateful and stateless rule groups, TLS inspection, subnet association, and logging configuration for traffic filtering across a VPC estate.

This project provides an OpenAPI spec for automating against the AWS Network Firewall REST API via an Integration Model.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS Network Firewall API OpenAPI specs — `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| AWS Network Firewall API | 2020-11-12 |
| AWS Network Firewall Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the AWS Network Firewall service endpoint for your region.

Authentication uses AWS Signature Version 4 — requests are signed with an AWS access key ID and secret access key in the `Authorization` header:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/network-firewall/aws4_request, SignedHeaders=..., Signature=<signature>
```

Generate an access key ID and secret access key for an IAM user or role with `network-firewall:*` permissions under **IAM > Users/Roles > Security credentials**.

## OpenAPIs

### `aws_network_firewall-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2020-11-12`). This is the complete, unmodified AWS Network Firewall API surface (36 operations) — the upstream API is already scoped to a single, cohesive product (firewalls, firewall policies, rule groups, TLS inspection configurations, logging, and resource sharing), so no trimming was applied.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`aws_network_firewall-2020-11-12.json`](./OpenAPIs/aws_network_firewall-2020-11-12.json) | Full spec for AWS Network Firewall API version 2020-11-12 (36 operations). |

## Dependencies

| Dependency | Notes |
|---|---|
| AWS Network Firewall Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
