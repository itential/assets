Amazon API Gateway is AWS's managed service for creating, publishing, and securing REST, HTTP, and WebSocket APIs. This folder covers the API Gateway management API — the control-plane operations used to define and operate REST APIs (resources, methods, integrations, deployments, stages, domain names, authorizers, and related configuration) rather than the runtime `execute-api` data plane.

This project provides an OpenAPI spec for automating against the API Gateway management REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`amazon_api_gateway-latest.json`](#amazon_api_gateway-latestjson)
  - [`amazon_api_gateway-2015-07-09.json`](#amazon_api_gateway-2015-07-09json)
- [Studio Projects](#studio-projects)
  - [Amazon API Gateway Project](#amazon-api-gateway-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Amazon API Gateway management API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/Amazon API Gateway](./Studio%20Projects/Amazon%20API%20Gateway.project.json) | 24 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Amazon API Gateway | `2015-07-09` API version |
| Amazon API Gateway Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the AWS API Gateway management endpoint (e.g. `apigateway.<region>.amazonaws.com`).

Authentication is AWS Signature Version 4 in the `Authorization` header:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/apigateway/aws4_request, SignedHeaders=..., Signature=<signature>
```

Sign requests with an AWS access key ID and secret access key belonging to an IAM user or role with the appropriate `apigateway:*` permissions. See [AWS Signature Version 4 signing](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) for details on constructing the signature.

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
    "host": "apigateway.us-east-1.amazonaws.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`amazon_api_gateway-latest.json`](./OpenAPIs/amazon_api_gateway-latest.json) | latest (curated) | 104 | Trimmed to 104 of 120 upstream operations covering common CRUD for automation — see breakdown below |
| [`amazon_api_gateway-2015-07-09.json`](./OpenAPIs/amazon_api_gateway-2015-07-09.json) | 2015-07-09 | 120 | Full spec for the Amazon API Gateway `2015-07-09` management API (120 operations). |

Both specs are converted in-house from **AWS's own official Amazon API Gateway service model** (`apigateway-2015-07-09.normal.json`, published by AWS at [`github.com/aws/aws-sdk-js`](https://github.com/aws/aws-sdk-js/blob/master/apis/apigateway-2015-07-09.normal.json) — the same machine-readable definition AWS uses to generate its own SDKs), not from a third-party OpenAPI conversion. AWS does not publish a ready-made OpenAPI/Swagger document for this service directly.

### `amazon_api_gateway-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2015-07-09`). Trimmed to 104 of 120 upstream operations covering common CRUD for automation.

Resources included, by category:

- **REST APIs**: REST APIs (incl. import), Resources, Methods, Integrations, Integration Responses, Method Responses
- **Deployments & Stages**: Deployments, Stages (incl. cache invalidation)
- **Custom Domains**: Domain Names, Base Path Mappings
- **Access Control**: API Keys (incl. import), Usage Plans, Usage Plan Keys, Authorizers, Client Certificates, VPC Links
- **API Configuration**: Models, Request Validators, Gateway Responses
- **Account & Tags**: Account settings, Resource Tags

Excluded as niche developer-tooling/reporting add-ons not core to REST API lifecycle automation: API documentation generation (Documentation Parts/Versions), SDK generation (SDK Types, SDK export), API definition export, and usage plan analytics (usage-by-date reporting).

### `amazon_api_gateway-2015-07-09.json`

Full spec, converted in-house from AWS's official service model, for the Amazon API Gateway `2015-07-09` management API (120 operations) — the entire upstream API surface as AWS defines it. See `amazon_api_gateway-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### Amazon API Gateway Project

Backed by the **`Amazon API Gateway:latest`** Integration Model (see [`amazon_api_gateway-latest.json`](./OpenAPIs/amazon_api_gateway-latest.json) above). The project contains **24 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| REST APIs | List, Create, Get, Update, Delete REST API | REST API lifecycle |
| Resources | List, Create, Get, Update, Delete Resource | Resource tree management |
| Methods | Get, Put, Update, Delete Method | Method definitions on a resource |
| Deployments | List, Create, Get, Update, Delete Deployment | Deployment lifecycle |
| Stages | List, Create, Get, Update, Delete Stage | Stage lifecycle |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Amazon API Gateway:latest` Integration Model | Import from [`amazon_api_gateway-latest.json`](./OpenAPIs/amazon_api_gateway-latest.json) before importing the project |
| `Amazon API Gateway` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Amazon API Gateway` — update the `adapter_id` value in each workflow task if yours is named differently |
