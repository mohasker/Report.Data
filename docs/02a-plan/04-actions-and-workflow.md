# Actions and Workflow

**Document ID:** AH-SYS-P2A-004 · **Revision:** 2 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Not built, not tested**
**Derived from:** `../01-data-foundation/03-status-transition-matrix.md` and
[`24-capture-once-workflow.md`](24-capture-once-workflow.md)
**Revision 2** adds the capture-once actions (D-16 to D-21).

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
| **Capture Photographs** | SiteVisits | Always while `Draft` | Opens the camera once and writes one `Photos` row per shot under a single `CaptureBatchID` | **The only file selection in the workflow (CAP-01)** |
| **Confirm AI Proposal** | Photos | `AIAnalysisStatus` = `Completed` and `AIProposalDisposition` = `NotOffered` | Copies the proposed stage and caption into the confirmed columns and sets the disposition to `Accepted` | A human action. One tap. The proposal is never auto-applied |
| **Correct AI Proposal** | Photos | Same | The supervisor edits the stage or caption; disposition becomes `Corrected` | The supervisor's words always win |
| **Share to Contractor Group** | SiteVisits | Photographs exist, and `ShareStatus` is `NotShared`, `ShareCancelled` or `ShareFailed` | Opens the **native share sheet** with the stored files already attached and a formatted summary; sets `ShareInitiated`, increments `ShareAttemptCount` | **Must not re-select, re-upload or re-encode the files.** No public link. Unverified: `CAP-GATE` |
| **Confirm Share Completed** | SiteVisits | `ShareInitiated` | Sets `ShareConfirmed`, stamps `SharedAt` and `SharedByUserID` | A human claim. The app cannot observe delivery inside the messaging application |
| **Report Share Failed** | SiteVisits | `ShareInitiated` | Sets `ShareFailed` | Recoverable. Re-sharing re-uses the stored files |
| **Grant Access** | TemporaryAccessGrants | General manager only | Creates a time-bound grant | Reason, expiry and notification all mandatory |
| **Revoke Access** | TemporaryAccessGrants | General manager only | Stamps `RevokedAt` | Takes effect immediately |

## 2. Submit: what happens, in order

```
1  client-side completeness         at least one activity; required photographs; minimum count;
                                    quantity present, numeric, non-negative; unit with quantity;
                                    mandatory captions on Observation, Snag, Material and Safety
                                    NOT checked: a written work description. It is optional for a
                                    normal photographic submission (D-18)
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
| `OnPhotoAdded` | New `Photos` row synced | Call Scenario 02 webhook | Key includes `PhotoID`. **Deferred in release 1** — per-photograph orchestration costs more operations than the whole allowance (`23-operations-budget.md`) |
| `OnCaptureBatchStored` | A capture batch completes | Queue advisory analysis for the batch, one call for all its photographs | Key `S03:CaptureBatch:{CaptureBatchID}`. **Quick Share runs this after the share, by design** |
| `OnVisitApproved` | `WorkflowStatus` becomes `TechnicallyApproved` | Write the approval row, refresh completeness | — |
| `OnDocumentRequested` | New `DocumentJobs` row | Call Scenario 05 webhook | Requester authorisation re-checked server-side |
| `DailyMonitor` | Schedule | Call Scenario 12 | Consolidated alerts only |

**All bots are created disabled** and are enabled only when Phase 3 is authorised. A bot that calls a
webhook is an external action, and external actions are off by default (operating rule 5).

## 4. What the app must never do

1. **Change a workflow status by a route not in the matrix.** No hidden status set in a form, no bulk edit.
2. **Let AI write a decision field.** `ReviewerDecision`, `ApprovedForReport` and `PercentComplete` are human or formula, never model output. Sixteen columns are closed to AI by declaration and by check `CAP-14`, including `ProjectID`, `LocationID`, `VisitDate`, `ActivityTypeID`, `Quantity`, `UnitID`, `EvidenceStage` and both captions.
3. **Let a user approve their own work**, in any view, by any route.
4. **Delete anything.** No delete action exists for any role on any table.
5. **Alter an original photograph.** No rotate, crop, annotate or replace action exists. Derivatives are separate records.
6. **Show a field role a financial column.** The columns are absent from the slice, not hidden in it.
7. **Send anything externally.** No email action exists in the MVP application. The share action is not an exception: it hands files to the operating system's share sheet, where a human chooses the destination. The application sends nothing by itself.
8. **Ask the supervisor to select the same photographs twice (CAP-01).** Not for the first share, not for a retry, not for analysis, not for a correction, not for a report. A workflow that needs a second selection fails acceptance and is replaced, not worked around.
9. **Create a public link to evidence.** Not to share it, not to analyse it, not as a fallback.
10. **Automate a messaging client.** No WhatsApp Web automation, no group scraping, no unofficial messaging API.
11. **Require a typed description of work the photographs already show.**
