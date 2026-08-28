# Delinea Secret Server

Delinea Secret Server is a privileged access management (PAM) platform for storing and controlling access to credentials, keys, and secrets.

This project provides a custom secret-provider plugin so Itential Gateway can resolve credentials from Secret Server Cloud at runtime, instead of storing them in Gateway's own encrypted store.

**Requirements:** Itential Gateway >= 5.5

## Contents

| Asset | Description |
|---|---|
| [secret-providers/](./secret-providers/) | IG5 custom secret-provider plugin — resolves Delinea Secret Server secrets into Gateway secret aliases, usable in device inventory credentials and Gateway-executed Integration Model instances |

See [secret-providers/README.md](./secret-providers/README.md) for full setup details: how Secret Server API access works, registration steps, and how to reference the resulting alias.
