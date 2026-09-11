# Owner Decision Record — Phase 0 Approval

**Document ID:** AH-SYS-P0-010 · **Revision:** 0 · **Date:** 2026-09-11
**Decision by:** General Manager (system owner) · **Effect:** Phase 0 approved; Phase 1 authorised

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
