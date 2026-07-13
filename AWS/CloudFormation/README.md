AWS CloudFormation is Amazon's infrastructure-as-code service. It lets you model, provision, and manage AWS and third-party resources using declarative templates, and it manages the full lifecycle of a deployment — called a stack — including change previews, rollback, and drift tracking.

This project provides an OpenAPI spec for automating against the CloudFormation API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for stack automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS CloudFormation API OpenAPI specs — curated `-latest` plus the full dated spec |

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

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`aws_cloudformation-latest.json`](./OpenAPIs/aws_cloudformation-latest.json) | latest (curated) | Trimmed to 74 of 132 upstream operations — see breakdown below |
| [`aws_cloudformation-2010-05-15.json`](./OpenAPIs/aws_cloudformation-2010-05-15.json) | 2010-05-15 | Full spec for the CloudFormation 2010-05-15 API (132 operations). |

### `aws_cloudformation-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2010-05-15`). Trimmed to 74 of 132 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Stacks**: Create, Update, Delete, Describe Stacks, Describe Stack Events, Describe Stack Resource(s), List Stacks, List Stack Resources, Get Template, Get Template Summary, Validate Template, Cancel Update, Continue Update Rollback, Rollback, Get/Set Stack Policy, Signal Resource, Update Termination Protection
- **Change Sets**: Create, Describe, Delete, Execute, List
- **StackSets**: Create, Update, Delete, Describe, List, Create/Update/Delete Stack Instances, Describe/List Stack Instances, List/Describe/Stop Stack Set Operations

Not included: type/extension registry management (`RegisterType`, `PublishType`, `ActivateType`, etc.), stack and resource drift detection, template cost estimation, export/import listing, and account limits — these are vendor tooling, reporting, or niche verticals rather than core stack automation. Pull the full spec below if you need something not covered here.
