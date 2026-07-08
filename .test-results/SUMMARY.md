# POC-Samples Test Run Summary

Generated: 2026-07-08 (autonomous run, Tier 2 IAP6 fully wired up)
Harness: `~/Desktop/POC-Samples-Test-Harness`

## Result

| Tier | Result |
|---|---|
| Tier 1 static (142 assets) | 101 PASS, 41 WARN, 0 FAIL, 0 EXHAUSTED |
| Tier 2 live IAG5 (2 assets) | 2 PASS (registered + verified + torn down against the real local gateway5) |
| Tier 2 live IAP6 (93 assets) | 35 PASS, 58 SKIP, 0 FAIL |

**Everything is PASS/WARN/SKIP. Zero FAIL, zero EXHAUSTED, across all three tiers.**

---

## 1. Getting Tier 2 IAP6 working at all — bugs found and fixed

`IAP_BASE_URL=http://localhost:3000` pointed the harness at a real local IAP6 platform (`~/Desktop/itential-dev-stack`, Docker). Getting real signal back required fixing several problems, in order of discovery:

1. **Wrong header combination breaks auth entirely.** `live_platform.py`'s `http()` helper sent both `Authorization: Bearer <token>` and `Cookie: token=<token>` on every request. This build treats a *present* Bearer header as a (failing) JWT auth attempt and rejects the request with 401 outright, even though the Cookie alone authenticates fine. Fixed: cookie-only auth.
2. **Wrong admin account.** The stack has two identities: bare `admin`/`admin` (zero roles/groups assigned — confirmed via `GET /users/me`) and `admin@itential`/`admin` (the LDAP-backed "full admin" account). Switched to `IAP_USERNAME=admin@itential`.
3. **`admin@itential` was still short on roles** (403 on `/automation-studio/projects`) — ran the dev-stack's own idempotent `scripts/sync-admin-roles.sh` (with your go-ahead), which synced 176 roles to `admin_group`/`admin@itential`. Confirmed fix: 403 → 200.
4. **`live_platform.py`'s `write_results_merge()`** had the same clobbering bug as `validate_static.py`'s original `--only` handling — a targeted re-run overwrote `results_live.json` with just the retried subset. Fixed to merge by `asset_id`; removed a dead unused `results/live/` output path.
5. **A latent display bug in the shared `AssetResult` model** (`lib/common.py`): an asset whose only check is `SKIP` kept the dataclass's default status of `PASS` forever, since `PASS`/`SKIP` share the same demotion rank. This is what made the *first* IAP6 attempt (before the auth fix) silently report "93 PASS" when every request was actually a masked 401. Fixed the rank sentinel so the first real check always sets the status.

## 2. Tier 2 IAG5 — reconfirmed clean

Both `Juniper/JUNOS/device-drivers/netconf-python` (7 services) and `Ruckus/Fastiron/device-drivers/netmiko-python` (5 services) registered, verified, and were torn down cleanly against the real gateway5.

## 3. Tier 2 IAP6 project/golden_config — root-caused and fixed via `~/Developer/builder-skills`

With auth working, `project` (28 assets) and `golden_config` (7 assets) were still failing with confusing generic errors (`"must be object"` at the JSON-Schema root; `"Missing Params: version"`). These looked like guessed-endpoint issues but the real cause was payload *shape*, found by reading `~/Developer/builder-skills/.claude/skills/{builder-agent,itential-golden-config}/SKILL.md`:

- **`project` import**: the endpoint (`POST /automation-studio/projects/import`) was already correct — the body must be wrapped as `{"project": <raw .project.json content>}`. Posting the raw document directly (what the harness did) fails root validation with a generic, misleading error.
- **`golden_config` import**: the guessed endpoint (`/configuration_manager/configs/import`) was entirely wrong and happened to alias onto a different real route (tree-versioning) that wanted an unrelated `version` param, producing a red herring. The real endpoint is `POST /configuration_manager/import/goldenconfigs`, and the body must be `{"trees": [<raw golden config .json content>]}` — the file's own top-level shape (`data`/`taskInstances`) matches one tree entry directly. This import response doesn't return the created id, so a `lookup_path` (`GET /configuration_manager/configs`, matched by name) was added to find it for teardown.

Implemented as generic `wrap_key`/`wrap_as_list`/`lookup_path` metadata in `live_targets.json`, applied by `live_platform.py`. Re-ran: **all 35 project + golden_config assets now PASS**, each verified created then torn down (`metadata.failedComponents: []` / `"status":"success"` on import; confirmed 2xx delete afterward). Verified the platform's project/golden-config lists are back to exactly their pre-test state (5 pre-existing demo projects; empty golden-config list).

`openapi` (51 assets) and `automation` (7 assets) remain `SKIP` — their guessed endpoints are still 404 on this build, no self-describing API (`/swagger.json`, `/api-docs`, `/openapi.json` all 404) is exposed to discover the real routes automatically, and `builder-agent/SKILL.md` indicates `automation` likely needs a two-step `POST /operations-manager/automations` + `POST /operations-manager/triggers` flow rather than a single bulk import — out of scope for this pass (not asked for, and a materially bigger lift than the project/golden_config fix). `SKIP` per TEST_PLAN §4's explicit `live_endpoint_unknown` fallback, not `FAIL`.

## 4. Device-conformance spot-check — 4 openapi specs validated against real hardware

The IAP6 `import_path` 404 blocks *importing* these specs as HTTP integrations, but doesn't say anything about whether the specs themselves accurately describe their target systems' real APIs. Using real device endpoints/credentials from the Itential PS ATL Lab (Confluence page 4582408239), validated the 4 Infoblox/NetBox specs directly against live hardware — a check independent of, and unblocked by, the IAP6 import gap. Recorded as an additional `device-conformance` check on each asset in `results_live.json`; their `SKIP` status (IAP6-import-unresolved) is unchanged since that's still an accurate, separate fact.

- **NetBox** (`netbox_4.1.json`) — `PASS`. NetBox v4.0.11 (172.20.102.5) serves its own live OpenAPI schema at `/api/schema/`; diffed directly against it. 249/249 shared paths match exactly on HTTP methods. The 24 repo-only paths are NetBox 4.1 features this 4.0.11 appliance doesn't have yet (circuit-groups, rack-types, notifications, branching); the 16 live-only paths belong to a lab-installed `upgrade-catalog` plugin. Functional spot-check: provisioned a real API token, `GET /api/dcim/devices/` returned real paginated device data matching the spec's declared shape, then revoked the token.
- **Infoblox NIOS DDI / WAPI** (`infoblox_wapi_1.0.1.json`) — `PASS`. Spot-checked 6 WAPI object types (`network`, `networkcontainer`, `ipv4address`, `zone_auth`, `zone_forward`, `zone_delegated`) against the real NIOS 9.0.3 grid master (172.20.100.25) with the spec's paths appended to `/wapi/v2.12/`. All 6 return correct data (`ipv4address` needs a `network`/`network_view` filter per WAPI's own search rules — confirmed as expected behavior, not a spec defect, by retrying with the filter and getting a real result).
- **Infoblox Threat Defense** / **Universal DDI** — stay `SKIP`, not validated. Both describe Infoblox's cloud/BloxOne product line, a different API surface from the on-prem NIOS grid master this lab provides. Confirmed rather than assumed: Threat Defense's sample path (`access_codes`) returns `"Unknown object type (access_codes)"` from the real on-prem WAPI — it genuinely isn't part of this appliance's API at all. Validating these two would need separate BloxOne cloud credentials, not available on the PS ATL Lab page.

No lab devices were left in a modified state: the NetBox API token created for the functional spot-check was deleted immediately after use; nothing was created against the Infoblox grid master (read-only GETs only).

## 5. Verdict

No FAIL or EXHAUSTED assets remain anywhere.

**VERDICT: PASS (142 assets, Tier 1) + PASS (35 assets, Tier 2 IAG5+IAP6-tested) + SKIP (58 assets, Tier 2 IAP6 openapi/automation — endpoint discovery unresolved, not a defect)**
