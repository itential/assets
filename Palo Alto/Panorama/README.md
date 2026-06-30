# Palo Alto Panorama

Assets for the Itential Automation Platform.

## Overview

Palo Alto Panorama is a centralized network security management platform that provides unified policy control, visibility, and automation across Palo Alto Networks next-generation firewalls. Unlike PANOS — which is the operating system running on individual firewall devices — Panorama is an **API controller** that manages device groups, security and NAT policy rulebases, address and service objects, and configuration commits across an entire firewall estate.

This project provides a complete set of IAP workflows backed by the **Palo Alto Panorama 11.1 REST API** via an Integration Model. No Automation Gateway or SSH/NETCONF connectivity is required. All operations are REST calls authenticated with an API key in the `X-PAN-KEY` header.

The 47 workflows span 12 operational categories and cover the full policy automation lifecycle: object management, rule CRUD, rule positioning, commit, and commit-all (push to managed devices).

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | Panorama 11.1 REST API OpenAPI spec used by the Integration Model |
| [Projects/](./Projects/) | IAP project containing all 46 workflows in 12 folders |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | P6+ |
| Palo Alto Panorama | 11.1 |
| `Palo Alto Panorama:11.1` Integration Model | Installed via IAP marketplace |

> **Note:** This project does **not** require Itential Automation Gateway (IAG). All API calls are made directly from the IAP platform to the Panorama REST API.

## Integration Configuration

Before importing the project, configure the `Palo Alto Panorama:11.1` Integration Model in **Admin > Integrations** and create an integration named `Panorama`. The integration connects IAP to your Panorama management server.

### Connection Properties

```json
{
  "server": {
    "protocol": "https",
    "host": "<panorama-hostname-or-ip>",
    "base_path": ""
  },
  "authentication": {
    "apiKeyHeader": {
      "value": "<your-panorama-api-key>"
    }
  },
  "tls": {
    "enabled": true,
    "rejectUnauthorized": false
  },
  "variables": {},
  "version": "11.1"
}
```

### Generating an API Key

Generate a Panorama API key with a `curl` command against the XML API:

```bash
curl -k -X GET "https://<panorama>/api/?type=keygen&user=<username>&password=<password>"
```

The response contains an `<key>` element. Use that value as `authentication.apiKeyHeader.value` in the integration.

### Integration Name

The workflows in this project are wired to the integration instance named **`Panorama`**. If your integration is named differently, update the `adapter_id` value in each workflow task before importing.

---

## Projects

### Palo Alto Panorama

The project contains **47 workflows** organized into **12 folders**. All workflows follow the naming convention `<Operation> <Resource>` (e.g. `List Security Pre-Rules`, `Create Address`).

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Security Rules - Pre | List, Create, Update, Delete, Move | Pre-rulebase security policy |
| Security Rules - Post | List, Create, Update, Delete, Move | Post-rulebase security policy |
| NAT Rules - Pre | List, Create, Update, Delete, Move | Pre-rulebase NAT policy |
| NAT Rules - Post | List, Create, Update, Delete, Move | Post-rulebase NAT policy |
| Address Objects | List, Create, Update, Delete | Shared or device-group address objects |
| Address Groups | List, Create, Update, Delete | Address group objects |
| Service Objects | List, Create, Update, Delete | TCP/UDP service port definitions |
| Service Groups | List, Create, Update, Delete | Service group objects |
| Tags | List, Create, Update, Delete | Object tags |
| Device Groups | List, Create, Update, Delete | Panorama device group containers |
| Zones | List | Template-scoped network zones |
| Commit | Commit Configuration, Commit All Configuration | Panorama candidate config commit and push to managed devices |

---

## Workflow Input Reference

All workflows accept a JSON object when run manually or called as a child workflow. The tables below document the expected input fields for each category.

### Security Rules (Pre and Post) / NAT Rules (Pre and Post)

#### List

```json
{
  "location": "device-group",
  "device_group": "my-device-group"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `location` | string | Yes | Policy scope. Use `"device-group"` for Panorama-managed device groups. |
| `device_group` | string | Yes | Panorama device group name (e.g. `"Shared"`, `"East-DG"`). |

#### Create / Update

```json
{
  "name": "allow-web",
  "location": "device-group",
  "device_group": "my-device-group",
  "config": {
    "entry": {
      "@name": "allow-web",
      "from": { "member": ["trust"] },
      "to": { "member": ["untrust"] },
      "source": { "member": ["any"] },
      "destination": { "member": ["any"] },
      "application": { "member": ["web-browsing", "ssl"] },
      "service": { "member": ["application-default"] },
      "action": "allow"
    }
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Rule name. |
| `location` | string | Yes | Policy scope (`"device-group"`). |
| `device_group` | string | Yes | Device group name. |
| `config` | object | Yes | Full rule entry body. The `@name` attribute inside `entry` must match the top-level `name`. |

#### Delete

```json
{
  "name": "allow-web",
  "location": "device-group",
  "device_group": "my-device-group"
}
```

#### Move

```json
{
  "name": "allow-web",
  "location": "device-group",
  "device_group": "my-device-group",
  "where": "before",
  "dst": "block-all"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Rule to move. |
| `location` | string | Yes | Policy scope. |
| `device_group` | string | Yes | Device group name. |
| `where` | string | Yes | Position: `"before"`, `"after"`, `"top"`, `"bottom"`. |
| `dst` | string | For `before`/`after` | The anchor rule name when using `before` or `after`. |

---

### Address Objects / Address Groups / Service Objects / Service Groups / Tags

#### List

```json
{
  "location": "device-group",
  "device_group": "my-device-group"
}
```

#### Create / Update

```json
{
  "name": "web-server-1",
  "location": "device-group",
  "device_group": "my-device-group",
  "config": {
    "entry": {
      "@name": "web-server-1",
      "ip-netmask": "10.10.1.100/32",
      "description": "Primary web server"
    }
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Object name. |
| `location` | string | Yes | Object scope (`"device-group"` or `"shared"`). |
| `device_group` | string | For `device-group` scope | Device group name. |
| `config` | object | Yes | Full entry body. See Panorama REST API docs for the schema of each object type. |

#### Delete

```json
{
  "name": "web-server-1",
  "location": "device-group",
  "device_group": "my-device-group"
}
```

---

### Device Groups

#### List

```json
{
  "name": "East-DG"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | No | Filter by device group name. Omit to list all. |

#### Create / Update

```json
{
  "name": "East-DG",
  "config": {
    "entry": {
      "@name": "East-DG",
      "description": "East coast firewall cluster"
    }
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Device group name. |
| `config` | object | Yes | Device group entry body. |

#### Delete

```json
{
  "name": "East-DG"
}
```

---

### Zones

Zones in Panorama are template-scoped — they are not tied to a device group but to a Template or Template Stack.

#### List

```json
{
  "location": "template",
  "vsys": "vsys1",
  "template": "my-template",
  "template_stack": null
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `location` | string | Yes | `"template"` or `"template-stack"`. |
| `vsys` | string | Yes | Virtual system name (e.g. `"vsys1"`). |
| `template` | string | When `location=template` | Template name. |
| `template_stack` | string | When `location=template-stack` | Template stack name. |

---

### Commit Configuration

```json
{}
```

No inputs required. The commit payload (`type=commit&cmd=<commit></commit>`) is pre-configured in the workflow. Commits the current Panorama candidate configuration.

---

### Commit All Configuration

```json
{}
```

No inputs required. The commit-all payload (`type=commit-all&cmd=<commit-all><shared-policy></shared-policy></commit-all>`) is pre-configured in the workflow. Pushes the last committed Panorama configuration to all managed firewalls. Run this after **Commit Configuration** to fully deploy changes to devices.

---

## Dependencies

| Dependency | Notes |
|---|---|
| `Palo Alto Panorama:11.1` Integration Model | Install from the IAP marketplace before importing the project |
| `Panorama` integration instance | Create in **Admin > Integrations** with the connection properties above |

