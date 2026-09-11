# Al-Haram Integrated Field Reporting, Technical Reports and Invoicing System

Implementation repository for the system specified in [`MASTER_SPEC.md`](MASTER_SPEC.md).

**Owner:** Al-Haram for Maintenance & Agriculture · Doha, Qatar
**System owner:** General Manager

---

## Status

| | |
|---|---|
| **Phase 0 — Discovery** | **Approved 2026-09-11** subject to owner decisions D-01 … D-15 ([decision record](docs/00-discovery/10-owner-decisions.md)). |
| **Phase 1 — Data foundation** | **Complete 2026-09-11.** 141 of 141 checks executed and passing. Awaiting owner review of the data dictionary, transition matrix and security model. |
| **Next phase** | Phase 2 — the multi-project capture and review application. Needs EF-01, EF-03, EF-05, EF-06. |
| **Production systems touched** | **None.** No Google account, Drive folder, AppSheet app, Make scenario, API connection, QuickBooks company or credential has been created or connected. |
| **Real data** | **None.** All data in this repository is synthetic and marked as such. |
| **Tests executed** | Phase 1 validation checks run locally against synthetic data; results recorded in [`17-validation-evidence.md`](docs/01-data-foundation/17-validation-evidence.md). No claim is made about any system that has not been built. |

> **Read this before quoting anything from this repository.**
> Everything here is design and decision documentation. Nothing in it asserts that a system exists,
> works, is secure, or has been tested. Operating rule 1 of the specification forbids such claims
> without a recorded, executed test — and no test has been executed yet.

---

## Start here

| If you are… | Read |
|---|---|
| **The owner, reviewing Phase 1** | [`docs/01-data-foundation/00-PHASE-1-SUMMARY.md`](docs/01-data-foundation/00-PHASE-1-SUMMARY.md), then [`17-validation-evidence.md`](docs/01-data-foundation/17-validation-evidence.md) for what was actually executed. |
| **Looking for the decisions already taken** | [`docs/00-discovery/10-owner-decisions.md`](docs/00-discovery/10-owner-decisions.md) — D-01 … D-15. |
| **Looking for what is still unknown** | [`docs/01-data-foundation/16-external-facts-register.md`](docs/01-data-foundation/16-external-facts-register.md) — every external fact awaiting confirmation, by the phase it blocks. |
| **Reviewing the original discovery** | [`docs/00-discovery/00-DISCOVERY-SUMMARY.md`](docs/00-discovery/00-DISCOVERY-SUMMARY.md) — the eight required discovery outputs. |
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
    10-owner-decisions.md       Owner decisions D-01 … D-15 (governs the Phase 0 docs)
    adr/                        ADR-0001 … ADR-0008
  01-data-foundation/           Phase 1: data dictionary, key/hash strategy, transition
                                matrix, security model, evidence rules, numbering, legal
                                entity + bilingual model, residency model, approval and
                                delegation, calculation spec, AppSheet plan matrix,
                                QuickBooks mapping, orchestration contract, prompt specs,
                                external-facts register, validation evidence
model/model.json                Canonical model — the single source of truth for Phase 1
schemas/                        Table schemas generated from the model + AI output contracts
seed/                           Controlled vocabularies + synthetic project data
config/                         Named configuration variables. No values, ever.
tools/                          Stdlib-only generators, validators and tests
```

Directories created in later phases: `prompts/`, `templates/`.

---

## The four principles the design is built to protect

0. **Unbounded width.** The platform is multi-project, multi-client and multi-entity from the first version. Adding a project is master-data configuration — never modified logic, a cloned app, duplicated scenarios, rewritten prompts or changed code.
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

## Running the Phase 1 checks

Standard-library Python 3 only — no installation, no dependency, no network:

```
python3 tools/run_validation.py
```

It regenerates the schemas and the data dictionary from `model/model.json`, runs every validation
and test, and rewrites `docs/01-data-foundation/17-validation-evidence.md` with the results —
passing or failing.

## Approval required to proceed to Phase 2

Phase 2 begins when the owner reviews the Phase 1 exit criteria in
[`08-phase-1-artifact-manifest.md`](docs/00-discovery/08-phase-1-artifact-manifest.md) and records
approval.
