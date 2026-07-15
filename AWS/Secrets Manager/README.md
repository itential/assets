AWS Secrets Manager protects access to applications, services, and IT resources by enabling rotation, management, and retrieval of database credentials, API keys, and other secrets.

This project provides an OpenAPI spec for automating against the AWS Secrets Manager API via an Integration Model. AWS Secrets Manager's API surface is narrow and single-purpose, so the `-latest` spec was reviewed and curated for common CRUD automation.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aws_secrets_manager-latest.json`](#aws_secrets_manager-latestjson)
  - [`aws_secrets_manager-2017-10-17.json`](#aws_secrets_manager-2017-10-17json)

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

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aws_secrets_manager-latest.json`](./OpenAPIs/aws_secrets_manager-latest.json) | latest (curated) | 22 | Actively-maintained, reviewed and confirmed already scoped to core secret lifecycle management — see breakdown below |
| [`aws_secrets_manager-2017-10-17.json`](./OpenAPIs/aws_secrets_manager-2017-10-17.json) | 2017-10-17 | 22 | Full spec for AWS Secrets Manager API version 2017-10-17. |

### `aws_secrets_manager-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2017-10-17`). AWS Secrets Manager's entire API is 22 operations, all of which are core to secret lifecycle management, so the full upstream operation set is kept as-is — nothing was removed. There is no separate health-check, heartbeat, metrics, or self-introspection/version-info surface in this API to exclude.

Operations included, by category:

- **Secrets**: Create, delete (scheduled or immediate), restore a pending-deletion secret, describe, list, update
- **Secret values/versions**: Get secret value, put (set) secret value, list version IDs, move/update a version's staging label
- **Rotation**: Start rotation, cancel an in-progress rotation
- **Resource policies**: Get, put, delete, validate (dry-run check of a policy document before applying it)
- **Cross-region replication**: Replicate a secret to regions, remove regions from replication, stop replication to a replica
- **Tagging**: Tag resource, untag resource
- **Utilities**: Generate a random password (used when creating secrets that need a generated value)

### `aws_secrets_manager-2017-10-17.json`

Full, unmodified vendor spec for AWS Secrets Manager API version 2017-10-17 (22 operations) — the vendor's complete API surface, preserved as-is. See `aws_secrets_manager-latest.json` above for the curated automation spec; since AWS Secrets Manager's full API was already in scope for common CRUD, both specs cover the same 22 operations, but `-latest` is the one Studio Projects and new automation should target.
