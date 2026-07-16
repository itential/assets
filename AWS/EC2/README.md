Amazon EC2 (Elastic Compute Cloud) provides scalable virtual compute capacity in the AWS cloud, enabling you to launch and manage server instances alongside the VPC networking that surrounds them.

This project provides two complementary ways to automate against EC2:

- **Studio Project workflows** built on the **AWS EC2 Adapter** — VPC and networking provisioning workflows (create a VPC, subnet, route, internet gateway, security group) and instance lifecycle workflows (create and destroy).
- **OpenAPI specs** for building new automation directly against the EC2 API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for compute and networking automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
  - [Adapter (Studio Project workflows)](#adapter-studio-project-workflows)
  - [Integration Model (OpenAPI-based automation)](#integration-model-openapi-based-automation)
- [Studio Projects](#studio-projects)
  - [AWS EC2 Project](#aws-ec2-project)
- [Golden Configurations](#golden-configurations)
- [OpenAPIs](#openapis)
  - [`amazon_ec2-latest.json`](#amazon_ec2-latestjson)
  - [`amazon_ec2-2016-11-15.json`](#amazon_ec2-2016-11-15json)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | EC2 API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/](./Studio%20Projects/) | Itential Platform project containing VPC/networking and instance lifecycle workflows |
| [Golden Configurations/](./Golden%20Configurations/) | Security Group golden configuration |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| AWS EC2 Adapter | Required for the Studio Project workflows below |
| AWS EC2 Integration Model | Required only if building new automation directly against the OpenAPI specs |

## Integration Configuration

### Adapter (Studio Project workflows)

Install the [AWS EC2 Adapter](https://gitlab.com/itentialopensource/adapters/adapter-aws_ec2) and configure an instance in **Admin > Adapters**, then update the `adapterId` value in each workflow task to match your instance name before importing.

### Integration Model (OpenAPI-based automation)

To build automation directly against the EC2 API instead, import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at your AWS region endpoint (e.g. `ec2.us-east-1.amazonaws.com`).

Authentication is AWS Signature Version 4 — sign requests with an AWS access key ID and secret access key.

---

## Studio Projects

### AWS EC2 Project

| Folder | Workflows | Scope |
|---|---|---|
| Provision VPC with Networking / Create VPC | Create VPC | Create a VPC |
| Provision VPC with Networking / Create Route | Create Route | Create a route in a route table |
| Provision VPC with Networking | Create VPC Subnet, Add Ingress Rule to Security Group, Create Security Group with Ingress Rules, Create and Attach Internet Gateway, Provision VPC with Networking | Build out VPC networking end to end |
| Create EC2 Instance | Create EC2 Instance | Launch an EC2 instance |
| Destroy VPC and EC2 Instance / Delete Security Groups | (child workflow) | Delete security groups by VPC |
| Destroy VPC and EC2 Instance / Delete Subnets | (child workflow) | Delete subnets by VPC |
| Destroy VPC and EC2 Instance | Destroy VPC and EC2 Instance, Detach and Delete Internet Gateways by VPC | Tear down a VPC and its instances |

#### Dependencies

| Dependency | Notes |
|---|---|
| [AWS EC2 Adapter](https://gitlab.com/itentialopensource/adapters/adapter-aws_ec2) | Required. Update `adapterId` in each workflow task to match your instance name. |

## Golden Configurations

- [AWS EC2 - Security Group](./Golden%20Configurations/AWS%20-%20Security%20Group.json)

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`amazon_ec2-latest.json`](./OpenAPIs/amazon_ec2-latest.json) | latest (curated) | 212 | Trimmed to 212 of 1182 upstream operations covering common CRUD for compute and networking automation — see breakdown below |
| [`amazon_ec2-2016-11-15.json`](./OpenAPIs/amazon_ec2-2016-11-15.json) | 2016-11-15 | 1182 | Full spec for the EC2 API version 2016-11-15. |

### `amazon_ec2-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2016-11-15`). Trimmed to 212 of 1182 upstream operations covering common CRUD for compute and networking automation. The full upstream spec models the entire EC2 API surface, including Transit Gateway, Client VPN, IPAM, Spot Fleet, Reserved Instances, Capacity Reservations, Outposts, and dozens of other specialized areas — none of those are included here. Pull the full spec from [AWS's official EC2 API reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/) if you need one of the excluded areas.

Resources included, by category:

- **Instances**: Run, Describe, Start, Stop, Reboot, Terminate, Monitor/Unmonitor, Modify/Describe Attribute, Instance Types
- **Images**: Describe, Create, Deregister, Modify/Describe Attribute (AMIs)
- **Security Groups**: Describe, Create, Delete, Authorize/Revoke Ingress and Egress, Update Rule Descriptions
- **Key Pairs**: Describe, Create, Delete, Import
- **VPCs**: Describe, Create, Delete, Create Default, Modify/Describe Attribute
- **Subnets**: Describe, Create, Delete, Create Default, Modify Attribute
- **Route Tables & Routes**: Describe, Create, Delete Route Table; Create/Delete/Replace Route; Associate/Disassociate/Replace Association
- **Internet Gateways**: Describe, Create, Delete, Attach, Detach
- **NAT Gateways**: Describe, Create, Delete
- **Elastic IPs**: Describe, Allocate, Release, Associate, Disassociate
- **Network Interfaces**: Describe, Create, Delete, Attach, Detach, Modify/Describe Attribute
- **EBS Volumes**: Describe, Create, Delete, Attach, Detach, Modify, Volume Status, Describe Attribute
- **Snapshots**: Describe, Create, Delete, Copy, Modify/Describe Attribute
- **VPC Peering**: Describe, Create, Accept, Reject, Delete
- **Flow Logs**: Describe, Create, Delete
- **VPC Endpoints**: Describe, Create, Delete, Modify
- **Placement Groups**: Describe, Create, Delete
- **Reference data**: Availability Zones, Regions, Account Attributes
- **Tags**: Create, Delete, Describe

### `amazon_ec2-2016-11-15.json`

Full, unmodified vendor spec for EC2 API version 2016-11-15 (1,773 operations) — the vendor's complete API surface, preserved as-is. See `amazon_ec2-latest.json` above for the curated subset if you just need common CRUD automation.
