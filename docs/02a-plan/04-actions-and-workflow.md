# Actions and Workflow

**Document ID:** AH-SYS-P2A-004 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Not built, not tested**
**Derived from:** `../01-data-foundation/03-status-transition-matrix.md`

> Every action below implements a transition that the matrix already declares. If an action is not
> in the matrix, it does not exist. The matrix is the specification; this is its user interface.

---

## 1. Actions

| Action | Row source | Shown when | Does | Behind it |
|---|---|---|---|---|
| **Save Draft** | SiteVisits | Always while `Draft` | Saves without submitting | Deliberately separate from Submit (spec 7.3) |
| **Submit Visit** | SiteVisits | `Draft` and the submitter owns it | Runs client-side completeness, sets `Submitted`, stamps `SubmittedAt` | Blocks with a specific list of what is missing |
| **Return for Correction** | SiteVisits | `UnderTechnicalReview`, reviewer is not the submitter | Sets `CorrectionRequired` | **Reason is mandatory** |
| **Approve Visit** | SiteVisits | `UnderTechnicalReview`, reviewer is not the submitter, no photograph still `Pending` | Sets `TechnicallyApproved`, writes an `Approvals` row with version and hash | Self-approval refused in the action, the slice and the rule |
| **Approve Photo** | Photos | `Pending`, reviewer is not the uploader | Sets `Approved`; `ApprovedForReport` follows by formula | AI can never trigger this |
| **Reject Photo** | Photos | `Pending` or `Approved` | Sets `Rejected` | **Comment mandatory.** The file is retained unchanged |
| **Exclude Photo** | Photos | `Pending` | Sets `Excluded` | Valid evidence deliberately left out of this report |
| **Raise Snag** | Photos | Any approved or pending photograph | Creates a `Snags` row pre-filled from the photograph | Category and severity required |
| **Assign Snag** | Snags | `Open` | Sets `Assigned` | Responsible party and target date required |
| **Submit Closure** | Snags | `InProgress` | Sets `PendingVerification` | Closure evidence photograph required |
| **Verify Closure** | Snags | `PendingVerification`, verifier is not the raiser | Sets `Closed` | Closure date and verifier recorded |
| **Request Document** | Projects | Role holds `MayRequestDocuments` | Creates a `DocumentJobs` row | Phase 5 |
| **Grant Access** | TemporaryAccessGrants | General manager only | Creates a time-bound grant | Reason, expiry and notification all mandatory |
| **Revoke Access** | TemporaryAccessGrants | General manager only | Stamps `RevokedAt` | Takes effect immediately |

## 2. Submit: what happens, in order

```
1  client-side completeness         at least one activity; required photographs; minimum count;
                                    quantity present, numeric, non-negative; unit with quantity;
                                    mandatory captions
        fails ->  a specific list, in the user's language, WHILE THEY ARE STILL ON SITE
2  set Submitted, stamp SubmittedAt, increment EntityVersion, compute ContentHash
3  protected fields become read-only to the submitter
4  webhook fires AFTER the device syncs   (offline submissions enter the pipeline late by design)
5  server-side validation           re-reads the authoritative record; re-validates authorisation,
                                    project status, referential integrity
        fails ->  ValidationFailed with specific correctable errors
        passes -> UnderTechnicalReview, reviewer notified once
```

Step 1 exists because of the offline problem (C-07): a supervisor who submits offline and fails
validation an hour later has often already left the site, and the evidence gap becomes unfixable
without a return visit. Every rule that *can* be checked on the device is checked there.

## 3. Bots and events *(Phase 3, specified here, not enabled)*

| Bot | Event | Task | Guard |
|---|---|---|---|
| `OnVisitSubmitted` | `WorkflowStatus` becomes `Submitted` | Call Scenario 01 webhook | Idempotency key `S01:SiteVisit:{VisitID}:Submitted` |
| `OnPhotoAdded` | New `Photos` row synced | Call Scenario 02 webhook | Key includes `PhotoID` |
| `OnVisitApproved` | `WorkflowStatus` becomes `TechnicallyApproved` | Write the approval row, refresh completeness | — |
| `OnDocumentRequested` | New `DocumentJobs` row | Call Scenario 05 webhook | Requester authorisation re-checked server-side |
| `DailyMonitor` | Schedule | Call Scenario 12 | Consolidated alerts only |

**All bots are created disabled** and are enabled only when Phase 3 is authorised. A bot that calls a
webhook is an external action, and external actions are off by default (operating rule 5).

## 4. What the app must never do

1. **Change a workflow status by a route not in the matrix.** No hidden status set in a form, no bulk edit.
2. **Let AI write a decision field.** `ReviewerDecision`, `ApprovedForReport` and `PercentComplete` are human or formula, never model output.
3. **Let a user approve their own work**, in any view, by any route.
4. **Delete anything.** No delete action exists for any role on any table.
5. **Alter an original photograph.** No rotate, crop, annotate or replace action exists. Derivatives are separate records.
6. **Show a field role a financial column.** The columns are absent from the slice, not hidden in it.
7. **Send anything externally.** No email action exists in the MVP application.
