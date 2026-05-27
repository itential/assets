# Cisco Crosswork Network Controller (CNC) Assets
Assets for the Itential Platform.

## OpenAPIs
- [CNC L3VPN 7.2.0](./OpenAPIs/cnc_l3vpn_7.2.0.json)
- [CNC Device Management 7.2.0](./OpenAPIs/cnc_devicemgmt_7.2.0.json)

#### Dependencies
- Cisco Crosswork Network Controller 7.2.0 instance
- CNC API Client credentials (username/password for the CAS TGT exchange)
- **Authentication note:** These specs use Bearer JWT. The JWT is obtained via a two-step CAS exchange — not a standard OAuth2 flow. See the `info.description` field in each spec for the exact procedure.
- [Cisco Crosswork Network Controller Documentation](https://developer.cisco.com/docs/crosswork/)
