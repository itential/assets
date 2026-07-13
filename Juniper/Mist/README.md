Juniper Mist is a cloud-managed networking platform for AI-driven wireless, wired, and WAN infrastructure — organizations, sites, access points, switches, gateways, WLANs, and wireless policy are all configured and monitored through the Mist cloud API.

This project provides OpenAPI specs for automating against the Mist Cloud API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for network automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Juniper Mist Cloud API OpenAPI specs — curated `-latest` plus the full dated spec |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Juniper Mist | Cloud API `2509.1.1` (see OpenAPIs below) |
| Juniper Mist Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your Mist Cloud API base URL (e.g. `api.mist.com`, or your regional/on-prem equivalent).

Authentication is an API token in the `Authorization` header:

```
Authorization: Token <your-mist-api-token>
```

Generate an API token in the Mist dashboard under **Organization → Settings → API Token**. The token carries the same privileges as the admin it was generated for.

## OpenAPIs

| Spec | Version | Description |
|---|---|---|
| [`juniper_mist-latest.json`](./OpenAPIs/juniper_mist-latest.json) | latest (curated) | Trimmed to 137 of 1011 upstream operations — see breakdown below |
| [`juniper_mist-2509.1.1.json`](./OpenAPIs/juniper_mist-2509.1.1.json) | 2509.1.1 | Full spec for Juniper Mist Cloud API 2509.1.1 (1011 operations) |

### `juniper_mist-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2509.1.1`). Trimmed to 137 of 1011 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Organizations & Sites**: Organizations, Sites, Site Groups
- **Device Onboarding**: Inventory (claim/assign), device claim, device read/update
- **Configuration Templates**: Network Templates, Gateway Templates, AP Templates, RF Templates, Site Templates, Device Profiles
- **Networking**: Networks
- **Wireless**: WLANs (org and site scoped), WxRules, WxTags, WxTunnels, PSKs (org and site scoped)
- **WAN**: Services, Service Policies, VPNs
- **Settings**: Org Settings, Site Settings

The full upstream spec also covers MSPs, admin/SSO/API-token administration, webhooks, alarms, analytics/insights/SLEs, Marvis AI, NAC (network access control), guest portals, PSK/guest portals, asset tracking (BLE beacons, RTLS zones), RF planning (maps, spectrum analysis, RRM, rogues), device diagnostics/troubleshooting commands, EVPN topologies, Mist Edge (mxedge/mxtunnel), Session Smart Router (SSR/128T), and third-party security integrations (SkyATP, Zscaler, Cradlepoint) — none of those are included here. Pull the full spec from [Mist's official OpenAPI documentation](https://www.mist.com/documentation/mist-api/) if you need one of the excluded areas.
