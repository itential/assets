Cloudflare's REST API — DNS, zones, firewall/WAF, load balancing, SSL/TLS, Zero Trust tunnels and Access, Workers, Email Routing, Page Rules, and custom hostnames. Ships as two specs: a curated Integration Model (`cloudflare-latest.json`) covering the most-commonly-automated operations, and the full Cloudflare v4 API (`cloudflare-4.0.0.json`) for complete coverage.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`cloudflare-latest.json`](#cloudflare-latestjson)
  - [`cloudflare-4.0.0.json`](#cloudflare-400json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Curated Cloudflare Integration Model (`cloudflare-latest.json`) and the full Cloudflare v4 spec (`cloudflare-4.0.0.json`) |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| Cloudflare API token | A token with permissions scoped to the zones/resources being automated |

## Integration Configuration

Import `cloudflare-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration instance pointing at `api.cloudflare.com`.

Authentication is a static Bearer token: create a Cloudflare API token at [dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens) and scope it to the permissions your workflows need (Zone:Read, DNS:Edit, etc.). The token is sent as `Authorization: Bearer <token>` on every call — no login step or token exchange.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "bearerAuth": {
      "token": "<your-cloudflare-api-token>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.cloudflare.com",
    "base_path": "/client/v4"
  }
}
```

**Token scoping:** Cloudflare API tokens support fine-grained permission scopes. Scope your token to only the zones and permission sets (Read/Edit) your workflows actually use — avoid using a Global API Key, which has account-wide write access and can't be scoped.

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`cloudflare-latest.json`](./OpenAPIs/cloudflare-latest.json) | latest (curated) | 406 | Curated Cloudflare API: DNS, zones, firewall/WAF, load balancing, SSL/TLS, Zero Trust, Workers, Email Routing, Page Rules, custom hostnames |
| [`cloudflare-4.0.0.json`](./OpenAPIs/cloudflare-4.0.0.json) | 4.0.0 | 3460 | Full Cloudflare v4 REST API — all operations across all product areas |

### `cloudflare-latest.json`

Sourced from Cloudflare's official api-schemas GitHub repo (github.com/cloudflare/api-schemas). Curated to the most-commonly-automated operations across 51 tags:

| Area | Tags included |
|---|---|
| DNS | DNS Records for a Zone, DNSSEC, DNS Settings for a Zone, DNS Firewall |
| Zones | Zone, Zone Settings, Zone Cache Settings, Zone Lockdown |
| Firewall / WAF | Firewall rules, Filters, Lists, IP Access rules for a zone, User Agent Blocking rules, Rate limits for a zone, WAF packages, WAF rule groups, WAF rules, WAF overrides |
| Load Balancing | Load Balancers, Load Balancer Pools, Load Balancer Monitors, Account Load Balancers, Account Load Balancer Pools, Account Load Balancer Monitors, Health Checks |
| SSL / TLS | Certificate Packs, Custom SSL for a Zone, Universal SSL Settings for a Zone, Automatic SSL/TLS, Total TLS, Origin CA |
| Zero Trust | Cloudflare Tunnel, Tunnel Routing, Tunnel Virtual Network, Access applications, Access groups, Zero Trust organization |
| Workers | Workers, Worker Script, Worker Routes, Workers KV Namespace |
| Email Routing | Email Routing settings, Email Routing routing rules, Email Routing destination addresses |
| Page Rules / Transforms | Page Rules, Managed Transforms |
| Custom Hostnames | Custom Hostname for a Zone |
| Account | Accounts, Account Members, Account Roles, Audit Logs |
| Notifications | Notification policies, Notification webhooks |

### `cloudflare-4.0.0.json`

Sourced from Cloudflare's official api-schemas GitHub repo (github.com/cloudflare/api-schemas). Full Cloudflare v4 REST API — 3,460 operations across 553 tags covering all Cloudflare product areas including Radar analytics, R2 storage, D1 databases, AI Gateway, Magic networking, CASB, Email Security, and more. Import this spec if you need operations not covered by the curated build.
