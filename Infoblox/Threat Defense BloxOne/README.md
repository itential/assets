Infoblox Threat Defense (BloxOne) is a cloud-native DNS security service that protects networks and roaming users at the DNS layer — enforcing security policies, category and application filtering, custom allow/block lists, and threat-intelligence feeds to stop malicious and unwanted domains before a connection is made.

This project provides the OpenAPI spec for automating against the Infoblox Threat Defense (BloxOne) API via an Integration Model.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Infoblox Threat Defense (BloxOne) API OpenAPI spec — `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Infoblox Threat Defense (BloxOne) API | 1 |
| Infoblox Threat Defense (BloxOne) Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at `csp.infoblox.com`.

Authentication is an API key in the `Authorization` header:

```
Authorization: Token <your-infoblox-api-key>
```

Generate an API key in the Infoblox Cloud Services Portal under **Administration → API Keys**.

## OpenAPIs

### `infoblox_threat_defense_bloxone-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1`). This is the full, upstream operation set (61 operations) — Infoblox Threat Defense (BloxOne) is already a single, narrow product surface covering DNS security policy management (security policies, application/category/network filters, named and internal domain lists, threat feeds, and access codes), so no trimming was applied. One operation (`security_policiesMigrateSecurityPolicy`) was missing its path-parameter definition in the vendor's published spec; that was added here so the spec validates, with no other content changes.

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`infoblox_threat_defense_bloxone-1.json`](./OpenAPIs/infoblox_threat_defense_bloxone-1.json) | Full spec for the Infoblox Threat Defense (BloxOne) API, version 1. |

## Dependencies

| Dependency | Notes |
|---|---|
| Infoblox Threat Defense (BloxOne) Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
