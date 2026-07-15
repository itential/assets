AWS Network Firewall is a managed, stateful network firewall and intrusion detection/prevention service for Amazon VPCs — it provides firewall policies, stateful and stateless rule groups, TLS inspection, subnet association, and logging configuration for traffic filtering across a VPC estate.

This project provides an OpenAPI spec for automating against the AWS Network Firewall REST API via an Integration Model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aws_network_firewall-latest.json`](#aws_network_firewall-latestjson)
  - [`aws_network_firewall-2020-11-12.json`](#aws_network_firewall-2020-11-12json)

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

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aws_network_firewall-latest.json`](./OpenAPIs/aws_network_firewall-latest.json) | latest (curated) | 36 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`aws_network_firewall-2020-11-12.json`](./OpenAPIs/aws_network_firewall-2020-11-12.json) | 2020-11-12 | 36 | Full, unmodified vendor spec |

### `aws_network_firewall-latest.json`

Reviewed and confirmed already scoped to common CRUD for automation (`x-vendor-api-version: 2020-11-12`, 36 operations). Every operation is CRUD or a provisioning action on the firewall/policy/rule-group resource model — there is no health, heartbeat, metrics, version-info, or other self-introspection surface to exclude, so nothing was removed.

Operations included, by category:

- **Firewalls**: Create, delete, describe, list; associate a firewall policy; associate/disassociate subnets; update delete-protection, description, encryption configuration, policy-change-protection, and subnet-change-protection flags
- **Firewall Policies**: Create, delete, describe, list, update
- **Rule Groups**: Create, delete, describe (and describe metadata), list, update
- **TLS Inspection Configurations**: Create, delete, describe, list, update
- **Logging Configuration**: Describe, update
- **Resource Policies** (cross-account sharing of rule groups/firewall policies): Put, describe, delete
- **Tags**: List tags for a resource; add/remove tags

### `aws_network_firewall-2020-11-12.json`

Full, unmodified vendor spec for API version 2020-11-12 (36 operations) — the vendor's complete API surface, preserved as-is. See `aws_network_firewall-latest.json` above for the curated `-latest` copy; per the review noted there, no operations were excluded, so both specs cover the same operation set.
