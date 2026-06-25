# F5 BIG-IP — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/f5-bigip`  
**Status:** Complete  
**Files modified:**
- `F5/BIG-IP/Projects/runCode/F5 BIG-IP.project.json` — GatewayManager `runCode` (Python) variant
- `F5/BIG-IP/Projects/sendRequest/F5 BIG-IP.project.json` — GatewayManager `sendRequest` variant

---

## Summary

Six `AutomationGateway` tasks using a `sendRequest` HTTP REST pattern (pre-check, provision, post-check) across two workflows. Both GatewayManager migration paths are provided as separate sub-variants.

---

## Tasks to Migrate

### Workflow: Create Pool and Members

| # | Task Name | Current App | Phase |
|---|---|---|---|
| 1 | `sendRequest` | AutomationGateway | Pre-Check |
| 2 | `sendRequest` | AutomationGateway | Provision |
| 3 | `sendRequest` | AutomationGateway | Post-Check |

---

### Workflow: Create Virtual Server

| # | Task Name | Current App | Phase |
|---|---|---|---|
| 1 | `sendRequest` | AutomationGateway | Pre-Check |
| 2 | `sendRequest` | AutomationGateway | Provision |
| 3 | `sendRequest` | AutomationGateway | Post-Check |

**Incoming variables (current — all 6 tasks):**
```json
{
  "adapter_id": "...",
  "host": "...",
  "endpoint": "...",
  "method": "GET|POST|PUT|DELETE",
  "data": "...",
  "headers": "...",
  "auth": "...",
  "cookies": "...",
  "params": "...",
  "timeout": "...",
  "proxies": "...",
  "verify": "...",
  "allowRedirects": "..."
}
```

---

## Implemented Variants

Two sub-variants are provided under `Projects/`. Choose one based on the target environment:

### `Projects/runCode/` — GatewayManager `runCode` (Python)

Each task replaced with `GatewayManager runCode`. A Python script (using the `requests` library) reads connection parameters from stdin and makes the HTTP call. `adapter_id` removed; `clusterId: "cluster-itential"` added.

```json
{
  "app": "GatewayManager", "name": "runCode",
  "variables": {
    "incoming": {
      "clusterId": "cluster-itential",
      "language": "python",
      "code": "<Python requests script>",
      "data": { "host": "...", "endpoint": "...", "method": "...", "auth": {...}, ... },
      "safety": { "timeout": 30 },
      "packages": ["requests"]
    },
    "outgoing": { "result": "" }
  }
}
```

### `Projects/sendRequest/` — GatewayManager `sendRequest`

Each task stays as `sendRequest` but migrated to `GatewayManager`. `adapter_id` removed; `clusterId: "cluster-itential"` added. All other incoming variables preserved.

```json
{
  "app": "GatewayManager", "name": "sendRequest",
  "variables": {
    "incoming": {
      "clusterId": "cluster-itential",
      "host": "...", "endpoint": "...", "method": "...", "auth": {...}, ...
    },
    "outgoing": { "result": "" }
  }
}
```

---

## Other Adapters

`WorkFlowEngine`, `JsonForms` — no changes needed.

---

## Reference Templates

- `Cisco/IOS/Projects/Cisco IOS.project.json` — `runCode` pattern for Python-in-gateway
- `Juniper/JUNOS/Projects/Juniper JUNOS.project.json` — `runService` pattern for service-based execution

---

## Testing

- [ ] Create Pool and Members — pre-check, provision, and post-check all complete via GatewayManager
- [ ] Create Virtual Server — pre-check, provision, and post-check all complete via GatewayManager

> Test each variant (`runCode/` and `sendRequest/`) against a live F5 BIG-IP to determine which path to carry forward.
