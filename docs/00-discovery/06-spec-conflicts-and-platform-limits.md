# Specification Conflicts, Platform Limitations, and Simplification Opportunities

**Document ID:** AH-SYS-P0-006 · **Revision:** 0 · **Status:** draft for owner approval

The specification asked for contradictions, missing decisions, security risks, platform limitations
and opportunities to simplify. This document records them. Each item states **what the specification
says**, **what the problem is**, and **the proposed resolution** — which the owner may accept or
override.

---

# Part 1 — Conflicts within the specification

## C-01 — The company's legal name is stated two different ways
**Spec:** §2 gives "Al-Haram for Maintenance & Agriculture L.L.C." Another internal company source
used in this workspace gives "W.L.L." for the same company.
**Problem:** the legal entity name appears on invoices, completion certificates and contractual
correspondence. Only one form is correct, and the wrong one on a certificate submitted to a
government client is a documentation defect.
**Resolution:** the owner confirms the exact legal name, CR number and address as they appear on the
commercial registration. It is stored **once** as controlled reference data and referenced by every
template — never retyped per document. Tracked as **A-06**.

## C-02 — "Preserve original photographs unchanged" vs. how mobile platforms deliver images
**Spec:** operating rule 9 — never overwrite, resize, enhance, annotate or delete the original
evidence file. §5.10 requires `OriginalChecksum`, `OriginalWidth/Height`, `OriginalSizeBytes`.
**Problem:** an image captured through a mobile app framework is not necessarily the byte-identical
file the camera sensor produced. Upload-quality settings, platform image pickers and EXIF handling
can all mean the file that arrives is already a re-encoding. The rule as literally written may be
unachievable end-to-end, and claiming it without testing would violate operating rule 1.
**Resolution:**
1. Configure the highest available image-upload fidelity.
2. **Test on real iOS and Android devices in Phase 2 and record the actual result** — this is the only way to know.
3. Define the enforceable guarantee precisely: **"the file as first received by the system is stored write-once and is never thereafter modified, moved destructively, annotated or deleted, and its checksum is recorded at registration and re-verified."**
4. State that definition openly in the administrator runbook rather than implying a stronger guarantee than the platform can deliver.
5. If byte-for-byte camera fidelity turns out to be contractually necessary for a client, evaluate a separate raw-upload path — as scope, not as a claim.
Tracked as **R-03**.

## C-03 — Checksums are required, but the capture layer cannot compute them
**Spec:** §5.10 requires `OriginalChecksum`; §8 Scenario 02 says "compute checksum where possible."
**Problem:** the capture app has no hashing function. Computing a hash by downloading every file's
bytes into the orchestration layer is slow and consumes operations at exactly the point of highest
volume.
**Resolution:** obtain the checksum from **Drive's own file metadata**, which exposes a hash for
binary files, at registration time in Scenario 02. It is one metadata read instead of a full file
download, and it is computed by the storage layer rather than asserted by the client — which makes
it better evidence, not merely cheaper. Record the algorithm used alongside the value. Fall back to
computed hashing only where metadata does not provide one.

## C-04 — Google Sheets cannot guarantee unique sequential document numbers
**Spec:** §6 defines document filename patterns including a revision; §11 requires a draft invoice
number separate from the final accounting number.
**Problem:** a spreadsheet has no atomic increment. Two concurrent generations can read the same
last number and both write the next one. §14 criterion 7 forbids duplicates, and §2 forbids
duplicate numbering across projects.
**Resolution:** a single **numbering service** (ADR-0005) holding one counter per series in an
orchestration Data Store with an atomic update, plus a uniqueness check before issue. Numbers are
issued only at the moment a document is actually created — never reserved speculatively, which
leaves gaps that look like missing documents to an auditor. Tracked as **R-05**.

## C-05 — "Word/Google Docs" output implies two different generation paths
**Spec:** §3 item 10 says "controlled Word/Google Docs and PDF drafts"; §16 item 5 mentions both.
**Problem:** producing a genuinely editable `.docx` with controlled styles, and producing a Google
Doc from a template, are different mechanisms with different fidelity and different failure modes.
Building both doubles template maintenance and doubles the visual-inspection burden.
**Resolution — simplification:** generate the editable draft as a **Google Doc from a controlled
Google Docs template**, and export the PDF from it. Where a client requires a `.docx`, export one
from the same approved Doc. One template, one merge path, one inspection pass. Revisit only if a
client contractually requires native Word with specific styling.

## C-06 — "Approval invalidated by material edit" needs a definition of *material*
**Spec:** §5.18 — any material edit after approval invalidates downstream approvals.
**Problem:** "material" is undefined. If every keystroke voids an approval, reviewers will be
re-approving constantly and will stop reading. If nothing voids it, the control is theatre.
**Resolution:** define `ContentHash` over a **canonical serialisation of the fields that actually
affect the output** — quantities, dates, statuses, captions, approved-photo set and sequence,
descriptions — and explicitly exclude presentation-only and system fields (`UpdatedAt`, UI ordering,
internal comments). The included field list is published in the Phase 1 data dictionary and is
itself version-controlled, so "what counts as material" is a documented, reviewable decision rather
than an implementation accident.

## C-07 — Field users must submit offline, but validation runs server-side
**Spec:** §3 item 5 and §7.5 require offline submission; §8 Scenario 01 validates after submission.
**Problem:** a supervisor can complete and submit a visit offline that fails validation hours later,
after they have left the site. The evidence gap is then unfixable without a return visit.
**Resolution:** enforce every rule that **can** be checked on-device at form level (required
activity, required photo count, required caption, quantity present and non-negative) so the common
failures are caught while the supervisor is still standing on site. Server-side validation then
covers only what genuinely requires authoritative data — authorisation, project status, referential
integrity — and remains the security boundary, because client-side checks can never be trusted for
security. Failures return to the submitter's queue with specific correctable errors, never a generic
rejection.

## C-08 — GPS and geofencing are specified without a policy for what to do when they fail
**Spec:** §5.6 has `GeofenceRadiusM`; §5.8 and §5.10 record GPS coordinates.
**Problem:** location permission can be denied, indoor accuracy is poor, and a suspended-ceiling
inspection is by definition indoors. If an out-of-geofence capture blocks submission, the system
blocks legitimate work.
**Resolution:** GPS is recorded as **evidence, not as a gate**. Out-of-geofence captures are flagged
for reviewer attention, never auto-rejected. Missing GPS is recorded as missing, not as zero — zero
is a real coordinate and would silently place the work off the coast of Africa. Raised as **OQ-06**.

## C-09 — Multi-currency is required in the model but has no operational rule
**Spec:** §5.3/§5.4 carry `Currency`; §11 says derive currency from the contract; §13 mentions
"multi-currency rejection/configuration."
**Problem:** if a project and its client disagree on currency, or an invoice mixes currencies, the
behaviour is undefined — and undefined behaviour in a financial path is the worst kind.
**Resolution:** MVP rule — **an invoice request must be single-currency, and the currency must come
from the contract.** Any mismatch between contract, project and client currency is a validation
failure that stops the job with a specific message. No conversion is performed anywhere in the
system, and no exchange rate is stored, until a real multi-currency contract exists and a rate
source is approved.

## C-10 — Retention policy is required but never defined
**Spec:** §2 lists retention policy as project configuration; §16 requires a backup policy.
**Problem:** unbounded photo retention consumes storage indefinitely; premature deletion destroys
evidence that may be needed for a claim or an audit.
**Resolution:** implement retention as a **per-project configuration value** with a system default,
and make expiry **flag for review, never auto-delete**. Nothing is deleted automatically — the
system moves items to `08_Archive` and raises them for a human decision. Raised as **OQ-03**.

## C-11 — "Unlimited child photo rows" collides with real platform limits
**Spec:** §14 criterion 1 — "unlimited child photo rows within platform limits."
**Problem:** the phrase is self-limiting but untested. A visit with 200 photographs will strain form
rendering, sync payloads and report pagination.
**Resolution:** measure the practical ceiling during the Phase 2 gate and publish it as a documented
operational limit (for example, a soft warning above a tested threshold per visit). Report layout is
tested at 1, 3, 20 and 100 photographs as §13 requires. A published, tested limit is honest; the word
"unlimited" is not.

## C-12 — OwlAgent is named as a target tool with no defined role
**Spec:** header lists it as a target tool; §4 makes it optional, non-authoritative.
**Problem:** an ambiguous integration invites a status-query interface to become a control interface.
**Resolution — simplification:** exclude it from the MVP entirely. If added later, it is
**read-only** — status queries and summaries — and may never trigger a state transition, an
approval, a send or a posting.

---

# Part 2 — Platform limitations to design around

| # | Limitation | Consequence | Design response |
|---|---|---|---|
| **P-01** | **Spreadsheets are not databases.** No transactions, no atomic increment, no row-level locking, and performance degrades as row counts grow. | The Photos table is the growth risk. | ADR-0002 store abstraction with a defined migration trigger; ADR-0005 numbering service; monitor row counts and sync duration from day one (**R-01**). |
| **P-02** | **Automation triggers only after sync.** An offline submission is invisible to the pipeline until the device reconnects. | "Real-time" is not achievable, and should not be promised. | Design every downstream process as eventually-consistent; monitor for stuck drafts and unsynced files; state the behaviour plainly in the field-user guide. |
| **P-03** | **Webhook and API capability is licence-gated.** | Without it there is no pipeline at all. | **BQ-02** asked before Phase 2 begins. |
| **P-04** | **Client-side security is not security.** Views, slices and hidden columns control presentation, not access. | A determined user with a deep link or API access could reach unfiltered data. | Security filters as the enforcement layer, re-validated server-side; explicit cross-project security test at every gate (**R-11**). |
| **P-05** | **Orchestration platforms bill by operation.** Per-photo processing multiplies operations quickly. | Cost scales with evidence volume, which is exactly what the company wants to increase. | Batch where safe; avoid per-row polling; measure real consumption in Phase 3 and size the plan from measurement (**BQ-03**). |
| **P-06** | **Language models are non-deterministic and can be truncated.** | Identical input can produce differing output. | Strict schemas with validation before storage; advisory-only fields; `PromptVersion` and `AIModel` recorded for reproducibility; never in the arithmetic path (**I-4**). |
| **P-07** | **Vision analysis cost scales with image size.** | Full-resolution originals are expensive to analyse at volume. | Analyse **downscaled derivatives**, never originals — which also protects rule 9, since originals are never opened for processing. |
| **P-08** | **Google Workspace has no Qatar data region.** | Evidence and reports are processed outside Qatar. | **BQ-10** raised in Phase 0, before storage design is fixed (**R-04**). |
| **P-09** | **QuickBooks Online is region-bound.** | Qatar is not a principal supported market. | Invoicing deferred; **BQ-05** answered by the accountant before Phase 6 design; calculation module kept independent of the accounting product (**R-02**). |
| **P-10** | **Right-to-left and mixed-direction text is genuinely hard to render**, particularly inside table cells and headers, and PDF export can differ from on-screen appearance. | Arabic output carries real layout risk. | English-first (**BQ-09**); Arabic treated as separate scope with its own template set and its own visual-inspection matrix. |
| **P-11** | **Drive permits duplicate filenames in the same folder.** | Name-based lookup is unreliable and silently wrong. | Address every file by **file ID**; provision folders idempotently by parent + exact name; sanitise and collision-check generated names. |
| **P-12** | **Personal Drive storage dies with the account.** | The evidence archive would be hostage to one person's employment. | Shared Drive owned by the company (ADR-0001, **BQ-01**, **R-32**). |

---

# Part 3 — Opportunities to simplify the MVP

Each of these reduces build and maintenance cost **without weakening a control**.

| # | Simplification | Saved | Cost of the choice |
|---|---|---|---|
| **S-01** | **One document type in the MVP** — the Monthly Technical Report. | Template, QA, numbering and inspection work for eight other document types. | Daily/weekly reports wait. The engine is identical, so adding them later is template work, not development. |
| **S-02** | **Google Docs template as the single generation path** (C-05). | An entire second document toolchain and a second visual-inspection pass. | Native `.docx` styling fidelity is exported rather than authored. |
| **S-03** | **English-only client documents in the MVP** (**BQ-09**). | Roughly half the template, QA and rendering work, and the RTL risk in P-10. | Arabic-preferring clients wait for Phase 5b. |
| **S-04** | **Manual send throughout the MVP.** | Scenario 11, its idempotency design, recipient-snapshot delivery logic and the mailbox-reconciliation problem. | A person presses send — which is also the strongest possible control against the highest-consequence irreversible action. |
| **S-05** | **Defer Materials, Equipment and Manpower tables** to Phase 5b–6. | Six tables, their forms, their rules and their permissions. | Cost control arrives later. The schema is designed in Phase 1 so adding them is additive, never a migration. |
| **S-06** | **Defer OwlAgent entirely** (C-12). | An integration with no defined requirement. | No loss — every capability it would offer exists in the app's dashboards. |
| **S-07** | **Advisory AI only in the MVP — no auto-classification writing to authoritative fields.** | Confidence-threshold tuning, auto-approval rules and the error paths they need. | A reviewer reads the AI observation and decides. Which is what §11 and rule 11 require anyway. |
| **S-08** | **Three synthetic projects instead of real client data for Phase 2 testing.** | The risk of a real client's evidence being exposed by an untested security filter. | Real data enters only after segregation is proven and evidenced. |
| **S-09** | **Flag duplicates, never merge or delete them.** | Duplicate-resolution logic, merge semantics and their failure modes. | Reviewers see a flag and decide. §5.10 requires exactly this. |
| **S-10** | **Publish a tested per-visit photo limit rather than pursuing "unlimited"** (C-11). | Open-ended performance engineering against an undefined target. | A documented, honest operational limit. |

---

# Part 4 — Security observations raised in Phase 0

| # | Observation | Response |
|---|---|---|
| **SEC-01** | The webhook payload from the capture layer is **attacker-controllable in principle** (replay, forgery). | Never act on payload contents. Re-read the authoritative record by ID, re-validate authorisation server-side, and check the idempotency key before any side effect. |
| **SEC-02** | Captions and image-embedded text reach a language model and are therefore an **injection surface**. | Wrap as untrusted data; instruction-ignoring system prompt; strict output schema; no tool access; injection test at the Phase 4 gate (**R-15**). |
| **SEC-03** | Review-notification emails could leak evidence through image links. | §8 Scenario 04 already requires a deep link to the record rather than photo links. Reinforced: no evidence content, thumbnails or public links in any notification. |
| **SEC-04** | Field roles must never see contract rates, invoice totals, client tax data or accounting IDs (§7.4). | Enforced by security filters **and** by keeping financial tables out of the field app's data set entirely — the strongest form of the control is that the data is not there to leak. |
| **SEC-05** | An administrator could disable an evidence rule to force a submission through. | Administrator overrides are recorded **as overrides**, with actor, reason and timestamp, and surfaced on the audit dashboard. Silent override is the failure mode to prevent (**R-30**). |
| **SEC-06** | This repository must never contain a secret. | `.env.example` holds variable **names only**; configuration documents name variables and their owners, never values; secret scan before every commit (**R-26**). |
| **SEC-07** | Released documents shared with clients could carry over-permissive links. | Least-privilege sharing only, at release, recorded in the recipient snapshot; permission audit in the monitoring scenario (**R-27**). |
