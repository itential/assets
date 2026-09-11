AWS Lambda runs code without provisioning or managing servers, executing functions in response to events and automatically scaling to demand — covering function packaging, versioning, invocation, triggers, and the shared layers and permissions that surround them.

This project provides an OpenAPI spec for automating against the AWS Lambda API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aws_lambda-latest.json`](#aws_lambda-latestjson)
  - [`aws_lambda-2015-03-31.json`](#aws_lambda-2015-03-31json)
- [Studio Projects](#studio-projects)
  - [AWS Lambda Project](#aws-lambda-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS Lambda API OpenAPI spec — curated `-latest` plus the full dated version |
| [Studio Projects/AWS Lambda](./Studio%20Projects/AWS%20Lambda.project.json) | 30 workflows covering common CRUD automation |

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
    "host": "lambda.us-east-1.amazonaws.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aws_lambda-latest.json`](./OpenAPIs/aws_lambda-latest.json) | latest (curated) | 54 | Actively-maintained, curated for common CRUD automation — see breakdown below |
| [`aws_lambda-2015-03-31.json`](./OpenAPIs/aws_lambda-2015-03-31.json) | 2015-03-31 | 68 | Full spec for the AWS Lambda API (2015-03-31). |

Both specs are converted in-house from **AWS's own official AWS Lambda service model** (`lambda-2015-03-31.normal.json`, published by AWS at [`github.com/aws/aws-sdk-js`](https://github.com/aws/aws-sdk-js/blob/master/apis/lambda-2015-03-31.normal.json) — the same machine-readable definition AWS uses to generate its own SDKs), not from a third-party OpenAPI conversion. AWS does not publish a ready-made OpenAPI/Swagger document for this service directly.

### `aws_lambda-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2015-03-31`). Trimmed to 54 of 68 upstream operations covering common CRUD for automation.

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

### `aws_lambda-2015-03-31.json`

Full spec, converted in-house from AWS's official service model, for the AWS Lambda API (2015-03-31) — the entire upstream API surface as AWS defines it. See `aws_lambda-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### AWS Lambda Project

Backed by the **`AWS Lambda:latest`** Integration Model (see [`aws_lambda-latest.json`](./OpenAPIs/aws_lambda-latest.json) above). The project contains **30 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Functions | Create, List, Get Function, Get/Update Configuration, Update Code, Delete, Invoke | Function lifecycle and invocation |
| Aliases | Create, List, Get, Update, Delete Alias | Alias management |
| Event Source Mappings | Create, List, Get, Update, Delete Event Source Mapping | Trigger management |
| Function URL Config | Create, Get, Update, Delete Function Url Config | Function URL configuration |
| Layers | Publish Layer Version, List Layers, List/Get Layer Version, Delete Layer Version | Layer management |
| Tags | List, Tag, Untag Resource | Tagging management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `AWS Lambda:latest` Integration Model | Import from [`aws_lambda-latest.json`](./OpenAPIs/aws_lambda-latest.json) before importing the project |
| `AWS Lambda` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `AWS Lambda` — update the `adapter_id` value in each workflow task if yours is named differently |
