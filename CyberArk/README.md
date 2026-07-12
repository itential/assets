CyberArk Conjur is an open-source secrets management platform for storing, controlling, and auditing access to secrets used by applications, containers, and automation tools. It provides authentication, policy-based authorization, and secure secrets retrieval across a range of authenticator types (API key, LDAP, OIDC, Kubernetes, Azure, GCP, IAM, JWT).

This project provides OpenAPI specs for automating against Conjur's REST API via an Integration Model. Conjur's own API is already a narrow, single-purpose secrets-management surface; the `-latest` spec additionally trims a handful of generic diagnostic/introspection endpoints — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Conjur REST API OpenAPI spec — `-latest` plus the full dated version |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| CyberArk Conjur | 5.3.2 (see OpenAPIs below for exact spec version available) |
| Conjur Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Conjur instance.

Authentication uses HTTP Basic auth with a Conjur username and password (users) or API key (hosts and users):

```
Authorization: Basic <base64(username:password_or_api_key)>
```

Conjur also exposes dedicated authenticator endpoints (`/authn`, `/authn-ldap`, `/authn-oidc`, `/authn-k8s`, `/authn-azure`, `/authn-gcp`, `/authn-iam`, `/authn-jwt`) that exchange credentials for a short-lived Conjur access token, which can then be used for subsequent calls. See the spec's `/authn/{account}/login` and `/authn/{account}/{login}/authenticate` operations for details.

## OpenAPIs

### `conjur-latest.json` (curated)

Trimmed to 34 of 38 upstream operations (`x-vendor-api-version: 5.3.2`). Conjur's API is already a narrow, single-purpose secrets-management surface, but the upstream spec mixes in a small "status" group of generic diagnostic/introspection endpoints alongside the real authentication/secrets/policy/role automation surface. Excludes:

- `GET /authenticators` — lists which authenticator types are installed/configured/enabled on the server (a static server-capability listing, not a resource you create/read/update/delete)
- `GET /authn-gcp/{account}/status` and `GET /{authenticator}/{service_id}/{account}/status` — "is this authenticator service configured properly" diagnostic/health checks, not status of an action you triggered via this API
- `GET /whoami` — self-introspection endpoint that reports the calling client's identity/IP/user-agent, not a business resource

Operations included, by category:

- **Authentication / token issuance**: Get a short-lived access token via basic auth, LDAP, OIDC, Azure, GCP, AWS IAM, JWT (with and without optional ID), or Kubernetes; get a user's API key via basic auth or LDAP; rotate a role's API key; change a user's password; inject a Kubernetes client certificate; enable/disable an authenticator (with or without a `service_id`)
- **Certificate authority**: Get a signed certificate from a configured CA service
- **Host factory**: Create a host; create host identity token(s); revoke a token
- **Policies**: Load (add to), update, or replace a policy document
- **Public keys**: Get all public keys for a resource
- **Resources**: List resources (across all accounts, by account, or by kind); get a single resource
- **Roles**: Get role info; add or remove a role membership
- **Secrets**: Fetch one or many secret values; create a secret value

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`conjur-5.3.2.json`](./OpenAPIs/conjur-5.3.2.json) | Full spec for Conjur Open Source 5.3.2. |

## Dependencies

| Dependency | Notes |
|---|---|
| Conjur Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
