# Azure Key Vault

Azure Key Vault is Microsoft's cloud secrets management service for storing and retrieving credentials, keys, and certificates.

This project provides a custom secret-provider plugin so Itential Gateway can resolve credentials from Azure Key Vault at runtime, instead of storing them in Gateway's own encrypted store.

**Requirements:** Itential Gateway >= 5.5

## Contents

| Asset | Description |
|---|---|
| [secret-providers/](./secret-providers/) | IG5 custom secret-provider plugin — resolves Azure Key Vault secrets into Gateway secret aliases, usable in device inventory credentials and Gateway-executed Integration Model instances |

See [secret-providers/README.md](./secret-providers/README.md) for full setup details: the service principal and role assignment it needs, registration steps, and how to reference the resulting alias.
