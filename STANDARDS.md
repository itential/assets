# Itential Assets — Content Standards

This document holds the detailed content and authoring rules for every asset type in this repo. [`CONTRIBUTING.md`](./CONTRIBUTING.md) covers the contribution *process* (forking, branching, PR naming, submitting); this document covers what a contribution actually needs to look like before it's ready for review.

All asset types below live at `{Vendor}/[{Product}/]{AssetType}/`. The `{Product}` segment only applies to vendors with more than one product (e.g., `AWS/EC2/OpenAPIs/`) — single-product vendors omit it (e.g., `Kentik/OpenAPIs/`).

## Table of Contents

- [General Principles](#general-principles)
- [Studio Projects](#studio-projects-vendorproductstudio-projects)
- [Automations](#automations-vendorproductautomations)
- [Golden Configurations](#golden-configurations-vendorproductgolden-configurations)
- [OpenAPIs](#openapis-vendorproductopenapis)
- [LCM Resource Models](#lcm-resource-models-vendorproductlcm-resource-models)
- [Repo-Wide Requirements](#repo-wide-requirements)

## General Principles

- The Assets should be modular (_where possible_) and well-structured.
- Follow best practices for readability, maintainability, and scalability.
- Use clear, descriptive variable and Asset names.
- Aim for automation workflows that can be reused in different contexts.
- Ensure workflows are documented and easy to understand.

## Studio Projects (`{Vendor}/[{Product}/]Studio Projects/`)
- Examples - Examples of how to perform reusable generic tasks.
- Sample Use Cases - An example of an orchestrated workflow that utilizes your contribution example.
- When submitting a Sample Use Case, include a corresponding Automation and Trigger (_when applicable_).
- Files are exported Studio projects in `.project.json` format.
- **Target the `-latest` Integration Model**: when building or updating a project against an OpenAPI-backed integration, wire its tasks to the `-latest` spec's Integration Model, not a pinned dated version — so projects automatically pick up the curated, actively-maintained spec rather than drifting to a version that will eventually be superseded.

## Automations (`{Vendor}/[{Product}/]Automations/`)
- Exported automation definitions that correspond to a Studio Project submission.
- Should be paired with a Trigger where applicable.

## Golden Configurations (`{Vendor}/[{Product}/]Golden Configurations/`)
- Template examples that illustrate an OS or the consumption of JSON returned from an API call (in the case of JSON Compliance).

## OpenAPIs (`{Vendor}/[{Product}/]OpenAPIs/`)
Imported into Itential Platform as Integration Models.

- **`.json` format.** The `-latest.json` spec must be OpenAPI 3.x — if the vendor only publishes a Swagger 2.0 spec, convert it to OpenAPI 3.0 (e.g. with `swagger2openapi`) before using it as `-latest`. The dated `{title}-{version}.json` file preserves the vendor's spec exactly as published, including its original OpenAPI/Swagger version — do not convert it.
- **Filename convention**: `{snake_case_title}-{version}.json`, with exactly one hyphen separating the title from the version (e.g., `cisco_meraki_dashboard-1.48.0.json`). The title portion must use lowercase `snake_case` only — no spaces, camelCase, or PascalCase.
- **Version labeling**:
    - The version segment must be exactly the value in that spec's `info.version` field (e.g., `info.version: "3.7.8"` → `netbox-3.7.8.json`; `info.version: "v2"` → `servicenow_table_api-v2.json`).
    - To mark a spec as the actively-maintained, most current one, overwrite `info.version` to `"latest"` and rename the file to match (e.g., `cisco_meraki_dashboard-latest.json`). Since this overwrites the vendor's real version number, preserve it in an `x-vendor-api-version` field (e.g., `"x-vendor-api-version": "1.48.0"`) so it isn't lost — see any existing `-latest.json` spec for an example.
    - Never use an underscore in place of the separating hyphen (e.g., `meraki_1.48.0.json` is incorrect; `meraki-1.48.0.json` is correct).
- `info.title` must contain only the integration name — no version numbers (e.g., `Cisco Meraki Dashboard`, not `Cisco Meraki Dashboard v1.48`).
- `info.version` must reflect the actual API version (use `"latest"` to match a `-latest.json` filename).
- **Slim the `-latest` spec to common CRUD for automation**: A vendor's full published spec is often far larger than anything Itential Platform automation actually needs. The `-latest.json` file should be a curated subset — keep the core create/read/update/delete operations and resources someone would realistically automate, and drop long tails like device-type/config templates, modular-hardware sub-resources, the vendor's own internal tooling (scripts, webhooks, job/task management, user/permission administration), health/heartbeat/metrics/self-introspection endpoints, and other niche feature areas. Go operation-by-operation — a small, already-narrow vendor API can still have a handful of non-automation plumbing endpoints mixed in; don't skip the review just because the spec looks small. When you slim a spec, keep the full original as its own dated `{title}-{version}.json` file (per the version-labeling rule above) so nothing is lost — the `-latest.json` is a derived copy, not a replacement, even in the case below where nothing ends up excluded. Document what's included/excluded in the product's `README.md` (list the kept resources by category so it's scannable — see NetBox's `README.md` for the pattern). `-latest` should always read as the deliberately-curated automation spec — never label it "full" or "untouched" in the README, even when a review finds nothing to cut.
    - `info.description` is shown in the Itential Platform GUI — keep it a normal, concise vendor/product description. Don't put curation notes there, and don't repeat boilerplate across specs.
    - Instead, add a single `x-itential-curated` string field to `-latest.json`'s `info` block. This field is **always present** on every `-latest.json` — its wording is what differs:
        - If operations were removed: briefly note **what's included** (not what's excluded) and point to the README, e.g. `"Trimmed to <N> of <M> upstream operations covering <categories>. See the repo README for the full scope and the full spec."`.
        - If the review found nothing to cut (the vendor's full surface is already common CRUD for automation): say so explicitly rather than omitting the field, e.g. `"Reviewed against the repo's common-CRUD-for-automation policy: all <N> upstream operations are already in scope, so the full spec is carried through as -latest. See the repo README for the operation breakdown and the full spec."`. A missing field means "not yet reviewed," not "nothing to cut" — don't leave it off just because the spec passed review untouched.
- **File size**: The spec must be under 15MB.
- **One auth method defined**: Only one `securityScheme` should be defined. Itential Platform supports a single authentication method per integration instance, so additional schemes will not be usable. If a vendor's API supports multiple incompatible auth methods (e.g., an API key header vs. a Bearer token), publish separate specs with distinct filenames (e.g., `cisco_meraki_dashboard-latest.json` vs. `cisco_meraki_dashboard_bearer_variant-latest.json`) rather than combining schemes in one spec.
- **Global security block encouraged**: Define security at the top level of the spec rather than on individual operations. Per-operation overrides are supported but the global block is preferred for consistency.
- **Supported auth method**: The `securityScheme` must use an auth type supported by Itential Platform. See the [Itential Platform Security Schemes documentation](https://docs.itential.com/itential-platform/admin-essentials/integrations/auth/security-schemes) for the full list of supported methods.
- **No duplicate specs**: Don't leave an old, differently-named spec in the same folder once a renamed/enriched replacement exists — update the product's `README.md` links and remove the superseded file in the same contribution.

## LCM Resource Models (`{Vendor}/[{Product}/]LCM Resource Models/`)
- Examples of Use Cases resource models.

## Repo-Wide Requirements

- **No Sensitive Data**: Ensure your contribution does not contain any sensitive or private data (e.g., API keys, passwords, personal information).
- **Product README structure**: Each product folder's `README.md` should keep a plain `# {Product}` title but skip a separate `## Overview` heading and any "Assets for the Itential Platform" boilerplate — the description paragraph(s) flow directly under the title. Keep that intro **product-agnostic**: describe the vendor/product itself, not the specifics of any one asset it ships with. Detail that's specific to one asset (e.g. a Studio Project's workflow count, folder count, or category breakdown) belongs under that asset's own heading (e.g. `## Studio Projects`), not in the top-level intro. Avoid superlative/marketing language ("the premier...", "industry-leading...") since competing vendors coexist in this repo. See NetBox's or GitHub's `README.md` for the pattern.
- **No generic import instructions**: Don't restate how to import a Studio Project, OpenAPI spec, Golden Configuration, LCM Resource Model, or device driver in a product's own README (e.g. "Import via Automation Studio > Projects > Import") — those generic click-paths already live once in the root [`README.md`](./README.md)'s Getting Started section. A product README's asset sections should only cover what's specific to that product: which Integration instance name a workflow expects, what an Automation's trigger needs, credential/config setup, etc.
- **Branding**: Refer to the products as "Itential Platform" and "Itential Gateway" (or "Platform"/"Gateway" for brevity once already introduced, or a specific version like "P6" or "IG5" when relevant) — never the retired abbreviations "IAP" or "IAG".
- **Table of Contents**: Every product `README.md` needs a `## Table of Contents` section right after the intro paragraph(s), before `## Contents`. Before writing it, check that the document's heading levels are actually correct — a section that documents a sibling section's content (e.g. a "Workflow Input Reference" section for a specific Studio Project's workflows) should be nested as that section's child, not left as a same-level sibling; fix the heading levels first, then build the TOC to match. List every `##` heading as a top-level bullet, and every genuine `###` child nested one level under its real parent — but don't go deeper than that (skip `####` and beyond) to avoid fragile GitHub-generated anchors on headings with special characters, duplicate text, or repeated leaf headings (e.g. several "List"/"Create"/"Delete" subsections across different resource types). Give both the curated `-latest` spec and the dated/full spec their own `###` heading under `## OpenAPIs` (even if the full spec's is a single sentence pointing back at the curated one), so both are reachable from the TOC. See GitHub's or Palo Alto Panorama's `README.md` for the pattern.
- **Proper Spelling and Grammar**: Proofread your contribution to make sure it is free of spelling and grammar errors.
- **Title Case**: Use Title Case for headings, function names, and any other key titles.
