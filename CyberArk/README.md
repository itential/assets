CyberArk Conjur is an open-source secrets management platform for storing, controlling, and auditing access to secrets used by applications, containers, and automation tools. It provides authentication, policy-based authorization, and secure secrets retrieval across a range of authenticator types (API key, LDAP, OIDC, Kubernetes, Azure, GCP, IAM, JWT).

This project provides OpenAPI specs for automating against Conjur's REST API via an Integration Model. The `-latest` spec is the vendor's own narrow, purpose-built API surface — see **OpenAPIs** below.

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

### `conjur-latest.json`

Full spec, untouched — Conjur's API is already a narrow, single-purpose secrets-management surface (authentication, secrets, policies, resources, roles) with no admin/reporting tail to trim.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`conjur-5.3.2.json`](./OpenAPIs/conjur-5.3.2.json) | Full spec for Conjur Open Source 5.3.2. |

## Dependencies

| Dependency | Notes |
|---|---|
| Conjur Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
