Prisma Access is Palo Alto Networks' cloud-delivered SASE platform, providing network and security configuration (security policies, threat prevention profiles, remote networks, mobile users, and more) for a distributed workforce, managed via Strata Cloud Manager.

This project provides an OpenAPI spec for automating against Prisma Access's SASE configuration API via an Integration Model, plus a Studio Project of ready-to-import CRUD workflows built on that model.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`palo_alto_prisma_access-latest.json`](#palo_alto_prisma_access-latestjson)
  - [`palo_alto_prisma_access-1.0.json`](#palo_alto_prisma_access-10json)
- [Studio Projects](#studio-projects)
  - [Palo Alto Prisma Access Project](#palo-alto-prisma-access-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Palo Alto Prisma Access API OpenAPI specs |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing all 344 workflows in 68 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| `Palo Alto Prisma Access:latest` Integration Model | Required to build automation against the OpenAPI spec, and to run the Studio Project below |

## Integration Configuration

Import `palo_alto_prisma_access-latest.json` as an Integration Model in **Admin > Integrations**, then create an integration pointing at Prisma Access's SASE API.

Authentication is OAuth 2.0 (client credentials grant), using an IAM service account's client ID/secret and your Tenant Service Group (TSG) ID as the scope. Set `auth_method` to `client_secret_basic` — Palo Alto's token endpoint requires HTTP Basic client credentials, not the alternate body-based method.

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "oauth2ClientCredentials": {
      "client_id": "<your-service-account-client-id>",
      "client_secret": "<your-service-account-client-secret>",
      "auth_method": "client_secret_basic",
      "scope": "tsg_id:<your-tenant-service-group-id>",
      "token_url": "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token",
      "refresh_url": "",
      "token": { "access_token": "" }
    }
  },
  "server": {
    "protocol": "https",
    "host": "api.sase.paloaltonetworks.com",
    "base_path": ""
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`palo_alto_prisma_access-latest.json`](./OpenAPIs/palo_alto_prisma_access-latest.json) | latest | 344 | All 68 published SASE configuration resource categories — see breakdown below |
| [`palo_alto_prisma_access-1.0.json`](./OpenAPIs/palo_alto_prisma_access-1.0.json) | 1.0 | 344 | Same content, dated per the individual resource specs' own version (1.0) |

### `palo_alto_prisma_access-latest.json`

Merged from Palo Alto's own 68 separate per-resource OpenAPI specs, [published directly in their `pan.dev` developer GitHub org](https://github.com/PaloAltoNetworks/pan.dev/tree/master/openapi-specs/access/prisma-access-config). Reviewed against this repo's common-CRUD-for-automation policy: all 344 upstream operations across all 68 resource categories are already in scope for automation, so nothing was excluded.

Resources included, by category:

- **Network & Security Objects**: Addresses, Address Groups, Services, Service Groups, Applications, Application Groups/Filters, Tags, Regions, Schedules, External Dynamic Lists, Dynamic User Groups
- **Security Policies & Rules**: Security Rules, Decryption Rules, Application Override Rules, Traffic Steering Rules, QoS Policy Rules, Authentication Rules
- **Threat Prevention Profiles**: Anti-Spyware, Vulnerability Protection, WildFire Antivirus, File Blocking, DNS Security, Profile Groups
- **Authentication & User Management**: Authentication Profiles/Portals/Sequences, Local Users/Groups, LDAP/SAML/RADIUS/TACACS+/Kerberos/MFA server profiles
- **Certificates & Encryption**: Certificates, Certificate Profiles, Trusted CAs, Decryption Profiles/Exclusions, IKE Gateways/Crypto Profiles, IPSec Tunnels/Crypto Profiles, SCEP, OCSP Responder
- **Application Control**: URL Access Profiles, URL Categories, HIP Objects/Profiles
- **Network Infrastructure**: Remote Networks, Service Connections/Groups, Locations, Internal DNS Servers, Infrastructure Settings, Bandwidth Allocations, QoS Profiles
- **Mobile Agent (GlobalProtect)**: agent profiles, tunnel profiles, authentication/infrastructure/global settings
- **Other**: Tags, HTTP Header Profiles, TLS Service Profiles, Auto Tag Actions, Quarantined Devices, Configuration Management (candidate push/versioning), License Types

Merging the 68 upstream files required resolving shared component definitions (parameter and response templates) referenced across files by the same name — where two files' definitions actually differed in content, the conflicting one was kept under a distinct name rather than silently overwritten.

### `palo_alto_prisma_access-1.0.json`

Identical content to `-latest.json` — kept as the dated file per this repo's convention of always pairing a curated spec with a preserved original, even when the review found nothing to exclude. Version `1.0` matches the individual upstream resource specs' own declared version.

## Studio Projects

### Palo Alto Prisma Access Project

Backed by the **`Palo Alto Prisma Access:latest`** Integration Model (see [`palo_alto_prisma_access-latest.json`](./OpenAPIs/palo_alto_prisma_access-latest.json) above). The project contains **344 workflows** organized into **68 folders**, one per resource category.

#### Folder Structure

| Category | Folders | Workflows |
|---|---|---|
| Mobile Agent | MobileAgent | 24 |
| Configuration Management | ConfigurationManagement | 9 |
| Network Infrastructure | ServiceConnections, ServiceConnectionGroups, RemoteNetworks, Regions, InternalDNSServers, InfrastructureSettings, BandwidthAllocations, QoSProfiles, Locations | 40 |
| Security Policies & Rules | SecurityRules, DecryptionRules, ApplicationOverrideRules, TrafficSteeringRules, QoSPolicyRules, AuthenticationRules | 34 |
| Network & Security Objects | Addresses, AddressGroups, Services, ServiceGroups, Applications, ApplicationGroups, ApplicationFilters, Tags, Schedules, ExternalDynamicLists, DynamicUserGroups | 55 |
| Threat Prevention Profiles | AntiSpywareProfiles, AntiSpywareSignatures, VulnerabilityProtectionProfiles, VulnerabilityProtectionSignatures, WildFireAntivirusProfiles, FileBlockingProfiles, DNSSecurityProfiles, ProfileGroups | 39 |
| Authentication & User Management | AuthenticationProfiles, AuthenticationPortals, AuthenticationSequences, LocalUsers, LocalUserGroups, LDAPServerProfiles, SAMLServerProfiles, RadiusServerProfiles, TACACSServerProfiles, KerberosServerProfiles, MFAServers | 54 |
| Certificates & Encryption | Certificates, CertificateProfiles, TrustedCertificateAuthorities, DecryptionProfiles, DecryptionExclusions, IKEGateways, IKECryptoProfiles, IPSecTunnels, IPSecCryptoProfiles, SCEPProfiles, OCSPResponder | 50 |
| Application Control | URLAccessProfiles, URLCategories, URLFilteringCategories, HIPObjects, HIPProfiles | 21 |
| Other | HTTPHeaderProfiles, TLSServiceProfiles, AutoTagActions, QuarantinedDevices, LicenseTypes | 18 |

#### Dependencies

| Dependency | Notes |
|---|---|
| `Palo Alto Prisma Access:latest` Integration Model | Import from [`palo_alto_prisma_access-latest.json`](./OpenAPIs/palo_alto_prisma_access-latest.json) before importing the project |
| `Palo Alto Prisma Access` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `Palo Alto Prisma Access` — update the `adapter_id` value in each workflow task if yours is named differently |
