# Make Operations Budget — Designing to 60–70% of the Verified Limit

**Document ID:** AH-SYS-P2A-023 · **Revision:** 2 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Nothing built, nothing activated**
**Verified limit:** 1,000 operations per month, 2 active scenarios, no overage
**Revision 2** prices the AI proposal step that the capture-once correction introduces (D-16, D-17),
and reports the result plainly: **it does not fit in the Free plan through Make.** §6b.

---

## 1. The target

The owner's instruction: design the prototype for **no more than ~60–70% of the verified monthly
limit under expected usage** — **600–700 operations** — keeping headroom for retries, failed
records, corrections, duplicate triggers, report generation, notifications and administrative tests.

**And explicitly not by removing validation, auditability or error handling.** Those are the reason
the system exists; trimming them to fit a free tier would be trimming the product to fit the tooling.

## 2. How operations are actually consumed

**Stated assumption, to verify in Phase 3:** in Make, each **module that performs an action**
consumes one operation, per bundle it processes. Filters and routers do not. A module that processes
20 bundles consumes 20 operations.

This assumption is the whole budget. If it is wrong, every number below is wrong in the same
proportion, and the first week of real running replaces it with measurement.

**The consequence is severe and was not visible before the account was inspected:** a per-photograph
scenario of six modules costs **six operations per photograph**. At 360 photographs a month that is
**2,160 operations** — more than twice the entire monthly allowance, for one scenario.

## 3. The redesign

**Per-photograph orchestration is removed from the prototype.** Not weakened — removed, and its work
relocated:

| Work | Was | Now, in the prototype | Auditability |
|---|---|---|---|
| Photograph row created | Make | **The app writes it directly.** The file lands in Drive through the app's own storage | Unchanged — the row and its audit columns exist either way |
| Checksum and file metadata recorded | Make, per photograph | **Deferred to release 1b**, where it runs on a paid tier or through the Workspace-side component | The write-once rule still holds; the checksum is recorded later rather than never |
| Derivative creation | Make, per photograph | **Deferred with AI analysis.** Release 1 produces no report, so no report derivative is needed yet | No loss: nothing in release 1 consumes a derivative |
| Visit validation | Make | **Kept in full** | Unchanged |
| Error and integration logging | Make | **Kept in full** | Unchanged |
| Monitoring digest | Make, daily | **Kept, weekly** | Unchanged; the digest covers the same ground less often |

Nothing in the validation rules, the audit trail or the error handling is reduced. What is removed is
**per-photograph processing**, which release 1 does not need because release 1 produces no document.

## 4. The budget

Expected usage: three synthetic projects, 20 visits per project per month.

| Scenario | Runs per month | Modules per run | Operations | Note |
|---|---|---|---|---|
| **S01 Submission validation** | 60 visits | 8 | **480** | Webhook, idempotency claim, re-read visit, read activities, read photographs, update status, write integration log, hand off |
| **S12 Weekly monitoring digest** | 4 | 3 | **12** | Count stuck drafts, unreviewed evidence, overdue corrections; one consolidated message |
| **Subtotal, expected usage** | | | **492** | **49% of 1,000** |
| Retries on retriable failures (allow 10%) | | | 49 | Network and provider errors only; validation failures are never retried |
| Corrections and resubmissions (allow 15% of visits) | 9 | 8 | 72 | A returned visit is re-submitted and re-validated |
| Duplicate triggers suppressed | ~20 | 2 | 40 | Webhook plus idempotency check, then stop |
| Administrative tests | | | 50 | Deliberate failure injection, gate evidence |
| **Total, with allowances** | | | **703** | **70% of 1,000** |

**703 operations — the top of the owner's band**, with every allowance funded. Two levers bring it
to the middle of the band if measurement shows the estimate is optimistic:

| Lever | Saves | Costs |
|---|---|---|
| Fold the integration-log write into the status update (7 modules instead of 8) | ~60 | Slightly coarser logging; the row still exists |
| Monitoring digest fortnightly instead of weekly | 6 | Slower notice of a stuck submission |
| Run the pilot on two projects instead of three | ~230 | One fewer segregation fixture in live use; the synthetic third project still proves segregation in testing |

With the first lever: **643 operations, 64%** — the middle of the band.

## 5. Scenario count

The design fits the **2 active scenarios** the plan allows:

| Slot | Scenario | Why this one |
|---|---|---|
| 1 | S01 Submission validation | The only path that must run promptly and must re-validate authorisation server-side |
| 2 | S12 Weekly monitoring digest | The only thing that notices a submission nobody looked at |

**Review notification becomes part of the weekly digest** rather than a per-submission email. At 60
visits a month that is a real reduction in reviewer responsiveness, and it is the honest cost of
staying inside the free tier. The 15-minute minimum interval is irrelevant here: nothing in release 1
is time-critical.

## 6. If the owner wants per-photograph processing in the prototype

Then the Free plan is insufficient, and the requirement is specific:

| Need | Quantity |
|---|---|
| Photographs per month, 3 projects | 360 |
| Minimum modules per photograph (metadata, update, log) | 3 |
| **Additional operations** | **1,080** |
| Total with visit validation and allowances | **~1,780** |
| To sit at 60% of a limit | **a plan providing ≥ 3,000 operations/month** |
| Active scenarios needed | **3** (validation, photograph registration, monitoring) |
| Transfer, if derivatives pass through Make | ~86 MB/month at pilot volume — inside 512 MB |

**That is the exact paid-plan requirement: at least 3,000 operations a month and at least 3 active
scenarios.** The price is unverified — make.com is unreachable from this environment, and the owner
can read it on their own billing page. **No purchase is proposed.**

## 6b. The capture-once correction does not fit through Make on the Free plan

This is the finding the owner needs, and it is not a comfortable one.

**AI Reviewed Share requires an analysis before the supervisor confirms.** Batching by capture batch
is the cheapest honest shape — one Claude call per visit rather than one per photograph — but the
photographs still have to be fetched and encoded individually, and in Make a module inside an
iterator consumes one operation **per bundle**.

| Module | Runs per visit | Operations |
|---|---|---|
| Webhook / trigger on capture batch complete | 1 | 1 |
| Read the batch's photograph rows | 1 | 1 |
| Iterator over 6 photographs — fetch derivative | 6 | 6 |
| Iterator over 6 photographs — encode for the request | 6 | 6 |
| Aggregate into one request | 1 | 1 |
| Call Claude once for the batch | 1 | 1 |
| Parse and validate the response against the schema | 1 | 1 |
| Iterator over 6 results — write the advisory columns | 6 | 6 |
| Write the integration log row | 1 | 1 |
| **Per visit** | | **24** |
| **60 visits per month** | | **1,440** |

**1,440 operations for analysis alone**, on top of the 703 already budgeted — **2,143 against a
1,000 limit, and a third active scenario against a ceiling of two.** Neither fits.

### The four honest responses

| Option | Effect | Cost | Verdict |
|---|---|---|---|
| **A. Release 1 ships Quick Share only; AI analysis is deferred** | Capture once, store, native share. The internal record is complete; the *proposal* is not offered | **None.** 703 operations, 2 scenarios, unchanged | **Recommended for release 1.** It delivers the whole of CAP-01 — the second selection disappears — and defers only the convenience layer on top of it |
| **B. AppSheet calls the Claude API directly, without Make** | The proposal returns to the supervisor without any orchestration operation | Make operations: **0**. Requires AppSheet API/webhook capability, which is question 4 of the Admin Console check | **The right answer if the entitlement allows it.** It is also architecturally better: the supervisor is waiting, and a round trip through an orchestrator is latency nobody needs |
| **C. A Workspace-side component (Apps Script) performs the analysis** | Same as B, without depending on AppSheet's automation entitlement | Make operations: **0**. One more component to operate and monitor | The fallback if B is unavailable. It is the same component Option B of the derivative architecture already anticipates at scale |
| **D. Pay for a Make plan** | The design runs as written | **≥ 3,000 operations/month and ≥ 3 active scenarios**, price unverified | Available, not recommended yet: paying to route bytes through an orchestrator that neither stores nor decides anything is the weakest of the four |

**Recommendation: A for release 1, and test B during Phase 2A**, because question 4 of the Admin
Console checklist already asks whether AppSheet has API access and webhook automation. If it does,
the AI proposal costs zero Make operations and the capture-once workflow arrives complete. If it
does not, C is the fallback and D is a decision the owner takes with a real price in front of them.

**What does not change under any of the four:** the supervisor captures once. CAP-01 is satisfied by
Option A alone; B and C add the proposal, not the guarantee.

## 7. What is measured in Phase 3, before anything is trusted

| Measurement | Why |
|---|---|
| Actual operations per S01 run | The module-counting assumption in §2 |
| Actual operations per suppressed duplicate | Whether an early stop really costs 2 |
| Operations consumed in week 1 against the projection | Whether the whole model holds |
| Proportion of runs that retry | The 10% allowance |
| Proportion of visits returned for correction | The 15% allowance |
| Operations consumed by one batch analysis, if it ever runs through Make | The 24-per-visit estimate in §6b |
| Latency of the batch analysis, measured from the supervisor's point of view | AI Reviewed Share is only usable if the wait is short |

Make's own execution history retains 7 days, so **our `IntegrationJobs` table is the authoritative
record** — which is why it is one of the twelve tables in release 1 and not something that could be
trimmed to save operations.

## 8. What this budget does not do

It does not reduce validation, auditability or error handling. Every check in the submission
validation scenario survives; every failure still produces a classified, correlated row an operator
can work from; every state transition is still recorded. The saving comes entirely from **not
orchestrating photographs in a release that produces no documents.**
