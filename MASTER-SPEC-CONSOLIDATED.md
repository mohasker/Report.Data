# Al-Haram Integrated Field Reporting, Technical Reports and Invoicing System
## Consolidated Master Specification — the current authority

**Document ID:** AH-SYS-SPEC-C01 · **Version:** 1.1 · **Date:** 2026-09-11
**Prepared for:** Al-Haram for Maintenance & Agriculture — Doha, State of Qatar
**System owner:** General Manager

> ### This document supersedes every earlier specification version.
>
> It incorporates the original requirements baseline of 2026-09-10 **as amended by owner decisions
> D-01 to D-24**. Where it disagrees with `MASTER_SPEC.md`, with any earlier prompt, or with any
> document dated before 2026-09-11, **this document governs**.
>
> `MASTER_SPEC.md` is retained unaltered in substance as the **received baseline**, so that the
> difference between what was asked for and what was agreed remains auditable. It is not the
> authority.
>
> **§0 lists everything that has been withdrawn or superseded.** Read it first. It is the section
> that prevents a reader from reintroducing a statement the owner has already corrected.

---

## 0. Superseded and withdrawn — the register

Nothing in this specification may contradict this table. Each entry is a statement that once
appeared in this project's documents and is now **wrong**, together with what replaced it.

| # | Withdrawn or superseded statement | Status | What is true instead |
|---|---|---|---|
| **W-01** | "Annual cost of USD 2,600–5,000" | **WITHDRAWN — invented figure** | No new mandatory subscription has been identified before entitlement verification. Variable automation, AI and storage costs may arise when those capabilities are enabled |
| **W-02** | "Expected pilot cost is USD 0" | **WITHDRAWN — an overstatement** | It asserted a verified entitlement that has not been verified. AppSheet is *assumed* USD 0 incremental, pending a 15-minute Admin Console check. AI analysis is a real variable cost, estimated at roughly $6.28 a month at pilot volume |
| **W-03** | "Migration to a database at year 1.4" | **WITHDRAWN — false precision** | Migration is triggered by measured thresholds — row counts, sync times, concurrent writers — not by a date |
| **W-04** | "Image bytes must never pass through Make" | **SUPERSEDED — it was wrong as stated** | Three image classes: **original evidence** never passes through, **the AI review derivative** does at pilot volume, **the report derivative** does at document-generation time only. Visual analysis requires the model to see an image |
| **W-05** | A written work description is required on a visit | **SUPERSEDED by D-18** | **A written description of completed work must not be mandatory for a normal photographic submission.** An optional site note carries facts a photograph cannot |
| **W-06** | Any workflow in which the supervisor selects, uploads or attaches the same photographs a second time | **FORBIDDEN by D-16, `CAP-01`** | The evidence is captured exactly once and re-used. If a platform cannot do this, **the platform is replaced — no duplicate-upload workaround is built** |
| **W-07** | "Three pilot projects" as a system property | **WITHDRAWN by D-01** | Three synthetic projects are **test fixtures**. The platform is designed for dozens or hundreds. Three must never become an architectural boundary |
| **W-08** | "The contracts are zero-rated" | **WITHDRAWN by D-08** | The tax treatment is unconfirmed. "Zero-rated", "exempt", "out of scope" and "not configured" are distinct, and the calculation engine returns `UNDETERMINED` and **blocks** rather than producing zero |
| **W-09** | "Arabic doubles the work" | **WITHDRAWN by D-11** | Bilingual structure is designed in from Phase 1. A supervisor writes in either language; both are carried |
| **W-10** | "80 GB a year is a non-issue" | **WITHDRAWN** | Whether it is an issue depends on the company's actual allocation and current consumption, neither of which is known |
| **W-11** | Any statement that local validation demonstrates that AppSheet, Drive, Make, the Claude API, QuickBooks, mobile offline sync or document rendering works | **FORBIDDEN** | Local checks prove a **rule**, not a **system**. §14 states the boundary |
| **W-12** | "Active scenarios: 2" read as a count of running scenarios | **CLARIFIED** | The Make account has **7 scenarios, 0 active**; **2** is the plan's *ceiling* on active scenarios, not a count |
| **W-13** | "WhatsApp is not in scope" without qualification | **CLARIFIED by D-16** | WhatsApp is **not** an input channel and never will be. It **is** an output channel, by native share only, chosen by a human, with no automation, no scraping and no public link |
| **W-14** | AI analysis runs only on reviewer-approved photographs | **SUPERSEDED twice** | D-17 corrected it to every captured photograph; **D-24 corrected that in turn** to every *eligible* photograph. Duplicates, unusable images and anything deleted or excluded never reach a model call. Skipping is about waste, never coverage |
| **W-15** | "The supervisor must supply five fields" — project, location, date, capture mode, evidence stage | **WITHDRAWN by D-22** | **Zero fields are mandatory manual inputs on the normal path.** Identity, date and time are automatic; project, location and capture mode are prefilled; the evidence stage is proposed or left pending; declaring an activity is not the price of submitting evidence |
| **W-16** | The AI activity assessment is untrusted free text, and nothing controlled replaces it | **SUPERSEDED by D-23** | Holding the assessment as untrusted text was right; leaving no structured classification was not. `ConfirmedActivityTypeID` is the trusted activity, set only by a human; the candidate is read by the confirmation screen and nothing else |

---

## 1. Mandatory operating rules

These are unchanged from the baseline and remain in force in full.

1. **Never claim** that the system is complete, functional, secure or tested unless the relevant test
   has actually been executed and its result recorded.
2. **Never invent** credentials, account IDs, folder IDs, API keys, email addresses, QuickBooks
   company IDs, AppSheet application IDs, webhook URLs, tax settings, contract values, invoice
   numbers, quantities, client contacts or approval decisions.
3. Represent every unknown external value as a **named configuration variable**, and request it only
   when it is required for the next safe step.
4. **Never print, commit, log or store secrets** in source code, spreadsheets, prompts, screenshots
   or documentation. Secrets live in secret managers, protected connection stores, orchestration
   connections or environment variables.
5. **Do not perform irreversible external actions during development.** Email sending, invoice
   creation, invoice posting, client sharing, deletion and publication default to sandbox, draft or
   disabled.
6. No report, quotation, completion certificate or invoice may be sent externally **without an
   explicit authorised approval record**.
7. An LLM may draft narrative content and classify evidence, but **must never be the authoritative
   calculator** of invoice totals, taxes, contract balances, measured quantities or payment status.
8. All financial calculations must be **deterministic, traceable, consistently rounded, and
   independently validated** before approval.
9. **Preserve original photographs unchanged.** Never overwrite, resize, enhance, annotate or delete
   the original evidence file. Derivatives are stored separately.
10. The system must distinguish **verified facts, user-entered claims, AI observations,
    recommendations, and unresolved uncertainties.**
11. AI must not state that work was completed merely because a caption says so. Completion must be
    supported by approved evidence or an authorised supervisor confirmation.
12. **Use official supported APIs and OAuth connections. Do not automate WhatsApp Web or use
    unofficial group-scraping libraries.**
13. Do not assume WhatsApp group messages can be read by the official WhatsApp Business API.
    **AppSheet is the field-input channel.**
14. Build incrementally, but **design and implement multi-project capability from the first
    version**. Adding or activating a project must never require changing application logic,
    orchestration scenarios, prompts or source code.
15. Before modifying an existing repository, spreadsheet, automation or app, **inspect it and
    preserve unrelated user work.**

---

## 2. Business context

Al-Haram for Maintenance & Agriculture, Doha, State of Qatar. ISO 9001, ISO 14001, ISO 45001.

Landscape and irrigation maintenance, civil maintenance, painting, epoxy, ceramic and marble works,
suspended ceilings, gypsum and cement-board partitions, signage, sports flooring, and related
maintenance services. Recurring contracts and one-off work orders.

The company operates **dozens of simultaneous and future projects** for different clients, locations,
disciplines, contract types, reporting frequencies, templates, approval chains, currencies and
billing methods. The solution must therefore be a **fully configurable multi-project, multi-client
platform**. Authorised administrators must be able to add, configure, suspend, archive and reactivate
projects as data.

**Legal identity is configurable master data** (D-02), not a value chosen from a document. The
`LegalEntities` table carries EN/AR legal names, CR number, establishment number, registered address,
country, currency, tax registration status, logo reference, official contact details, authorised
signatories, footer details, effective date and version. Synthetic data uses an explicit
`LEGAL_ENTITY_NAME_PENDING_VERIFICATION` placeholder until the current Commercial Registration is
supplied.

---

## 3. Target outcome

An integrated system in which an authorised field user can:

1. Open the field application.
2. **Select or confirm** a project, location, work order, visit date, activity and evidence stage —
   the project prefilled from the assignment where possible.
3. Enter quantities where applicable, and a site note **only where a photograph cannot establish the
   fact**. **A written work description is not required for a normal photographic submission.**
4. **Capture or select the photographs exactly once** (§4).
5. Submit even when connectivity is poor, subject to supported offline behaviour.
6. Synchronise records and original photographs to the controlled store, unchanged.
7. **Share the same stored files and a formatted summary to the existing main-contractor group
   through one native share action** (§4).
8. Allow the General Manager or reviewer to approve, reject, annotate or exclude each submission and
   each photograph.
9. Trigger orchestration only after valid state transitions.
10. Allow advisory AI analysis of the evidence and drafting of professional report text.
11. Generate controlled documents and PDF drafts from approved templates.
12. Generate completion-certificate and invoice drafts from approved contractual and quantity data.
13. Post to accounting only after a separate financial approval.
14. Deliver approved documents by email only after final release approval.

---

## 4. Capture once, use twice — the operating principle

*Owner decisions D-16 to D-24. Canonical form: `model/model.json` → `capture_once`. Rendered:
`docs/02a-plan/24-capture-once-workflow.md`. Tested: `tools/test_capture_once.py`, 28 checks.*

### 4.1 The rule

**The supervisor must never upload, select, or describe the same evidence twice.**

| Step | Actor | Action |
|---|---|---|
| 1 | Supervisor | Opens the field application |
| 2 | System | The assigned project is prefilled where possible — from `ProjectAssignments`, never from the photograph |
| 3 | Supervisor | Selects or confirms the location — a structured reference, never inferred |
| 4 | **Supervisor** | **Captures or selects the photographs once.** The only file selection in the workflow |
| 5 | System | Stores them in the controlled system, unchanged, under one `CaptureBatchID` |
| 6 | AI | **Proposes** visible activity; evidence stage; professional caption; visible condition; possible snag; image-quality warning; uncertainty and confidence |
| 7 | Supervisor | Confirms or corrects with minimum interaction |
| 8 | Supervisor | Shares the same files and a formatted summary to the existing main-contractor WhatsApp group through **one native share action** |
| 9 | System | The same stored evidence is re-used in daily, weekly, monthly, corrective-action, inspection and completion reports |

### 4.2 `CAP-01` — the acceptance requirement

> **The workflow fails acceptance if the supervisor must select or upload the images a second time.**

It binds the first share, a retry after a failed or cancelled share, AI analysis, reviewer
correction, and every report that re-uses the evidence.

### 4.3 Two operating modes

| | **Quick Share** | **AI Reviewed Share** |
|---|---|---|
| Sequence | capture → store → **native share immediately** | capture → store → AI proposal → supervisor confirmation → native share |
| AI | Runs **afterwards**, asynchronously; prepares the internal report metadata | Runs **before** the share |
| Use when | The contractor group must receive the site evidence immediately | A reviewed professional caption is wanted before group submission |
| Captures | **once** | **once** |

### 4.3a Minimum interaction — the supervisor supplies the photographs (D-22)

**On the normal path the supervisor is asked for nothing but the photographs.** Zero fields are
mandatory manual inputs.

| Value | Populated from | When the supervisor is asked |
|---|---|---|
| User identity | The authenticated session | **Never** |
| Date and time | The device clock, at first and last capture | **Never** |
| Project | The single active assignment, else the last used today, else the project default | Only when several assignments are active and none resolves |
| Location | The project default, else the last used today | Only when several active locations exist and none resolves |
| Capture mode | **Defaults to Quick Share** | Never on the normal path |
| Evidence stage | Proposed by analysis, pre-tagged from the activity rule, or left `Pending` | **Never before capture** |
| Additional site note | — | Optional, always |
| Work description | — | **Not required** (§4.4) |

**The intended normal path:** open the app → confirm project and location **if necessary** → capture
the photographs → save and share.

**Declaring an activity is not the price of submitting evidence.** A visit carrying photographs and
no activity is a valid photographic submission; the completeness rule requires *evidence*, not an
activity. An activity that does exist still satisfies its effective rule in full.

**Prefilled is not hidden.** Project and location are always visible on the capture screen and
changeable in one tap, because the cost of asking nothing is that a silent default can be silently
wrong (R-40).

### 4.3b A confirmed structured activity (D-23)

Reports and business rules need a controlled, human-confirmed activity classification. The
proposal and the confirmation are different columns:

| Column | Standing |
|---|---|
| `Photos.AIProposedActivityText` | **Advisory.** Free text. Untrusted |
| `Photos.AIProposedActivityTypeID` | **Advisory candidate.** A suggested catalogue code. Read by the confirmation screen and by nothing else — no report, rule, calculation, filter, join or approval |
| `Photos.ConfirmedActivityTypeID` | **Trusted.** Set only by a supervisor or reviewer. What every report and rule reads, and what the content hash binds |
| `Photos.AIProposalDisposition` | What the supervisor did with the proposal |
| `Photos.ClassificationStatus` | `Pending` · `AIProposed` · `Confirmed` · `NotApplicable` · `Excluded` |

**For Quick Share, classification may remain `Pending` and be reviewed later.** Pending is a normal
state and blocks nothing. **AI-generated free text must never directly become the trusted structured
activity.**

### 4.3c When analysis runs, and when it does not (D-24)

**Do not assume every captured photograph requires a separate immediate AI call.**

| | **AI Reviewed Share** | **Quick Share** *(default)* |
|---|---|---|
| Timing | Immediate, before the share | **Deferred**, after the share |
| Filtering | Local duplicate and quality checks first | Duplicates, unusable images, deletions **and exclusions** first |
| Why | The supervisor is waiting | Nothing is waiting, so the cheapest correct moment is after the waste is removed |

**Never analysed:** a near-duplicate of one already analysed in the batch; an image below the
project's quality threshold; an image deleted or explicitly excluded before analysis ran; an image
already analysed; anything in a project where analysis is off or the monthly cap is reached.

**Still analysed:** every photograph a reviewer may approve for a report. **Skipping is about waste,
never about coverage.**

**The filters cost nothing** — a perceptual hash and a blur measure, both local.

**Recalculated, as estimates until the pilot measures them:** eligibility ~83% (Quick Share) and
~92% (AI Reviewed Share); Claude ~$6.28 and ~$6.95 a month; Make ~1,167 and ~1,353 operations a
month, so **neither policy fits the free orchestration tier** — three operations per photograph is
irreducible once bytes pass through an orchestrator.

### 4.4 The field description

**A written description of completed work must not be mandatory for a normal photographic
submission.**

- **Additional Site Note** — optional, classified by `SiteNoteCategory`.
- **Voice note and speech-to-text** — future input methods for that same field, not new fields.
- **A mandatory reason survives only** in exceptional workflows where photographs cannot establish
  the required fact: a record returned for correction; a visit reporting non-completion; a caption on
  an Observation, Snag, Material or Safety photograph; a measured quantity claimed without a
  photographed measurement.

The optional note exists for information that cannot be reliably derived from an image: client
instruction; access restriction; permit issue; hidden or underground defect; measured quantity;
material quantity or batch; equipment failure; reason for non-completion; safety restriction; work
postponed by another party.

### 4.5 AI limitations

AI may describe **only visually supportable** conditions and activities. It must not infer or
confirm:

measured quantity · hidden defect or cause · exact material brand · compliance with contract or
specification · exact completion percentage · exact project or location from the photograph alone ·
responsibility or negligence · date unless supplied as trusted metadata · that Al-Haram executed the
visible work merely because it appears in the photograph.

**Project, location, date, assigned user, contract and work-order context must come from trusted
system data.** Sixteen columns are closed to AI by declaration and by automated check. The AI's view
of the activity is free text, deliberately **not** a reference to the activity catalogue, so no
contractual activity can be created by an image.

Every proposal is written to its own advisory column, is excluded from every content hash, and is
never copied into the confirmed value except by an explicit human action recorded in
`Photos.AIProposalDisposition`.

### 4.6 The capture-platform requirement — `CAP-GATE`, unverified

**Phase 2A must verify whether the capture platform can reliably share multiple actual image files
and formatted text through the native share sheet to an existing WhatsApp or WhatsApp Business group,
on iOS and Android.**

Fifteen conditions, both platforms, both modes: one photograph; six photographs; portrait and
landscape; image order; formatted summary; standard WhatsApp; WhatsApp Business; normal connection;
weak connection; offline capture then synchronisation; whether images are attached or only links;
**whether the user must select the images again**; whether a public Drive link is created; whether
temporary files remain on the device; failed or cancelled share recovery.

**If the platform cannot meet the requirement, do not implement a duplicate-upload workaround.**
Prepare a decision comparison between:

1. AppSheet with a proven native-share method.
2. A lightweight custom PWA or mobile field application using supported native file sharing.
3. Any other official, policy-compliant approach.

**The same backend data model, Drive security, orchestration, AI controls, approval rules and audit
requirements must remain re-usable if the capture interface changes.**

### 4.7 What is forbidden

Unofficial WhatsApp Web automation · group scraping · any unofficial messaging automation · a
publicly accessible Drive link to evidence · any flow that asks the supervisor to select the files
again · compressing, re-encoding or altering original evidence.

### 4.8 The honest limit

The application can record that the share sheet was opened and that the supervisor confirmed it
completed. **It cannot observe delivery inside the messaging application.** No document may claim
otherwise. `ShareStatus` values are named for what they actually assert.

---

## 5. Architecture

```
  CAPTURE      Field application  - AppSheet, pending CAP-GATE
  STORE        Google Sheets (tables, behind a contract) + Google Drive (evidence, write-once)
  ORCHESTRATE  Make.com - validation, registration, notification, monitoring
  ANALYSE      Claude API - advisory only
  PRODUCE      Google Docs -> PDF, one generation path, numbered and released
  ACCOUNT      QuickBooks Online - Phase 7, behind a separate approval
```

### The four invariants

1. **One canonical model.** `model/model.json`, authored by `tools/build_model.py`. Schemas, data
   dictionary, transition matrix, security matrix, AppSheet workbook, security filters, scope matrix,
   release-1 scope and the capture-once workflow are all **generated** from it and cannot drift.
   **Never hand-edit a generated file.**
2. **Row-level security derives solely from `ProjectAssignments`** and is re-validated server-side.
   Views and slices are presentation, never enforcement.
3. **Approvals bind to `ContentHash` + `EntityVersion`.** Advisory AI fields are excluded from every
   content hash by design, so an analysis arriving later can never void a human approval.
4. **Numbering is reserved → issued → cancelled**, through one atomic counter. Never reused, never
   silently skipped.

### Architecture decisions

Nine ADRs in `docs/00-discovery/adr/`, each with context, options, decision, consequences and what
would cause it to be revisited: company-owned Shared Drive with a system-owned account; Sheets as the
MVP store behind a table contract; Make as orchestrator; **AI advisory only**; one central numbering
service; approvals bind to a content hash; a single document generation path; deterministic
calculation before any accounting posting; and **capture once, use twice with a native share**.

---

## 6. Data model

**46 tables, 857 columns, 32 enums, 82 declared transitions, 36 explicitly forbidden, 10 roles × 46
tables = 460 access grants with 20 documented exceptions.**

### Build order

| Stage | Tables | Capability |
|---|---|---|
| **Release 1** | **12** | Capture and review. **No document generation** |
| Release 1b | +4 | Report generation: `DocumentJobs`, `Documents`, `NumberRegister`, `LegalEntities` |
| Lean MVP | **17** | + `ProjectActivityRules` |
| Reference architecture | **46** | The other 29 designed, schema'd, added additively |

**Release 1:** `Users`, `Projects`, `ProjectAssignments`, `Locations`, `ActivityTypes`, `SiteVisits`,
`VisitActivities`, `Photos`, `Snags`, `Approvals`, `AuditLog`, `IntegrationJobs`.

**Field exposure:** 290 fields in storage · 162 generated and never typed · 236 synchronised to a
device · 54 administrative and absent from the field data set · **15 on the normal field form, of
which 0 are mandatory (D-22)**. Project and location are confirmed only when they do not resolve
automatically; everything else is populated, optional, or a one-tap confirmation.

### Evidence stage vocabulary

`Before` · `During` · `After` · `Observation` · `Snag` · `Material` · `Equipment` · `Safety` ·
`Other`. Captions are mandatory on Observation, Snag, Material and Safety.

### Bilingual model

Paired EN/AR columns with an `at_least_one` constraint, NFC normalisation, and **no
transliteration**. A supervisor may write in either language; both are carried to the report. Arabic
template *production* is deferred; the bilingual *architecture* is not.

---

## 7. Security and approvals

Ten roles. Project segregation derived solely from `ProjectAssignments`, re-validated server-side.
**No delete grant exists for any role on any table.** Self-approval is refused in the action, the
slice and the rule. Neither administrator may read evidence or documents — a deliberate separation of
duties. Every temporary access grant requires a reason, an expiry, a notification and an audit
reference, all four mandatory. Break-glass restores **administration**, not content. Recoverability
is a **computable go-live blocker**: no go-live without a second administrator or a documented,
tested recovery route.

---

## 8. Deterministic calculation

Decimal arithmetic, `ROUND_HALF_UP`, a stored calculation trace, and independent validation before
approval. **An unconfirmed tax treatment returns `UNDETERMINED` and blocks. It never yields zero.**
No LLM output may reach a monetary path.

---

## 9. AI usage

Four versioned prompts: `evidence-analysis`, `evidence-analysis-batch`, `report-narrative`,
`report-qa`, plus `invoice-narrative`. Closed JSON schemas (`additionalProperties: false`) validated
before anything is stored; a response that does not validate is classified `SchemaMismatch`,
dead-lettered with a sanitised payload, and never retried blindly.

**The evidence schemas contain no numeric quantity, measurement, area, length, count, brand,
compliance, responsibility or completion-percentage field of any kind.** A model cannot report a
quantity because there is nowhere to put one. That is a structural control, not an instruction.

Analysis is **batched by capture batch** — one request per capture, not one per photograph. Data
minimisation: the derivative, the activity name, the recorded stage, the caption and the date are
sent; the client name, project name, location name and GPS coordinates are withheld. Prompt-injection
attempts found in an image, caption or filename are ignored and reported.

**Cost:** ~$0.021 per analysed photograph on the default model at a 1024 px derivative;
**~$6.28 a month at pilot volume** under Quick Share and ~$6.95 under AI Reviewed Share — an
estimate, not a measurement; bounded by a hard monthly cap the owner sets.

**Analysis is filtered before it is paid for (D-24).** Near-duplicates, images below the quality
threshold, anything deleted or explicitly excluded, and anything already analysed never reach a
model call. The filters — a perceptual hash and a blur measure — run locally at no cost. Estimated
eligibility is ~83% under Quick Share and ~92% under AI Reviewed Share. **Skipping is about waste,
never about coverage:** a skipped photograph is kept as evidence in full and remains approvable for
any report.

---

## 10. Orchestration

Idempotency keys before any side effect. Server-side re-validation of every webhook payload.
Classified, correlated error rows for every failure — nothing fails silently. **`IntegrationJobs` is
the authoritative record**, because the orchestration platform retains only 7 days of history.

**Verified capacity constraints** (Make free plan, inspected 2026-09-11): 1,000 operations/month;
**2** active scenarios; 1 data store of 1 MB; 512 MB transfer; 5 MB maximum file size; 15-minute
minimum interval; 5-minute maximum execution; no overage — work **stops** at the ceiling.

Release 1 is budgeted at **703 operations, 70% of the limit, 2 active scenarios**, with retries,
corrections, duplicates and administrative tests all funded and **no reduction in validation,
auditability or error handling**.

**A stated finding:** the AI proposal step does **not** fit this tier — roughly 1,440 operations a
month. Four costed responses exist; release 1 ships Quick Share, and the capture-once guarantee holds
regardless.

---

## 11. Documents and numbering

One generation path. Templates keyed by **type and language**, right-to-left capable. Series
configurable by entity, document type, year, scope, client and revision. Reserved → issued →
cancelled, atomic, never reused. Generation runs from an **immutable approved snapshot**, so a
document always states what was approved at the moment it was approved.

---

## 12. Accounting

Deferred to Phase 7, behind a separate financial approval, with `QBO_POSTING_ENABLED` defaulting to
FALSE. The company file's capability for tax codes, classes, currencies and API operations is
**inspected, not assumed** — 24 questions in `docs/01-data-foundation/13-quickbooks-mapping-and-inspection.md`.

---

## 13. Phases

| Phase | Scope | Status |
|---|---|---|
| 0 | Discovery | **Approved** |
| 1 | Data foundation | **Completed · Validated Locally · Submitted for Owner Review** |
| **2A** | **Plan and synthetic prototype design** | **Completed · Submitted for Owner Review.** Connects nothing |
| 2B | First external connection, segregation and field measurement | **Not authorised** |
| 3 | Orchestration and Drive provisioning | Not started |
| 4 | AI analysis | Not started. **May be skipped entirely — the pipeline works without it** |
| 5 | Documents and reports | Not started |
| 6 | Contracts, quantities and certificates | Not started |
| 7 | Accounting integration | Not started |

---

## 14. Acceptance criteria, and what is proven

Seventeen acceptance criteria, each mapped to the checks that bear on it in
`docs/01-data-foundation/17-validation-evidence.md`. Three are proven in logic, ten are partial, and
four are untested because the capability does not exist yet.

**240 automated checks across 13 suites, all passing, against synthetic data, locally. Byte-identical
regeneration confirmed.**

### What that does NOT prove

**Local model validation must never be represented as proof that AppSheet, Google Drive, Make, the
Claude API, QuickBooks, mobile offline synchronisation or document rendering works.** Specifically
unproven: platform security-filter enforcement; offline capture and sync on real devices; image
fidelity; Drive provisioning idempotency and originals surviving registration byte-for-byte;
scenario execution and real idempotency; schema-valid model output and real injection resistance;
Arabic and right-to-left PDF rendering; accounting reconciliation; **field usability — whether a
supervisor can complete a visit faster than the habit it replaces**; and **`CAP-GATE` — whether any
platform can perform the native multi-file share at all**.

### The two acceptance criteria added by the correction

| # | Criterion | Evidence |
|---|---|---|
| 15 | **Capture once, use twice: the supervisor never selects or uploads the same evidence twice** | `CAP-01`, `CAP-18`, `CAP-19`, `CAP-20`, `CAP-21` in the model. **Not tested on any platform — this is `CAP-GATE`** |
| 16 | **A written description is never mandatory for a normal photographic submission** | `CAP-02` … `CAP-05`, `CAP-26`. **Proven in logic**, with a regression guard |
| 17 | **AI proposes; a human decides; trusted context never comes from a photograph** | `CAP-06` … `CAP-15`. **Proven in logic.** Whether a real model obeys its prompt is Phase 4 |

---

## 15. Cost position

> **No new mandatory subscription has been identified before entitlement verification. Variable
> automation, AI and storage costs may arise when those capabilities are enabled.**

Workspace and QuickBooks are already paid. AppSheet is **assumed** USD 0 incremental pending the
Admin Console check; if it is not included, a specific costed option goes to the owner and **no
purchase is made without written approval**. Make is free for release 1 and not permanently free. AI
analysis is estimated at ~$6.28 a month at pilot volume. Storage is ~377 MB live per project-month,
~679 MB with one backup.

**W-01, W-02 and W-03 in §0 are withdrawn and must not reappear.**

---

## 16. Outstanding external facts

26, each recorded with the phase it blocks, in
`docs/01-data-foundation/16-external-facts-register.md`. **None has been guessed at.**

The two that gate the next step: the **Admin Console entitlement check** (the owner, 15 minutes) and
**`CAP-GATE`** (a real-device test that nobody can answer from documentation).

---

## 17. Standing prohibitions

Do not connect any production account. Do not create, activate or modify any orchestration scenario,
webhook or connection. Do not purchase or upgrade any plan. Do not upload real client data, real
photographs or real user identities. Do not send any email or external message. Do not deploy or
publish any application. Do not automate WhatsApp Web or scrape any group. Do not create a publicly
accessible link to evidence. Do not compress or alter original evidence. Do not implement a
duplicate-upload workaround. Do not assign real people or email addresses until the owner supplies
them. Do not touch the seven pre-existing orchestration scenarios, which belong to unrelated company
work.

**Every one of these requires the owner's separate written authorisation, and none has been given.**
