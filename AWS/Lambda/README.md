AWS Lambda runs code without provisioning or managing servers, executing functions in response to events and automatically scaling to demand — covering function packaging, versioning, invocation, triggers, and the shared layers and permissions that surround them.

This project provides an OpenAPI spec for automating against the AWS Lambda API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS Lambda API OpenAPI spec — curated `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| AWS Lambda | API version 2015-03-31 |
| AWS Lambda Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the Lambda API endpoint for your AWS region.

Authentication is AWS Signature Version 4 — requests are signed using an AWS access key ID and secret access key:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/lambda/aws4_request, SignedHeaders=..., Signature=...
```

Generate an access key ID and secret access key for an IAM user or role with the required Lambda permissions in the AWS IAM console.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`aws_lambda-latest.json`](./OpenAPIs/aws_lambda-latest.json) | latest (curated) | Actively-maintained, curated for common CRUD automation — see breakdown below |
| [`aws_lambda-2015-03-31.json`](./OpenAPIs/aws_lambda-2015-03-31.json) | 2015-03-31 | Full spec for the AWS Lambda API (2015-03-31). |

### `aws_lambda-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2015-03-31`). Trimmed to 54 of 66 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Functions**: Create, Delete, Get, List, Update Code, Get/Update Configuration, Get/Delete Concurrency
- **Versions & Aliases**: Publish Version, List Versions by Function, Create/Get/Update/Delete Alias, List Aliases
- **Event Source Mappings (triggers)**: Create, Delete, Get, List, Update
- **Layers**: Publish Layer Version, Get/Delete Layer Version, Get Layer Version by ARN, List Layers, List Layer Versions, Add/Remove Layer Version Permission, Get Layer Version Policy
- **Function URLs**: Create, Delete, Get, Update Function URL Config, List Function URL Configs
- **Function Event Invoke Config (async invocation)**: Put, Get, Update, Delete, List
- **Provisioned Concurrency**: Put, Get, Delete Config, List Provisioned Concurrency Configs
- **Permissions**: Add/Remove Permission, Get Policy
- **Tags**: List, Tag, Untag Resource
- **Invocation**: Invoke, Invoke With Response Streaming
- **Account**: Get Account Settings, Get Function Concurrency

Not included: code signing configs (create/describe/update/delete config plus function code-signing-config associations), runtime management config (get/put), and the deprecated legacy `InvokeAsync` operation superseded by `Invoke`. Pull the full spec below if you need one of these.
