# Phase Plan

**Document ID:** AH-SYS-P0-007 · **Revision:** 0 · **Status:** draft for owner approval

**Working rule (§18):** one phase in progress at a time. A phase closes only when its gate evidence
exists and is recorded. No phase claims a test result that was not executed (operating rule 1).

**No duration estimates appear in this document.** They depend on decisions not yet made (BQ-01 …
BQ-10), on people not yet named, and on licences not yet confirmed. Estimating before those are
answered would be inventing information.

---

## Phase 0 — Discovery and decision record — *in progress*

**Delivers:** this document set — discovery summary, MVP boundary, architecture, assumptions and
dependencies, blocking questions, risk and controls register, specification conflicts and platform
limits, ADRs, Phase 1 artifact manifest, configuration register.

**Does not deliver:** any account, connection, app, sheet, folder, scenario or credential.

**Gate:** owner approves the discovery output **and answers BQ-01 … BQ-10.**

---

## Phase 1 — Data foundation

**Delivers:** data dictionary · key/ID/hash strategy · status-transition matrix · security model ·
evidence rules · naming and numbering specification · migration and versioning policy · machine-
readable table schemas · seed lookup data · three synthetic project datasets · configuration
reference.

**Still no production system.** Phase 1 is design and data definition. Documents and schema files
only.

**Gate evidence:**
- Data dictionary reviewed field by field with the owner or the nominated administrator.
- Status-transition matrix approved, including which transitions void which approvals.
- The three synthetic projects modelled end to end on paper, proving the model has no project-specific logic in it.
- Security model reviewed: every role × every table × every operation, with justification for each grant.
- Canonical `ContentHash` field list agreed (resolves C-06).

**Depends on:** BQ-01, and A-06/A-14/A-17 confirmed.

---

## Phase 2 — Multi-project AppSheet MVP

**Delivers:** the capture and review application — master-data administration, field capture with
per-activity evidence rules, draft/submit separation, reviewer queues with visit- and photo-level
decisions, snags, dashboards, security filters, project assignments.

**Gate evidence — this is the most important gate in the project:**
1. **Segregation test, recorded.** A user assigned to Project A attempts to reach Project B data through views, search, a deep link and the API. The result is recorded whether it passes or fails.
2. **Evidence-rule tests, recorded.** Each required-photo, required-quantity and required-caption rule blocks an incomplete submission.
3. **Configurability proof.** A fourth synthetic project is added **as data only**, with no change to any logic. This is the direct test of requirement 14.
4. **Real-device field test, recorded.** Real supervisors, their own phones, both platforms if used, camera capture, multiple photos, weak network, offline capture and delayed sync, Arabic and English text entry. Offline behaviour is documented **from this test**, never from expectation (A-15).
5. **Adoption signal (R-06).** Time to complete a typical visit, measured with a real supervisor. If it is slower than the habit it replaces, the form is simplified before the phase closes.
6. **Image fidelity test (C-02 / R-03).** Compare the stored file against the source on both platforms and record exactly what is preserved.

**Depends on:** BQ-01, BQ-02, BQ-07; A-05, A-13, A-19.

---

## Phase 3 — Drive and Make foundation

**Delivers:** idempotent folder provisioning · evidence registration with checksum from storage
metadata · submission validation · review notification · correlation IDs · failure classification ·
retry policy · dead-letter queue · daily monitoring.

**Gate evidence:**
1. Duplicate and replayed triggers produce **one** job — recorded (§14 criterion 7).
2. Originals verified unchanged after registration by checksum comparison — recorded.
3. Each failure class injected deliberately; each produces a queue entry with correlation ID, entity ID and a recommended operator action — recorded.
4. Folder provisioning run twice produces no duplicate folders — recorded.
5. Real operation consumption measured, so the plan tier is sized from measurement (P-05).
6. Permission audit: no evidence folder is publicly accessible — recorded.

**Depends on:** BQ-01, BQ-03, BQ-10; Phase 2 closed.

---

## Phase 4 — Claude evidence analysis

**Delivers:** versioned prompt files · JSON schemas · schema validation · minimised payloads on
derivatives · cost controls and usage tracking · injection defence · advisory-only storage.

**Gate evidence:**
1. Schema-invalid output is rejected and dead-lettered without corrupting a record — recorded.
2. **Injection test:** a caption containing an embedded instruction, and an image containing visible instruction text, are both ignored — recorded.
3. An ambiguous image produces low confidence and explicit uncertainty rather than a confident guess — recorded.
4. No AI output writes to an authoritative field — verified by inspection of every write path.
5. Cost per 100 photographs measured against the cap (BQ-04).
6. A caption contradicting its image is flagged (§9.1) — recorded.

**Depends on:** BQ-04, BQ-10; Phase 3 closed.

---

## Phase 5 — Monthly report generation

**Delivers:** controlled template · frozen input manifest · narrative generation · QA pass · Google
Doc draft and PDF · content hash and revision control · technical approval · release with recipient
snapshot · numbering service.

**Gate evidence:**
1. Draft generated from a frozen snapshot; a source record changed afterwards does **not** alter the draft — recorded (§14 criterion 9).
2. PDF inspected page by page against the §10 checklist, with the inspector named — recorded.
3. Layout tested at 1, 3, 20 and 100 photographs, and with portrait, landscape and very long captions — recorded.
4. Editing an approved source record voids the document approval and forces a new revision — recorded (§14 criterion 11).
5. Numbering service tested under concurrent generation; no duplicate number issued — recorded (C-04).
6. QA pass demonstrably catches a deliberately planted unsupported claim — recorded.

**Depends on:** BQ-08, BQ-09; approved templates and logo; Phase 4 closed (or Phase 4 formally skipped).

### Phase 5b — optional, only if approved
Arabic or bilingual output; additional document types; Materials, Equipment and Manpower tables.
Each is separately scoped and separately approved. Not part of MVP acceptance.

---

## Phase 6 — Contracts, completion certificates, invoice drafts

**Delivers:** Contracts, WorkOrders, BOQItems · cumulative quantity controls · completion
certificates · deterministic financial calculation module with a stored trace · invoice drafts.
**No posting to any accounting system.**

**Gate evidence — worked test cases, each recorded:**
zero quantity · decimal quantities · negative rejected · over-contract quantity rejected without an
authorised override · approved variation applied correctly · retention · advance recovery ·
discount · configured tax rule (including the zero-rate case) · prior certification carried forward
correctly · duplicate billing period detected · rounding edge cases · currency mismatch rejected
(C-09) · full calculation trace reproducible from stored inputs.

**Depends on:** BQ-05, BQ-06; contract and BOQ data; Phase 5 closed.

---

## Phase 7 — QuickBooks synchronisation and approved release

**Delivers:** sandbox posting · finance approval gate · reconciliation before marking synchronised ·
approved email delivery with idempotency and recipient snapshot.

**Gate evidence:**
1. Sandbox invoice totals reconcile to locally calculated totals to the last decimal — recorded.
2. Customer and item resolution uses stored immutable IDs; name-similarity matching is proven not to create duplicates — recorded.
3. No send occurs without a Released record — attempted and blocked, recorded (§14 criterion 12).
4. Duplicate send suppressed by idempotency key — recorded.
5. An ambiguous send timeout results in a mailbox/API check rather than a blind resend — recorded (§8 Scenario 11).
6. Production posting remains **disabled** until the owner explicitly authorises it in writing.

**Depends on:** BQ-05, BQ-06, BQ-07; Phase 6 closed.

---

## Phase 8 — Controlled onboarding and scaling

**Delivers:** real project onboarding through configuration only · controlled data import ·
portfolio dashboards · capacity and performance monitoring · operator, reviewer, finance and
administrator guides.

**Gate evidence:**
1. A real project is onboarded **with no change to app logic, scenarios, prompts or code** — recorded. This is the definitive test of requirement 14.
2. Row counts, sync duration and operation consumption monitored against the Phase 1 migration threshold (R-01).
3. Guides delivered and walked through with the people who will actually use them (§14 criterion 14).
4. Rollback plan tested, not merely written.

---

## Cross-phase standing rules

1. **No production mutation without owner approval** of the phase that authorises it.
2. **No irreversible external action** — send, post, share, delete — until the phase that specifically enables it, with its gate evidence recorded.
3. **No credential in chat, in this repository, in a sheet, in a prompt or in a log.**
4. **Every claim of "tested" points to a recorded result** with date, executor and outcome.
5. **Any ambiguous business rule stops work** and is raised, rather than being resolved by assumption.
6. **The defect log is maintained from Phase 2 onward** and reviewed at every gate.
