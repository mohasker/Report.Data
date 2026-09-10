# Al-Haram Integrated Field Reporting, Technical Reports and Invoicing System

Implementation repository for the system specified in [`MASTER_SPEC.md`](MASTER_SPEC.md).

**Owner:** Al-Haram for Maintenance & Agriculture · Doha, Qatar
**System owner:** General Manager

---

## Status

| | |
|---|---|
| **Current phase** | **Phase 0 — Discovery.** Complete and awaiting owner approval. |
| **Next phase** | Phase 1 — Data foundation. **Does not start until Phase 0 is approved and BQ-01 … BQ-10 are answered.** |
| **Production systems touched** | **None.** No Google account, Drive folder, AppSheet app, Make scenario, API connection or credential has been created or connected. |
| **Tests executed** | **None.** No test result is claimed anywhere in this repository. |

> **Read this before quoting anything from this repository.**
> Everything here is design and decision documentation. Nothing in it asserts that a system exists,
> works, is secure, or has been tested. Operating rule 1 of the specification forbids such claims
> without a recorded, executed test — and no test has been executed yet.

---

## Start here

| If you are… | Read |
|---|---|
| **The owner, deciding whether to proceed** | [`docs/00-discovery/00-DISCOVERY-SUMMARY.md`](docs/00-discovery/00-DISCOVERY-SUMMARY.md) — the eight required discovery outputs, then [`04-open-questions.md`](docs/00-discovery/04-open-questions.md) for the ten decisions needed. Each carries a recommendation you can simply approve. |
| **Deciding scope and budget** | [`01-mvp-boundary.md`](docs/00-discovery/01-mvp-boundary.md) — what is in, what is deferred, and why. |
| **Reviewing the technical approach** | [`02-architecture.md`](docs/00-discovery/02-architecture.md) and the [ADRs](docs/00-discovery/adr/). |
| **Assessing risk** | [`05-risk-and-controls-register.md`](docs/00-discovery/05-risk-and-controls-register.md) and [`06-spec-conflicts-and-platform-limits.md`](docs/00-discovery/06-spec-conflicts-and-platform-limits.md). |
| **Planning the work** | [`07-phase-plan.md`](docs/00-discovery/07-phase-plan.md) and [`08-phase-1-artifact-manifest.md`](docs/00-discovery/08-phase-1-artifact-manifest.md). |

---

## Contents

```
MASTER_SPEC.md                  Authoritative requirements baseline (v1.0)
CHANGELOG.md                    Dated revision history
docs/
  VERSION-MANIFEST.md           Document control: ID, revision, status per document
  00-discovery/
    00-DISCOVERY-SUMMARY.md     The eight discovery outputs required by §18
    01-mvp-boundary.md          MVP scope, deferrals, acceptance mapping
    02-architecture.md          Layers, invariants, trust boundaries, failure taxonomy
    03-assumptions-register.md  Labelled assumptions and dependency list
    04-open-questions.md        10 blocking questions + 14 open questions
    05-risk-and-controls-register.md
    06-spec-conflicts-and-platform-limits.md
                                12 conflicts, 12 platform limits, 10 simplifications,
                                7 security observations
    07-phase-plan.md            Phases 0-8 with gate evidence requirements
    08-phase-1-artifact-manifest.md
    09-configuration-register.md
                                Every external value as a NAMED VARIABLE. No values.
    adr/                        ADR-0001 … ADR-0008
```

Directories created in later phases: `schemas/`, `seed/`, `config/`, `prompts/`, `templates/`, `tests/`.

---

## The four principles the design is built to protect

1. **Segregation.** Every row carries a project. Every user's access derives from their assignments, enforced by security filters *and* re-validated server-side — never by view visibility alone.
2. **Evidence immutability.** The original photograph is written once and never altered, annotated or deleted. Everything else is a derivative, stored separately, with its own record.
3. **Approval binds to content.** An approval records the exact content hash it approved. Change the content and the approval is void, along with everything downstream of it.
4. **Determinism of money.** No monetary or quantity figure ever originates from a language model. AI writes the sentence; the formula writes the number.

---

## Standing rules for anyone working in this repository

- **No secrets.** No key, token, password, account ID, folder ID, application ID or webhook URL — not in code, not in documentation, not in a commit message, not in a spreadsheet, not in a prompt, not in a log. Configuration is recorded as variable *names* in [`09-configuration-register.md`](docs/00-discovery/09-configuration-register.md).
- **No invented values.** Unknown external values are named configuration variables and are requested only when the next safe step needs them.
- **No real client data** until Phase 8, under controlled import. Test data is synthetic and clearly marked.
- **No irreversible external action** — send, post, share, delete — outside the phase that specifically enables it, with its gate evidence recorded.
- **No claim of "tested"** without a recorded result carrying a date, an executor and an outcome.
- **One phase in progress at a time.** A phase closes only when its gate evidence exists.

---

## Approval required to proceed

Phase 1 begins when the owner records a decision in
[`00-DISCOVERY-SUMMARY.md`](docs/00-discovery/00-DISCOVERY-SUMMARY.md) and answers the ten blocking
questions in [`04-open-questions.md`](docs/00-discovery/04-open-questions.md).
