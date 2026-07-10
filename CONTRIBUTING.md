# Code Contribution Guidelines

We welcome and appreciate contributions to our project! To ensure high-quality and consistent contributions, please follow the guidelines below.

## What We Look For

All asset types below live at `{Vendor}/[{Product}/]{AssetType}/`. The `{Product}` segment only applies to vendors with more than one product (e.g., `AWS/EC2/OpenAPIs/`) — single-product vendors omit it (e.g., `Kentik/OpenAPIs/`).

### Studio Projects (`{Vendor}/[{Product}/]Studio Projects/`)
- Examples - Examples of how to perform reusable generic tasks.
- Sample Use Cases - An example of an orchestrated workflow that utilizes your contribution example.
- When submitting a Sample Use Case, include a corresponding Automation and Trigger (_when applicable_).
- Files are exported Studio projects in `.project.json` format.

### Automations (`{Vendor}/[{Product}/]Automations/`)
- Exported automation definitions that correspond to a Studio Project submission.
- Should be paired with a Trigger where applicable.

### Golden Configurations (`{Vendor}/[{Product}/]Golden Configurations/`)
- Template examples that illustrate an OS or the consumption of JSON returned from an API call (in the case of JSON Compliance).

### OpenAPIs (`{Vendor}/[{Product}/]OpenAPIs/`)
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

### LCM Resource Models (`{Vendor}/[{Product}/]LCM Resource Models/`)
- Examples of Use Cases resource models.

## Before You Submit

### Cleanly Organized
- The Assets should be modular (_where possible_) and well-structured.
- Follow best practices for readability, maintainability, and scalability.
- Use clear, descriptive variable and Asset names.
- Aim for automation workflows that can be reused in different contexts.
- Ensure workflows are documented and easy to understand.

### Housekeeping Items
- Tested against the current GA release of Itential Platform.
- Free from Errors
- Include enough detail so that others can easily replicate the setup.
- Clearly explain what your contribution does.
- Describe why it is valuable and how it improves or complements existing functionality.
- **Keep the root `README.md` in sync**: If your contribution adds a new vendor, a new product under an existing vendor, or a new asset type, update the corresponding table in the repo's root [`README.md`](./README.md) (the Vendor Index and/or Asset Type table) in the same contribution.

## Additional Requirements

- **No Sensitive Data**: Ensure your contribution does not contain any sensitive or private data (e.g., API keys, passwords, personal information).
- **Proper Spelling and Grammar**: Proofread your contribution to make sure it is free of spelling and grammar errors.
- **Title Case**: Use Title Case for headings, function names, and any other key titles.

## Naming Your Pull Request

Title your PR (and its commits) as `<type>(<scope>): <summary>`.

- **`type`** — what kind of change it is:

  | Type | Use for |
  |---|---|
  | `feat` | A new asset: a new vendor, product, or asset (OpenAPI spec, Studio Project, Automation, Golden Configuration) |
  | `fix` | A correction to an existing asset (bad workflow task, wrong variable reference, invalid operationId, broken spec field, etc.) |
  | `chore` | Non-functional maintenance (renaming, removing duplicates, reorganizing folders, metadata-only edits) |
  | `docs` | Changes to `README.md`, `CONTRIBUTING.md`, or a product's own `README.md` only |

- **`scope`** — the lowercase, hyphenated vendor or vendor-product the change applies to, matching the folder it lives in (e.g. `junos`, `panorama`, `servicenow`, `servicenow-change-management`). Omit the product part for single-product vendors. If a PR spans multiple vendors, drop the scope.
- **`summary`** — imperative mood, lowercase, no trailing period, describing what changed (e.g. `add commit-all operation`, not `added` or `this PR adds`).

Examples:
- `feat(junos): add port turn up use case to project`
- `fix(junos-netconf): remap port turn up template refs to repo project ID`
- `chore(panorama): remove outdated v10.1 integration model spec`
- `docs: update README vendor index`

## How to Submit

- Submit a pull request with a detailed description of your contribution.
- Make sure your contribution is fully tested and documented.
- Address any review comments promptly to ensure a smooth review process.

We value your efforts and look forward to your contributions!
