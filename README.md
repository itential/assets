# Itential Assets

Community-contributed content for the **Itential Platform** and **Itential Gateway**. Import these assets directly into your environment to accelerate automation for common network, cloud, and ITSM use cases.

> All assets are provided as examples. Review and adapt them to your environment before using in production.

---

## What's in This Repo

Assets are organized by vendor and product. Each folder may contain one or more of the following asset types:

| Asset Type | Description |
|---|---|
| **Studio Projects** | Bundles of related automation assets (workflows, forms, templates, and transformations) for a specific use case |
| **OpenAPIs** | JSON-based definitions imported as Integration Models that specify how Itential Platform connects to external APIs, databases, and systems |
| **Golden Configurations** | Config Manager compliance trees for auditing device configuration drift |
| **device-drivers** | Netmiko-based drivers for connecting Itential Gateway to physical and virtual devices |
| **Configuration Parsers** | Scripts for parsing structured output from device CLI commands |

---

## Vendor Index

| Vendor | Products |
|---|---|
| **1Password** | Connect (secrets access) |
| **6connect** | IP address management |
| **Akamai** | CDN & edge platform APIs |
| **Ansible** | AWX / Tower |
| **Apache** | Airflow · Kafka |
| **ARIN** | RDAP · Whois-RWS |
| **Arista** | EOS |
| **Atlassian** | Bitbucket Cloud · Confluence Cloud · Confluence Server & Data Center · Jira Cloud · Jira Server & Data Center · Opsgenie |
| **AWS** | API Gateway · CloudFormation · Cognito · Connect · Direct Connect · EC2 · EKS · Lambda · Network Firewall · Organizations · Route 53 · S3 · Secrets Manager |
| **Cisco** | ASA · Crosswork Network Controller · IOS · ISE · Meraki · NSO · NX-OS · PSIRT Open Vulnerability · Umbrella · Webex |
| **CyberArk** | Conjur (secrets management) |
| **Datadog** | Observability |
| **Docker** | Docker Engine · Docker Hub |
| **F5** | BIG-IP · BIG-IQ · Insight |
| **Fortinet** | FortiGate |
| **GitHub** | GitHub |
| **GitLab** | GitLab |
| **GoDaddy** | Domain management |
| **Google** | Cloud Compute Engine · Drive |
| **HashiCorp** | Vault (secrets management) |
| **Infoblox** | NIOS WAPI · Threat Defense BloxOne · Universal DDI BloxOne |
| **IP Fabric** | Network intelligence |
| **Juniper** | JUNOS · Mist |
| **Kentik** | Network observability |
| **Kubernetes** | Container orchestration |
| **LogicMonitor** | Observability |
| **Microsoft** | Graph Mail · Teams |
| **Nautobot** | Nautobot 2.4 |
| **NetBox** | IPAM / DCIM |
| **NetScaler** | ADC |
| **New Relic** | Observability |
| **Okta** | Identity management |
| **OpenAI** | AI / LLM APIs |
| **Paessler** | PRTG monitoring |
| **PagerDuty** | Incident management |
| **Palo Alto** | Panorama · Prisma Cloud CSPM |
| **RingCentral** | Unified communications |
| **Ruckus** | Fastiron |
| **Selector** | AIOps |
| **ServiceNow** | Change management · Incident management · RITM |
| **Slack** | Messaging |
| **Sonatype** | Nexus |
| **Twilio** | Communications APIs |
| **Versa** | Director |
| **VMware** | vSphere vCenter |
| **Zoom** | Meetings / collaboration |

---

## Repository Structure

```
Vendor/
└── Product/
    ├── Configuration Parsers/
    ├── device-drivers/
    ├── Golden Configurations/
    ├── OpenAPIs/
    ├── Studio Projects/
    └── README.md
```

The `Product/` level only appears for vendors with more than one product (e.g., `AWS/EC2/`, `Cisco/IOS/`). Single-product vendors are flattened, with asset folders directly under the vendor (e.g., `Kentik/OpenAPIs/`).

Each product folder includes a `README.md` with import instructions, dependencies, and configuration details.

---

## Getting Started

### Import a Project
See [Create and manage projects](https://docs.itential.com/itential-platform/studio/projects/create-manage) for full details.
1. In Itential Platform, go to **Studio → Projects**.
2. Click the **Import** button on the Projects homepage.
3. Upload the `.json` file by drag-and-drop or browse the file system.

### Import an OpenAPI spec/Integration Model
See [Integration models](https://docs.itential.com/itential-platform/6/admin-essentials/integration-models) for full details.
1. In Itential Platform, go to **Admin Essentials**.
2. Click the **Import** icon in the top toolbar.
3. Select **Integration Model** from the dropdown.
4. Upload the `.json` OpenAPI/Swagger file.

### Import a Golden Configuration
See [Golden Configuration overview](https://docs.itential.com/itential-platform/configuration-manager/golden-configurations/overview) for full details.
1. In Itential Platform, go to **Configuration Manager**.
2. Click the **Search** (🔍) button to open the Collection modal.
3. Click the **Golden Configurations** tab, then click **Import** in the toolbar.
4. After importing, bind the tree to your devices.

### Install a Device Driver (Gateway)
Follow the instructions in the driver's `README.md`. Drivers typically require copying files to your Itential Gateway host and restarting the Itential Gateway service.

---

## Requirements

Minimum versions vary by asset - check each product's `README.md` for specifics. In general:

- **Itential Platform** ≥ 6.4
- **Itential Gateway** ≥ 5.0 (for device-driver assets)

---

## Contributing

Have an asset to share? Sanitize it and follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md). See [STANDARDS.md](./STANDARDS.md) for the detailed content rules each asset type needs to follow.

---

## License

[Apache 2.0](./LICENSE)
