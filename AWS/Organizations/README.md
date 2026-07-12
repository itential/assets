AWS Organizations is AWS's account-management service for centrally governing multiple AWS accounts — creating and closing accounts, grouping them into organizational units, attaching service control and other policies, managing invitations between accounts, registering delegated administrators, and tagging organizational resources.

This project provides the OpenAPI spec for automating against the AWS Organizations API via an Integration Model.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | AWS Organizations API OpenAPI spec — `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| AWS Organizations API | 2016-11-28 |
| AWS Organizations Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the AWS Organizations endpoint for your region (e.g. `organizations.us-east-1.amazonaws.com`).

Authentication uses AWS Signature Version 4, signed with an AWS access key ID and secret access key, sent in the `Authorization` header:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/organizations/aws4_request, ...
```

Generate an access key ID and secret access key for an IAM principal with the appropriate Organizations permissions in the AWS IAM console under **Security credentials**. Note that most Organizations API calls must be made from (or on behalf of) the organization's management account or a registered delegated administrator account.

## OpenAPIs

### `aws_organizations-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2016-11-28`). This is the full, untouched upstream spec (55 operations) — AWS Organizations is already a single, narrow product surface covering account, organizational unit, policy, handshake (invitation), delegated administrator, service access, resource policy, and tagging management, so no trimming was applied.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`aws_organizations-2016-11-28.json`](./OpenAPIs/aws_organizations-2016-11-28.json) | Full spec for the AWS Organizations 2016-11-28 API. |

## Dependencies

| Dependency | Notes |
|---|---|
| AWS Organizations Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
| AWS IAM credentials | An access key ID/secret access key pair with Organizations permissions, used to sign requests with AWS Signature Version 4. |
