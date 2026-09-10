# NSX

VMware NSX is Broadcom's network virtualization and security platform, providing software-defined networking (segments, gateways, routing), distributed and gateway firewalling, load balancing, VPN, and DHCP/DNS services across on-premises and cloud environments. The NSX Policy API is the current, declarative REST API surface for managing all of this centrally through NSX Manager.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`vmware_nsx_policy-latest.json`](#vmware_nsx_policy-latestjson)
  - [`vmware_nsx_policy-9.1.1.0.json`](#vmware_nsx_policy-9110json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | VMware NSX Policy API Integration Model |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| VMware NSX | 9.1.x |

## Integration Configuration

Import `vmware_nsx_policy-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration instance pointing at your NSX Manager.

Authentication is HTTP Basic:

```
Authorization: Basic <base64(username:password)>
```

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "basicAuth": {
      "username": "<your-nsx-username>",
      "password": "<your-nsx-password>"
    }
  },
  "server": {
    "protocol": "https",
    "host": "<nsx-manager-host>",
    "base_path": "/policy/api/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`vmware_nsx_policy-latest.json`](./OpenAPIs/vmware_nsx_policy-latest.json) | latest (curated) | 976 | Trimmed to 976 of 3740 upstream operations covering common network virtualization automation |
| [`vmware_nsx_policy-9.1.1.0.json`](./OpenAPIs/vmware_nsx_policy-9.1.1.0.json) | 9.1.1.0 | 3740 | Full NSX Policy API, officially published by Broadcom |

### `vmware_nsx_policy-latest.json`

Actively-maintained spec (`x-vendor-api-version: 9.1.1.0`), converted to OpenAPI 3.0 from the vendor's native Swagger 2.0 spec. Trimmed to 976 of 3740 upstream operations. The full upstream spec also covers federation/multi-site management, Kubernetes/container networking, malware prevention and IDS/IPS, endpoint protection, licensing, user/role administration, system health and diagnostics, upgrade orchestration, and a long tail of per-protocol statistics/status/table read endpoints (ARP tables, forwarding tables, tunnel status, etc.) — none of those are included here.

Resources included, by category:

- **Networking**: Segments (including fixed segments), segment ports, Tier-0 and Tier-1 gateways, gateway interfaces, locale services, static routes, BGP, transport zones, transport nodes, edge clusters, edge transport nodes
- **Groups & Services**: Groups, group members, services, domains, tags
- **Firewall**: Gateway firewall (rules, settings, Tier-0/Tier-1 scoped), distributed firewall (rules, settings)
- **NAT**: NAT rules for Tier-0 and Tier-1 gateways
- **DHCP & DNS**: DHCP server configs, DHCP relay configs, DHCP static bindings (segments and fixed segments), DHCP leases, DNS zones, DNS forwarder
- **Load Balancing**: Load balancers, virtual servers, pools, application/monitor/persistence profiles, LB services
- **VPN**: IPSec VPN sessions, services, local endpoints
- **IP Management**: IP pools, IP blocks, IP allocations

### `vmware_nsx_policy-9.1.1.0.json`

Full spec (3740 operations), sourced directly from Broadcom's official [`vmware/vcf-api-specs`](https://github.com/vmware/vcf-api-specs) GitHub repository (`specifications/nsx/openapi-2.0/nsx_policy_api.yaml`). Preserved as published in its native Swagger 2.0 format, per this repo's convention of keeping the dated full spec exactly as the vendor published it. See `vmware_nsx_policy-latest.json` above for the curated OpenAPI 3.0 subset if you just need common network virtualization automation.
