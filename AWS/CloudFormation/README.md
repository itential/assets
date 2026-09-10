AWS CloudFormation is Amazon's infrastructure-as-code service. It lets you model, provision, and manage AWS and third-party resources using declarative templates, and it manages the full lifecycle of a deployment — called a stack — including change previews, rollback, and drift tracking.

This project provides an OpenAPI spec for automating against the CloudFormation API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for stack automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aws_cloudformation-latest.json`](#aws_cloudformation-latestjson)
  - [`aws_cloudformation-2010-05-15.json`](#aws_cloudformation-2010-05-15json)
- [Studio Projects](#studio-projects)
  - [AWS CloudFormation Project](#aws-cloudformation-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS CloudFormation API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/AWS CloudFormation](./Studio%20Projects/AWS%20CloudFormation.project.json) | 19 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| AWS CloudFormation API | 2010-05-15 |
| AWS CloudFormation Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the CloudFormation endpoint for your target AWS region (e.g. `cloudformation.us-east-1.amazonaws.com`).

Authentication is AWS Signature Version 4 — every request is signed with an AWS access key ID and secret access key:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/cloudformation/aws4_request, SignedHeaders=..., Signature=<signature>
```

Generate an access key ID and secret access key in the AWS Console under **IAM > Users > Security credentials**, scoped to a role with the CloudFormation permissions your automation needs.

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
    "host": "cloudformation.us-east-1.amazonaws.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aws_cloudformation-latest.json`](./OpenAPIs/aws_cloudformation-latest.json) | latest (curated) | 74 | Trimmed to 74 of 164 upstream operations — see breakdown below |
| [`aws_cloudformation-2010-05-15.json`](./OpenAPIs/aws_cloudformation-2010-05-15.json) | 2010-05-15 | 164 | Full spec for the CloudFormation 2010-05-15 API (164 operations). |

Both specs are converted in-house from **AWS's own official AWS CloudFormation service model** (`cloudformation-2010-05-15.normal.json`, published by AWS at [`github.com/aws/aws-sdk-js`](https://github.com/aws/aws-sdk-js/blob/master/apis/cloudformation-2010-05-15.normal.json) — the same machine-readable definition AWS uses to generate its own SDKs), not from a third-party OpenAPI conversion. AWS does not publish a ready-made OpenAPI/Swagger document for this service directly.

### `aws_cloudformation-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2010-05-15`). Trimmed to 74 of 164 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Stacks**: Create, Update, Delete, Describe Stacks, Describe Stack Events, Describe Stack Resource(s), List Stacks, List Stack Resources, Get Template, Get Template Summary, Validate Template, Cancel Update, Continue Update Rollback, Rollback, Get/Set Stack Policy, Signal Resource, Update Termination Protection
- **Change Sets**: Create, Describe, Delete, Execute, List
- **StackSets**: Create, Update, Delete, Describe, List, Create/Update/Delete Stack Instances, Describe/List Stack Instances, List/Describe/Stop Stack Set Operations

Not included: type/extension registry management (`RegisterType`, `PublishType`, `ActivateType`, etc.), stack and resource drift detection, template cost estimation, export/import listing, and account limits — these are vendor tooling, reporting, or niche verticals rather than core stack automation. Pull the full spec below if you need something not covered here.

### `aws_cloudformation-2010-05-15.json`

Full spec, converted in-house from AWS's official service model, for the CloudFormation 2010-05-15 API (164 operations) — the entire upstream API surface as AWS defines it. See `aws_cloudformation-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### AWS CloudFormation Project

Backed by the **`AWS CloudFormation:latest`** Integration Model (see [`aws_cloudformation-latest.json`](./OpenAPIs/aws_cloudformation-latest.json) above). The project contains **19 workflows** organized into **4 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

CloudFormation is an AWS query-protocol API — every operation is a `POST` whose `Action`/`Version` query parameters are fixed single-value constants already baked into the operation's path, not real user input, so those are omitted from each workflow's input schema in favor of the single `requestBody` (XML) parameter.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Stacks | List, Create, Describe, Update, Delete Stack | Stack lifecycle |
| Change Sets | List, Create, Describe, Execute, Delete Change Set | Change preview and execution |
| StackSets | List, Create, Describe, Update, Delete StackSet | Multi-account/region StackSet management |
| Stack Instances | List, Create, Update, Delete Stack Instances | StackSet instance management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `AWS CloudFormation:latest` Integration Model | Import from [`aws_cloudformation-latest.json`](./OpenAPIs/aws_cloudformation-latest.json) before importing the project |
| `AWS CloudFormation` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `AWS CloudFormation` — update the `adapter_id` value in each workflow task if yours is named differently |
