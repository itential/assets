# Code Contribution Guidelines

We welcome and appreciate contributions to our project! To ensure high-quality and consistent contributions, please follow the guidelines below.

## What We Look For

- Workflows (`{Vendor}/studio/`):
    - Examples - Examples of how to perform reusable generic tasks.
    - Sample Use Cases - An example of an orchestrated workflow that utilizes your contribution example.
    - When submitting a Sample Use Case, include a corresponding Operations Manager Automation and Trigger (_when applicable_).
    - Files are exported IAP Studio projects in `.project.json` format.
- Operations Manager Automations (`{Vendor}/operations_manager/`):
    - Exported automation definitions that correspond to a workflow submission.
    - Should be paired with a Trigger where applicable.
- Golden Configuration (`{Vendor}/golden_config/`):
    - Template examples that illustrate an OS or the consumption of an API (in the case of API Compliance).
- Integration Models (`{Vendor}/integration_models/`):
    - Version 2.x or 3.x OpenAPI specifications in `.json` format.
    - Filename must follow the convention `{title}-{version}.json` (e.g., `cisco_meraki_dashboard-1.48.0.json`).
    - `info.title` must contain only the integration name — no version numbers (e.g., `Cisco Meraki Dashboard`, not `Cisco Meraki Dashboard v1.48`).
    - `info.version` must reflect the actual API version.
    - **File size**: The spec must be under 15MB.
    - **One auth method defined**: Only one `securityScheme` should be defined. Itential Platform supports a single authentication method per integration instance, so additional schemes will not be usable.
    - **Global security block encouraged**: Define security at the top level of the spec rather than on individual operations. Per-operation overrides are supported but the global block is preferred for consistency.
    - **Supported auth method**: The `securityScheme` must use an auth type supported by Itential Platform. See the [Itential Platform Security Schemes documentation](https://docs.itential.com/itential-platform/admin-essentials/integrations/auth/security-schemes) for the full list of supported methods.
    - **OperationId required on every operation**: Every path operation must have a unique `operationId` in camelCase (e.g., `getDevice`, `createNetworkDevice`).
- LCM Resource Models:
    - Examples of Use Cases resource models.


When submitting your contribution, please make sure it includes the following:

### 1. Cleanly Organized
- The Assets should be modular (_where possible_) and well-structured.
- Follow best practices for readability, maintainability, and scalability.
- Use clear, descriptive variable and Asset names.
- Aim for automation workflows that can be reused in different contexts.
- Ensure workflows are documented and easy to understand.

### 2. Housekeeping Items
- Tested against the current GA release of Itential Platform.
- Free from Errors
- Include enough detail so that others can easily replicate the setup.
- Clearly explain what your contribution does.
- Describe why it is valuable and how it improves or complements existing functionality.

## Additional Requirements

- **No Sensitive Data**: Ensure your contribution does not contain any sensitive or private data (e.g., API keys, passwords, personal information).
- **Proper Spelling and Grammar**: Proofread your contribution to make sure it is free of spelling and grammar errors.
- **Title Case**: Use Title Case for headings, function names, and any other key titles.

## How to Submit

- Submit a pull request with a detailed description of your contribution.
- Make sure your contribution is fully tested and documented.
- Address any review comments promptly to ensure a smooth review process.

We value your efforts and look forward to your contributions!

