Amazon Connect is AWS's cloud-based contact center service, providing telephony, chat, and task management along with the agents, queues, routing profiles, and contact flows used to run a customer contact center.

This project provides OpenAPI specs for automating against the Amazon Connect API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for contact center automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`amazon_connect-latest.json`](#amazon_connect-latestjson)
  - [`amazon_connect-2017-08-08.json`](#amazon_connect-2017-08-08json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Amazon Connect API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Amazon Connect | API version 2017-08-08 |
| Amazon Connect Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the Amazon Connect API endpoint for your AWS region.

Authentication is AWS Signature Version 4 — requests are signed using an AWS access key ID and secret access key:

```
Authorization: AWS4-HMAC-SHA256 Credential=<access-key-id>/<date>/<region>/connect/aws4_request, SignedHeaders=..., Signature=...
```

Generate an access key ID and secret access key for an IAM user or role with the required Amazon Connect permissions in the AWS IAM console.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`amazon_connect-latest.json`](./OpenAPIs/amazon_connect-latest.json) | latest (curated) | 96 | Actively-maintained, trimmed to 96 of 171 upstream operations covering common CRUD for automation — see breakdown below |
| [`amazon_connect-2017-08-08.json`](./OpenAPIs/amazon_connect-2017-08-08.json) | 2017-08-08 | 171 | Full spec for Amazon Connect API version 2017-08-08 (171 operations). |

### `amazon_connect-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2017-08-08`). Trimmed to 96 of 171 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Instances**: List, Create, Describe, Delete
- **Users**: List, Create, Describe, Delete, Update Identity Info, Update Phone Config, Update Routing Profile, Update Security Profiles, Update Hierarchy, Put Status
- **Agent Statuses**: List, Create, Describe, Update
- **User Hierarchy Groups**: List, Create, Describe, Delete, Update Name; Describe/Update Hierarchy Structure
- **Queues**: List, Create, Describe, Update Name/Hours of Operation/Max Contacts/Outbound Caller Config/Status, Associate/Disassociate Quick Connects, List Quick Connects
- **Routing Profiles**: List, Create, Describe, Update Name/Concurrency/Default Outbound Queue/Queues, Associate/Disassociate Queues, List Queues
- **Quick Connects**: List, Create, Describe, Delete, Update Config/Name
- **Hours of Operations**: List, Create, Describe, Update, Delete
- **Security Profiles**: List, Create, Describe, Update, Delete, List Permissions
- **Contact Flows**: List, Create, Describe, Delete, Update Content/Metadata/Name
- **Contact Flow Modules**: List, Create, Describe, Delete, Update Content/Metadata
- **Phone Numbers**: List, Claim, Search Available, Describe, Update, Release, Associate/Disassociate Contact Flow
- **Contacts**: Describe, Update, Update/Get Attributes, Start Chat/Outbound Voice/Task Contact, Stop, Transfer
- **Tags**: List, Tag, Untag Resource

Not included: real-time and historical metrics/reporting, custom vocabularies (Contact Lens transcription), traffic distribution groups (multi-region resiliency), contact automation rules, Lex/Amazon Lex V2 bot and Lambda function associations, instance storage/security-key/approved-origin/integration-association configuration, task templates, chat participant and contact-monitoring/recording/streaming controls, federation tokens, and the `Search*` filtering variants of the list operations above. Pull the full spec below if you need one of these.

### `amazon_connect-2017-08-08.json`

Full, unmodified vendor spec for Amazon Connect API version 2017-08-08 (171 operations) — the vendor's complete API surface, preserved as-is. See `amazon_connect-latest.json` above for the curated subset if you just need common CRUD automation.
