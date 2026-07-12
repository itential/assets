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

| Spec | Version | Description |
|---|---|---|
| [`infoblox_threat_defense_bloxone-latest.json`](./OpenAPIs/infoblox_threat_defense_bloxone-latest.json) | latest (curated) | Trimmed to 60 of 61 upstream operations — see breakdown below |
| [`infoblox_threat_defense_bloxone-1.json`](./OpenAPIs/infoblox_threat_defense_bloxone-1.json) | 1 | Full, unmodified vendor spec |

### `infoblox_threat_defense_bloxone-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1`). Trimmed to 60 of 61 upstream operations covering DNS security policy management (security policies and rules, application/category/network filters, named and internal domain lists, threat feeds, content categories, PoP regions, access codes, and application/address-block approvals). Excludes the vendor's own hidden/internal security-policy-migration endpoint (`security_policiesMigrateSecurityPolicy`, `POST /security_policy_migrations/{policy_id}`) — it's flagged `@hidden true` in the vendor's own spec and its request/response schemas are opaque (empty) objects, marking it as vendor-internal tooling rather than a documented business operation. Removing it also dropped 5 schemas (`atcfwPolicyMigrationRequest`, `atcfwPolicyMigrationResponse`, `atcfwPolicyMigrationStatus`, `atcfwPolicyScopeTags`, `atcfwRuleTags`) that only that operation referenced. One operation (`security_policiesMigrateSecurityPolicy`) was also missing its path-parameter definition in the vendor's published spec, but that fix is moot now that the operation itself is excluded.

Operations included, by category:

- **Security Policies**: List, create, delete (bulk), get, update, delete a security policy; list security policy rules
- **Filters**: Application Filters (list/create/delete/get/update/delete-by-id), Category Filters (list/create/delete/get/update/delete-by-id), Content Categories (list — reference data for building category filters)
- **Network Lists**: List, create, delete (bulk), get, update, delete a network list
- **Named Lists** (threat-intel/custom lists): List, create, delete (bulk), patch (bulk), get, update, delete, patch a named list; insert/delete/partial-update list items; download named lists as CSV
- **Internal Domain Lists**: List, create, delete (bulk), get, update, delete an internal domain list; patch list items
- **DoH FQDNs**: Create or retrieve a DNS-over-HTTPS FQDN
- **Threat Feeds**: List available threat-intelligence feeds (reference data referenced by security policy rules)
- **Access Codes**: List, create, delete (bulk), get, delete-by-id, update an access code
- **Approvals**: List/update/patch Application Approvals; read/patch Address Block Approvals
- **PoP Regions**: List, get a Point-of-Presence region (reference data for policy/proxy placement)

## Dependencies

| Dependency | Notes |
|---|---|
| Infoblox Threat Defense (BloxOne) Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
