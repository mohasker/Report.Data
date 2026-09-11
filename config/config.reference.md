# Configuration Reference

**Document ID:** AH-SYS-CFG-000 · **Revision:** 1 · **Date:** 2026-09-11

> **Names, owners and storage locations. Never values.**
> No key, token, password, account identifier, folder identifier, application identifier, company
> identifier or webhook URL appears in this repository — not in code, not in documentation, not in a
> commit message, not in a spreadsheet, not in a prompt, not in a log (operating rule 4, GOV-01).

## Where real values live

| Kind | Location | How it gets there |
|---|---|---|
| **Secrets** — API keys, tokens, client secrets, webhook signing secrets | The provider's own connection store | **The owner authorises OAuth personally in each provider's console.** No credential is ever pasted into chat or committed here |
| **Non-secret identifiers** — folder, spreadsheet, application, company identifiers | A protected configuration table readable only by `SystemAdmin` | Entered once at provisioning, then referenced by name |
| **Business configuration** — legal entity, tax rules, approval matrix, numbering series, residency rules, templates, retention, recipients | **Master data inside the application** | Maintained by authorised administrators through administration screens — never by editing code, a scenario, a prompt or a file. That is what requirement 14 means |

That third row is the important one. Almost nothing about running a project is an environment
variable, because a project must be addable through configuration alone.

## The full register

`docs/00-discovery/09-configuration-register.md` holds the complete list with owners, the phase each
is needed by, and its status.

`.env.example` holds the small subset that genuinely is environment configuration — names only, no
values, ever.

## Phase 1 needed none of this

Every Phase 1 artifact was produced from local fixtures and synthetic data. No credential exists, no
service was contacted, and no external value was assumed (D-14). The 23 outstanding external facts
are tracked in `docs/01-data-foundation/16-external-facts-register.md`, each with the phase it
blocks.

## Rules

1. No value is written into this repository. Names, owners, locations and status only.
2. A variable reaching its phase without a value **blocks that phase**, rather than being guessed at.
3. Secrets are authorised by the owner in the provider's console, never requested in chat.
4. Business configuration is administered in the application, never in a file.
5. Every variable has one named owner. "The system" is not an owner.
