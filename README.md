# Itential Assets

Community-contributed content for the **Itential Platform** and **Itential Gateway**. Import these assets directly into your environment to accelerate automation for common network, cloud, and ITSM use cases.

> All assets are provided as examples. Review and adapt them to your environment before using in production.

---

## What's in This Repo

Assets are organized by vendor and product. Each folder may contain one or more of the following asset types:

| Asset Type | Description |
|---|---|
| **Projects** | Bundles of related automation assets (workflows, forms, templates, and transformations) for a specific use case |
| **Integration Models** | JSON-based definitions that specify how Itential Platform connects to external APIs, databases, and systems |
| **Golden Configurations** | Config Manager compliance trees for auditing device configuration drift |
| **device-drivers** | Netmiko-based drivers for connecting IAG to physical and virtual devices |
| **Configuration Parsers** | Scripts for parsing structured output from device CLI commands |
| **Automations** | Standalone automation scripts |
| **LCM Resource Models** | JSON Schema definitions that specify which properties Lifecycle Manager tracks for an infrastructure entity over time |

---

## Vendor Index

| Vendor | Products |
|---|---|
| **6connect** | IP address management |
| **AWS** | EC2 |
| **Alkira** | SD-WAN |
| **Apache** | Kafka 2.x |
| **Arista** | EOS |
| **Atlassian** | Jira / Confluence |
| **Cisco** | ASA · IOS · ISE · Meraki · NSO · NX-OS · PSIRT Open Vulnerability |
| **F5** | BIG-IP |
| **GitHub** | GitHub |
| **GitLab** | GitLab |
| **Infoblox** | NIOS DDI · Threat Defense · Universal DDI |
| **IP Fabric** | Network intelligence |
| **Itential** | Platform utilities (data manipulation, config management, regex, email, workflow utilities) |
| **Juniper** | JUNOS |
| **Kentik** | Network observability |
| **Microsoft** | Teams |
| **Nautobot** | Nautobot 2.4 |
| **NetBox** | IPAM / DCIM |
| **New Relic** | Observability |
| **Palo Alto** | Panorama |
| **Ruckus** | Fastiron |
| **Selector** | AIOps |
| **ServiceNow** | Change management · Incident management · RITM |
| **Sonatype** | Nexus |
| **Versa** | Director |

---

## Repository Structure

```
Vendor/
└── Product/
    ├── Automations/
    ├── Configuration Parsers/
    ├── device-drivers/
    ├── Golden Configurations/
    ├── OpenApis/
    ├── LCM Resource Models/
    ├── Studio Projects/
    └── README.md
```

Each product folder includes a `README.md` with import instructions, dependencies, and configuration details.

---

## Getting Started

### Import a Project
See [Create and manage projects](https://docs.itential.com/itential-platform/studio/projects/create-manage) for full details.
1. In Itential Platform, go to **Studio → Projects**.
2. Click the **Import** button on the Projects homepage.
3. Upload the `.json` file by drag-and-drop or browse the file system.

### Import an Integration Model
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

### Import an LCM Resource Model
See [Manage Lifecycle Manager resources](https://docs.itential.com/itential-platform/6/lifecycle-manager/manage-resources) for full details.
1. In Itential Platform, go to **Lifecycle Manager**.
2. Click **Create Resource +** and enter a name.
3. On the **Model** tab, paste the JSON Schema from the file and click **Save**.

### Install a Device Driver (IAG)
Follow the instructions in the driver's `README.md`. Drivers typically require copying files to your IAG host and restarting the IAG service.

---

## Requirements

Minimum versions vary by asset - check each product's `README.md` for specifics. In general:

- **Itential Platform** ≥ 6.4
- **Itential Automation Gateway** ≥ 5.0 (for device-driver assets)

---

## Contributing

Have an asset to share? Sanitize it and follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## License

[Apache 2.0](./LICENSE)
