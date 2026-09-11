# Deployment and Rollback Checklists

**Document ID:** AH-SYS-P2A-008 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Nothing deployed**

---

## 1. Before anything is created

| # | Check | Blocks deployment? |
|---|---|---|
| 1 | Owner has given **written** approval to connect external services | **Yes** |
| 2 | Platform capabilities verified from an official source (EF-03) | **Yes** — three requirements are pipeline-blocking |
| 3 | Company Workspace tenant confirmed paid, with Shared Drive capability (EF-01) | **Yes** |
| 4 | System account created and owning the app, workbook and connections — never an individual (ADR-0001) | **Yes** |
| 5 | Administrator **and** backup named, or a documented recovery route approved (EF-06) | **Yes** — the go-live blocker |
| 6 | Residency review complete for every project whose data will be uploaded (EF-16) | **Yes, per project** |
| 7 | Legal identity verified from the Commercial Registration (EF-02) | Blocks document issue, not the build |
| 8 | Existing manual numbering register reviewed (EF-08) | Blocks number issue, not the build |
| 9 | Tax treatment confirmed in writing (EF-17) | Blocks invoicing, not the build |
| 10 | Every credential authorised by the owner **in the provider's console**, never pasted anywhere | **Yes** |

## 2. Deployment sequence

Security before people, synthetic before real. Each step has a stop condition.

| # | Step | Stop if |
|---|---|---|
| 1 | Create the Shared Drive structure by running provisioning twice | A duplicate folder appears |
| 2 | Create the workbook from the generated schemas | Any column differs from the data dictionary |
| 3 | Load **synthetic** seed data only | Any real record is present |
| 4 | Build the app: tables, columns, expressions, slices, views | — |
| 5 | Apply security filters exactly as generated | Any filter is loosened "temporarily" |
| 6 | **Run the segregation tests with synthetic accounts** | Any leak, through any route |
| 7 | Run the evidence-rule negative tests | Any incomplete submission is accepted |
| 8 | Run the configurability test: add a project as data only | Any code or logic change is needed |
| 9 | Real-device field test per profile (EF-05) | Offline loss, or a visit slower than the habit it replaces |
| 10 | Record image-fidelity results and set the verification flag accordingly | A claim is made that the test does not support |
| 11 | Add real users, **one project first** | Any step 6 test was not recorded |
| 12 | Enable orchestration scenarios one at a time, monitoring the error queue | Duplicate jobs, or silent failures |
| 13 | Run one full reporting period in parallel with the existing manual process | Any discrepancy that cannot be explained |

Step 13 is the one most often skipped and most worth keeping. A parallel month costs a month; a
wrong first report in front of a government client costs more.

## 3. Rollback

| Scope | Rollback | Recovery time |
|---|---|---|
| App configuration | Restore the previous app version; the platform retains version history | Minutes |
| Security filter | Revert to the generated specification and **re-run the segregation tests before reopening access** | Minutes, plus test time |
| Workbook schema | Additive changes are reverted by removing the column; destructive changes are not permitted in place (see `07-migration-and-versioning.md`) | Hours |
| Orchestration scenario | Disable the scenario. Records stay in their current state; nothing is lost because every step is idempotent and recoverable | Immediate |
| A bad document | **Never rolled back.** Issue a superseding revision; the superseded one is retained and marked | Hours |
| A bad approval | **Never edited.** Void it with a reason; a fresh approval of the new content is required | Immediate |
| An issued document number | **Never reused.** Cancel with a reason and issue the next | Immediate |
| Real data loaded prematurely | Stop uploads, quarantine the affected project, notify the owner. **Loaded evidence is not deleted** — it is evidence | Immediate stop; resolution depends on the contract |
| Total rollback to manual | The parallel month in step 13 means the manual process still exists and still works | Immediate |

## 4. Go-live blockers

The system carries these as data, not as recollection. `SystemRecoveryPlan.GoLiveBlocker` stays TRUE
until either a backup administrator exists or a documented recovery route does.

| Blocker | Cleared by |
|---|---|
| No backup administrator and no documented recovery route | EF-06 |
| Any segregation test unrecorded or failed | Phase 2B gate 1 |
| Any residency assignment still `VerifiedFromContract = FALSE` for a project with real data | EF-16, per project |
| Legal identity unverified, for document issue | EF-02 |
| Manual numbering register unreviewed, for number issue | EF-08 |
| Tax treatment unconfirmed, for invoicing | EF-17 |

## 5. After go-live, first month

| Cadence | Check |
|---|---|
| Daily | Error queue; oldest pending job; any submission stuck in Draft for more than 48 hours |
| Weekly | Submissions per supervisor — **the adoption signal that matters** (R-06); unreviewed evidence; open snags past target date |
| Monthly | Row counts and sync duration against the migration threshold; AI usage against the cap; a restore actually tested, not merely scheduled |
| Once | Recovery route exercised with the primary administrator deliberately unavailable |
