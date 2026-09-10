AWS Network Firewall is a managed, stateful network firewall and intrusion detection/prevention service for Amazon VPCs — it provides firewall policies, stateful and stateless rule groups, TLS inspection, subnet association, and logging configuration for traffic filtering across a VPC estate.

This project provides an OpenAPI spec for automating against the AWS Network Firewall REST API via an Integration Model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aws_network_firewall-latest.json`](#aws_network_firewall-latestjson)
  - [`aws_network_firewall-2020-11-12.json`](#aws_network_firewall-2020-11-12json)
- [Studio Projects](#studio-projects)
  - [AWS Network Firewall Project](#aws-network-firewall-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS Network Firewall API OpenAPI specs — `-latest` plus the full dated spec |
| [Studio Projects/AWS Network Firewall](./Studio%20Projects/AWS%20Network%20Firewall.project.json) | 23 workflows covering common CRUD automation |

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
    "host": "network-firewall.us-east-1.amazonaws.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aws_network_firewall-latest.json`](./OpenAPIs/aws_network_firewall-latest.json) | latest (curated) | 36 | Reviewed and confirmed already scoped to common CRUD for automation — see breakdown below |
| [`aws_network_firewall-2020-11-12.json`](./OpenAPIs/aws_network_firewall-2020-11-12.json) | 2020-11-12 | 36 | Full spec, converted in-house from AWS's official service model |

Both specs are converted in-house from **AWS's own official AWS Network Firewall service model** (`network-firewall-2020-11-12.normal.json`, published by AWS at [`github.com/aws/aws-sdk-js`](https://github.com/aws/aws-sdk-js/blob/master/apis/network-firewall-2020-11-12.normal.json) — the same machine-readable definition AWS uses to generate its own SDKs), not from a third-party OpenAPI conversion. AWS does not publish a ready-made OpenAPI/Swagger document for this service directly.

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

Full spec, converted in-house from AWS's official service model, for API version 2020-11-12 (36 operations) — the entire upstream API surface as AWS defines it. See `aws_network_firewall-latest.json` above for the curated `-latest` copy; per the review noted there, no operations were excluded, so both specs cover the same operation set.

---

## Studio Projects

### AWS Network Firewall Project

Backed by the **`AWS Network Firewall:latest`** Integration Model (see [`aws_network_firewall-latest.json`](./OpenAPIs/aws_network_firewall-latest.json) above). The project contains **23 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec. This is an AWS JSON-protocol API — every operation is a `POST` distinguished by a required `X-Amz-Target` header, which each workflow exposes as an input alongside the request body.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Firewalls | Create, Describe, List, Delete Firewall, Update Firewall Description | Firewall lifecycle |
| Firewall Policies | Create, Describe, List, Delete, Update Firewall Policy | Firewall policy management |
| Rule Groups | Create, Describe, List, Delete, Update Rule Group | Rule group management |
| TLS Inspection Configurations | Create, Describe, List, Delete, Update TLS Inspection Configuration | TLS inspection configuration management |
| Tags | List, Tag, Untag Resource | Tagging management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `AWS Network Firewall:latest` Integration Model | Import from [`aws_network_firewall-latest.json`](./OpenAPIs/aws_network_firewall-latest.json) before importing the project |
| `AWS Network Firewall` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `AWS Network Firewall` — update the `adapter_id` value in each workflow task if yours is named differently |
