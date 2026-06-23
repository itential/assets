# F5 BIG-IP — Gateway5 Upgrade Notes

**Branch:** `feature/gw5-upgrade/f5-bigip`  
**Status:** Planning  
**Files to modify:** `F5/BIG-IP/Projects/F5 BIG-IP.project.json`

---

## Summary

Six `AutomationGateway` tasks using a `sendRequest` HTTP REST pattern (pre-check, provision, post-check) across two workflows. This is a different migration path than the AGManager CLI pattern — `AutomationGateway sendRequest` made raw HTTP calls; the Gateway5 equivalent needs to be determined.

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

## Migration Options to Evaluate

F5 BIG-IP uses the iControl REST API (not CLI/SSH). Options for Gateway5:

1. **Keep as REST adapter** — If a native F5 BIG-IP REST adapter is available in IAP, use that instead of routing through GatewayManager at all. Check if `F5BigIQ` adapter pattern (used in BIG-IQ project) applies here.

2. **GatewayManager `runCode`** — Wrap the REST calls in a Python script executed via `GatewayManager` `runCode`, reading connection params from stdin and making HTTP calls via the `requests` library.

3. **GatewayManager `sendRequest`** — Check if Gateway5 exposes a `sendRequest` equivalent for HTTP REST calls through the cluster.

> **Decision needed:** Confirm the intended migration path with the team before implementing. Review how the Cisco IOS project handles any REST-based interactions for clues.

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
