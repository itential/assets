AWS Direct Connect creates dedicated private network connections between your data center or office and AWS, bypassing the public internet — it manages the connections, virtual interfaces, link aggregation groups (LAGs), and gateways that make up a Direct Connect deployment.

This project provides an OpenAPI spec for automating against the AWS Direct Connect API via an Integration Model. The `-latest` spec covers the full Direct Connect operation surface — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`aws_direct_connect-latest.json`](#aws_direct_connect-latestjson)
  - [`aws_direct_connect-2012-10-25.json`](#aws_direct_connect-2012-10-25json)

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

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`aws_direct_connect-latest.json`](./OpenAPIs/aws_direct_connect-latest.json) | latest (curated) | 63 | Actively-maintained, curated for common CRUD automation — see breakdown below |
| [`aws_direct_connect-2012-10-25.json`](./OpenAPIs/aws_direct_connect-2012-10-25.json) | 2012-10-25 | 63 | Full, unmodified vendor spec (63 operations) |

### `aws_direct_connect-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2012-10-25`, 63 operations). Every operation was checked individually against the upstream spec; all 63 are genuine CRUD/provisioning actions on Direct Connect's own resources (connections, virtual interfaces, gateways, LAGs, interconnects, BGP peers, tags) or the lookups needed to drive those actions (locations, router config, LOAs, customer agreements) — there is no health/heartbeat/metrics/version-info/self-introspection surface to exclude, so nothing was removed. The `security` block is already global (`hmac`), with no redundant per-operation overrides.

Operations included, by category:

- **Connections**: Create, delete, update, describe connections; confirm a connection; allocate a connection on an interconnect; allocate/associate/describe hosted connections; describe connections on an interconnect; get a connection's LOA-CFA
- **Link Aggregation Groups (LAGs)**: Create, delete, update, describe LAGs; associate/disassociate a connection with/from a LAG
- **Interconnects**: Create, delete, describe interconnects; get an interconnect's LOA-CFA
- **Virtual Interfaces**: Create/allocate private, public, and transit virtual interfaces; confirm private/public/transit virtual interfaces; delete, describe, associate virtual interfaces; update virtual interface attributes; describe virtual gateways
- **Direct Connect Gateways & Associations**: Create/delete/update/describe gateways; create/delete/update/describe gateway associations; create/delete/accept/describe gateway association proposals; describe gateway attachments
- **BGP Peering & Failover Testing**: Create/delete BGP peers; start/stop a BGP failover test; list virtual interface failover test history
- **MAC Security (MACsec)**: Associate/disassociate a MACsec key with a connection or interconnect
- **Letters of Authorization**: Get the LOA-CFA for a connection, interconnect, or LAG (generic lookup, in addition to the connection- and interconnect-specific variants above)
- **Locations & Router Configuration**: List the Direct Connect locations available for provisioning; describe a virtual interface's router configuration
- **Customer Agreements**: Describe customer metadata/agreements; confirm a customer agreement when creating a connection/LAG
- **Tagging**: Tag/untag resources; describe tags on a resource

### `aws_direct_connect-2012-10-25.json`

Full, unmodified vendor spec for AWS Direct Connect API version 2012-10-25 (63 operations) — the vendor's complete API surface, preserved as-is. See `aws_direct_connect-latest.json` above for the curated subset if you just need common CRUD automation.
