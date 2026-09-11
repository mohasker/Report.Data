# Phase 2A — Implementation Plan and Synthetic Prototype Design

**Document ID:** AH-SYS-P2A-000 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · **Submitted for Owner Review**
**Revision 2** — incorporates the owner's simplification and cost corrections of 2026-09-11
**Authorisation:** the owner's Phase 2A boundary of 2026-09-11

---

## 1. The boundary, stated first

**Phase 2A is design and specification on synthetic data. It connects nothing.**

| Phase 2A may | Phase 2A may not |
|---|---|
| Specify the AppSheet workbook, columns and expressions | Connect a real Workspace or Shared Drive |
| Specify slices, views and security filters | Add real supervisors |
| Define actions and workflow | Upload actual project photographs |
| Write the offline test plan | Enable live Make webhooks |
| Produce synthetic sample data | Use a production Claude API key |
| Design Drive folder provisioning | Connect QuickBooks |
| Write Make scenario specifications as **disabled blueprints** | Send external email |
| Write deployment and rollback checklists | Publish the application to production users |
| Build the cost and licensing matrix | |

Every artifact in this folder is a specification. **Nothing in it has been executed on any
platform**, and the platform's capabilities themselves remain unverified (see
`../01-data-foundation/12-appsheet-feature-to-plan-matrix.md`).

## 2. What Phase 2A delivers

| # | Artifact | File | Derived from the model? |
|---|---|---|---|
| 1 | AppSheet implementation workbook: worksheets, columns, types, expressions | [`01-appsheet-workbook.md`](01-appsheet-workbook.md) | **Yes — generated** |
| 2 | Security-filter specification, per table, per role | [`02-security-filter-specification.md`](02-security-filter-specification.md) | **Yes — generated** |
| 3 | Slices and views, per role | [`03-views-and-slices.md`](03-views-and-slices.md) | Hand-written against the profiles |
| 4 | Actions, workflow and state transitions in the app | [`04-actions-and-workflow.md`](04-actions-and-workflow.md) | Hand-written from the transition matrix |
| 5 | Offline test plan, per user and device profile | [`05-offline-test-plan.md`](05-offline-test-plan.md) | Hand-written |
| 6 | Google Drive folder-provisioning design | [`06-drive-folder-provisioning.md`](06-drive-folder-provisioning.md) | Hand-written |
| 7 | Make scenario specifications and disabled blueprints | [`07-make-scenario-specifications.md`](07-make-scenario-specifications.md) + `blueprints/` | Hand-written |
| 8 | Deployment and rollback checklists | [`08-deployment-and-rollback.md`](08-deployment-and-rollback.md) | Hand-written |
| 9 | Cost and licensing matrix | [`09-cost-and-licensing-matrix.md`](09-cost-and-licensing-matrix.md) | Hand-written; **costs unverified** |
| 10 | How synthetic data is loaded into a prototype | [`10-synthetic-data-loading.md`](10-synthetic-data-loading.md) | Hand-written |
| 11 | **Lean MVP scope: 17 tables built, 29 deferred with fold-ins** | [`11-lean-mvp-scope.md`](11-lean-mvp-scope.md) | **Yes — from the model's lean manifest** |
| 12 | **AppSheet entitlement verification checklist** | [`12-appsheet-entitlement-checklist.md`](12-appsheet-entitlement-checklist.md) | Hand-written |
| 13 | **Field workflow, tap count and multi-photograph capture** | [`13-field-workflow-and-taps.md`](13-field-workflow-and-taps.md) | Hand-written |
| 14 | **Expected storage and image volume** | [`14-storage-and-image-volume.md`](14-storage-and-image-volume.md) | Hand-written |

Items 1, 2 and 11 regenerate from `model/model.json`, so the application specification, the security
filters and the scope decision can never disagree with each other or with the data foundation. Run
`python3 tools/gen_appsheet_workbook.py` after any model change.

## 2b. What the owner asked for before requesting a production connection

| Requested | Delivered in |
|---|---|
| Lean MVP table list | [`11-lean-mvp-scope.md`](11-lean-mvp-scope.md) §1 — **17 tables** |
| Deferred-table list | [`11-lean-mvp-scope.md`](11-lean-mvp-scope.md) §3 — **29 tables**, each folded in or scheduled |
| AppSheet entitlement verification checklist | [`12-appsheet-entitlement-checklist.md`](12-appsheet-entitlement-checklist.md) |
| Revised itemised monthly cost | [`09-cost-and-licensing-matrix.md`](09-cost-and-licensing-matrix.md) rev 2 — five categories, **USD 0 incremental expected** |
| Expected storage and image volume | [`14-storage-and-image-volume.md`](14-storage-and-image-volume.md) |
| Field-user workflow and number of taps | [`13-field-workflow-and-taps.md`](13-field-workflow-and-taps.md) §2 — **9–13 interface taps plus 6 shutter presses** |
| Multiple-photo capture method | [`13-field-workflow-and-taps.md`](13-field-workflow-and-taps.md) §3 — three methods, one recommended, decided by measurement |
| Phase 2A implementation plan | This document |

## 3. Sequence, and what gates each step

Phase 2A is entirely local. **Phase 2B — the first build that touches a real account — begins only
on the owner's written approval**, and only after the three prerequisites below.

```
2A.1  Lean scope decided: 17 built, 29 deferred      done, in the model and tested
2A.2  Workbook and expressions for the lean set      done, generated
2A.3  Security filters for the lean set              done, generated
2A.4  Views, slices, actions                         done
2A.5  Field workflow and tap budget                  done, target ~60s, NOT yet measured
2A.6  Multi-photograph capture: 3 methods            done, A recommended, decided by measurement
2A.7  Offline test plan                              done, awaiting devices
2A.8  Drive and Make design                          done, nothing connected
2A.9  Storage and volume projection                  done, from stated assumptions
2A.10 Deployment and rollback                        done
2A.11 Cost matrix, five categories                   done, USD 0 incremental expected
2A.12 Entitlement checklist                          done, AWAITING the owner's console check
 ---- gate: owner's WRITTEN approval + entitlement check (E-2, E-3, F-1, F-4) + EF-01 + EF-06 ----
2B.1  Create the workbook in the company Workspace
2B.2  Build the 17-table app against synthetic data only
2B.3  Security testing BEFORE any real person is added
2B.4  Field test: measure the one-minute target on the oldest handset
2B.5  Segregation, configurability and recovery gate evidence
```

**The entitlement check is now the first gate, not a parallel task.** If security filters or offline
image capture are unavailable, that is a capture-layer decision and no app should be built at all —
which is cheap to discover now and expensive to discover after a build.

| Prerequisite | Why Phase 2B cannot start without it |
|---|---|
| **Entitlement check** (E-2, E-3, F-1, F-4) | Fifteen minutes in the Admin Console. Security filters and offline image capture have **no** Make fallback; webhooks and the API both do. A gap in the first two changes the capture layer; a gap in the second two changes one scenario and costs nothing |
| **EF-01** Workspace account and Shared Drive | The first thing 2B.1 touches |
| **EF-06** administrator and backup, or an approved recovery route | The recovery go-live blocker stays set until one exists |

## 4. What Phase 2B must prove, and in what order

Security before people. Nobody real is added to the application until the segregation tests have
passed against synthetic accounts.

| Order | Gate evidence |
|---|---|
| 1 | **Segregation on the real platform.** An unassigned account attempts a view, a search, a deep link and an API call against another project. Result recorded either way |
| 2 | **Evidence rules block incomplete submissions**, one negative test per rule |
| 3 | **Configurability.** A further project added as data only, plus a second legal entity |
| 4 | **Image fidelity** on iOS and Android: what is actually stored, compared with the camera file (C-02, D-13) |
| 5 | **Offline behaviour** per profile, on real devices, with the queue interrupted |
| 6 | **Time to complete a visit**, measured with a real supervisor. If it is slower than the habit it replaces, the form is simplified before the phase closes (R-06) |
| 7 | **Recovery**: administrative control restored using the documented route, with the primary administrator deliberately unavailable |

Gate 1 comes first because a leak found after real data is loaded is an incident; found before, it
is a bug.

## 5. Risks this plan carries into Phase 2

| Risk | Handling |
|---|---|
| Platform capability differs from the specification | Every expression is a specification, not a tested artifact. Expect rework at 2B.2, and do the entitlement check first to bound it |
| **The one-minute target is missed** | It is a tap-count derivation, not a measurement. If the field test exceeds 90 seconds, switch capture method, then simplify the form — before the phase closes |
| **Deferring delegation bites** | With no delegate, approvals wait while the general manager is away. One table and one named person fixes it; the schema already exists |
| Offline behaviour is entirely unknown | The test plan is written per profile so the unknown is measured rather than assumed |
| Field usability | Measured at gate 6 as an acceptance criterion, not treated as a training problem |
| Adding real users too early | Structurally prevented: gates 1–3 run on synthetic accounts |

## 6. Standing constraints

1. No real client, project, photograph, employee or financial record enters any environment during Phase 2A or 2B until the residency review (EF-16) permits it for that project.
0. **No purchase of any kind, and no external production connection, without the owner's written approval.** Phase 2A costs nothing: it is design on synthetic data, plus optionally the free development tier.
2. No production document number is issued until the existing manual register is reviewed (EF-08).
3. No invoice is calculated for production until the tax treatment is confirmed in writing (EF-17).
4. No credential is stored in this repository, at any point, for any reason.
5. Every claim of "tested" points to a recorded result with a date, an executor and an outcome.
