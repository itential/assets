Amazon API Gateway is AWS's managed service for creating, publishing, and securing REST, HTTP, and WebSocket APIs. This folder covers the API Gateway management API — the control-plane operations used to define and operate REST APIs (resources, methods, integrations, deployments, stages, domain names, authorizers, and related configuration) rather than the runtime `execute-api` data plane.

This project provides an OpenAPI spec for automating against the API Gateway management REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`amazon_api_gateway-latest.json`](#amazon_api_gateway-latestjson)
  - [`amazon_api_gateway-2015-07-09.json`](#amazon_api_gateway-2015-07-09json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Amazon API Gateway management API OpenAPI specs — curated `-latest` plus the full dated spec |

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

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`amazon_api_gateway-latest.json`](./OpenAPIs/amazon_api_gateway-latest.json) | latest (curated) | Trimmed to 104 of 120 upstream operations covering common CRUD for automation — see breakdown below |
| [`amazon_api_gateway-2015-07-09.json`](./OpenAPIs/amazon_api_gateway-2015-07-09.json) | 2015-07-09 | Full spec for the Amazon API Gateway `2015-07-09` management API (120 operations). |

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

Full, unmodified vendor spec for the Amazon API Gateway `2015-07-09` management API (120 operations) — the vendor's complete API surface, preserved as-is. See `amazon_api_gateway-latest.json` above for the curated subset if you just need common CRUD automation.
