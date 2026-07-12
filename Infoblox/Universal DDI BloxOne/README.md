Infoblox Universal DDI (BloxOne) is Infoblox's cloud-managed DNS, DHCP, and IPAM platform, providing centralized visibility and control across hybrid and multi-cloud environments. The spec in this folder covers the DHCP and IPAM portions of the BloxOne REST API; DNS configuration is served by a separate BloxOne API surface not covered here.

This project provides an OpenAPI spec for automating against the BloxOne REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Infoblox Universal DDI (BloxOne) REST API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Infoblox Universal DDI (BloxOne) | Cloud Services Portal API, version 1 |
| Infoblox Universal DDI (BloxOne) Integration Model | Required to build automation against the OpenAPI spec |

## Integration Configuration

Import the OpenAPI spec from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the Infoblox Cloud Services Portal (`https://csp.infoblox.com`).

Authentication is an API key in the `Authorization` header:

```
Authorization: Token <your-bloxone-api-key>
```

Generate an API key from the Infoblox Cloud Services Portal under **Administration → API Keys**.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`infoblox_universal_ddi_bloxone-latest.json`](./OpenAPIs/infoblox_universal_ddi_bloxone-latest.json) | latest (curated) | Actively-maintained spec, trimmed to 105 of 119 upstream operations covering common CRUD for automation — see breakdown below |
| [`infoblox_universal_ddi_bloxone-1.json`](./OpenAPIs/infoblox_universal_ddi_bloxone-1.json) | 1 | Full spec for Infoblox Universal DDI (BloxOne) API version 1, including Automated Scope Management, DNS usage reporting, config-profile linking, and bulk import/copy operations not carried into the curated spec. |

### `infoblox_universal_ddi_bloxone-latest.json`

Actively-maintained spec (`x-vendor-api-version: 1`). Trimmed to 105 of 119 upstream operations covering common CRUD for automation.

Resources included, by category:

- **DHCP**: Global DHCP config, DHCP Servers, DHCP Hosts (with associations), HA Groups, Fixed Addresses, Hardware Filters, Option Filters, Option Codes, Option Spaces, Option Groups, MAC Address Items, DHCP Filters, DHCP Service instances, Universal Service associations, lease actions (clear leases)
- **IPAM**: IP Spaces, Address Blocks (with ancestor/copy/next-available lookups), Subnets (with ancestor/copy/next-available lookups), Ranges (with next-available-IP), Addresses, Hosts

## Dependencies

| Dependency | Notes |
|---|---|
| Infoblox Universal DDI (BloxOne) Integration Model | Import from the OpenAPI spec above to build automation against the REST API. |
