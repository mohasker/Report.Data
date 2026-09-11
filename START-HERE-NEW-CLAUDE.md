# START HERE — Al-Haram Field Reporting System

**This file is the entry point for a new Claude account taking this project over.**

**Package version:** 1.0 · **Date:** 2026-09-11
**Repository:** `mohasker/Report.Data` · **Branch:** `claude/alharam-field-reporting-spec-afq1fr`
**Validated commit:** `20af0a20c9770d9e782219b5a4186c3f4914800f`
**Package commit:** recorded in `HANDOFF-MANIFEST.json` → `package_commit`

> **Read this file completely before running anything.** It is written to be self-contained: it
> assumes you have no access to the previous conversation, no memory of this project, no internal
> company skill, and possibly no repository links that resolve. Everything you need to continue is
> either stated here or named by an exact path inside the package.

---

## 0. The two instructions that matter most

**1. Do not restart, redesign, or reconnect anything.** This project is roughly 219 automated checks
and 70-odd documents into a deliberate, phased build. The design has been reviewed and corrected by
the owner six times. If something looks wrong, it is far more likely to be a decision you have not
read yet than a mistake. Read `DECISIONS-AND-ASSUMPTIONS.md` before proposing any change.

**2. You have no external access and no authorisation to obtain any.** No Google account, no
AppSheet application, no Make scenario, no Claude API key, no QuickBooks connection, no real
photographs, no real people, no email. **Nothing in this project may be connected without the
owner's separate written authorisation**, and that authorisation has not been given. Section 21
below states the boundary exactly.

Also: **do not assume any internal company skill, private knowledge base, or prior chat is available
to you.** If a document refers to one, treat the document as the source of truth and say so.

---

## 1. Company and system objective

**Al-Haram for Maintenance & Agriculture** — Doha, State of Qatar. An integrated facilities
management and contracting company: landscape and irrigation maintenance, civil maintenance,
painting, epoxy, ceramic and marble works, suspended ceilings, gypsum and cement-board partitions,
signage, sports flooring. ISO 9001, ISO 14001, ISO 45001. The system owner is the **General
Manager**.

The company runs **dozens of simultaneous and future projects** for different clients, locations,
disciplines, contract types, reporting frequencies, templates, approval chains, currencies and
billing methods.

**The objective:** an integrated system in which an authorised field user captures evidence of work
once, on a phone, and that single capture flows through review, approval, professional reports,
completion certificates and eventually invoices — without the evidence being re-entered, re-selected,
or reconstructed from memory. Today the company's evidence lives in a messaging group and its
reports are written afterwards from recollection.

---

## 2. Approved business requirements

The authoritative statement is **`MASTER-SPEC-CONSOLIDATED.md`** in this package. Read it second,
after this file. `MASTER_SPEC.md` is the original baseline as the owner supplied it, retained so the
difference between what was asked for and what was agreed stays auditable; where the two disagree,
the consolidated version governs.

The requirements in one page:

| # | Requirement |
|---|---|
| 1 | **Multi-project from the first version.** No project name, location, client, activity, folder, template, approval route, report rule or billing rule may be hard-coded. Adding a project must be master-data configuration only |
| 2 | **Capture once, use twice.** The supervisor never uploads, selects or describes the same evidence twice — see §7 |
| 3 | **Row-level project segregation.** No data, image, recipient, template, document number or financial record may cross a project boundary |
| 4 | **Originals preserved unchanged.** Never overwritten, resized, enhanced, annotated or deleted. Derivatives are separate records |
| 5 | **AI is advisory, never authoritative.** It may describe and suggest; it may never decide, approve, calculate or classify of record |
| 6 | **Deterministic financial calculation.** Traceable, consistently rounded, independently validated. An unconfirmed tax treatment blocks; it never silently yields zero |
| 7 | **Approvals bind to content.** An approval records what exactly was approved, by hash, so editing approved source data invalidates or versions the approval |
| 8 | **Bilingual EN/AR from the start**, right-to-left capable, no transliteration |
| 9 | **Nothing irreversible during development.** Email, invoice creation, posting, sharing, deletion and publication default to disabled |
| 10 | **No claim of completeness or correctness without a recorded, executed test.** This rule has been enforced literally throughout |
| 11 | **Never invent** a credential, account ID, folder ID, API key, email address, company ID, webhook URL, tax setting, contract value, invoice number, quantity, client contact or approval decision |
| 12 | **Official APIs only.** No WhatsApp Web automation, no group scraping |

---

## 3. Current architecture

A layered design in which each layer can be replaced without the others being rewritten.

```
  CAPTURE          AppSheet mobile application  (UNVERIFIED - see §20, CAP-GATE)
                   - the only layer whose platform is not yet decided
       |
  STORE            Google Sheets  = the operational tables, behind a table contract
                   Google Drive   = original evidence, write-once, never shared publicly
       |
  ORCHESTRATE      Make.com  = validation, registration, notification, monitoring
                   - identifiers and small payloads, not image bytes (with one
                     costed exception: the AI review derivative)
       |
  ANALYSE          Claude API  = advisory description and drafting only
       |
  PRODUCE          Google Docs -> PDF, one generation path, numbered and released
       |
  ACCOUNT          QuickBooks Online  = Phase 7 only, behind a separate approval
```

**Four invariants hold across every layer:**

1. **The canonical model is the single source of truth.** `model/model.json` is authored by
   `tools/build_model.py`; the schemas, data dictionary, transition matrix, security matrix,
   AppSheet workbook, security filters, scope matrix, release-1 scope and capture-once workflow are
   all **generated** from it. They cannot drift. Never hand-edit a generated file.
2. **Row-level security derives solely from `ProjectAssignments`**, is re-validated server-side, and
   is never enforced by a view or a slice. Views are presentation.
3. **Approvals bind to `ContentHash` + `EntityVersion`.** Advisory AI fields are deliberately
   excluded from every content hash, so an analysis arriving later can never void a human approval.
4. **Numbering is reserved → issued → cancelled**, through one atomic counter. Numbers are never
   reused and never silently skipped.

---

## 4. Multi-project requirement

This is the owner's first and most emphatic correction (D-01), and it constrains everything.

Three synthetic projects exist in `seed/synthetic_projects/` as **test fixtures only**. They
demonstrate segregation, differing clients, locations, disciplines, activity rules, assigned users,
approval routes, templates, numbering and billing configuration.

**Three projects must never become an operational limitation or an architectural boundary.** Adding
a project must require only controlled master-data configuration — never modified application logic,
a cloned application, duplicated scenarios, rewritten prompts, changed formulas or source code, and
never a separate system per project.

This is enforced by test, not by intention: `tools/test_configurability.py` scans every logic file
for a hard-coded identifier and then adds a fourth project **in memory** and re-runs the rule engines
against it. Twelve checks. If you introduce a hard-coded project reference anywhere, the suite fails.

---

## 5. Lean scope — what actually gets built first

| Layer | Tables | What it is |
|---|---|---|
| **Release 1** | **12** | Capture and review only. **Produces no document** |
| Release 1b | +4 | `DocumentJobs`, `Documents`, `NumberRegister`, `LegalEntities` — report generation |
| Lean MVP | **17** | Release 1 + 1b + `ProjectActivityRules` |
| Reference architecture | **46** | The full model. The other 29 are designed, schema'd, and added additively |

**The twelve tables of release 1:** `Users`, `Projects`, `ProjectAssignments`, `Locations`,
`ActivityTypes`, `SiteVisits`, `VisitActivities`, `Photos`, `Snags`, `Approvals`, `AuditLog`,
`IntegrationJobs`.

**Four consolidations**, each with a stated cost: `ProjectActivityRules` folds into `ActivityTypes`
with an optional ProjectID; `Roles` becomes a RoleCode enum; `Clients` becomes three columns on
`Projects`; and `LegalEntities` + the three document tables are simply absent, because release 1
generates nothing.

**Field exposure — the answer to "do not deploy hundreds of fields to a phone":** 282 fields in the
release-1 storage model, 151 of them generated and never typed, 228 synchronised to a device, 54
administrative and absent from the field data set entirely, **17 on the normal field form, of which
only 5 are mandatory** — project, location, date, capture mode, evidence stage. **None of the five is
a description.**

An honest caveat that must not be lost: a row synchronises whole. Views and slices control what is
*shown*, not what is *delivered*. The two levers that genuinely reduce sync payload are keeping a
table out of the field role's data set, and keeping row counts down through security filters.

Detail: `docs/02a-plan/21-release-1-twelve-tables.md` (generated) and
`docs/02a-plan/11-lean-mvp-scope.md`.

---

## 6. The 46-table reference architecture

46 tables, 849 columns, 30 enums, 82 declared transitions and 36 explicitly forbidden ones, 10 roles
× 46 tables = 460 access grants with 20 documented exceptions.

| Domain | Tables |
|---|---|
| Identity and access | `Users`, `Roles`, `ProjectAssignments`, `TemporaryAccessGrants`, `EntityVersions`, `SystemRecoveryPlan`, `DataClassifications` |
| Clients and projects | `Clients`, `Contacts`, `Projects`, `Locations`, `Disciplines`, `ActivityTypes`, `ProjectActivityRules`, `Units`, `Languages` |
| Visits, activities, evidence | `SiteVisits`, `VisitActivities`, `Photos` |
| Corrective action | `Snags` |
| Resources | `Materials`, `MaterialUsage`, `Equipment`, `VisitEquipment`, `Employees`, `VisitManpower` |
| Contracts and quantities | `Contracts`, `WorkOrders`, `BOQItems` |
| Documents | `DocumentTypes`, `DocumentTemplates`, `DocumentJobs`, `Documents`, `NumberingSeries`, `NumberRegister` |
| Finance | `InvoiceRequests`, `InvoiceLines`, `TaxRules` |
| Approvals | `Approvals`, `ApprovalMatrix`, `ApprovalDelegations` |
| Governance | `LegalEntities`, `ResidencyRequirements`, `ResidencyAssignments`, `AuditLog`, `IntegrationJobs` |

Deferred tables are scheduled by phase: resources at Phase 5, contracts and finance at Phase 6,
residency at Phase 3. Every one keeps its schema in `schemas/tables/`, so adding it later is
**additive**, not a migration.

Full detail: `docs/01-data-foundation/01-data-dictionary.md` (generated, every column).

---

## 7. Capture once, use twice — the operating principle

**This is the most recent owner correction (D-16 … D-21) and the one most likely to be violated by
an assistant who has not read it.** Canonical form: `model/model.json` → `capture_once`. Rendered:
`docs/02a-plan/24-capture-once-workflow.md`. Tested: `tools/test_capture_once.py`, 28 checks.

**The supervisor must never upload, select or describe the same evidence twice.**

1. The supervisor opens the field application.
2. The assigned project is prefilled where possible.
3. The supervisor selects or confirms the location.
4. **The supervisor captures or selects the photographs once.** This is the only file selection in
   the entire workflow.
5. The photographs are stored in the controlled system under one `CaptureBatchID`.
6. AI analyses them and **proposes**: visible activity; evidence stage (Before, During, After,
   Observation, Snag, Material, Equipment, Safety, Other); a professional caption; visible
   condition; a possible snag; an image-quality warning; uncertainty and confidence.
7. The supervisor confirms or corrects with minimum interaction.
8. The same image files and a formatted summary go to the existing main-contractor WhatsApp group
   through **one native share action**.
9. The same stored evidence is re-used in daily, weekly, monthly, corrective-action, inspection and
   completion reports.

> **`CAP-01` — the acceptance requirement: the workflow fails acceptance if the supervisor must
> select or upload the images a second time.** It binds the first share, a retry after a failed or
> cancelled share, AI analysis, reviewer correction, and every report that re-uses the evidence.

**Two operating modes, both capturing exactly once:**

| | Quick Share | AI Reviewed Share |
|---|---|---|
| Sequence | capture → store → **native share immediately** | capture → AI proposal → confirm → native share |
| AI | asynchronous, afterwards; prepares internal report metadata | synchronous, before the share |
| Use when | the contractor group must receive the evidence immediately | a reviewed professional caption is wanted first |

**Forbidden, permanently:** a duplicate-upload workaround; a publicly accessible Drive link;
WhatsApp Web automation; group scraping; any flow that asks the supervisor to select the files again.

**An honest limit that must be repeated, not softened:** the application can record that the share
sheet was opened and that the supervisor said it completed. It **cannot** observe delivery inside the
messaging application. No document may claim otherwise.

---

## 8. Optional notes and AI analysis rules

### The written description is optional (D-18)

**A written description of completed work must not be mandatory for a normal photographic
submission.** The photographs are the submission. `SiteVisits.AdditionalSiteNote` is optional, with
`SiteNoteCategory` naming why it was written. Voice note and speech-to-text are future **input
methods for that same field**, not new fields.

The optional note exists for facts a photograph cannot carry: client instruction; access
restriction; permit issue; hidden or underground defect; measured quantity; material quantity or
batch; equipment failure; reason for non-completion; safety restriction; work postponed by another
party.

A mandatory reason survives only in four exceptional workflows: a record returned for correction; a
visit reporting non-completion; a caption on an Observation, Snag, Material or Safety photograph;
and a measured quantity claimed without a photographed measurement.

`CAP-26` is a regression guard: if any document in `docs/` reintroduces a mandatory work
description, the validation suite fails.

### What AI may never infer (D-19)

AI may describe only **visually supportable** conditions and activities. It must not infer or
confirm:

1. measured quantity · 2. hidden defect or its cause · 3. exact material brand · 4. compliance with
contract or specification · 5. exact completion percentage · 6. exact project or location from the
photograph alone · 7. responsibility or negligence · 8. date, unless supplied as trusted metadata ·
9. that Al-Haram executed the visible work merely because it appears in the photograph.

**Project, location, date, assigned user, contract and work-order context come from trusted system
data.** Sixteen columns are closed to AI by declaration and by check `CAP-14`. The AI's view of the
activity is free text in `Photos.AIProposedActivityText`, deliberately **not** a reference to
`ActivityTypes`, so no contractual activity can be created by an image (D-20).

Every proposal goes to its own advisory column; no AI column enters any content hash; the
supervisor's response is recorded in `Photos.AIProposalDisposition` so a confirmation is always
distinguishable from a correction.

---

## 9. Platform responsibilities

| Platform | Responsible for | Explicitly not responsible for |
|---|---|---|
| **AppSheet** | The field interface: capture, forms, offline queueing, dependent dropdowns, the review screens, and the native share action | Security enforcement of record (server-side re-validation is authoritative), calculation, document generation |
| **Google Sheets** | The operational tables, behind a table contract so the store can be replaced | Business logic. No formula in a sheet is authoritative |
| **Google Drive** | Original evidence, write-once, never publicly shared; generated documents | Any processing of originals |
| **Make.com** | Validation, evidence registration, notification, monitoring, numbering counters. Identifiers and small payloads | Routing original image bytes. Being the record of its own runs — its history retains 7 days, so `IntegrationJobs` is authoritative |
| **Claude API** | Advisory description of evidence, narrative drafting from approved records, draft QA | Any decision, approval, classification of record, quantity, percentage or monetary figure |
| **QuickBooks Online** | Accounting, from Phase 7, behind a separate financial approval | Being the source of truth for quantities or certified values |

---

## 10. Security and approval model

**Ten roles:** `SystemAdministrator`, `BusinessAdministrator`, `GeneralManager`, `TechnicalReviewer`,
`FinanceReviewer`, `ProjectManager`, `SiteSupervisor`, `FieldUser`, `ReadOnlyAuditor`,
`EmergencyAccess`.

| Principle | How it is held |
|---|---|
| Project segregation | Derived solely from `ProjectAssignments`, re-validated server-side. 12 checks across 6 profiles × 7 tables |
| Neither administrator may read evidence or documents | A deliberate separation of duties. It is the exception most likely to provoke owner disagreement, and it is stated plainly in the review pack |
| No delete grant exists | For any role, on any table. Rejected evidence is retained, marked rejected |
| Self-approval is impossible | Refused in the action, in the slice, and in the rule |
| Approvals bind to content | `ContentHash` + `EntityVersion`. Editing approved source data invalidates or versions the approval |
| Time-bound access | Every temporary grant requires a reason, an expiry, a notification and an audit reference. All four mandatory |
| Break-glass | `EmergencyAccess` restores **administration**, not content. It cannot read evidence |
| Recoverability | A computable go-live blocker: no go-live without a second administrator or a documented, tested recovery route |

Detail: `docs/01-data-foundation/04-security-model.md` (generated) and `10-approval-and-delegation-model.md`.

---

## 11. Current verified external facts

**Exactly one external system has been inspected, read-only, with written owner authorisation.**
Everything else in this project is design.

**Make.com account, inspected 2026-09-11** (`docs/02a-plan/15-make-inspection-record.md`):

| Fact | Value |
|---|---|
| Zone | `us2.make.com` — **United States**. A data-residency fact, recorded for the contract review |
| Plan | **Free** |
| Operations | **1,000 per month**, 0 consumed |
| **Scenarios present** | **7** |
| **Currently active** | **0** |
| **Plan ceiling on active scenarios** | **2** — a ceiling, not a count |
| Data stores | 1, maximum 1 MB |
| Data transfer | 512 MB/month |
| Maximum file size | 5 MB |
| Minimum scheduling interval | 15 minutes |
| Overage | **None.** Work stops at the ceiling; it does not silently bill |
| Required integrations | **All present** — Sheets, Drive, Docs, Gmail, Webhooks, AppSheet, Data store, Anthropic Claude, QuickBooks, HTTP, JSON |

**The seven existing scenarios belong to unrelated company work.** They were listed and nothing more:
none was opened, no execution history was read, no connection, key or webhook was inspected.
**They must not be modified, renamed, activated, deleted or reused without separate authorisation.**
Anything created for this project goes in a dedicated `AHFR` folder with its own naming convention,
label, system-account ownership and project-only connections.

**Claude vision capability** was verified from official documentation: three source types
(base64, URL, file_id), a 10 MB base64 limit, visual tokens ≈ ⌈w/28⌉ × ⌈h/28⌉, image metadata is not
read by the model, and in-request images are ephemeral and auto-deleted — which is why base64 in the
request was chosen over any stored or linked copy.

---

## 12. Current unverified facts

| # | Unverified | Blocks | Note |
|---|---|---|---|
| **EF-24** | **`CAP-GATE`** — whether the capture platform can share several stored image files and formatted text through the native share sheet to an existing WhatsApp or WhatsApp Business group, iOS and Android, **without a second image selection** | The capture-platform decision | **Nobody knows this.** It is not documented anywhere. Only a real-device test answers it. Highest-impact unknown in the project |
| **EF-01/EF-03** | Whether the existing Workspace subscription includes AppSheet, and whether that tier provides **security filters** and **offline use** | The build itself | A 15-minute Admin Console check the owner has been given and has not yet returned |
| **EF-25** | Whether AppSheet has **API access or webhook automation** | Whether the AI proposal costs anything to run | Question 4 of the same check |
| — | Make's paid-tier price | Any upgrade decision | make.com is unreachable from the build environment. The owner can read it on their own billing page |
| — | Whether Workspace storage is sufficient | Sizing, not the build | The Storage screen of the same check |
| — | Whether photographs are re-encoded by the capture platform | The "original device image" claim | `IsOriginalDeviceImageVerified` stays FALSE until a real device proves otherwise |
| — | Whether a visit can be submitted in ≤ 75 seconds | Nothing; it is an acceptance target | A design target from a tap count. **Never describe it as achieved** |
| **EF-17** | The tax treatment of these contracts, in writing, from the accountant | Production invoicing | "Zero-rated", "exempt", "out of scope" and "not configured" are distinct. The engine returns `UNDETERMINED` and blocks rather than producing zero |

26 outstanding external facts in total: `docs/01-data-foundation/16-external-facts-register.md`,
each with the phase it blocks.

---

## 13. Cost position

> **No new mandatory subscription has been identified before entitlement verification. Variable
> automation, AI and storage costs may arise when those capabilities are enabled.**

That sentence is the whole position and it has been carefully worded. Three earlier statements were
**withdrawn** and must not be reintroduced:

- ~~USD 2,600–5,000 annually~~ — invented, withdrawn.
- ~~"Expected pilot cost is USD 0"~~ — an overstatement; it asserts a verified entitlement that has
  not been verified.
- ~~"Migration at year 1.4"~~ — a false precision; replaced by threshold triggers.

| Item | Position |
|---|---|
| Google Workspace | Already paid. **No incremental cost** |
| QuickBooks Online | Already in use. **No incremental cost** |
| AppSheet | **Assumed USD 0 incremental, pending verification.** If not included, a specific costed option goes to the owner. **No purchase without written approval** |
| Make | Free plan fits release 1 at **703 operations, 70% of the verified limit, 2 active scenarios**. Not permanently free: restoring per-photograph processing needs **≥ 3,000 operations/month and ≥ 3 active scenarios**, price unverified |
| Claude API | **~$0.021 per analysed photograph** → **~$7.56/month** at pilot volume (360 photographs), ~$50/month at 20 projects. On Haiku 4.5 instead: ~$1.50 and ~$10. Bounded by a hard monthly cap the owner sets |
| Drive storage | ~380 MB live per project-month; ~682 MB with one backup. A backup copy nearly doubles it, which makes backup policy the largest storage decision in the system |

**A finding you must not soften:** the AI proposal step **does not fit the Make free tier** —
roughly 1,440 operations a month against a 1,000 limit, and a third scenario against a ceiling of
two. Four costed responses are in `docs/02a-plan/23-operations-budget.md` §6b. Release 1 ships Quick
Share; the capture-once guarantee holds either way.

---

## 14. Completed phases

| Phase | What it produced | Status |
|---|---|---|
| **Phase 0 — Discovery** | Eight discovery outputs, 9 ADRs, MVP boundary, assumptions, risks, spec conflicts, phase plan, configuration register | **Approved** 2026-09-11, subject to D-01 … D-15, extended by D-16 … D-21 |
| **Phase 1 — Data foundation** | The canonical model, all generators, 13 check suites, synthetic data for three materially different projects, 19 specifications, the owner review pack | **Completed · Validated Locally · Submitted for Owner Review** |
| **Phase 2A — Plan and synthetic prototype design** | 25 planning documents: AppSheet workbook, security filters, views, actions, offline plan, Drive provisioning, Make specifications with disabled blueprints, deployment and rollback, cost matrix, lean scope, entitlement checklists, field workflow, storage volume, the Make inspection record, device test protocol, release-1 scope, image derivative architecture, operations budget, capture-once workflow | **Completed · Submitted for Owner Review.** Connects nothing |
| Phase 2B — first external connection | — | **Not authorised** |

---

## 15. Current project status, in the approved vocabulary

The owner approved a seven-value status vocabulary (`docs/STATUS-DEFINITIONS.md`). Use these words
and no others; in particular, never say "working", "done", "tested" or "ready" without one of them.

| Status | Means | Does **not** mean |
|---|---|---|
| **Completed** | The artifact has been created | That it works, is correct, or has been looked at |
| **Validated Locally** | Internal automated checks passed against synthetic data in this repository | That any external platform works |
| **Submitted for Owner Review** | Awaiting the owner's business and design acceptance | Approved |
| **Approved** | Expressly accepted by the owner | That it has been built, connected or tested against a real platform |
| **Verified in Integration** | Tested against the actual external platform | Production ready |
| **Production Ready** | All applicable security, field, integration, recovery and acceptance tests passed | Live |
| **Live** | Explicitly deployed and authorised for real use | — |

**Where this project stands today:**

| Scope | Status |
|---|---|
| Phase 0 — Discovery | **Approved** |
| Phase 1 — Data foundation | **Completed · Validated Locally · Submitted for Owner Review** |
| Phase 2A — Plan and synthetic prototype design | **Completed · Submitted for Owner Review** |
| Capture-once correction (D-16 … D-21) | **Completed · Validated Locally · Submitted for Owner Review** |
| Every external integration | **Not started.** Nothing is Verified in Integration, Production Ready or Live |

---

## 16. Branch and commit

| | |
|---|---|
| Repository | `mohasker/Report.Data` |
| **Branch — develop and push here, and nowhere else** | **`claude/alharam-field-reporting-spec-afq1fr`** |
| **Validated commit** | **`20af0a20c9770d9e782219b5a4186c3f4914800f`** — the commit the 219-check run in §17 was executed against |
| **Package commit** | See `HANDOFF-MANIFEST.json` → `package_commit`. It adds only this handoff package to the validated commit |
| Default branch | Do **not** push to it |

If you have the repository, `git log --oneline -5` should show the capture-once commit at or near the
tip. If you have only the ZIP, `HANDOFF-MANIFEST.json` carries the SHAs and the checksum of every
file, and `AlHaram-Field-Reporting-System.bundle` carries the full history — see §23.

---

## 17. Validation command and result

```bash
cd <repository root>
python3 tools/run_validation.py
```

**Standard library only. No network, no credential, no external service, no installation step.**
Python 3.11 was used. The command regenerates every derived artifact from `model/model.json`, runs
every check, compares the regenerated files against what is on disk, and rewrites
`docs/01-data-foundation/17-validation-evidence.md` with the full result.

**Result at the validated commit:**

```
  Seed conformance                                       3 passed   0 failed
  Capture once, use twice                               28 passed   0 failed
  Lean operational MVP                                  19 passed   0 failed
  Configurability and unbounded width                   12 passed   0 failed
  Project segregation                                   12 passed   0 failed
  Role separation, time-bound access and recoverability  31 passed   0 failed
  Evidence rules                                        14 passed   0 failed
  Status transitions, approvals and delegation          20 passed   0 failed
  Content hashing and approval binding                  14 passed   0 failed
  Document numbering                                    13 passed   0 failed
  Deterministic calculation                             22 passed   0 failed
  Bilingual and right-to-left readiness                 13 passed   0 failed
  Governance and safety rules                           18 passed   0 failed
  TOTAL 219/219 checks passed
  byte-identical regeneration : yes
```

**A note on reproducing it.** Run it on a clean tree. The evidence document records the commit it
tested and the working-tree state; running it against uncommitted changes correctly reports
"byte-identical regeneration: NO", which is the tool working, not a failure.

---

## 18. What has been tested locally

| Suite | What it genuinely establishes |
|---|---|
| **Capture once, use twice** (28) | The description is optional in the model; project and location are trusted structured refs; every AI column is advisory and outside every content hash; no quantitative or contractual field is AI-sourced; no public link is required; `CAP-01` is present in the model and the documentation; a regression guard fires if a mandatory description reappears |
| **Project segregation** (12) | The access rule is correct across 6 user profiles × 7 tables, including deep links and API-shaped access |
| **Role separation and recoverability** (31) | Time-bound grants require all four fields; break-glass restores administration without opening content; recoverability is a computable go-live blocker |
| **Content hashing** (14) | The canonical serialisation and hashing algorithm. **This one is genuinely complete — the algorithm here is the algorithm** |
| **Document numbering** (13) | A reference numbering service under concurrency: 200 threads produced 200 distinct numbers with no gap and no reuse |
| **Deterministic calculation** (22) | The arithmetic, the rounding policy, and that an unconfirmed tax treatment **blocks** rather than yielding zero |
| **Configurability** (12) | No identifier is hard-coded in any logic file, and a fourth project added as data works |
| **Evidence rules** (14) | The effective-rule resolver and completeness evaluator against synthetic visits |
| **Transitions** (20) | The declared matrix forbids the dangerous paths; every status is reachable |
| **Bilingual** (13) | Bilingual structure and Unicode integrity through hashing |
| **Governance** (18) | No secret, no non-synthetic identity, no AI field in a hash, no delete grant, no missing attribution |
| **Lean MVP** (19) | The build subset holds together; no lean table requires a deferred one without a declared replacement |
| **Seed conformance** (3) | The synthetic data validates against the canonical model |

---

## 19. What has NOT been integration-tested

**This list is not a caveat. It is the honest boundary of everything above, and it must be repeated
whenever this project's status is described.**

| Platform | What is unproven | Phase |
|---|---|---|
| **AppSheet** | That security filters, offline capture, image fidelity, dependent dropdowns or sync behave as designed on the real platform or on real devices | Phase 2 |
| **Native multi-file share (`CAP-GATE`)** | That **any** capture platform can hand several image files and a formatted summary to an existing WhatsApp group through the share sheet, on iOS and Android, without a second selection | Phase 2A device test |
| **Google Drive** | That folder provisioning is idempotent, that originals survive registration byte-for-byte, or that permissions are least-privilege in practice | Phase 3 |
| **Make.com** | That scenarios run, that idempotency keys suppress duplicates in the real data store, or that error routes catch what they are meant to | Phase 3 |
| **Claude API** | That prompts return schema-valid output, that injection defences hold against a real model, or what analysis actually costs | Phase 4 |
| **Document rendering** | That any template merges, paginates, or renders Arabic and right-to-left text correctly in a PDF | Phase 5 |
| **QuickBooks Online** | That the company file supports the required tax codes, classes, currencies or API operations, or that totals reconcile | Phase 7 |
| **Mobile offline sync** | That a visit captured offline on a real phone syncs completely, in order, with its photographs | Phase 2 field test |
| **Field usability** | That a supervisor can complete a visit faster than the habit it replaces — the single largest risk to the whole system (R-06) | Phase 2 field test |

**Local model validation is not evidence that any of these work.** Do not represent it as such, in a
summary, a status line, or a message to the owner.

---

## 20. Outstanding blockers

| # | Blocker | Who resolves it | What it blocks |
|---|---|---|---|
| **1** | **The Admin Console entitlement check.** Does the Workspace subscription include AppSheet, and does that tier provide **security filters** and **offline use**? | **The owner**, in about 15 minutes. The click-by-click checklist is `docs/02a-plan/16-admin-console-checklist-owner.md` | The capture-platform decision and the first external connection. **This is the only external gate on Phase 2A** |
| **2** | **`CAP-GATE`** — the native share, on two real phones | A device test. Nobody can answer it from documentation | The capture-platform decision. If it fails, the comparison in ADR-0009 runs and **no duplicate-upload workaround is built** |
| 3 | Real administrator identities, and a second administrator or documented recovery route | The owner | Go-live. It is a computable blocker in the model, not a note |
| 4 | Written tax confirmation from the accountant | The accountant | Production invoicing only |
| 5 | Legal identity from the current Commercial Registration | The owner | Production documents only |
| 6 | The existing manual numbering register | The owner | Phase 5 number issue |
| 7 | Device inventory and the real supervisors who will test | The owner | The Phase 2B field measurement |

**Nothing else is waiting on anyone.** Every other part of Phase 2A is complete and proceeds on
synthetic data.

---

## 21. Current authorisation boundary

**You are authorised to:** read and modify this repository; run the local validation suite; write
specifications, schemas, generators and checks; use synthetic data; commit and push to
`claude/alharam-field-reporting-spec-afq1fr`.

**You are NOT authorised to:**

- connect Google Workspace, Drive, Sheets, AppSheet, Claude API or QuickBooks;
- create, edit, activate, deactivate, delete or run any Make scenario, webhook or connection;
- inspect or reveal any connection credential or secret;
- purchase or upgrade any plan;
- upload real client data, real project data, real photographs, or real user identities;
- send any email or external message;
- deploy or publish any application;
- perform any irreversible external action.

**Additional standing rules:**

- **Never invent** a credential, account ID, folder ID, API key, email address, QuickBooks company
  ID, AppSheet application ID, webhook URL, tax setting, contract value, invoice number, quantity,
  client contact or approval decision. Represent every unknown as a named configuration variable and
  request it only when the next safe step needs it.
- **Never print, commit, log or store a secret** in source, a spreadsheet, a prompt, a screenshot or
  documentation.
- **Do not assign real people or email addresses** until the owner provides them. Nine representative
  profiles stand in for them.
- The seven existing Make scenarios belong to unrelated company work and are **not to be touched**.

---

## 22. The exact next recommended action

**Do not start by building anything.**

1. **Verify the package.** Confirm the checksums in `HANDOFF-MANIFEST.json`, then run
   `python3 tools/run_validation.py` and confirm you get **219/219 passed** and **byte-identical
   regeneration: yes**. Report whether your reproduction matches. If it does not, stop and say so —
   a mismatch means something in transfer, not something to fix by editing.
2. **Read, in the order given in §23.** Roughly 90 minutes. Do not skip
   `DECISIONS-AND-ASSUMPTIONS.md`: it is the file that stops you from re-proposing something the
   owner already withdrew.
3. **Summarise the current status and blockers back to the owner**, using the seven-value vocabulary
   in §15, and say plainly that the Admin Console check and `CAP-GATE` are the two things waiting on
   a human.
4. **Then continue Phase 2A from its existing state.** The open work that needs no external access:
   OQ-15 to OQ-19 (the default operating mode, whether a formatted summary accompanies every share,
   internal-group sharing, whether a draft may be shared, voice-note handling); the Phase 2B test
   scripts; and the Make scenario blueprints for the capture-once actions, written disabled.
5. **Make no external connection until the owner authorises it separately and in writing.**

---

## 23. Files to read, in order

| # | File | Why | Minutes |
|---|---|---|---|
| 1 | **This file** | Orientation | 15 |
| 2 | `MASTER-SPEC-CONSOLIDATED.md` | The current authoritative requirements | 25 |
| 3 | `DECISIONS-AND-ASSUMPTIONS.md` | D-01 … D-21, what was withdrawn, what is assumed, what is unknown. **Read before proposing any change** | 20 |
| 4 | `CURRENT-STATUS-AND-NEXT-PROMPT.md` | Where work stopped and what is allowed next | 5 |
| 5 | `docs/OWNER-REVIEW-PACK.md` | The whole design as the owner sees it, with diagrams | 35 |
| 6 | `docs/02a-plan/24-capture-once-workflow.md` | The operating principle, generated from the model | 10 |
| 7 | `docs/02a-plan/21-release-1-twelve-tables.md` | What gets built first, and what a field user actually sees | 10 |
| 8 | `docs/01-data-foundation/17-validation-evidence.md` | What was executed, and — more importantly — what it does **not** prove | 10 |
| 9 | `docs/02a-plan/00-PHASE-2A-PLAN.md` | The phase you are continuing | 10 |
| 10 | `model/model.json` + `tools/build_model.py` | The canonical model and how it is authored. **Never hand-edit a generated file** | 30 |
| 11 | `docs/00-discovery/adr/` | Nine architecture decisions, each with its context and what would cause it to be revisited | 20 |
| 12 | `docs/02a-plan/15-make-inspection-record.md` | The only verified external facts in the project | 10 |

**Then, as reference rather than reading:** `docs/01-data-foundation/01-data-dictionary.md` (every
column), `docs/01-data-foundation/04-security-model.md` (every grant),
`docs/01-data-foundation/03-status-transition-matrix.md` (every transition). All three are generated.

### Recovering the repository from this package

If you have the ZIP but not the repository:

```bash
unzip AlHaram-Field-Reporting-System-Handoff.zip -d alharam
cd alharam
python3 tools/run_validation.py          # expect 219/219
```

If you have the Git bundle and want the history:

```bash
git clone AlHaram-Field-Reporting-System.bundle alharam-repo
cd alharam-repo
git checkout claude/alharam-field-reporting-spec-afq1fr
```

---

## 24. Do not restart, redesign, or reconnect

**Do not rebuild the model from the specification.** It exists, it is canonical, and 219 checks
depend on its exact shape. Change it by editing `tools/build_model.py` and re-running
`python3 tools/run_validation.py` — never by editing `model/model.json` or any generated document
directly.

**Do not re-open a settled decision without reading why it was settled.** Twenty-one owner decisions
and nine ADRs record the reasoning, the options considered, and what would cause each to be
revisited. Several current design choices look odd until you read the decision behind them — for
example, that neither administrator may read evidence, that the AI's activity assessment is free text
rather than a reference, and that the Arabic description is an alternative to the English one rather
than an addition.

**Do not re-attempt external verification that has already been recorded as blocked.**
`about.appsheet.com`, `cloud.google.com`, `support.google.com` and `make.com` were unreachable from
the build environment; that was recorded honestly rather than substituted with third-party figures.
Re-check if your environment differs, but do not treat the absence as an oversight.

**Do not connect anything.** See §21.

**Do not weaken the honest language.** Several statements in this repository are deliberately
uncomfortable — that the pilot cost is not confirmed as zero, that the share cannot be observed, that
the 75-second target is unmeasured, that Quick Share sends evidence before review. They were written
that way on purpose, some of them after the owner corrected an earlier overstatement. Preserve them.

---

## 25. You have no internal company skill and no previous chat

**Assume none of the following is available to you:** the previous conversation and its memory, any
internal company-knowledge skill, any private document store, any credential, and any
repository-relative link that does not resolve inside this package.

Everything this project needs is either in this file, in the three companion documents, or at an
exact path inside the repository archive. If you find yourself needing something that is none of
those, it is an **outstanding external fact** — record it in
`docs/01-data-foundation/16-external-facts-register.md` with the phase it blocks, and ask the owner.
**Do not fill the gap by inference.** That rule is the reason this project's documentation can be
trusted, and it is the easiest one to break without noticing.
