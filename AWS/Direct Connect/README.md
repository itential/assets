AWS Direct Connect creates dedicated private network connections between your data center or office and AWS, bypassing the public internet — it manages the connections, virtual interfaces, link aggregation groups (LAGs), and gateways that make up a Direct Connect deployment.

This project provides an OpenAPI spec for automating against the AWS Direct Connect API via an Integration Model. The `-latest` spec covers the full Direct Connect operation surface — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS Direct Connect API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| AWS Direct Connect API | 2012-10-25 |
| AWS Direct Connect Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import `aws_direct_connect-latest.json` from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the AWS Direct Connect endpoint (e.g. `directconnect.<region>.amazonaws.com`).

Authentication uses AWS Signature Version 4, sent in the `Authorization` header:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/directconnect/aws4_request, SignedHeaders=..., Signature=<signature>
```

Sign requests with an AWS access key ID and secret access key that has IAM permission to call the Direct Connect API. Generate or retrieve credentials in the AWS IAM console under your user's **Security credentials**.

## OpenAPIs

### `aws_direct_connect-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2012-10-25`). Left as the full, untrimmed spec — the AWS Direct Connect API is already a single, cohesive product surface (63 operations covering connections, virtual interfaces, gateways, LAGs, interconnects, and tagging), with no admin/reporting/bulk-import tail to remove.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`aws_direct_connect-2012-10-25.json`](./OpenAPIs/aws_direct_connect-2012-10-25.json) | Full spec for AWS Direct Connect API version 2012-10-25 (63 operations). |

## Dependencies

| Dependency | Notes |
|---|---|
| AWS Direct Connect Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
| AWS IAM credentials | Access key ID and secret access key with permission to call Direct Connect API actions. |
