Amazon Route 53 is AWS's Domain Name System (DNS) web service, used to register domains, manage hosted zones and DNS records, and configure health checks and routing for internet applications.

This project provides an OpenAPI spec for automating against the Route 53 REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for DNS automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Amazon Route 53 REST API OpenAPI spec — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Amazon Route 53 | 2013-04-01 API |
| Amazon Route 53 Integration Model | Required to build automation against the OpenAPI spec |
| AWS IAM credentials | An access key ID and secret access key with `route53:*` permissions for the operations you automate |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the Route 53 endpoint (`https://route53.amazonaws.com`).

Route 53 authenticates requests with **AWS Signature Version 4 (SigV4)**, not a static bearer token. Each request must carry a signed `Authorization` header computed from an AWS access key ID and secret access key:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/route53/aws4_request, SignedHeaders=..., Signature=<signature>
```

Generate an access key ID and secret access key for an IAM user or role with Route 53 permissions in the AWS Console under **IAM > Users > Security credentials**, then configure your integration's connection to sign requests with SigV4 using those credentials.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`amazon_route_53-latest.json`](./OpenAPIs/amazon_route_53-latest.json) | latest (curated) | Actively-maintained, trimmed to common CRUD for automation — see breakdown below |
| [`amazon_route_53-2013-04-01.json`](./OpenAPIs/amazon_route_53-2013-04-01.json) | 2013-04-01 | Full spec for the Route 53 2013-04-01 API (70 operations). |

### `amazon_route_53-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2013-04-01`). Trimmed to 23 of 70 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Hosted Zones**: List, Create, Get, Update Comment, Delete
- **Resource Record Sets**: List, Change (create/upsert/delete DNS records)
- **Change Tracking**: Get Change (poll propagation status of a record change)
- **VPC Associations**: Associate/Disassociate a Private Hosted Zone with a VPC, List/Create/Delete Cross-Account VPC Association Authorizations
- **Health Checks**: List, Create, Get, Update, Delete, Get Status, Get Last Failure Reason
- **Tags**: List Tags for a Resource, List Tags for Multiple Resources, Change Tags for a Resource

Not included: CIDR collections, DNSSEC/key-signing key management, traffic policies and traffic policy instances, query logging configuration, reusable delegation sets, account/resource limit and count lookups, checker IP ranges, geolocation lookups, and the DNS answer test tool. Pull the full spec above if you need one of those areas.

## Dependencies

| Dependency | Notes |
|---|---|
| Amazon Route 53 Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
| AWS IAM credentials | Used to sign requests with AWS Signature Version 4. |
