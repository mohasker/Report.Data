# Phase 0 — Discovery Output

**Document ID:** AH-SYS-P0-000
**Revision:** 0 (draft for owner approval)
**Date:** 2026-09-10
**Prepared by:** Implementation agent (Claude Code)
**Approval required from:** General Manager / owner
**Status:** AWAITING OWNER APPROVAL — no production mutation has been performed

This document answers, in order, the eight outputs required by §18 of `MASTER_SPEC.md`.
Supporting detail lives in the numbered companion documents in this folder.

---

## 0. What has actually been done so far

Recorded honestly, per operating rule 1:

| Action | Result |
|---|---|
| Inspected the target repository `mohasker/Report.Data` | Empty. No commits, no remote branches, no prior files. Nothing to preserve. |
| Inspected available Al-Haram knowledge sources in this workspace | One internal knowledge skill found (company profile, service lines, client types, technical standards, reporting style). Used as *unverified input*, not as fact. |
| Inspected Google Workspace / Drive / AppSheet / Make / Claude / QuickBooks accounts | **NOT DONE.** No credentials or account access were provided, and none were requested in chat. All such values remain named configuration variables — see `09-configuration-register.md`. |
| Created production connections, apps, sheets, folders, scenarios | **NOT DONE — deliberately.** §15 Phase 0 requires owner approval first. |
| Executed any test | **NOT DONE.** No test result is claimed anywhere in this repository. |

Everything in this repository at revision 0 is **documentation and decisions**. No external system
has been touched.

---

## 1. Understanding of the objective

Al-Haram runs many maintenance and landscaping contracts at the same time, for different clients,
in different disciplines, with different reporting and billing rules. Today the evidence of that
work — what was done, where, when, and with what result — exists mainly as photographs and
messages held by individual people, and it is converted into client-facing reports, completion
certificates and invoices by manual effort concentrated on a very small number of staff.

The objective is to replace that manual chain with one governed pipeline:

> **field evidence → controlled review → approved evidence set → generated document →
> approved document → released document → (only then) accounting posting and client delivery.**

The system must be:

- **Configuration-driven and multi-project from day one.** Adding a project is master-data entry, not development work. No project, client, location, activity, template, approval route or billing rule is written into logic.
- **Evidence-based.** A claim that work was completed must trace to approved evidence or to an authorised human confirmation. AI may describe and draft; it may never assert completion or compute money.
- **Approval-gated.** Nothing leaves the company — no email, no certificate, no invoice — without a recorded approval that is tied to the exact version of the content approved.
- **Deterministic where money is involved.** Every figure on a certificate or invoice is produced by a formula whose inputs, rounding and trace can be re-derived and re-checked.
- **Recoverable and auditable.** Failures are classified, logged with correlation IDs, retried only when safe, and surfaced to an operator with a recommended action.

The business value is not "AI writes reports." It is that the General Manager stops being the single
bottleneck and single point of failure for reporting, certification and billing, while the company's
ISO 9001 / 14001 / 45001 document-control obligations get stronger rather than weaker.

---

## 2. Proposed MVP boundary

Full detail and rationale: `01-mvp-boundary.md`.

**IN — the MVP is "one governed month, end to end, on three projects."**

- Master data: Users, Roles, ProjectAssignments, Clients, Contacts, Projects, Locations (hierarchical), ActivityTypes, Units.
- Field capture: SiteVisit → VisitActivities → Photos, with per-activity evidence rules, draft/submit separation, and offline capture.
- Review: technical reviewer approves/rejects a visit and each individual photograph, with comments and correction return.
- Snags: raise, assign, track, close with closure evidence.
- Drive: idempotent per-project/year/month folder provisioning; originals written once to a protected folder; derivatives kept separately.
- Make: submission validation, evidence registration, review notification, error queue, daily monitoring — all idempotent and correlation-tracked.
- Claude: evidence analysis returning schema-validated JSON, stored as non-authoritative advisory data.
- Documents: **Monthly Technical Report only**, generated from a frozen input manifest, into a controlled template, as editable draft + PDF, with technical approval, revision control, and release.
- Audit: AuditLog and IntegrationJobs populated for every state transition and every external call.

**OUT of the MVP — deliberately deferred, not dropped.**

| Deferred | Moves to | Why |
|---|---|---|
| Contracts, BOQ, cumulative quantity control | Phase 6 | Needs real contract/BOQ data and a confirmed certification process; wrong here is expensive. |
| Completion certificates | Phase 6 | Depends on approved BOQ quantities. |
| Invoice drafts, tax, retention, advance recovery | Phase 6 | Blocked on tax and accounting decisions (BQ-05, BQ-06). |
| QuickBooks posting | Phase 7 | Blocked on whether a QBO company file usable from Qatar exists at all (BQ-05). |
| Outbound client email release | Phase 7 | Highest-consequence irreversible action; needs release approval workflow proven first. |
| Daily/weekly reports, quotations, inspection reports, transmittals | Phase 8+ | Same engine, more templates. Cheap once the engine is proven; noise before then. |
| Arabic and bilingual document output | Phase 5b, gated by BQ-09 | Doubles template, QA and PDF-rendering work. Needs a policy decision, not a guess. |
| OwlAgent conversational interface | Post-MVP, optional | Convenience layer; must never be a system of record or a critical trigger. |
| WhatsApp as an input channel | Not planned | Operating rules 12–13. AppSheet is the field-input channel. |

**MVP acceptance = criteria 1–11, 13 and 14 of §14.** Criterion 12 (no email/QuickBooks without
approval) is satisfied in the MVP by the fact that neither capability is built or connected; it is
re-tested properly in Phase 7.

---

## 3. Architecture summary

Full detail and diagram: `02-architecture.md`.

Six layers, each with one job, communicating only through immutable IDs and explicit statuses —
never through filenames, row positions or display names.

1. **Capture and review (AppSheet).** Mobile forms, dependent dropdowns, per-activity evidence rules, reviewer queues, dashboards. Enforces UX; does not enforce trust on its own.
2. **Operational store (Google Sheets for MVP).** Normalised tables, one row per entity, `UNIQUEID()` keys, audit columns on every table. Sheets is a deliberate, reversible MVP choice with a defined migration trigger (see ADR-0002).
3. **Evidence and document store (Google Drive, on a Shared Drive).** Write-once originals, separate derivatives, controlled templates, drafts, released documents, archive. Referenced everywhere by Drive **file ID**, never by path.
4. **Orchestration (Make.com).** Every cross-system action is a named, idempotent scenario with a correlation ID, an explicit error route, a classified failure taxonomy, capped retries and a dead-letter queue that a human can work from.
5. **Advisory intelligence (Claude API).** Two strictly separated jobs: describe evidence, and draft narrative from structured records. Both constrained by versioned prompts and JSON schemas. Output is always stored as *advisory*, never as a fact and never as a number that reaches a document unchecked.
6. **Financial system of record (QuickBooks Online, Phase 7).** Receives only figures computed deterministically upstream, only after finance approval, and only after totals reconcile.

**Four architectural invariants** that everything else is built to protect:

- **I-1 Segregation.** Every row carries `ProjectID`. Every user's access derives from `ProjectAssignments`. Enforced by AppSheet security filters *and* re-validated server-side in Make — never by view visibility alone.
- **I-2 Immutability of evidence.** The original photo file is written once and never modified, moved destructively, annotated or deleted. Everything else (previews, crops, report images) is a derivative in a different folder with its own record.
- **I-3 Approval binds to content.** Every approval stores the `ContentHash` and `EntityVersion` it approved. If the underlying content changes, the approval is void and downstream approvals are void with it. This is what makes the audit trail defensible to a government client or an ISO auditor.
- **I-4 Determinism of money.** No monetary or quantity figure ever originates from, or passes through, a language model. Claude writes the sentence; the formula writes the number.

---

## 4. Assumptions (explicitly labelled)

Full register with owner-confirmation checkboxes: `03-assumptions-register.md`.

These are **assumptions, not facts.** Each is safe to proceed on for documentation work, and each is
marked with the phase at which it must be confirmed or it becomes a blocker.

| # | Assumption | Confirm by |
|---|---|---|
| A-01 | Al-Haram has a **paid Google Workspace** tenant on its own domain (not consumer Gmail), so Shared Drives, admin control and per-user licensing are available. | Phase 1 |
| A-02 | An AppSheet plan that includes **webhooks and the AppSheet API** will be licensed. Automation to Make is not possible without it. | Phase 2 |
| A-03 | A Make.com organisation with **Data Stores, error handlers and scheduled scenarios** will be available. | Phase 3 |
| A-04 | A Claude API workspace with a **hard monthly spend cap** will be provided. | Phase 4 |
| A-05 | Field users have **company-managed or personally-owned smartphones with a working camera**, and each has an individual sign-in identity. Shared accounts are not acceptable — they destroy attribution. | Phase 2 |
| A-06 | The company's **legal name, CR number, logo and contact block** used on client documents will be supplied by the owner as controlled reference data. The spec says "L.L.C." while another internal source says "W.L.L." — see conflict C-01. | Phase 1 |
| A-07 | **No VAT is currently charged** on these Qatar contracts. The system will still be built tax-rule-driven with a zero-rate configuration, so a future tax regime is a configuration change, not a rebuild. Must be confirmed by the company's accountant, not assumed. | Phase 6 |
| A-08 | Default currency is **QAR**, and MVP projects are single-currency. Multi-currency is validated-and-rejected in the MVP rather than silently mishandled. | Phase 6 |
| A-09 | Reporting frequency for the MVP pilot is **monthly**, calendar-month aligned, with an agreed cut-off day. | Phase 2 |
| A-10 | MVP document language is **English**, with Arabic field labels in the app. Arabic document output is a separate, later, explicitly-approved scope. | Phase 5 |
| A-11 | Photographic evidence is **client-confidential but not classified**, and may be stored in Google's cloud under the company's Workspace tenant. Government clients may impose stricter terms — see R-04 and BQ-10. | Phase 1 |
| A-12 | The General Manager may act as sole technical approver during the MVP, with the approval matrix designed to support delegation later without redesign. | Phase 2 |
| A-13 | Three **synthetic** pilot projects (different clients, disciplines, locations, users, templates, approval routes) are acceptable for proving segregation before any real client data is entered. | Phase 2 |
| A-14 | Existing project, client and location registers exist in some form (spreadsheets, proposals, contracts) and can be exported for controlled import rather than retyped. | Phase 1 |
| A-15 | The company accepts that **offline behaviour is bounded** by what AppSheet actually supports on real devices, and that any offline claim will be stated only after device testing. | Phase 2 |

---

## 5. Blocking questions (maximum ten, prioritised)

Full text, options and consequences: `04-open-questions.md`.

Each question carries a **recommended answer**. Approving the recommendation is a valid response —
you do not need to compose an alternative unless you disagree.

| # | Priority | Question | Recommended answer |
|---|---|---|---|
| **BQ-01** | Blocks everything | Which Google account owns the system, and is it a **paid Workspace** tenant with Shared Drive capability? | Create a dedicated Workspace account (e.g. a `system`/`operations` mailbox on the company domain) as the technical owner, and host everything on a **Shared Drive**, not in a personal My Drive. |
| **BQ-02** | Blocks Phase 2 | Which **AppSheet plan**, and how many named users in year one? | License the tier that includes webhooks + API for the ~5–10 office/review users; keep field users on the minimum viable tier. Verify current tiers and pricing with Google directly — this document does not state prices. |
| **BQ-03** | Blocks Phase 3 | Is a **Make.com** organisation available, and on which plan? If not, do we fall back to Google Apps Script? | Use Make. It gives visual error routes, data stores and operational visibility a non-developer can supervise — which matters when the company has one technical decision-maker. |
| **BQ-04** | Blocks Phase 4 | **Claude API** workspace and the monthly spend cap you will authorise. | Provision a dedicated workspace with a hard monthly cap and per-project usage tracking. Analyse only reviewer-approved evidence, on downscaled derivatives, to keep cost proportional to output. |
| **BQ-05** | Blocks Phases 6–7 | Does a **QuickBooks Online company file** exist and is it usable and supported for a Qatar-registered entity? Is a sandbox available? | Confirm with the accountant before any accounting design work. If QBO is not properly supported for the Qatari entity, stop and choose the accounting target explicitly (see R-02) rather than building against an unsupported product. |
| **BQ-06** | Blocks Phase 6 | Confirm the **tax treatment** actually applied to these contracts today (VAT / withholding / none), from the accountant. | Configure a named zero-rate tax rule now; never hard-code "no tax". Written confirmation from the accountant to be filed against A-07. |
| **BQ-07** | Blocks Phase 2 | Who are the **named approvers** — technical reviewer, finance reviewer, releaser — with their email addresses and per-project routing? | GM as sole technical approver and releaser for the MVP; nominate at least one delegate before go-live so absence does not stop billing. |
| **BQ-08** | Blocks Phase 5 | What is the **document numbering scheme**, the company code, and what series are already in use in existing manual documents? | Adopt one central numbering service with a documented format and a recorded starting number per series that continues, and never collides with, existing manual numbering. |
| **BQ-09** | Blocks Phase 5 | **Language policy** for client-facing documents: English only, Arabic only, or bilingual — and for which clients? | English for the MVP. Treat Arabic/bilingual output as a separately approved scope; it roughly doubles template, QA and rendering effort and needs its own testing. |
| **BQ-10** | Blocks Phase 1 sign-off | Do any client contracts (particularly **government/MOEHE**) restrict where evidence and reports may be stored or processed, or require data to stay in Qatar? | Owner to check the contracts. Google Workspace does not offer a Qatar data region; if a contract requires local residency, that changes the storage design and must be known now, not after go-live. |

---

## 6. Phase-by-phase implementation plan

Full plan with gates, exit criteria and test evidence requirements: `07-phase-plan.md`.

| Phase | Outcome | Gate to exit |
|---|---|---|
| **0 — Discovery** *(this document)* | Assumptions, risks, ADRs, MVP boundary, conflicts, configuration register. | **Owner approves this document and answers BQ-01…BQ-10.** |
| **1 — Data foundation** | Data dictionary, table templates, key strategy, status-transition matrix, seed lookup data, ID/versioning/hashing rules. | Data dictionary reviewed; three synthetic projects modelled on paper; transition matrix approved. |
| **2 — Multi-project AppSheet MVP** | Working capture + review app, security filters, ProjectAssignments, per-project locations and activity rules. | **Segregation tested and evidenced** across three synthetic projects; evidence rules block incomplete submission; recorded device test on real phones. |
| **3 — Drive + Make foundation** | Folder provisioning, evidence registration, validation, notification, idempotency, error queue. | Duplicate trigger produces one job, evidenced; originals byte-identical after registration, evidenced; failures land in the error queue with a correlation ID. |
| **4 — Claude evidence analysis** | Versioned prompts, JSON schemas, schema validation, cost control, injection defence. | Schema-invalid output rejected safely, evidenced; injected instruction in a caption ignored, evidenced; cost per 100 photos measured. |
| **5 — Monthly report generation** | Frozen input manifest, template merge, draft + PDF, QA pass, revision control, technical approval, release. | PDF visually inspected page by page; editing an approved source record demonstrably invalidates the document approval. |
| **6 — Contracts, certificates, invoice drafts** | Contracts/BOQ/cumulative controls, completion certificates, deterministic invoice drafts. **No posting.** | Worked financial test cases pass, including over-contract rejection, retention, rounding and duplicate-period detection. |
| **7 — QuickBooks + release** | Sandbox posting, finance approval, reconciliation, approved email delivery with idempotency. | Sandbox invoice reconciles to local totals to the last decimal; no send occurs without a Released record. |
| **8 — Controlled onboarding and scaling** | Real projects onboarded purely as configuration; portfolio dashboards; capacity monitoring. | A new project is onboarded **without any change to app logic, scenarios, prompts or code** — this is the proof that requirement 14 was actually met. |

Working rule: **one phase in progress at a time**, with test evidence recorded at each gate before
the next phase opens.

---

## 7. Risks that could change the design

Full register with controls and owners: `05-risk-and-controls-register.md`.
Specification conflicts and platform limits: `06-spec-conflicts-and-platform-limits.md`.

The seven that could genuinely force a redesign:

| # | Risk | Why it can change the design |
|---|---|---|
| **R-01** | **Google Sheets hits its practical concurrency/volume ceiling.** The Photos table grows fastest — several rows per visit, per location, per day, across dozens of projects. | Forces migration to AppSheet Database or Cloud SQL. Mitigated in advance by ADR-0002: keep all access behind a defined table contract so migration is a swap, not a rewrite, and define the trigger threshold before it is reached. |
| **R-02** | **QuickBooks Online may not be properly supported for a Qatar-registered entity.** | Phases 6–7 change target. This is why invoicing is deferred and BQ-05 is asked before any accounting work begins. |
| **R-03** | **AppSheet image handling may not preserve the camera's original file byte-for-byte** (upload quality settings, EXIF handling). This directly touches operating rule 9. | See conflict C-02. May require defining "original" as *"the file as first received by the system, thereafter never altered"*, or adding a separate raw-upload path. Must be tested on real devices before any immutability claim is made. |
| **R-04** | **Data residency / confidentiality obligations in government contracts.** No Qatar data region exists in Google Workspace. | Could force a different storage location or an on-premise archive. Asked as BQ-10 now, because discovering it after go-live is far more expensive. |
| **R-05** | **Document numbering collisions.** Spreadsheets cannot guarantee atomic increments under concurrency, and legacy manual numbering already exists. | Forces a single atomic numbering service (ADR-0005) and a recorded starting number per series. A duplicate invoice or certificate number in front of a government client is a serious credibility failure. |
| **R-06** | **Adoption risk — the real one.** If supervisors find the app slower than sending photos to WhatsApp, the pipeline starves and everything downstream is worthless. | Drives the whole UX design: minimum fields, dependent dropdowns, offline capture, no typing where a choice will do. Measured explicitly in Phase 2 with real supervisors on real phones, and treated as an acceptance concern, not a training problem. |
| **R-07** | **Key-person concentration.** The internal knowledge base names heavy reliance on the owner as a company weakness; this system, badly designed, would reproduce that by making the GM the only approver. | Drives the delegation-capable approval matrix (A-12, BQ-07) from the start, so the design does not have to change when a delegate is appointed. |

---

## 8. Exact artifacts to be created in Phase 1

Full manifest with content definitions: `08-phase-1-artifact-manifest.md`.
Phase 1 is **documentation, schema definition and seed data only** — still no production system, no
connections, no credentials.

```
docs/01-data-foundation/
  01-data-dictionary.md              Every table, every column: type, key, required,
                                     validation, default, source, sensitivity, example.
  02-key-and-id-strategy.md          UNIQUEID vs UUID, immutability, foreign keys,
                                     canonical serialisation and ContentHash definition.
  03-status-transition-matrix.md     Allowed transitions per entity, actor role per
                                     transition, and what each transition invalidates.
  04-security-model.md               Roles × tables × operations; security-filter
                                     expressions; fields hidden from field roles.
  05-evidence-rules.md               Per-ActivityType evidence requirements and how a
                                     submission is judged complete.
  06-naming-and-numbering.md         File names, document numbers, folder names,
                                     sanitisation, collision handling.
  07-migration-and-versioning.md     Schema versioning, additive-change policy,
                                     backfill and rollback approach.

schemas/
  tables/*.schema.json               Machine-readable definition of each table.
  ai/evidence-analysis.v1.json       JSON schema for §9.1 output (built in P1, used in P4).
  ai/report-qa.v1.json               JSON schema for §9.3 output.

seed/
  roles.csv, units.csv               Controlled vocabularies.
  activity_types.csv                 Landscaping + civil activities from §5.7 with
                                     evidence and quantity rules.
  workflow_statuses.csv              Status vocabulary with descriptions.
  synthetic_projects/*.csv           Three synthetic projects, clients, locations, users
                                     and assignments for segregation testing.
                                     Synthetic only — clearly marked, no real client data.

config/
  config.reference.md                Every external value as a NAMED VARIABLE with owner,
                                     where it is stored, and how it is obtained.
  .env.example                       Variable names only. No values. No secrets. Ever.

docs/
  CHANGELOG.md (updated)             Dated revision entries.
  README.md (updated)                Current phase, status, how to navigate the repo.
```

**Explicitly not created in Phase 1:** no Google Sheet, no AppSheet app, no Drive folder, no Make
scenario, no API connection, no credential, no real client or project data.

---

## Approval

Phase 1 does not begin until the owner records a decision here.

| Decision | Name | Date | Notes |
|---|---|---|---|
| ☐ Approved as written | | | |
| ☐ Approved with changes | | | |
| ☐ Not approved | | | |

**Answers required with approval:** BQ-01 … BQ-10 (see `04-open-questions.md`).
