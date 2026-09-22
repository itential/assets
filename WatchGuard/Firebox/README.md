# Firebox

WatchGuard Firebox is a line of network security appliances (UTM/next-gen firewalls) managed centrally through WatchGuard Cloud, providing firewall policy enforcement, VPN, intrusion prevention, web/content filtering, and related network security controls.

This project provides an OpenAPI spec for automating against the Firebox Management API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`watchguard_firebox-latest.json`](#watchguard_firebox-latestjson)
  - [`watchguard_firebox-1.29.0.json`](#watchguard_firebox-1290json)
- [Studio Projects](#studio-projects)
  - [`WatchGuard Firebox.project.json`](#watchguard-fireboxprojectjson)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Firebox Management API OpenAPI specs |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing 84 workflows in 25 resource-category folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `WatchGuard Firebox:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Fireboxes are managed through WatchGuard Cloud, so all requests target a regional WatchGuard Cloud API host, not the Firebox appliance directly.

Authentication requires **two independent, simultaneously-required credentials** on every request:

1. **OAuth 2.0 client credentials bearer token** — exchange your WatchGuard Cloud API Access ID/Password for a short-lived `access_token` by POSTing to `/oauth/token` (form-urlencoded body, `grant_type=client_credentials&scope=api-access`) with your Access ID/Password sent as an HTTP Basic `Authorization` header. The resulting token is replayed as `Bearer <access_token>` on the `Authorization` header; it expires after 3600 seconds and Itential Platform re-retrieves it automatically. Modeled as the `oauth2ClientCredentials` security scheme (native OAuth2 client-credentials support).
2. **Static `WatchGuard-API-Key` header** — your account's API Key from the WatchGuard Cloud Managed Access page, sent unchanged on every request. Modeled as the `ApiKeyAuth` security scheme.

Both schemes are combined (AND'd) in the spec's `security` block — this is not a choice between two auth methods, both are required together, matching WatchGuard's own documented authentication flow. Set the client ID/secret for the OAuth2 scheme and the static header value for `ApiKeyAuth` when creating the integration instance.

The default server is the Prod USA region (`api.usa.cloud.watchguard.com`). WatchGuard Cloud also offers DEU and JPN regions (see the full spec's `servers` list) — override the integration instance's host if your account is provisioned in one of those regions.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`watchguard_firebox-latest.json`](./OpenAPIs/watchguard_firebox-latest.json) | latest | 84 | Curated common-CRUD subset — see breakdown below |
| [`watchguard_firebox-1.29.0.json`](./OpenAPIs/watchguard_firebox-1.29.0.json) | 1.29.0 | 100 | Full upstream spec, unmodified |

### `watchguard_firebox-latest.json`

Sourced directly from WatchGuard's own published OpenAPI specification for the Firebox Management API (`https://developer.cloud.watchguard.com/catalog-data/firebox-apis-01/firebox-apis-01-management-01/firebox-management/1.29.0/firebox-management-1.29.0.yaml`, linked from the [Firebox Management API documentation](https://www.watchguard.com/help/docs/API/Content/en-US/firebox/management/v1/management.html)).

Trimmed to 84 of 100 upstream operations: removed the health-check endpoint, deprecated v1 exception-list endpoints (superseded here by their non-deprecated v2 equivalents), config-template subscription management, and narrow authentication sub-resource lookups (AuthPoint user groups, SAML user groups, generic auth groups). Retains full CRUD for the categories someone would realistically automate:

- **Firewall Policies**: policies (list/create/get/update/patch/delete), policy groups, aliases, SNAT actions, traffic types (reference data)
- **BOVPN IPSec Tunnels**: tunnels (list/create/get/update/patch/delete, including bulk collection-level update/patch/delete) and Phase 1 shared settings
- **Exceptions**: full CRUD for all six types — blocked sites, botnet, file, geolocation, intrusion prevention (IPS), and WebBlocker — plus the all-types list endpoint and global exceptions enable/disable
- **Certificates**: list/create/get/delete plus install-to-device
- **Deployments**: create a deployment, list/get/update/cancel transactions
- **Reference data**: content filtering actions, networks, SD-WANs, system schedules, traffic shaping rules, devices, authentication users/groups

Upstream operations without a defined `operationId` had one added for stable task/workflow naming.

### `watchguard_firebox-1.29.0.json`

The full upstream spec as published by WatchGuard, unmodified (all 100 operations, original 3-region `servers` list, original `ApiKeyAuth`/`BearerAuth` security scheme declarations).

## Studio Projects

### `WatchGuard Firebox.project.json`

84 workflows — one per curated operation — organized into 25 folders by resource category (Firewall Policies, BOVPN IPSec Tunnel, the six Exceptions types, Firebox Certificates, Deployments, Global Exceptions, and the read-only reference-data categories). Each workflow wraps a single `WatchGuard Firebox:latest` adapter task and takes the operation's path/query parameters and request body (where applicable) as job input variables.
