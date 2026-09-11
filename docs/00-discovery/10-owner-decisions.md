# Owner Decision Record — Phase 0 Approval

**Document ID:** AH-SYS-P0-010 · **Revision:** 2 · **Date:** 2026-09-11
**Decision by:** General Manager (system owner) · **Effect:** Phase 0 approved; Phase 1 authorised
**Revision 1** adds D-16 to D-21, the operational correction of 2026-09-11.
**Revision 2** adds D-22 to D-24, the correction pass of the same day.

This record is the authority for the revision 1 changes made to the Phase 0 documents. Where a
decision below conflicts with an earlier revision of any Phase 0 document, **this record governs**.

---

## D-01 — Scope correction: this is not a three-project system

The platform is designed from the first version for **dozens or hundreds** of current and future
projects and clients. Three synthetic projects are **test fixtures only**, used to demonstrate
segregation, differing clients and contacts, differing locations, differing disciplines and activity
rules, differing assigned users and approval routes, differing templates and numbering, and
differing reporting and billing configuration.

Three projects must never become an operational limitation or an architectural boundary. Adding a
project must require **only controlled master-data configuration** — never modified application
logic, a cloned application, duplicated scenarios, rewritten prompts, changed formulas or source
code, and never a separate system per project.

**Applied to:** `00-DISCOVERY-SUMMARY.md` §2, `01-mvp-boundary.md`, `07-phase-plan.md`,
`08-phase-1-artifact-manifest.md`.

## D-02 — Legal entity is configurable master data, not a choice between two names

Conflict C-01 is **not** resolved by selecting "L.L.C." or "W.L.L." from the specification or an
internal source. Phase 1 creates a `LegalEntities` table carrying at minimum: legal entity ID; legal
name EN; legal name AR; commercial registration number; establishment/card number where applicable;
registered address; country; currency; tax registration status; approved logo; official email;
official telephone and WhatsApp; authorised signatories; document footer details; effective date and
version.

Synthetic data uses the placeholder `LEGAL_ENTITY_NAME_PENDING_VERIFICATION`. The final legal name
is taken from the current Commercial Registration before any production invoice, certificate,
quotation or external report is generated. **This does not block Phase 1.**

## D-03 — Google ownership and storage

Approved in principle: company-owned Workspace account; company Shared Drive preferred where the
plan supports it; never an employee's personal Drive; **no production account created or connected
during Phase 1 without explicit authorisation.** The owning account and Shared Drive ID remain
configuration values confirmed before production deployment. The folder and permission model is
designed now, against local fixtures and synthetic references.

## D-04 — AppSheet licensing

Approved in principle, **conditionally**. No plan or feature entitlement may be assumed. Phase 1
produces a **feature-to-plan requirements matrix** covering authenticated users, security filters,
offline operation, image capture, automation, webhooks, API access, audit history, user count,
external users, and governance and security controls, recommending the lowest plan that satisfies
the verified requirements. Entitlements and pricing are verified from current official Google
information before purchase. Phase 1 remains **platform-neutral enough to identify any requirement
AppSheet cannot safely or economically support**.

## D-05 — Make.com

Approved as the primary orchestration layer. The design must include independent reusable scenarios,
idempotency controls, correlation IDs, visible failure records, retry limits, a dead-letter/manual-
review queue, environment separation where practical, clear connection ownership, no secrets in
spreadsheets or logs, and an operator runbook suitable for a non-developer. **No production scenario
is created or connected.**

## D-06 — Claude API and evidence analysis

Approved in principle, with a **correction**: Claude **may pre-analyse a submitted image to assist
the technical reviewer**, provided the result is clearly marked as an AI observation. Conditions:
only human-approved evidence may generate an official report; AI analysis must never change workflow
approval status; the original caption and reviewer decision are preserved; contradictions and
uncertainty are flagged; prompt-injection controls apply to images, captions, PDFs, filenames and
emails.

No Claude API connection is required in Phase 1. Phase 1 produces prompt specifications, output
schemas, data-minimisation rules and cost-control design.

**Effect on ADR-0004:** the phrase "only reviewer-approved evidence is analysed" is corrected.
Analysis may run on **submitted** evidence to assist the reviewer; **report generation** remains
restricted to human-approved evidence.

## D-07 — QuickBooks Online

Al-Haram **currently uses QuickBooks Online**, so QBO remains the intended accounting system.
It must not be assumed that every required integration, tax setting, project feature, class,
currency or API operation is available for the current company configuration. Phase 1 keeps the
accounting integration modular, defines QuickBooks mapping fields, separates the deterministic
calculation layer from QuickBooks, and documents the required inspection checklist. **Nothing is
connected or posted; no customer, item, invoice or transaction is created.** QuickBooks compatibility
does not block Phase 1; it is a gate before the financial-integration phase.

## D-08 — Tax treatment

**"Zero-rated" must not be used** unless that exact classification is confirmed in writing by the
accountant. "Zero-rated", "exempt", "out of scope" and "no tax configured" are **not
interchangeable**. Phase 1 creates configurable `TaxRules` master data, uses a synthetic placeholder
rule, hard-codes no Qatar rate or classification, requires accountant confirmation before production
invoicing, and **preserves the tax rule and version applied to every invoice calculation**.

## D-09 — Approvals and delegation

The General Manager is the final technical, financial and release approver for the MVP. The system
must support **delegated and temporary delegation from the initial architecture**: delegation start
and end dates, approval scope, project limitations, approval stage, acting user, original
responsible user, and an audit record. The delegate's identity may remain unassigned until before
go-live. **No user may approve their own restricted transaction merely because another approver is
temporarily unavailable.**

## D-10 — Document numbering

**No single undifferentiated sequence.** The numbering service supports separate sequences by legal
entity, document type, calendar or financial year, project or company-wide scope as configured,
optional client requirement, and revision. Illustrative only, pending review of the existing
register: `AH-TR-YYYY-NNN` technical report, `AH-QT-YYYY-NNN` quotation, `AH-CC-YYYY-NNN` completion
certificate, and other controlled types as configured. Invoice numbering stays aligned with the
approved accounting and QuickBooks process. The service must prevent duplication under concurrent
requests, record **reserved / issued / cancelled** numbers, prohibit silent reuse, and support
migration from the existing manual register.

**Effect on ADR-0005:** revision 1 replaces "numbers are never reserved" with an explicit
reserved → issued → cancelled lifecycle.

## D-11 — Language

English may be the first generated-report language, but the architecture **supports English and
Arabic from Phase 1**. Arabic must not require redesigning the database, templates, interface or
workflows later. Phase 1 supports bilingual master-data labels; bilingual project, location,
activity, material and document descriptions; user language preference; Unicode throughout;
right-to-left template capability; separate approved templates by language; language-specific
generated content; and preservation of Arabic names without transliteration loss.

Full Arabic **template production** may be deferred. Bilingual **capability** is an architectural
requirement. The earlier characterisation that Arabic "doubles the system implementation" is
withdrawn — it applies to template production and its visual inspection, not to the system.

## D-12 — Data residency and government contracts

Residency and contractual-storage requirements are checked **before uploading real data to
production cloud services**; they do not block Phase 1 schema, security model, synthetic data, local
documentation or platform evaluation. Phase 1 creates a `DataClassification` and
`ResidencyRequirements` model; classifies photographs, personal data, contracts, financial data and
government/client records; allows residency and approved-storage rules per client, contract and
project; documents the proposed Google, Make, Claude, AppSheet and QuickBooks data flows; identifies
subprocessors and likely processing locations; and produces a contract-review checklist.

A contractual restriction blocks **production storage or processing for the affected project**, not
the generic system design. **No real MOEHE, school, government, client, employee or financial data
may be uploaded during Phase 1.**

## D-13 — Evidence-original wording

The revised enforceable definition is **approved**:

> The file as first received by the controlled system must be stored write-once and must never
> thereafter be altered or overwritten.

Additionally: preserve the original received file; record its checksum, MIME type, size, received
timestamp, source record and uploader; store resized, annotated, compressed or report-ready versions
separately; **never describe a file as the original device image** unless real-device testing proves
no upstream re-encoding occurred; include iOS and Android testing before any immutability claim.

## D-14 — Phase 1 authorisation

**Authorised:** repository artifacts, schemas, synthetic data, specifications, validation rules,
security models, state-transition models, prompt schemas, documentation.

**Not authorised:** connecting production Google accounts; connecting AppSheet production data;
creating production Make scenarios; creating or using Claude API credentials; connecting QuickBooks;
uploading real client or project photographs; sending email or messages; creating invoices or
accounting transactions; publishing or sharing external documents.

## D-15 — Required additions to the Phase 1 deliverables

1. Fully normalised multi-project and multi-client data model.
2. ProjectAssignments supporting users assigned to multiple projects.
3. Project-specific locations and hierarchical sublocations.
4. Project-specific activity and evidence rules.
5. Project-specific templates and reporting frequencies.
6. Project-specific approval matrices.
7. Legal-entity configuration.
8. Data classification and residency configuration.
9. Configurable document numbering and migration from existing sequences.
10. Bilingual / RTL readiness.
11. Complete allowed-status-transition matrix.
12. Role and row-level security matrix.
13. Deterministic calculation specification.
14. Audit-log and immutable approval/version model.
15. Synthetic seed data for at least three materially different projects.
16. Tests proving that no data, images, recipients, templates, document numbers or financial records cross project boundaries.
17. A list of every external fact still awaiting confirmation, categorised by the phase it blocks.

---

## Blocking questions — disposition

| # | Status after this record |
|---|---|
| BQ-01 Google ownership | **Decided in principle** (D-03). Account and Shared Drive ID remain configuration values due before production deployment. |
| BQ-02 AppSheet plan | **Converted to a Phase 1 deliverable** (D-04): feature-to-plan requirements matrix, then verification against official Google information. |
| BQ-03 Make.com | **Decided** (D-05). Organisation and plan remain configuration values due before Phase 3. |
| BQ-04 Claude API cap | **Decided in principle** (D-06). Cap value due before Phase 4. |
| BQ-05 QuickBooks | **Answered** (D-07): QBO is in use. Converted to a Phase 1 inspection checklist and a gate before the financial-integration phase. |
| BQ-06 Tax treatment | **Open — accountant confirmation required** (D-08). Blocks production invoicing, not Phase 1. |
| BQ-07 Approvers | **Decided** (D-09): GM as final approver; delegation modelled from the start; delegate identity due before go-live. |
| BQ-08 Numbering | **Decided** (D-10). Existing manual register still to be reviewed; blocks Phase 5 issue, not Phase 1 design. |
| BQ-09 Language | **Decided** (D-11): bilingual architecture from Phase 1; Arabic template production deferred. |
| BQ-10 Data residency | **Converted to a Phase 1 model plus a contract-review checklist** (D-12). Blocks production upload for an affected project, not Phase 1. |

No blocking question now prevents Phase 1. Every unresolved external fact is carried in
`docs/01-data-foundation/16-external-facts-register.md`, categorised by the phase it blocks.

---

# Operational correction, 2026-09-11 — capture once, use twice

Decisions D-16 to D-21 were issued after the release-1 scope was agreed. They change the field
workflow, not the data architecture. Where they conflict with any earlier statement in any
document, **they govern**, and the earlier statement is superseded rather than reinterpreted.

The canonical form of all six lives in `model/model.json` under `capture_once`, is rendered to
[`../02a-plan/24-capture-once-workflow.md`](../02a-plan/24-capture-once-workflow.md), and is tested
by `tools/test_capture_once.py` (checks `CAP-01` to `CAP-26`).

## D-16 — Capture once, use twice

The supervisor must never upload, select or describe the same evidence twice. The photographs are
captured or selected **exactly once**. The same stored files are shared to the existing
main-contractor group through **one native share action** and re-used by every daily, weekly,
monthly, corrective-action, inspection and completion report.

**CAP-01, the acceptance requirement:** *the workflow fails acceptance if the supervisor must select
or upload the images a second time.* This applies to the first share, to a retry after a failed or
cancelled share, to AI analysis, to reviewer correction, and to every report that re-uses the
evidence.

Two operating modes, both capturing exactly once:

| Mode | Sequence | Use when |
|---|---|---|
| **Quick Share** | capture → store → native share; AI runs afterwards | The contractor group must receive the site evidence immediately |
| **AI Reviewed Share** | capture → store → AI proposal → supervisor confirmation → native share | A reviewed professional caption is wanted before group submission |

**Applied to:** `SiteVisits.CaptureMode`, `SiteVisits.ShareStatus`, `SiteVisits.ShareAttemptCount`,
`Photos.CaptureBatchID`, `Photos.CaptureSequence`.

## D-17 — AI proposes; the supervisor decides, with minimum interaction

Image analysis proposes visible activity, evidence stage, a professional caption, visible condition,
a possible snag, an image-quality warning, uncertainty and confidence. Each proposal is written to
its **own advisory column**, never to the confirmed field. The supervisor confirms or corrects it,
and what they did is recorded in `Photos.AIProposalDisposition`.

No AI column enters a content hash, so an analysis arriving later can never void a human approval.
This extends D-06 rather than replacing it.

## D-18 — A written description is not mandatory for a normal submission

**A written description of completed work must not be mandatory for a normal photographic
submission.** The photographs are the submission.

- `SiteVisits.AdditionalSiteNote` — optional, with `SiteNoteCategory` naming why it was written.
- Voice note and speech-to-text are future **input methods for that same field**, not new fields.
- A mandatory reason survives only in the exceptional workflows where a photograph cannot establish
  the fact: a record returned for correction, a visit reporting non-completion, a caption on an
  Observation, Snag, Material or Safety photograph, and a measured quantity claimed without a
  photographed measurement.

The optional note exists for facts an image cannot carry: client instruction, access restriction,
permit issue, hidden or underground defect, measured quantity, material quantity or batch,
equipment failure, reason for non-completion, safety restriction, and work postponed by another
party.

**Supersedes** any earlier statement, in any document, that treats the work description as a
required field.

## D-19 — What AI may not infer, and where trusted context comes from

AI may describe only **visually supportable** conditions and activities. It must not infer or
confirm: measured quantity; hidden defect or its cause; exact material brand; compliance with
contract or specification; exact completion percentage; exact project or location from the
photograph alone; responsibility or negligence; date, unless supplied as trusted metadata; or that
Al-Haram executed the visible work merely because it appears in the photograph.

Project, location, date, assigned user, contract and work-order context come from **trusted system
data**. Sixteen columns are closed to AI by declaration and by automated check (`CAP-14`).

The share destination is held as a **label** in project configuration — never a telephone number,
group invitation link or messaging identifier.

## D-20 — No quantitative or contractual field may originate from an image

`Quantity`, `PercentComplete`, `UnitID`, `ActivityTypeID`, contract quantities, unit rates, contract
values and tax rates may never be AI-sourced. The AI's view of the visible activity is carried as
free text in `Photos.AIProposedActivityText`, deliberately **not** as a reference to
`ActivityTypes`, so a contractual activity can never be created by an image.

## D-21 — The capture platform is an interface decision, and it is gated

**CAP-GATE, unverified:** can AppSheet reliably share multiple actual image files and formatted text
through the native share sheet to an existing WhatsApp or WhatsApp Business group, on iOS and
Android? Fifteen conditions must be tested on real devices, including six photographs, portrait and
landscape, image order, weak connection, offline capture then synchronisation, whether images are
attached or only links, whether the user must select the images again, whether a public Drive link
is created, whether temporary files remain on the device, and recovery from a failed or cancelled
share.

If AppSheet cannot meet it, **no duplicate-upload workaround will be implemented.** The decision
comparison is between AppSheet with a proven native-share method, a lightweight custom PWA or mobile
field application using supported native file sharing, and any other official, policy-compliant
approach.

**Unofficial WhatsApp Web automation and group scraping remain forbidden, and a publicly accessible
Drive link is forbidden.** The data model, Drive security, Make orchestration, Claude controls,
approval rules and audit requirements must remain re-usable if the capture interface changes — which
is why this is an interface decision and not an architecture decision.

---

# Correction pass, 2026-09-11 — minimum interaction, confirmed classification, filtered analysis

Three further decisions, issued when the owner reviewed the capture-once implementation and found
that it still asked the supervisor for more than it needed to, that it had removed the trusted
activity classification along with the untrusted one, and that it assumed every photograph must be
analysed. All three **govern over any earlier statement.**

Canonical form: `model/model.json` → `capture_once.minimum_interaction`, `.classification` and
`.ai_analysis_policy`. Rendered:
[`../02a-plan/24-capture-once-workflow.md`](../02a-plan/24-capture-once-workflow.md) §3b, §3c, §3d.
Tested by `tools/test_capture_once.py` (`CAP-27` … `CAP-45`).

## D-22 — Minimum interaction: the normal path asks for nothing but the photographs

The earlier statement that the supervisor "must supply five fields" did not match the approved
workflow. It is withdrawn. **Zero fields are mandatory manual inputs on the normal path.**

| Value | Where it comes from | When the supervisor is asked |
|---|---|---|
| User identity | The authenticated session | **Never** |
| Date and time | The device clock, at first and last capture | **Never** |
| Project | The single active assignment, else the last project used today, else the project default | Only when several assignments are active and none resolves — **a genuine choice, not a routine question** |
| Location | The project's default location, else the last location used today | Only when several active locations exist and none resolves |
| Capture mode | **Defaults to Quick Share** | Never on the normal path. AI Reviewed Share is chosen by an explicit action |
| Evidence stage | Proposed by analysis, pre-tagged from the activity rule, or left `Pending` | **Never before capture.** It is not a mandatory manual field |
| Additional site note | — | Optional, always |
| Work description | — | **Not required** (D-18, unchanged) |

**The normal path:** open the app → confirm project and location **if necessary** → capture the
photographs → save and share.

**Declaring an activity is not the price of submitting evidence.** A visit carrying photographs and
no activity is a valid photographic submission; the completeness rule now requires *evidence*, not
an activity. An activity that does exist still satisfies its effective rule in full — quantity,
caption and minimum-photograph rules are unchanged.

**Regression guard `CAP-29`:** no table on the normal path may carry a required, user-typed column
with no automatic source. Reintroducing a mandatory supervisor input fails the validation suite.

## D-23 — A confirmed structured activity, separate from the proposal

Holding the AI's activity assessment as untrusted free text was right; discarding the structured
classification with it was not. Reports and business rules need a controlled, human-confirmed
activity. **Five columns, three roles:**

| Column | Standing |
|---|---|
| `Photos.AIProposedActivityText` | **Advisory.** Free text. Untrusted |
| `Photos.AIProposedActivityTypeID` | **Advisory candidate.** A suggested catalogue code, held in a typed column only so it can be shown beside the entry it points at. Nothing reads it except the confirmation screen |
| `Photos.ConfirmedActivityTypeID` | **Trusted.** Set only by a supervisor or reviewer. Reports, rules, calculations, filters, joins and approvals read this and no other |
| `Photos.AIProposalDisposition` | What the supervisor did with the proposal |
| `Photos.ClassificationStatus` | `Pending` · `AIProposed` · `Confirmed` · `NotApplicable` · `Excluded` |

**In Quick Share, classification stays `Pending` and is reviewed later.** Pending is a normal state
and blocks nothing: the share has already happened and the record catches up.

**AI-generated free text must never directly become the trusted structured activity.** Confirming
copies a value into `ConfirmedActivityTypeID` by an explicit human action, and that column — not the
candidate — binds the content hash, so changing a confirmed activity voids the approval.

## D-24 — Analysis is filtered before it is paid for

Do not assume every captured photograph requires a separate immediate AI call. **Two policies:**

| | **AI Reviewed Share** | **Quick Share** *(default)* |
|---|---|---|
| Timing | Immediate, before the share | **Deferred**, after the share |
| Filtering | Local duplicate and quality checks first | Duplicates, unusable images, deletions **and exclusions** first |
| Why | The supervisor is waiting | Nothing is waiting, so the cheapest correct moment is after the waste has been removed |

**Never analysed:** a near-duplicate of a photograph already analysed in the same batch; an image
below the project's quality threshold; an image deleted or explicitly excluded before analysis ran;
an image already analysed; anything in a project where analysis is off or the monthly cap is
reached.

**Still analysed: every photograph a reviewer may approve for a report.** Skipping is about waste,
never about coverage. A skipped photograph is retained as evidence in full.

**The filters cost nothing.** Perceptual hashing and the blur measure run locally, with no model
call and no transfer. `Photos.PerceptualHash`, `Photos.QualityScore` and
`Photos.AnalysisEligibility` carry the result.

**Recalculated, and labelled as estimates until measured:** eligible ~83% under Quick Share and
~92% under AI Reviewed Share, of 360 photographs a month at pilot volume. Claude: **~$6.28** and
**~$6.95** a month. Make: **~1,167** and **~1,353** operations a month — so **neither policy fits
the free orchestration tier**, because three operations per photograph is irreducible once bytes
pass through an orchestrator. Full arithmetic:
[`../02a-plan/23-operations-budget.md`](../02a-plan/23-operations-budget.md) §6b and
[`../02a-plan/22-image-derivative-architecture.md`](../02a-plan/22-image-derivative-architecture.md) §5.
