# Azure Key Vault — Custom Secret Provider for Itential Gateway

Itential Gateway 5.5+ supports **external secret providers**: instead of storing credentials in Itential Gateway's own encrypted store, Itential Gateway resolves them at execution time from an external secrets system. Out of the box it supports **HashiCorp Vault (KV v2)** and **CyberArk CCP** — see Itential's docs on [configuring a custom secret provider plugin](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider) and [managing secret aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases). Azure Key Vault isn't a built-in type, so this uses the third option — **`plugin`** — a small executable you provide that Itential Gateway calls to fetch a secret on demand.

This is a working example: a Python plugin for Azure Key Vault, the service principal and role assignment it needs, the registration steps, and how to reference the resulting alias — from device inventory or from an Integration Model instance.

## Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setting Up a Service Principal](#setting-up-a-service-principal)
- [The Plugin](#the-plugin)
- [Storing the Client Secret](#storing-the-client-secret)
- [Registering the Provider and Alias](#registering-the-provider-and-alias)
- [Referencing the Alias](#referencing-the-alias)
  - [In Device Inventory](#in-device-inventory)
  - [In an Integration Model Instance](#in-an-integration-model-instance)
- [Verifying It's Working](#verifying-its-working)
- [Adapting This Example](#adapting-this-example)
- [References](#references)

## Architecture

Itential Gateway is the only thing that ever talks to Azure Key Vault. Two different callers can trigger that resolution — Inventory Manager driving a device connection, or an Integration Model instance making an API call — but both go through the exact same alias → provider → plugin path, and the plaintext secret never travels back to Platform:

```
Itential Platform                                        Itential Gateway
──────────────────                                        ────────────────
device sync (Inventory Manager)  ─┐
Integration Model instance         ├─▶  resolves $GATEWAYSECRET_(alias)  ──▶  azure-plugin.py  ──(OAuth2 client credentials)──▶  Azure Key Vault
(Gateway-executed)                ─┘
```

Itential Gateway resolves the `$GATEWAYSECRET_(...)` reference just before the value is used, so the plaintext password is never stored in Inventory Manager, in a sync template, in an Integration Model instance's config, or in Itential Gateway's own database — only the alias name is.

## Prerequisites

- Itential Gateway 5.5 or later, with the `secret-provider` feature available (`iagctl create secret-provider --help` should show the `plugin`, `vault`, and `cyberark` provider types). See the [custom plugin provider docs](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider) for the full reference.
- An Azure Key Vault with the **Azure role-based access control (RBAC)** permission model enabled (this is the default/recommended option when creating a vault). This example uses an RBAC role assignment, not a legacy vault access policy.
- Python 3 on the Itential Gateway host (already required by Itential Gateway itself).

## Setting Up a Service Principal

Itential Gateway typically doesn't run on an Azure VM, so there's no Azure Managed Identity available to it — the plugin needs its own identity to authenticate as. If Itential Gateway *is* running on an Azure VM in your environment, use a **Managed Identity** instead of everything in this section — it removes the credential entirely.

Otherwise, create a dedicated App Registration for this integration (don't reuse a shared/general-purpose one):

```bash
# Create the App Registration
az ad app create --display-name "svc-iag-keyvault-reader"
# Note the appId from the output

# Create its service principal
az ad sp create --id <appId>

# Generate a client secret (Azure secrets expire — pick a lifetime and
# plan to rotate before it does; 6-12 months is a reasonable default)
az ad app credential reset --id <appId> --display-name "iag-plugin" --end-date 2027-07-10
# Note the password from the output — Azure will not show it again

# Grant the narrowest useful role, scoped to just this vault (not the
# resource group or subscription)
az role assignment create \
  --assignee <appId> \
  --role "Key Vault Secrets User" \
  --scope $(az keyvault show --name <vault-name> --resource-group <rg> --query id -o tsv)
```

This gives you three values the plugin needs: the **Tenant ID**, the **Client ID** (`appId`), and the **client secret**. A client certificate is a stronger alternative to a client secret if you want to harden this further — no shared secret in transit.

## The Plugin

Itential Gateway invokes the plugin as `<command> get`, writing a JSON request to stdin and reading a JSON response from stdout. Configuration (the non-sensitive values registered with the provider) arrives via the JSON on stdin, in `config.env` — the plugin process does not otherwise inherit Itential Gateway's environment.

**Request (stdin):**
```json
{
  "path": "IOSXE-PASSWORD",
  "key": "",
  "config": {
    "env": {
      "AZURE_VAULT_URL": "https://<vault-name>.vault.azure.net/",
      "AZURE_TENANT_ID": "<tenant-id>",
      "AZURE_CLIENT_ID": "<client-id>",
      "AZURE_CLIENT_SECRET_FILE": "/etc/gateway/azure_client_secret"
    }
  }
}
```

**Response (stdout, exit 0):**
```json
{"value": "the-plaintext-secret"}
```

On failure: write a message to stderr and exit non-zero.

See [`plugin.py`](./plugin.py) for the full implementation. Copy it to the Itential Gateway host — renaming it to something provider-specific like `azure-plugin.py` if you'll have more than one provider's plugin on the same host — and make it executable:

```bash
cp plugin.py /opt/gateway/azure-plugin.py
chmod +x /opt/gateway/azure-plugin.py
```

Unlike Secret Server-style providers, Key Vault secrets are addressed by **name**, not a numeric ID, and each secret is a single value rather than a multi-field record — so `path` is the secret's name and `key` is normally left empty.

## Storing the Client Secret

Never pass the client secret as a raw `--env` value — it would be stored in the gateway's provider configuration. Instead, write it to a file the plugin reads at runtime, and only pass the file path via `--env`:

```bash
sudo tee /etc/gateway/azure_client_secret <<< 'the-client-secret-value' > /dev/null
sudo chown itential:itential /etc/gateway/azure_client_secret
sudo chmod 400 /etc/gateway/azure_client_secret
```

The file should contain just the raw client secret as a single line of plain text — no quotes, no `KEY=value` formatting:

```
$ cat /etc/gateway/azure_client_secret
the-client-secret-value
```

## Registering the Provider and Alias

Full CLI reference: [configuring a custom secret provider plugin](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider) and [managing secret aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases).

```bash
# Provider: registers the plugin and its non-sensitive config
iagctl create secret-provider azure-keyvault-plugin \
  --type plugin \
  --command /opt/gateway/azure-plugin.py \
  --env AZURE_VAULT_URL=https://<vault-name>.vault.azure.net/ \
  --env AZURE_TENANT_ID=<tenant-id> \
  --env AZURE_CLIENT_ID=<client-id> \
  --env AZURE_CLIENT_SECRET_FILE=/etc/gateway/azure_client_secret \
  --description "Azure Key Vault via Entra ID client credentials"

# Alias: maps a friendly name to a specific secret on that provider
iagctl create secret AZURE-IOSXE-PASSWORD \
  --provider azure-keyvault-plugin \
  --secret IOSXE-PASSWORD
```

Verify:
```bash
iagctl get secret-providers
iagctl describe secret AZURE-IOSXE-PASSWORD
```

`describe secret` only shows the alias's metadata (provider/secret/key) — it never displays the resolved value.

## Referencing the Alias

Use `$GATEWAYSECRET_(alias-name)` anywhere Itential Gateway resolves secrets at execution time. Two common places:

### In Device Inventory

For example, a device synced from NetBox into Itential Platform:

```json
{
  "name": "device-name",
  "attributes": {
    "itential_host": "10.0.25.20",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "cisco_xe",
    "itential_user": "itential",
    "itential_password": "$GATEWAYSECRET_(AZURE-IOSXE-PASSWORD)",
    "itential_driver_options": {
      "netmiko": {
        "banner_timeout": 60,
        "conn_timeout": 60,
        "enable_fast_mode": true,
        "global_delay_factor": 3,
        "read_timeout_override": 600,
        "session_timeout": 300
      }
    }
  }
}
```

Itential Gateway resolves the alias just before the device driver call, so the real password is fetched fresh from Key Vault on every run rather than stored anywhere on the platform.

### In an Integration Model Instance

The same alias resolves in an **Integration Model instance's** credential fields too, as long as that instance's calls actually execute through Itential Gateway rather than directly from the Platform cluster:

- Set `proxyOverride.executionMode` to `cluster_no_proxy` or `proxy` — **not** `direct`. `direct` means Platform makes the call itself, Gateway is never involved, and the alias won't resolve.
- Optionally set `clusterOverride` to target a specific Gateway cluster instead of the Admin Essentials default.

```json
{
  "security": {
    "apiKey": {
      "value": "$GATEWAYSECRET_(AZURE-API-TOKEN)"
    }
  },
  "proxyOverride": {
    "overrideProxyBehavior": true,
    "executionMode": "cluster_no_proxy",
    "proxy": {
      "auth": {
        "authMode": "none"
      }
    }
  }
}
```

Gateway resolves the alias just before the outbound call executes, same as the device inventory case — the real token is never sent back to Platform.

## Verifying It's Working

- `iagctl get secret-providers` shows your provider.
- `iagctl describe secret <alias>` shows the correct provider/secret.
- The gateway log (`journalctl -u iagctl`) shows a line like `secret_resolution alias="..." provider="..." path="..." outcome=success` for each call that uses the alias.
- The device/API call using the resolved secret succeeds end to end.

## Adapting This Example

- **Multiple secrets**: register one provider, then create as many `secret` aliases as you need against it — each just needs its own `--secret <name>`.
- **Structured secrets**: if you store a JSON object as a secret's value (e.g. `{"username": "...", "password": "..."}`), pass `--key <field-name>` when creating the alias — the plugin will parse the value as JSON and pull out that field.
- **Itential Gateway running on an Azure VM**: use a Managed Identity instead of a service principal, and adjust the plugin's authentication step accordingly — no client secret to create, store, or rotate.
- **Client secret rotation**: unlike some other providers, Azure AD client secrets expire. Track the expiration date you set and rotate the secret (`az ad app credential reset`) and the file on the Itential Gateway host before it does.

## References

- [Itential Gateway — Configure a Custom Plugin Secret Provider](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider)
- [Itential Gateway — Manage Secret Aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases)
- [Azure Key Vault REST API reference](https://learn.microsoft.com/en-us/rest/api/keyvault/)
- [Microsoft Entra ID — OAuth2 client credentials flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow)
