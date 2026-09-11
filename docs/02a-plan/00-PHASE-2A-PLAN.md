# Phase 2A — Implementation Plan and Synthetic Prototype Design

**Document ID:** AH-SYS-P2A-000 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · **Submitted for Owner Review**
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

Items 1 and 2 regenerate from `model/model.json`, so the application specification cannot drift from
the data foundation. Run `python3 tools/gen_appsheet_workbook.py` after any model change.

## 3. Sequence, and what gates each step

Phase 2A is entirely local. **Phase 2B — the first build that touches a real account — begins only
on the owner's written approval**, and only after the three prerequisites below.

```
2A.1  Workbook and expressions           done, generated
2A.2  Security filters                   done, generated
2A.3  Views, slices, actions             done
2A.4  Offline test plan                  done, awaiting devices
2A.5  Drive and Make design              done, nothing connected
2A.6  Deployment and rollback            done
2A.7  Cost matrix                        done, costs UNVERIFIED
 ---- gate: owner approval + EF-01 + EF-03 + EF-06 ----
2B.1  Create the workbook in a company Workspace
2B.2  Build the app against synthetic data only
2B.3  Security testing before any real person is added
2B.4  Field test with real supervisors and devices
2B.5  Segregation and configurability gate evidence
```

| Prerequisite | Why Phase 2B cannot start without it |
|---|---|
| **EF-03** platform verification | Three requirements are pipeline-blocking and unverified. If security filters, webhooks or the API are unavailable at an economic tier, the capture layer should change *before* an app exists |
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
| Platform capability differs from the specification | Every expression is a specification, not a tested artifact. Expect rework at 2B.2, and verify EF-03 first to bound it |
| Offline behaviour is entirely unknown | The test plan is written per profile so the unknown is measured rather than assumed |
| Field usability | Measured at gate 6 as an acceptance criterion, not treated as a training problem |
| Adding real users too early | Structurally prevented: gates 1–3 run on synthetic accounts |

## 6. Standing constraints

1. No real client, project, photograph, employee or financial record enters any environment during Phase 2A or 2B until the residency review (EF-16) permits it for that project.
2. No production document number is issued until the existing manual register is reviewed (EF-08).
3. No invoice is calculated for production until the tax treatment is confirmed in writing (EF-17).
4. No credential is stored in this repository, at any point, for any reason.
5. Every claim of "tested" points to a recorded result with a date, an executor and an outcome.
