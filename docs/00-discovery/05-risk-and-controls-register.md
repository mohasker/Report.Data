# Risk and Controls Register

**Document ID:** AH-SYS-P0-005 · **Revision:** 1 · **Status:** approved 2026-09-11 — R-02, R-03 and R-24 updated per decisions D-07, D-13 and D-08

Scoring: **Likelihood** L/M/H · **Impact** L/M/H · **Rating** = combined exposure before controls.
"Owner" is the role accountable for the control, not the person who implements it.

---

## A. Architectural risks — these can change the design

| ID | Risk | L | I | Rating | Control | Owner | Trigger to act |
|---|---|---|---|---|---|---|---|
| **R-01** | **Google Sheets reaches its practical ceiling.** The Photos table grows fastest — several rows per visit, per location, per day, across dozens of projects. Symptoms appear as slow sync and sync errors, not as a clean failure. | M | H | **High** | ADR-0002: all access behind a defined table contract so the store can be swapped without rewriting the system. Define the migration threshold in Phase 1 and monitor row counts and sync duration from Phase 2. | Architect | Sync time or row count crosses the Phase 1 threshold. |
| **R-02** | **QuickBooks Online capability for the current company configuration is unverified.** QBO is the accounting system in use (D-07), but it is not established that every required tax setting, project/class feature, currency and API operation is available for this company file. | M | M | **Medium** | Integration kept modular; deterministic calculation layer independent of the accounting product; QuickBooks mapping fields defined in Phase 1; **a compatibility inspection checklist executed as a gate before the financial-integration phase**; nothing connected or posted before then. | GM + accountant | Inspection checklist result. |
| **R-03** | **The capture platform may not preserve the camera's original file byte-for-byte** (upload-quality settings, EXIF handling). | M | H | **High** | Enforceable definition approved (**D-13**): *the file as first received by the controlled system is stored write-once and never thereafter altered or overwritten*, with checksum, MIME type, size, received timestamp, source record and uploader recorded, and every resized, annotated, compressed or report-ready version stored separately. Upload fidelity set to the highest available. **No file is described as the original device image, and no immutability claim is made, before iOS and Android testing proves no upstream re-encoding.** | Architect | Phase 2 device test. |
| **R-04** | **Data residency or third-party-processing restrictions in client contracts.** Google Workspace has no Qatar data region, and AI analysis is third-party processing. | M | H | **High** | **BQ-10** raised in Phase 0. Per-project configuration flag to disable AI analysis where a contract makes it problematic. Restriction, if any, must be known before Phase 3. | GM | Contract review. |
| **R-05** | **Document numbering collisions.** Spreadsheets cannot guarantee atomic increments under concurrency, and manual numbering series already exist. | M | H | **High** | ADR-0005: single atomic numbering service, one counter per series, recorded starting number continuing existing manual series, plus a uniqueness check before issue. | Architect | Phase 5. |
| **R-06** | **Adoption failure.** If the app feels slower than sending photos to a messaging group, supervisors bypass it, evidence starves and everything downstream is worthless. **This is the most likely cause of overall failure — not a technical fault.** | H | H | **Critical** | Minimum-field forms; dependent dropdowns; choices instead of typing; offline capture; test with real supervisors on their own phones at the Phase 2 gate and treat the result as an acceptance criterion, not a training issue. Measure submissions per supervisor per week after go-live. | GM | Phase 2 gate and first month of live use. |
| **R-07** | **Key-person concentration.** The company's own knowledge base names reliance on the owner as a weakness. A design with the GM as sole approver reproduces exactly that. | H | M | **High** | Delegation-capable approval matrix from Phase 1 (**A-12**, **BQ-07**); named system administrator (**A-19**); every operating procedure written down as a runbook rather than held as knowledge in one head. | GM | Before go-live. |

---

## B. Data and evidence integrity

| ID | Risk | L | I | Rating | Control | Owner |
|---|---|---|---|---|---|---|
| R-08 | Original evidence overwritten, deleted or altered. | L | H | Med | Write-once folder; checksum recorded at registration and re-verified; derivatives isolated; no update/delete path exposed to any role; Drive file IDs so a move never breaks a reference. | Architect |
| R-09 | Photographs attached to the wrong project or location. | M | M | Med | Assignment-filtered project list; project-filtered locations; GPS and geofence radius recorded; reviewer sees project/location on every photo before approving; correction path exists and is audited. | Reviewer |
| R-10 | Recycled or stale photographs presented as current work. | M | H | High | Capture timestamp recorded; old-photo warning (§7.3, warn — never auto-reject, offline capture is legitimate); duplicate detection flags rather than deletes; AI flags caption/image contradiction; reviewer decision is the actual gate. | Reviewer |
| R-11 | Cross-project data leakage. | L | H | High | `ProjectID` on every row; `ProjectAssignments`; AppSheet security filters **plus** server-side re-validation in Make; explicit security test at every phase gate including deep-link and API access attempts. | Architect |
| R-12 | Evidence lost because a device is lost, wiped or never syncs. | M | M | Med | Sync-status monitoring (Scenario 12) flags visits stuck in Draft or unsynced files; supervisors instructed to sync before leaving coverage; documented in the field-user guide. | Administrator |
| R-13 | Duplicate submissions from repeated taps or webhook replays. | M | M | Med | Idempotency key per scenario/entity/target-state checked before any side effect; duplicate suppressed and logged, not treated as an error. | Architect |

---

## C. AI-specific

| ID | Risk | L | I | Rating | Control | Owner |
|---|---|---|---|---|---|---|
| R-14 | **AI states work was completed when the evidence does not support it.** | M | H | High | Operating rule 11; AI output stored in advisory fields only; AI never sets `ApprovedForReport` or `PercentComplete`; completion statements must trace to approved evidence or an authorised supervisor confirmation; QA prompt (§9.3) specifically hunts unsupported claims; human approval before release. | Reviewer |
| R-15 | **Prompt injection** through a caption, a filename, text visible inside a photograph, or a client document. | M | H | High | §9.5; untrusted-content wrapping; instruction-ignoring system prompts; strict output schemas; no tool access from the model; injection test at the Phase 4 gate using a caption and an image containing embedded instructions. | Architect |
| R-16 | Schema-invalid or truncated AI output corrupts a record. | M | M | Med | Validate every response against the JSON schema before storage; on failure classify as `SchemaMismatch`, do not retry blindly, dead-letter with the sanitised payload. | Architect |
| R-17 | AI cost escalates unexpectedly. | M | M | Med | Hard monthly cap (**BQ-04**); analyse only approved evidence; send downscaled derivatives; cap output tokens; per-project usage recorded; usage dashboard. | GM |
| R-18 | AI narrative reproduces a factual error consistently across months, making it look authoritative. | M | M | Med | Every generated document carries `AIModel` and `PromptVersion`; QA pass compares draft to structured records; reviewer approval per revision; DATA GAP output required instead of guessing. | Reviewer |
| R-19 | A person is identified or described in evidence analysis. | L | M | Med | §9.1 explicitly forbids identifying people; enforced in the prompt and checked at the Phase 4 gate. | Architect |

---

## D. Financial

| ID | Risk | L | I | Rating | Control | Owner |
|---|---|---|---|---|---|---|
| R-20 | An invoice figure originates from or is altered by a language model. | L | H | High | Invariant I-4; §9.4 forbids the model touching numbers; calculation module owns all arithmetic with a stored trace; reconciliation before any posting. | Finance reviewer |
| R-21 | Over-certification beyond contract plus approved variation. | M | H | High | Cumulative quantity check against `ContractQuantity + ApprovedVariationQuantity`; blocked unless an authorised override is recorded with a reason and an approver. | Finance reviewer |
| R-22 | Duplicate billing for the same period. | M | H | High | Duplicate detection by client + project + contract + billing period + source certificate before an invoice request can be created. | Finance reviewer |
| R-23 | Rounding inconsistency between line, tax, total and the accounting system. | M | M | Med | One central rounding policy applied everywhere; worked test cases including edge cases; reconciliation to the last decimal before marking synchronised. | Architect |
| R-24 | Wrong tax treatment applied, or a classification named that the accountant has not confirmed. | M | H | High | **D-08**: no classification assumed or named — "zero-rated", "exempt", "out of scope" and "no tax configured" are distinct and non-interchangeable; configurable `TaxRules` seeded with an obviously synthetic placeholder; the applied rule **and its version** preserved on every invoice calculation; accountant's written confirmation required before production invoicing. | GM + accountant |
| R-25 | An unapproved invoice reaches a client. | L | H | High | Finance approval required before draft creation; release approval required before delivery; manual send throughout the MVP; recipient snapshot recorded at release. | Finance reviewer |

---

## E. Operational and security

| ID | Risk | L | I | Rating | Control | Owner |
|---|---|---|---|---|---|---|
| R-26 | Secrets exposed in Sheets, logs, prompts, screenshots or this repository. | M | H | High | Operating rule 4; secrets only in Make connections and environment variables; `.env.example` carries names and never values; sanitised request/response summaries only; secret-scan before every commit. | Architect |
| R-27 | Evidence publicly shared through an over-permissive Drive link. | L | H | High | Never share `01_Original_Evidence`; least-privilege links only for released documents; permission audit in Scenario 12. | Administrator |
| R-28 | A silent integration failure means a report is simply never produced. | M | M | Med | Error queue with an oldest-pending-job alert; daily monitoring scenario; nothing fails silently — every failure produces a queue entry with a recommended action. | Administrator |
| R-29 | A platform vendor changes behaviour, pricing or API and breaks the pipeline. | M | M | Med | Standard APIs only; documented scenarios so they can be rebuilt; metadata export (Scenario 13) so data is never trapped; no reliance on undocumented behaviour. | Architect |
| R-30 | The system is built but never operated as designed — approvals rubber-stamped, evidence rules bypassed by a permissive administrator. | M | H | High | Approval requires an explicit decision record with the content hash; audit log reviewable; administrator overrides recorded as overrides with a reason, never silent. | GM |
| R-31 | Scope creep converts the MVP into a permanent build. | H | M | High | Fixed MVP boundary (`01-mvp-boundary.md`); one phase in progress at a time; deferred items recorded rather than argued. | GM |
| R-32 | Google account for the system is personal, and the archive is lost when that person leaves. | M | H | High | **BQ-01** and ADR-0001: Shared Drive owned by the company, system-owned service account, at least two managers. | GM |

---

## Controls that appear repeatedly (the load-bearing ones)

1. **Server-side re-validation.** Never trust the client, the webhook payload or view visibility.
2. **Idempotency keys before any side effect.** The difference between a reliable pipeline and a duplicate-invoice incident.
3. **Content hashing on approval.** The difference between an audit trail and a list of claims.
4. **Advisory-only AI fields.** The difference between assistance and fabrication.
5. **Deterministic calculation with a stored trace.** The difference between accounting and guessing.
6. **Test evidence recorded at every gate.** The difference between "it works" and *knowing* it works.
