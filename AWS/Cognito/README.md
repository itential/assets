Amazon Cognito User Pools provides user directory and authentication functionality for web and mobile applications — user sign-up/sign-in, admin user management, groups, MFA, remembered devices, identity provider federation, and OAuth resource servers.

This project provides an OpenAPI spec for automating against the Cognito User Pools REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Amazon Cognito User Pools REST API OpenAPI spec — curated `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Amazon Cognito User Pools | API version 2016-04-18 |
| Amazon Cognito User Pools Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your AWS account/region.

Cognito authenticates requests with AWS Signature Version 4, signed using your AWS access key ID and secret access key:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/cognito-idp/aws4_request, SignedHeaders=..., Signature=<signature>
```

Generate an access key ID and secret access key in the AWS IAM console under your user → **Security credentials** → **Access keys**.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`amazon_cognito_user_pools-latest.json`](./OpenAPIs/amazon_cognito_user_pools-latest.json) | latest (curated) | Trimmed to 87 of 101 upstream operations covering common CRUD for automation — see breakdown below |
| [`amazon_cognito_user_pools-2016-04-18.json`](./OpenAPIs/amazon_cognito_user_pools-2016-04-18.json) | 2016-04-18 | Full spec for the Amazon Cognito User Pools API (2016-04-18). |

### `amazon_cognito_user_pools-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2016-04-18`). Trimmed to 87 of 101 upstream operations covering common CRUD for automation.

Resources included, by category:

- **User pools**: Create, Describe, Update, Delete, List, Add Custom Attributes, Get/Set MFA Configuration
- **App clients**: Create, Describe, Update, Delete, List
- **Domains**: Create, Describe, Update, Delete
- **Users (admin)**: Create, Get, Update Attributes, Delete, Delete Attributes, Disable, Enable, Set/Reset Password, Confirm Sign-Up, Global Sign-Out, Set User Settings, List Users
- **Users (self-service)**: Sign-Up, Confirm Sign-Up, Get/Update/Delete Attributes, Get Attribute Verification Code, Verify Attribute, Resend Confirmation Code, Change Password, Forgot/Confirm Forgot Password, Global Sign-Out, Set User Settings
- **Authentication**: Initiate Auth, Respond to Auth Challenge (standard and admin), Revoke Token
- **MFA**: Associate/Verify Software Token, Set MFA Preference (standard and admin)
- **Groups**: Create, Get, Update, Delete, List, List Users in Group, Add/Remove User to/from Group (admin), List Groups for User (admin)
- **Devices**: Confirm, Get, Forget, List, Update Status (standard and admin)
- **Identity providers**: Create, Describe, Update, Delete, List, Get by Identifier, Disable/Link Provider for User (admin)
- **Resource servers**: Create, Describe, Update, Delete, List
- **Tags**: Tag Resource, Untag Resource, List Tags for Resource

Not included: user import jobs (bulk CSV import via S3), advanced security/risk configuration, hosted UI customization, auth event feedback/analytics, and signing certificate retrieval. Pull the full spec below if you need one of these.

## Dependencies

| Dependency | Notes |
|---|---|
| Amazon Cognito User Pools Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
