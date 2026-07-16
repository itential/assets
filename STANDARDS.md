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

## Automations (`{Vendor}/[{Product}/]Automations/`)
- Exported automation definitions that correspond to a Studio Project submission.
- Should be paired with a Trigger where applicable.

## Golden Configurations (`{Vendor}/[{Product}/]Golden Configurations/`)
- Template examples that illustrate an OS or the consumption of JSON returned from an API call (in the case of JSON Compliance).

## OpenAPIs (`{Vendor}/[{Product}/]OpenAPIs/`)
Imported into Itential Platform as Integration Models.

- Version 2.x or 3.x OpenAPI specifications in `.json` format.
- **Filename convention**: `{snake_case_title}-{version}.json`, with exactly one hyphen separating the title from the version (e.g., `cisco_meraki_dashboard-1.48.0.json`). The title portion must use lowercase `snake_case` only — no spaces, camelCase, or PascalCase.
- **Version labeling**:
    - The version segment must be exactly the value in that spec's `info.version` field (e.g., `info.version: "3.7.8"` → `netbox-3.7.8.json`; `info.version: "v2"` → `servicenow_table_api-v2.json`).
    - To mark a spec as the actively-maintained, most current one, overwrite `info.version` to `"latest"` and rename the file to match (e.g., `cisco_meraki_dashboard-latest.json`). Since this overwrites the vendor's real version number, preserve it in an `x-vendor-api-version` field (e.g., `"x-vendor-api-version": "1.48.0"`) so it isn't lost — see any existing `-latest.json` spec for an example.
    - Never use an underscore in place of the separating hyphen (e.g., `meraki_1.48.0.json` is incorrect; `meraki-1.48.0.json` is correct).
- `info.title` must contain only the integration name — no version numbers (e.g., `Cisco Meraki Dashboard`, not `Cisco Meraki Dashboard v1.48`).
- `info.version` must reflect the actual API version (use `"latest"` to match a `-latest.json` filename).
- **File size**: The spec must be under 15MB.
- **One auth method defined**: Only one `securityScheme` should be defined. Itential Platform supports a single authentication method per integration instance, so additional schemes will not be usable. If a vendor's API supports multiple incompatible auth methods (e.g., an API key header vs. a Bearer token), publish separate specs with distinct filenames (e.g., `cisco_meraki_dashboard-latest.json` vs. `cisco_meraki_dashboard_bearer_variant-latest.json`) rather than combining schemes in one spec.
- **Global security block encouraged**: Define security at the top level of the spec rather than on individual operations. Per-operation overrides are supported but the global block is preferred for consistency.
- **Supported auth method**: The `securityScheme` must use an auth type supported by Itential Platform. See the [Itential Platform Security Schemes documentation](https://docs.itential.com/itential-platform/admin-essentials/integrations/auth/security-schemes) for the full list of supported methods.
- **No duplicate specs**: Don't leave an old, differently-named spec in the same folder once a renamed/enriched replacement exists — update the product's `README.md` links and remove the superseded file in the same contribution.

## LCM Resource Models (`{Vendor}/[{Product}/]LCM Resource Models/`)
- Examples of Use Cases resource models.

## Repo-Wide Requirements

- **No Sensitive Data**: Ensure your contribution does not contain any sensitive or private data (e.g., API keys, passwords, personal information).
- **Proper Spelling and Grammar**: Proofread your contribution to make sure it is free of spelling and grammar errors.
- **Title Case**: Use Title Case for headings, function names, and any other key titles.
