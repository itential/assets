AWS Secrets Manager protects access to applications, services, and IT resources by enabling rotation, management, and retrieval of database credentials, API keys, and other secrets.

This project provides an OpenAPI spec for automating against the AWS Secrets Manager API via an Integration Model. AWS Secrets Manager's API surface is narrow and single-purpose, so the `-latest` spec is the full upstream operation set — no trimming was needed.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS Secrets Manager API OpenAPI spec — curated `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| AWS Secrets Manager | API version 2017-10-17 |
| AWS Secrets Manager Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import `aws_secrets_manager-latest.json` from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the AWS Secrets Manager endpoint for your region (e.g. `secretsmanager.<region>.amazonaws.com`).

Authentication uses AWS Signature Version 4 — requests are signed with your AWS access key ID and secret access key:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/secretsmanager/aws4_request, SignedHeaders=..., Signature=<signature>
```

Generate an access key ID and secret access key in the AWS IAM console under **Users → Security credentials → Access keys**. The IAM principal used must be granted the relevant `secretsmanager:*` permissions for the operations it will call.

## OpenAPIs

### `aws_secrets_manager-latest.json` (full spec, untrimmed)

Actively-maintained spec (`x-vendor-api-version: 2017-10-17`). AWS Secrets Manager's entire API is 22 operations, all of which are core to secret lifecycle management, so the full upstream operation set is kept as-is — nothing was removed.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`aws_secrets_manager-2017-10-17.json`](./OpenAPIs/aws_secrets_manager-2017-10-17.json) | Full spec for AWS Secrets Manager API version 2017-10-17. |

## Dependencies

| Dependency | Notes |
|---|---|
| AWS Secrets Manager Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
