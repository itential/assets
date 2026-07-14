HashiCorp Vault provides secrets management, encryption-as-a-service, and privileged access management, enabling secure storage and access control for sensitive data — API keys, passwords, certificates, and encryption keys.

This project provides OpenAPI specs for automating against the Vault HTTP API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for secrets automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`hashicorp_vault-latest.json`](#hashicorp_vault-latestjson)
  - [`hashicorp_vault-1.15.0.json`](#hashicorp_vault-1150json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Vault HTTP API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| HashiCorp Vault | 1.15.x (see OpenAPIs below for the exact spec version available) |
| HashiCorp Vault Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Vault instance.

Authentication is a Vault client token in the `X-Vault-Token` header:

```
X-Vault-Token: <your-vault-client-token>
```

Obtain a client token by authenticating against your configured auth method (userpass, AppRole, AWS, Kubernetes, etc.) — see the [Vault authentication documentation](https://developer.hashicorp.com/vault/docs/auth) for details on generating one for your environment.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`hashicorp_vault-latest.json`](./OpenAPIs/hashicorp_vault-latest.json) | latest (curated) | Trimmed to 193 of 1049 upstream operations — see breakdown below |
| [`hashicorp_vault-1.15.0.json`](./OpenAPIs/hashicorp_vault-1.15.0.json) | 1.15.0 | Full spec for HashiCorp Vault 1.15.0 (1049 operations). |

### `hashicorp_vault-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1.15.0`). Trimmed to 193 of 1049 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Token**: full lifecycle (create, create-orphan, lookup, lookup-accessor, lookup-self, renew, renew-accessor, renew-self, revoke, revoke-accessor, revoke-orphan, revoke-self, tidy) and token roles
- **Auth Methods**: AppRole (roles, secret IDs, login) and Userpass (users, policies, login)
- **KV Secrets Engine**: both v1 and v2 (data, metadata, config, delete/undelete/destroy)
- **PKI Secrets Engine**: CA and root/intermediate setup, certificate issue/sign/revoke, roles, CRL management, tidy
- **Transit Secrets Engine**: encryption keys, encrypt/decrypt/rewrap, sign/verify/HMAC, datakey generation, random bytes, hashing
- **Database Secrets Engine**: dynamic and static credentials, roles, root credential rotation
- **System (core admin)**: secrets engine mounts, auth method mounts, ACL policies, lease lifecycle (lookup/renew/revoke), response wrapping, health check

Pull the full spec from a running Vault instance's `sys/internal/specs/openapi` endpoint if you need something not covered here.

### `hashicorp_vault-1.15.0.json`

Full, unmodified vendor spec for HashiCorp Vault 1.15.0 (1049 operations) — the vendor's complete API surface, preserved as-is. See `hashicorp_vault-latest.json` above for the curated subset if you just need common CRUD automation.
