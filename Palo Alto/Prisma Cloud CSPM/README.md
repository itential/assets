# Palo Alto Prisma Cloud CSPM

Prisma Cloud CSPM is Palo Alto Networks' cloud security posture management product, providing continuous visibility, compliance monitoring, and threat detection across AWS, Azure, GCP, OCI, and Alibaba Cloud accounts.

This project provides OpenAPI specs for automating against the Prisma Cloud CSPM REST API via an Integration Model. Each `-latest` spec is scoped to one functional area of the API — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`palo_alto_prisma_cloud_cspm_alerts-latest.json`](#palo_alto_prisma_cloud_cspm_alerts-latestjson)
  - [`palo_alto_prisma_cloud_cspm_cloud_account_onboarding-latest.json`](#palo_alto_prisma_cloud_cspm_cloud_account_onboarding-latestjson)
  - [`palo_alto_prisma_cloud_cspm_alerts-v1.json`](#palo_alto_prisma_cloud_cspm_alerts-v1json)
  - [`palo_alto_prisma_cloud_cspm_cloud_account_onboarding-v1.json`](#palo_alto_prisma_cloud_cspm_cloud_account_onboarding-v1json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Prisma Cloud CSPM REST API OpenAPI specs — curated `-latest` plus full dated versions, split by functional area (Alerts, Cloud Account Onboarding) |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Prisma Cloud CSPM | v1 API (see OpenAPIs below for exact spec versions available) |
| Prisma Cloud CSPM Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Prisma Cloud tenant's API endpoint (e.g. `api.prismacloud.io`, or the region-specific endpoint for your tenant).

Authentication is a JSON Web Token (JWT) in the `x-redlock-auth` header:

```
x-redlock-auth: <jwt>
```

Obtain a JWT by calling `POST /login` with your Prisma Cloud access key ID and secret key (generated in the Prisma Cloud console under **Settings > Access Keys**). The JWT expires after a period of time and must be refreshed by calling `/login` again.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`palo_alto_prisma_cloud_cspm_alerts-latest.json`](./OpenAPIs/palo_alto_prisma_cloud_cspm_alerts-latest.json) | latest (curated) | Actively-maintained spec, left as the full upstream spec — see breakdown below |
| [`palo_alto_prisma_cloud_cspm_cloud_account_onboarding-latest.json`](./OpenAPIs/palo_alto_prisma_cloud_cspm_cloud_account_onboarding-latest.json) | latest (curated) | Actively-maintained spec, trimmed to 50 of 52 upstream operations — see breakdown below |
| [`palo_alto_prisma_cloud_cspm_alerts-v1.json`](./OpenAPIs/palo_alto_prisma_cloud_cspm_alerts-v1.json) | v1 | Full spec for the Prisma Cloud CSPM Alerts API v1. |
| [`palo_alto_prisma_cloud_cspm_cloud_account_onboarding-v1.json`](./OpenAPIs/palo_alto_prisma_cloud_cspm_cloud_account_onboarding-v1.json) | v1 | Full spec for the Prisma Cloud CSPM Cloud Account Onboarding API v1. |

### `palo_alto_prisma_cloud_cspm_alerts-latest.json`

Actively-maintained spec (`x-vendor-api-version: v1`). Left as the full upstream spec (25 operations) — every operation is a genuine read, write, or provisioning action against the `alert` resource itself; there's no health/heartbeat/metrics, version-info, or other server-housekeeping surface to trim.

Operations included, by category:

- **Alert listing/query**: List Alerts (GET/POST), List Alerts V2 (GET/POST), Get Alert Info by ID, Get Alerts Count By Status
- **Alert filtering**: List Alert Filters, List Alert Filter Autocomplete Suggestions
- **Alert counts by policy**: Get Alert Counts By Policy (GET/POST)
- **Alert status actions**: Dismiss Alerts, Reopen Alerts
- **Dismissal note setting**: Get/Update whether a dismissal note is required
- **Remediation**: List Alert Remediation Commands, Remediate Alert by ID
- **Async export jobs**: Submit/poll/download alerts-list job (JSON), submit/poll/download alert CSV job, submit/poll/download policy-alerts job (JSON)

### `palo_alto_prisma_cloud_cspm_cloud_account_onboarding-latest.json`

Actively-maintained spec (`x-vendor-api-version: v1`). Trimmed to 50 of 52 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Cloud Accounts**: Add, Update, Get, Delete, and List Cloud Accounts (AWS, Azure, GCP, OCI, Alibaba), Get Cloud Account Status, Get Cloud Account Details, List Cloud Account Names/Types, List Cloud Account Owners, Update Cloud Account Status
- **Cloud Account Hierarchy**: List Ancestors, List Children of Parent, List Folders/Projects of Parent (AWS, Azure, GCP), Get Saved Resource Hierarchy (GCP)
- **AWS Logging Accounts**: Add, Update, Get, Delete, and List AWS Logging Accounts; Generate/Regenerate CFT Templates; manage associated S3 buckets; Get Logging Account Status and External ID
- **Terraform**: Generate Zipped Terraform Script (OCI)

Removed the two vendor-marked "Legacy" AWS ancestor/children endpoints (`/cloud-accounts-manager/v1/cloudAccounts/awsAccounts/.../ancestors` and `.../children`), which are superseded by their `/cas/v1/aws_account/...` equivalents already in the spec.

### `palo_alto_prisma_cloud_cspm_alerts-v1.json`

Full, unmodified vendor spec for the Prisma Cloud CSPM Alerts API v1 (25 operations) — the vendor's complete API surface, preserved as-is. See `palo_alto_prisma_cloud_cspm_alerts-latest.json` above, which carries through the same 25 operations since none were trimmed.

### `palo_alto_prisma_cloud_cspm_cloud_account_onboarding-v1.json`

Full, unmodified vendor spec for the Prisma Cloud CSPM Cloud Account Onboarding API v1 (52 operations) — the vendor's complete API surface, preserved as-is. See `palo_alto_prisma_cloud_cspm_cloud_account_onboarding-latest.json` above for the curated subset if you just need common CRUD automation.
