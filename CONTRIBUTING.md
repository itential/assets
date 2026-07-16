# Contributing to Itential Assets

Thank you for your interest in contributing to Itential Assets! We welcome and appreciate contributions to this project. This document covers the process for contributing; see [`STANDARDS.md`](./STANDARDS.md) for the detailed content rules each asset type needs to follow.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Contribution Standards](#contribution-standards)
- [Before You Submit](#before-you-submit)
- [Naming Your Pull Request](#naming-your-pull-request)
- [How to Submit](#how-to-submit)
- [Getting Help](#getting-help)

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](./CODE_OF_CONDUCT.md). Please read it before contributing.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally.
3. **Create a topic branch** for your change.
4. **Make your changes**, following the rules in [`STANDARDS.md`](./STANDARDS.md) for the asset type(s) you're touching.
5. **Verify your contribution** — import it into a running Itential Platform (or Itential Gateway, for device drivers) instance and confirm it behaves as described.
6. **Submit a pull request** against `main`.

## Contribution Standards

Every asset type in this repo — Studio Projects, Automations, Golden Configurations, OpenAPIs, LCM Resource Models — has its own naming, versioning, and structural rules, plus a set of requirements that apply repo-wide (branding, README structure, no sensitive data, etc.). These all live in [`STANDARDS.md`](./STANDARDS.md).

**Read it before opening a PR** — most review feedback traces back to one of these rules.

## Before You Submit

- [ ] Tested against the current GA release of Itential Platform.
- [ ] Free from errors.
- [ ] Includes enough detail so that others can easily replicate the setup.
- [ ] Clearly explains what your contribution does, why it's valuable, and how it improves or complements existing functionality.
- [ ] No sensitive or private data included (see [`STANDARDS.md`](./STANDARDS.md#repo-wide-requirements)).
- [ ] Root [`README.md`](./README.md) updated if your contribution adds a new vendor, a new product under an existing vendor, or a new asset type (update the Vendor Index and/or Asset Type table).
- [ ] Reviewed against the relevant sections of [`STANDARDS.md`](./STANDARDS.md) for the asset type(s) you're contributing.

## Naming Your Pull Request

Title your PR (and its commits) as `<type>(<scope>): <summary>`.

- **`type`** — what kind of change it is:

  | Type | Use for |
  |---|---|
  | `feat` | A new asset: a new vendor, product, or asset (OpenAPI spec, Studio Project, Automation, Golden Configuration) |
  | `fix` | A correction to an existing asset (bad workflow task, wrong variable reference, invalid operationId, broken spec field, etc.) |
  | `chore` | Non-functional maintenance (renaming, removing duplicates, reorganizing folders, metadata-only edits) |
  | `docs` | Changes to `README.md`, `CONTRIBUTING.md`, `STANDARDS.md`, or a product's own `README.md` only |

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

## Getting Help

- **Resources**: Start with the root [`README.md`](./README.md) for repo structure and import instructions, [`STANDARDS.md`](./STANDARDS.md) for content rules, and the target product's own `README.md` for asset-specific details.
- **Issues**: Search [existing issues](https://github.com/itential/assets/issues) before opening a new one.
- Otherwise, open a [new issue](https://github.com/itential/assets/issues/new) describing what you're trying to do or the problem you've hit.

We value your efforts and look forward to your contributions!
