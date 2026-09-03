AWS Secrets Manager protects access to applications, services, and IT resources by enabling rotation, management, and retrieval of database credentials, API keys, and other secrets.

This project provides an OpenAPI spec for automating against the AWS Secrets Manager API via an Integration Model. AWS Secrets Manager's API surface is narrow and single-purpose, so the `-latest` spec was reviewed and curated for common CRUD automation.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aws_secrets_manager-latest.json`](#aws_secrets_manager-latestjson)
  - [`aws_secrets_manager-2017-10-17.json`](#aws_secrets_manager-2017-10-17json)
- [Secret Providers](#secret-providers)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS Secrets Manager API OpenAPI spec — curated `-latest` plus the full dated version |
| [secret-providers/](./secret-providers/) | IG5 custom secret-provider plugin — resolves AWS Secrets Manager secrets into Gateway secret aliases, usable in device inventory credentials and Gateway-executed Integration Model instances |

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
    "host": "secretsmanager.us-east-1.amazonaws.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aws_secrets_manager-latest.json`](./OpenAPIs/aws_secrets_manager-latest.json) | latest (curated) | 22 | Trimmed to 22 of 23 upstream operations — see breakdown below |
| [`aws_secrets_manager-2017-10-17.json`](./OpenAPIs/aws_secrets_manager-2017-10-17.json) | 2017-10-17 | 23 | Full spec for AWS Secrets Manager API version 2017-10-17. |

Both specs are converted in-house from **AWS's own official AWS Secrets Manager service model** (`secretsmanager-2017-10-17.normal.json`, published by AWS at [`github.com/aws/aws-sdk-js`](https://github.com/aws/aws-sdk-js/blob/master/apis/secretsmanager-2017-10-17.normal.json) — the same machine-readable definition AWS uses to generate its own SDKs), not from a third-party OpenAPI conversion. AWS does not publish a ready-made OpenAPI/Swagger document for this service directly.

### `aws_secrets_manager-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2017-10-17`). Trimmed to 22 of 23 upstream operations, all of which are core to secret lifecycle management. `BatchGetSecretValue` was added upstream since this spec was last reviewed and is not yet reviewed for inclusion. There is no separate health-check, heartbeat, metrics, or self-introspection/version-info surface in this API to exclude.

Operations included, by category:

- **Secrets**: Create, delete (scheduled or immediate), restore a pending-deletion secret, describe, list, update
- **Secret values/versions**: Get secret value, put (set) secret value, list version IDs, move/update a version's staging label
- **Rotation**: Start rotation, cancel an in-progress rotation
- **Resource policies**: Get, put, delete, validate (dry-run check of a policy document before applying it)
- **Cross-region replication**: Replicate a secret to regions, remove regions from replication, stop replication to a replica
- **Tagging**: Tag resource, untag resource
- **Utilities**: Generate a random password (used when creating secrets that need a generated value)

### `aws_secrets_manager-2017-10-17.json`

Full spec, converted in-house from AWS's official service model, for AWS Secrets Manager API version 2017-10-17 (23 operations) — the entire upstream API surface as AWS defines it. See `aws_secrets_manager-latest.json` above for the curated automation spec.

## Secret Providers

Separately from automating *against* AWS Secrets Manager via the Integration Model above, this product also ships a custom secret-provider plugin so **Itential Gateway** can resolve credentials *from* AWS Secrets Manager at runtime — for device inventory passwords or Gateway-executed Integration Model instances — instead of storing them in Gateway's own encrypted store.

See [secret-providers/README.md](./secret-providers/README.md) for full setup details: three ways to authenticate to AWS (EC2 instance role, IAM Roles Anywhere, or a static access key), registration steps, and how to reference the resulting alias.
