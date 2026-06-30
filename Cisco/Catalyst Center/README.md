# Cisco Catalyst Center Assets
Assets for the Itential Platform.

## OpenAPIs

| File | Paths | Schemas | Size |
|---|---|---|---|
| [cisco-catalyst-center.json](./OpenAPIs/cisco-catalyst-center.json) | 962 | 1,736 | 9.7 MB |
| [cisco-catalyst-center-slim.json](./OpenAPIs/cisco-catalyst-center-slim.json) | 274 | 521 | 2.8 MB |

The slim spec drops analytics/trend data, deprecated APIs, wireless-only endpoints, hardware detail reads, and UI/admin endpoints — keeping only what's needed for network automation workflows.

### Slim API Coverage
The slim spec includes:

| Domain | Paths | Description |
|---|---|---|
| Device Inventory | 36 | List, query, CRUD, config reads, interface lookup, site assignment |
| Sites & Topology | 25 | Areas, buildings, sites CRUD + per-site settings (AAA, DHCP, DNS, NTP, telemetry), L2/L3/physical topology |
| Templates | 25 | Projects + template CRUD, deploy, preview, version management |
| SDA Fabric | 50 | Fabric sites/zones, devices, L2/L3 VNs, anycast gateways, port assignments, transits, multicast, provisioning |
| Software Images (SWIM) | 36 | Image inventory, distribute/activate, golden tagging, readiness checks, CCO sync |
| PnP / Onboarding | 20 | Full PnP device lifecycle — claim, unclaim, reset, site-claim, workflows |
| IPAM & IP Pools | 14 | Global pools, site subpools, IPAM server, reserve/release |
| Tags | 16 | Tag CRUD + device/interface membership in bulk |
| Tasks & Async | 9 | Task polling (`/tasks`, `/activities`, execution status) |
| Discovery | 8 | Create/manage discovery jobs, list discovered devices |
| Compliance | 8 | Run compliance, view detail, remediate |
| Config Files | 5 | List/download device config snapshots (masked + unmasked) |
| LAN Automation | 11 | Start/stop sessions, status, port channels |
| Network Settings | 3 | Push site-level network settings |
| Credentials | 6 | CLI credentials CRUD, global credential read |

## Projects

### Catalyst Center Project
- Discover Network Devices
- Onboard Device via PnP
- Deploy Configuration Template
- Assign Device to Site
- Run Compliance Check
- Distribute and Activate Software Image
- Provision SDA Fabric Device
- Reserve IP Pool for Site

#### Dependencies
- [Cisco Catalyst Center Adapter](https://gitlab.com/itentialopensource/adapters/adapter-cisco-catalyst-center)
- Cisco Catalyst Center v3.1.x
