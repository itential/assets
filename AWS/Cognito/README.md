Amazon Cognito User Pools provides user directory and authentication functionality for web and mobile applications — user sign-up/sign-in, admin user management, groups, MFA, remembered devices, identity provider federation, and OAuth resource servers.

This project provides an OpenAPI spec for automating against the Cognito User Pools REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`amazon_cognito_user_pools-latest.json`](#amazon_cognito_user_pools-latestjson)
  - [`amazon_cognito_user_pools-2016-04-18.json`](#amazon_cognito_user_pools-2016-04-18json)
- [Studio Projects](#studio-projects)
  - [Amazon Cognito User Pools Project](#amazon-cognito-user-pools-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Amazon Cognito User Pools REST API OpenAPI spec — curated `-latest` plus the full dated version |
| [Studio Projects/Amazon Cognito User Pools](./Studio%20Projects/Amazon%20Cognito%20User%20Pools.project.json) | 30 workflows covering common CRUD automation |

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
    "host": "cognito-idp.us-east-1.amazonaws.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`amazon_cognito_user_pools-latest.json`](./OpenAPIs/amazon_cognito_user_pools-latest.json) | latest (curated) | 87 | Trimmed to 87 of 103 upstream operations covering common CRUD for automation — see breakdown below |
| [`amazon_cognito_user_pools-2016-04-18.json`](./OpenAPIs/amazon_cognito_user_pools-2016-04-18.json) | 2016-04-18 | 103 | Full spec for the Amazon Cognito User Pools API (2016-04-18). |

Both specs are converted in-house from **AWS's own official Amazon Cognito User Pools service model** (`cognito-idp-2016-04-18.normal.json`, published by AWS at [`github.com/aws/aws-sdk-js`](https://github.com/aws/aws-sdk-js/blob/master/apis/cognito-idp-2016-04-18.normal.json) — the same machine-readable definition AWS uses to generate its own SDKs), not from a third-party OpenAPI conversion. AWS does not publish a ready-made OpenAPI/Swagger document for this service directly.

### `amazon_cognito_user_pools-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2016-04-18`). Trimmed to 87 of 103 upstream operations covering common CRUD for automation.

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

### `amazon_cognito_user_pools-2016-04-18.json`

Full spec, converted in-house from AWS's official service model, for the Amazon Cognito User Pools API (2016-04-18) — the entire upstream API surface as AWS defines it (103 operations). See `amazon_cognito_user_pools-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### Amazon Cognito User Pools Project

Backed by the **`Amazon Cognito User Pools:latest`** Integration Model (see [`amazon_cognito_user_pools-latest.json`](./OpenAPIs/amazon_cognito_user_pools-latest.json) above). The project contains **30 workflows** organized into **6 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

Cognito User Pools is an AWS JSON-protocol API — every operation is a `POST` whose `X-Amz-Target` header is a fixed single-value constant already baked into the operation's path, not real user input, so it's omitted from each workflow's input schema in favor of the single `requestBody` (JSON) parameter.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| User Pools | List, Create, Describe, Update, Delete User Pool | User pool lifecycle |
| App Clients | List, Create, Describe, Update, Delete User Pool Client | App client lifecycle |
| Users | List Users, Admin Create/Get/Update Attributes/Delete User | Admin user lifecycle |
| Groups | List, Create, Get, Update, Delete Group | Group management |
| Identity Providers | List, Create, Describe, Update, Delete Identity Provider | Federation configuration |
| Resource Servers | List, Create, Describe, Update, Delete Resource Server | OAuth resource server management |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Amazon Cognito User Pools:latest` Integration Model | Import from [`amazon_cognito_user_pools-latest.json`](./OpenAPIs/amazon_cognito_user_pools-latest.json) before importing the project |
| `Amazon Cognito User Pools` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Amazon Cognito User Pools` — update the `adapter_id` value in each workflow task if yours is named differently |
