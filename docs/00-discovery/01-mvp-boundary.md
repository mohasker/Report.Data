# MVP Boundary

**Document ID:** AH-SYS-P0-001 · **Revision:** 1 · **Status:** approved 2026-09-11 (D-01 … D-15)

## The platform, and the MVP within it

**The platform is multi-project and multi-client from the first version** (D-01). It is built to
carry dozens or hundreds of current and future projects, each with its own client, contacts,
locations, disciplines, activity and evidence rules, assigned users, approval route, templates,
numbering series, reporting frequency and billing configuration. Adding a project is controlled
master-data configuration. It never requires modified application logic, a cloned application,
duplicated scenarios, rewritten prompts, changed formulas or source code, and never a separate
system per project.

**The MVP is a depth boundary, not a width boundary.** It is the first slice of the pipeline proven
end to end:

> A supervisor captures evidence in the field, a reviewer approves it, and the system produces an
> approved, release-controlled Monthly Technical Report from a frozen snapshot of that approved
> evidence — with nothing leaving the company automatically.

**Three synthetic projects are test fixtures, not a limit.** They exist to make segregation and
configurability failures visible, by differing from each other in every dimension that the
configuration model claims to support. A fourth project added as data only, with no change to logic,
is the standing proof that the width is unbounded (Phase 2 gate, requirement 14).

## Why this boundary and not a smaller or larger one

**Not smaller.** A capture-only app is a photo album. The value only appears when evidence
converts into a document that a client accepts. The report is therefore in the MVP, not after it.

**Not larger.** Invoicing is the most expensive thing to get wrong and the most blocked by unknowns
(BQ-05 QuickBooks availability, BQ-06 tax treatment, contract and BOQ data quality). Building
invoicing before those answers exist means building against guesses — which operating rule 2
forbids outright.

**Multi-project from the first line, at unlimited width.** Requirement 14 is not a "later" item.
Retrofitting project segregation into a single-project app is a rewrite, not a refactor. Every
operational table carries `ProjectID` from the beginning; every access decision derives from
`ProjectAssignments`; every project-varying behaviour — locations, activity and evidence rules,
templates, approval routes, numbering series, reporting frequency, billing, residency rules — is a
configuration row rather than a branch in logic. Segregation is proven against synthetic projects
before any real client data is entered (D-12).

## In scope

### Master data (fully configuration-driven)
LegalEntities (D-02) · Users · Roles · ProjectAssignments (many-to-many) · Clients · Contacts ·
Projects · Locations (hierarchical, project-filtered) · ActivityTypes with per-project overrides ·
Units · DocumentTemplates per type, language and project · NumberingSeries · ApprovalMatrix with
delegation (D-09) · TaxRules (placeholder only, D-08) · DataClassifications and
ResidencyRequirements (D-12) · Languages.

All master data is bilingual EN/AR where it is ever displayed or printed (D-11).

### Field capture
- SiteVisit → VisitActivities → Photos, three levels, unlimited child rows within platform limits.
- Project selected before Location; Location choices filtered by Project; Activities filtered by project discipline.
- Draft and Submit as separate, explicit actions.
- Per-activity evidence rules (before/after photo, quantity, caption) enforced at submission.
- Mandatory captions for Snag, Observation, Material and Safety evidence.
- Offline capture with delayed sync — behaviour documented only after real-device testing (A-15).
- Field users cannot edit protected fields after submission unless the record is returned for correction.

### Review
- Reviewer queue by project and by assignment.
- Approve / reject / return-for-correction at **visit** level.
- Approve / reject at **individual photograph** level, with comment and report sequence.
- Rejection requires a reason. Correction returns the record to the submitter's queue.

### Snags
Raise from a photo or activity · severity and category · responsible party and target date ·
status lifecycle · closure with closure-evidence photo and verification.

### Storage (Google Drive, Shared Drive)
- Idempotent provisioning of `{ProjectCode}/{Year}/{Month}/` with the eight standard subfolders.
- Originals written once to `01_Original_Evidence`, never modified, never publicly shared.
- Derivatives (report previews) written only to `02_Derived_Images`.
- Every file referenced by Drive **file ID**.

### Orchestration (Make)
Scenario 01 submission validation · 02 evidence registration · 04 review notification ·
05 report job creation · 06 monthly report generation · 07 approval and release ·
12 daily monitoring (reduced scope) · plus the shared error queue and idempotency store.

### Intelligence (Claude)
Scenario 03 evidence analysis: minimised payload, versioned prompt, schema-validated JSON output,
stored as advisory only, never auto-approving evidence.
Report narrative drafting (§9.2) and report QA (§9.3) inside Scenario 06.

### Documents
**Monthly Technical Report is the only document type produced in the MVP** — the document engine
itself is type-driven and adding a type is configuration. Frozen input manifest · controlled
template selected by type, language and project · editable draft + PDF · content hash · revision
control · technical approval · release with recipient snapshot · numbers issued by the configurable
numbering service (D-10). Release moves files to `07_Released_Documents`. **Sending is manual in the
MVP.**

### Audit
AuditLog on every state transition. IntegrationJobs on every external call. Correlation IDs
end-to-end.

## Out of scope for the MVP

| Item | Target phase | Reason |
|---|---|---|
| Contracts, WorkOrders, BOQItems, cumulative quantity control | 6 | Needs real contract data and a confirmed certification process. |
| Completion certificates | 6 | Depends on approved BOQ quantities. |
| InvoiceRequests, InvoiceLines, tax, retention, advance recovery, discounts | 6 | Blocked on BQ-05 and BQ-06. |
| QuickBooks Online integration of any kind | 7 | Blocked on BQ-05; irreversible accounting effects. |
| Automated outbound email to clients | 7 | Highest-consequence irreversible action. Manual send until the release gate is proven. |
| Daily, weekly, inspection, corrective-action reports; quotations; transmittals | 8+ | Same engine, additional templates. Add once the engine is trusted. |
| Arabic **document template production** — not bilingual capability | 5b | Bilingual data, labels, language preference, Unicode and RTL template capability are delivered in Phase 1 (D-11). What is deferred is authoring and visually inspecting the Arabic template set, which is template work with its own test matrix. |
| Materials, MaterialUsage, Equipment, Manpower tables | 5b–6 | Valuable for cost control, not required to produce an accepted report. Schema is designed in Phase 1 so adding them later is additive. |
| Client acknowledgement / client portal | Post-MVP | Client-facing surface increases risk before internal process is stable. |
| OwlAgent conversational interface | Post-MVP, optional | Convenience only. Never a system of record, never the sole trigger for a critical workflow. |
| WhatsApp as an input channel | Not planned | Operating rules 12–13. |
| Payroll data, HR records | Not planned | Explicitly excluded from field-visible data (§5.13). |

## MVP acceptance criteria

The §14 criteria, mapped to what the MVP can honestly demonstrate:

| §14 | Applies to MVP | How it is evidenced |
|---|---|---|
| 1 Multi-activity visit with multiple photos | Yes | Recorded test with a visit containing ≥3 activities and ≥20 photos. |
| 2 Project-dependent locations | Yes | Recorded test across the three synthetic projects. |
| 3 No cross-project leakage | Yes — **the critical one** | Security test: an assigned-to-Project-A user attempts to read Project B data through views, search, deep link and API. Extended per D-15 item 16 to prove that no data, image, recipient, template, document number or financial record crosses a project boundary. Result recorded either way. |
| 4 Originals correct and unchanged | Yes | Checksum comparison before/after registration, recorded. |
| 5 Evidence rules block incomplete submission | Yes | Negative tests per activity rule, recorded. |
| 6 Visit- and photo-level approve/reject with comments | Yes | Recorded test including return-for-correction. |
| 7 Duplicate triggers do not duplicate jobs | Yes | Deliberate duplicate/replayed webhook, one job created, recorded. |
| 8 Schema-valid AI analysis with uncertainty flagged | Yes | Schema validation test plus a deliberately ambiguous image. |
| 9 Draft generated from an immutable snapshot | Yes | Change a source record after snapshot; draft content must not change. |
| 10 PDF passes visual inspection | Yes | Page-by-page inspection against the §10 checklist, recorded with the reviewer's name. |
| 11 Editing approved source invalidates approval | Yes | Recorded test: edit → approval voided → new revision required. |
| 12 No email/QuickBooks without approval | **Deferred to Phase 7** | Neither capability exists in the MVP. Not claimed as tested. |
| 13 Failures produce actionable logs and recover | Yes | Injected failures per class, error queue entries reviewed. |
| 14 Operator and administrator guides exist | Yes | Field-user guide, reviewer guide, administrator runbook delivered with the MVP. |

## Explicit non-promises

Stated plainly so they are never implied later:

- No claim of "error-free." The target is minimised defects with deterministic controls, evidence and safe recovery.
- No offline guarantee beyond what real-device testing demonstrates.
- No claim that AI output is correct. AI output is advisory and always human-reviewed before it reaches a client document.
- No security claim without an executed and recorded security test.
- No performance claim at portfolio scale until measured under Phase 8 monitoring.
