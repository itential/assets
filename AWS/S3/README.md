Amazon Simple Storage Service (S3) is AWS's object storage service, providing scalable storage for buckets and objects with configurable access control, encryption, versioning, lifecycle, and replication.

This project provides an OpenAPI spec for automating against the S3 REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for storage automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`amazon_s3-latest.json`](#amazon_s3-latestjson)
  - [`amazon_s3-2006-03-01.json`](#amazon_s3-2006-03-01json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Amazon S3 REST API OpenAPI spec — curated `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Amazon S3 | API version 2006-03-01 |
| Amazon S3 Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your AWS account/region.

S3 authenticates requests with AWS Signature Version 4, signed using your AWS access key ID and secret access key:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/s3/aws4_request, SignedHeaders=..., Signature=<signature>
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
    "host": "s3.us-east-1.amazonaws.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`amazon_s3-latest.json`](./OpenAPIs/amazon_s3-latest.json) | latest (curated) | 54 | Trimmed to 54 of 99 upstream operations covering common CRUD for automation — see breakdown below |
| [`amazon_s3-2006-03-01.json`](./OpenAPIs/amazon_s3-2006-03-01.json) | 2006-03-01 | 99 | Full spec for the Amazon S3 API (2006-03-01). |

Both specs are converted in-house from **AWS's own official Amazon S3 service model** (`s3-2006-03-01.normal.json`, published by AWS at [`github.com/aws/aws-sdk-js`](https://github.com/aws/aws-sdk-js/blob/master/apis/s3-2006-03-01.normal.json) — the same machine-readable definition AWS uses to generate its own SDKs), not from a third-party OpenAPI conversion. AWS does not publish a ready-made OpenAPI/Swagger document for this service directly.

### `amazon_s3-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2006-03-01`). Trimmed to 54 of 99 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Buckets**: Create, Delete, Head, List Buckets, List Objects (v1 and v2), Get Location, Get/Put Versioning
- **Bucket access control**: Get/Put ACL, Get/Put/Delete Policy, Get/Put/Delete Public Access Block, Get/Put/Delete Ownership Controls
- **Bucket configuration**: CORS, Encryption, Lifecycle Configuration, Tagging, Logging (get/put/delete as applicable)
- **Objects**: Put, Get, Head, Delete (single and bulk), Copy, Restore, List Object Versions
- **Object tagging and ACL**: Get/Put/Delete Tagging, Get/Put ACL
- **Multipart upload**: Create, Upload Part, Upload Part (Copy), Complete, Abort, List Parts, List Multipart Uploads

Not included: bucket analytics/inventory/metrics/intelligent-tiering configurations, transfer acceleration, request payer, notification configuration, replication, static website hosting, object lock/legal-hold/retention, S3 Select, object attributes, torrent, and S3 Object Lambda's WriteGetObjectResponse. Pull the full spec below if you need one of these.

### `amazon_s3-2006-03-01.json`

Full spec, converted in-house from AWS's official service model, for the Amazon S3 API (2006-03-01) (99 operations) — the entire upstream API surface as AWS defines it. See `amazon_s3-latest.json` above for the curated subset if you just need common CRUD automation.
