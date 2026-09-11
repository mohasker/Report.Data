# Status Transition Matrix

**Document ID:** AH-SYS-P1-003 · **Revision:** 1 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-11 from `model/model.json` by `tools/gen_matrices.py`
**Tested by:** `tools/test_transitions.py` · **Evidence:** `17-validation-evidence.md` (TRN-01 … TRN-20)

> Work advances only through a transition declared here. Anything not listed is refused,
> and the transitions listed as forbidden are refused explicitly so that the refusal is a
> decision on the record rather than an accident of implementation.

## How to read this

- **Roles** — who may cause the transition. `System` means an automated workflow acting on validated data, never a person clicking through a gate.
- **Preconditions** — every one must hold. A failed precondition returns a specific, correctable message, never a generic rejection.
- **Invalidates** — approvals that this transition voids. This is the mechanism behind acceptance criterion 11.
- **Terminal** states have no outgoing transition, which is asserted by check TRN-09.

**11 lifecycles · 82 permitted transitions · 36 explicitly forbidden.**

## SiteVisits.WorkflowStatus

One reporting event at a location on a date. The unit of submission and review.

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Draft` | `Submitted` | FieldUser, SiteSupervisor | At least one VisitActivity exists; Every effective evidence rule satisfied; Submitter holds an active ProjectAssignment with MaySubmitEvidence; Project.Status = Active | SubmittedAt set; EntityVersion incremented; ContentHash computed; Protected fields become read-only to the submitter | — |
| `Draft` | `Cancelled` | FieldUser, SiteSupervisor, ProjectManager | Reason recorded | Record retained, never deleted | — |
| `Submitted` | `UnderTechnicalReview` | System | Server-side validation passed; Authorisation re-validated from the authoritative record | Reviewer notified once; Idempotency key claimed | — |
| `Submitted` | `ValidationFailed` | System | Server-side validation failed | Specific correctable errors recorded in ValidationErrors; Submitter notified | — |
| `ValidationFailed` | `Draft` | FieldUser, SiteSupervisor | — | Record editable again | — |
| `UnderTechnicalReview` | `CorrectionRequired` | TechnicalReviewer, ProjectManager, GeneralManager | RejectionReason recorded | Returned to the submitter's queue | — |
| `UnderTechnicalReview` | `TechnicallyApproved` | TechnicalReviewer, ProjectManager, GeneralManager | Reviewer is not the submitter (self-approval prohibited, D-09); Every photograph has a ReviewerDecision other than Pending | Approval row written with EntityVersion and ContentHash; TechnicalReviewedAt and TechnicalReviewedBy set | — |
| `CorrectionRequired` | `Draft` | FieldUser, SiteSupervisor | — | Record editable again | — |
| `TechnicallyApproved` | `ReadyForReport` | System | Period open; Project reporting configuration resolved | — | — |
| `TechnicallyApproved` | `CorrectionRequired` | TechnicalReviewer, GeneralManager | Reason recorded | Approval voided | Approvals for this visit |
| `ReadyForReport` | `IncludedInDraft` | System | Included in a frozen DocumentJob snapshot | Snapshot records version and hash | — |
| `IncludedInDraft` | `Released` | System | Parent document reached Released | — | — |
| `Released` | `Archived` | SystemAdministrator, BusinessAdministrator, GeneralManager | Retention review completed | Moved to archive folder; nothing deleted | — |
| `IncludedInDraft` | `ReadyForReport` | System | The document draft was cancelled | Reserved number cancelled, never reused | — |

**Explicitly forbidden:**

- Draft -> TechnicallyApproved (skips validation and review)
- Submitted -> TechnicallyApproved (skips validation)
- ValidationFailed -> UnderTechnicalReview (errors must be corrected first)
- Any state -> Released without a released parent document
- Archived -> any state (archive is terminal)
- Any transition performed by a user without an active ProjectAssignment

**Terminal states:** `Archived`, `Cancelled`

## VisitActivities.Status

What was actually done during a visit. One row per activity.

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Draft` | `Submitted` | FieldUser, SiteSupervisor | Parent visit submitted | — | — |
| `Submitted` | `UnderReview` | System | Parent visit under review | — | — |
| `UnderReview` | `Approved` | TechnicalReviewer, ProjectManager, GeneralManager | Reviewer is not the submitter; Evidence rule satisfied or a recorded override exists | Eligible for reporting | — |
| `UnderReview` | `Rejected` | TechnicalReviewer, ProjectManager, GeneralManager | Comment recorded | Excluded from reporting; record retained | — |
| `UnderReview` | `CorrectionRequired` | TechnicalReviewer, ProjectManager, GeneralManager | Comment recorded | — | — |
| `CorrectionRequired` | `Draft` | FieldUser, SiteSupervisor | — | — | — |
| `Approved` | `CorrectionRequired` | TechnicalReviewer, GeneralManager | Reason recorded | Approval voided | Approvals for this activity and its parent visit |
| `Draft` | `Cancelled` | FieldUser, SiteSupervisor | Reason recorded | — | — |

**Explicitly forbidden:**

- Draft -> Approved
- Rejected -> Approved (a new activity record is required instead)
- Any approval by the user who submitted the activity

**Terminal states:** `Cancelled`

## Photos.ReviewerDecision

One photograph per row. The received file is write-once and is never altered (D-13).

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Pending` | `Approved` | TechnicalReviewer, ProjectManager, GeneralManager | Reviewer is not the uploader; Caption present where the evidence stage requires one | ApprovedForReport set TRUE; ReviewedAt and ReviewedByUserID set; EntityVersion incremented | — |
| `Pending` | `Rejected` | TechnicalReviewer, ProjectManager, GeneralManager | ReviewerComment recorded | ApprovedForReport stays FALSE; file retained unchanged | — |
| `Pending` | `Excluded` | TechnicalReviewer, ProjectManager, GeneralManager | ReviewerComment recorded | Valid evidence deliberately left out of this report | — |
| `Approved` | `Rejected` | TechnicalReviewer, GeneralManager | Reason recorded; Not already frozen into a released document | ApprovedForReport set FALSE | Approvals for the parent visit; Unreleased draft documents containing it |
| `Rejected` | `Approved` | TechnicalReviewer, GeneralManager | Reason recorded | — | Approvals for the parent visit |

**Explicitly forbidden:**

- Any transition performed by AI or by an automation on AI output (ADR-0004, D-06)
- Any transition that modifies, replaces or deletes the original received file (D-13)
- Approval by the user who uploaded the photograph

## Snags.Status

Defects and observations tracked to closure with evidence.

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Open` | `Assigned` | ProjectManager, TechnicalReviewer, GeneralManager | ResponsibleParty and TargetDate set | — | — |
| `Assigned` | `InProgress` | SiteSupervisor, ProjectManager | — | — | — |
| `InProgress` | `PendingVerification` | SiteSupervisor, ProjectManager | Closure evidence photograph attached | — | — |
| `PendingVerification` | `Closed` | TechnicalReviewer, ProjectManager, GeneralManager | ClosureEvidencePhotoID present and approved; VerifiedBy is not the person who raised it; ClosureDate set | Verification recorded | — |
| `PendingVerification` | `InProgress` | TechnicalReviewer, ProjectManager, GeneralManager | Comment recorded | — | — |
| `Open` | `Rejected` | ProjectManager, GeneralManager | Reason recorded | — | — |
| `Open` | `Deferred` | ProjectManager, GeneralManager | Reason and review date recorded | — | — |
| `Deferred` | `Open` | ProjectManager, GeneralManager | — | — | — |

**Explicitly forbidden:**

- Open -> Closed (closure requires evidence and verification)
- Closure verified by the person who raised the snag

**Terminal states:** `Closed`, `Rejected`

## DocumentJobs.WorkflowStatus

A request to produce a document from a frozen snapshot of approved records.

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Requested` | `Validating` | System | Requester authorised on the project | — | — |
| `Validating` | `InputValidationFailed` | System | Completeness check failed | DATA GAP findings recorded explicitly | — |
| `Validating` | `SnapshotFrozen` | System | All inputs present; Every included record technically approved | Manifest of IDs, versions and hashes frozen; Number reserved (D-10) | — |
| `SnapshotFrozen` | `Generating` | System | Template resolved for type, language and project | — | — |
| `Generating` | `Generated` | System | Draft and PDF produced; Content hash computed | Number issued; Document row created | — |
| `Generating` | `Failed` | System | Error classified | Reserved number cancelled with a reason, never reused | — |
| `Requested` | `Cancelled` | ProjectManager, GeneralManager | Reason recorded | — | — |
| `SnapshotFrozen` | `Cancelled` | ProjectManager, GeneralManager | Reason recorded | Reserved number cancelled | — |

**Explicitly forbidden:**

- Requested -> Generating (a frozen snapshot is mandatory)
- Re-freezing a snapshot in place (a new job is required)

**Terminal states:** `Generated`, `Failed`, `Cancelled`

## Documents.ReleaseStatus

A produced document revision. Approval binds to ContentHash (ADR-0006).

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Draft` | `PendingTechnicalApproval` | System | Draft and PDF exist | — | — |
| `PendingTechnicalApproval` | `TechnicallyApproved` | TechnicalReviewer, GeneralManager | Approver is not the requester where the matrix requires segregation; ContentHash matches the approved content | Revision locked; Approval recorded with hash | — |
| `PendingTechnicalApproval` | `RevisionRequired` | TechnicalReviewer, GeneralManager | Comment recorded | — | — |
| `TechnicallyApproved` | `PendingRelease` | System | Finance approval complete where required for the type | — | — |
| `PendingRelease` | `Released` | GeneralManager | Explicit release decision recorded; Recipients are authorised contacts; ContentHash recomputed and unchanged | Recipient snapshot stored; Files moved to released folder | — |
| `TechnicallyApproved` | `RevisionRequired` | System | A source record changed: ContentHash no longer matches | Technical approval voided | Technical approval; Finance approval; Release approval |
| `RevisionRequired` | `Draft` | System | New revision created | VersionNumber incremented; the previous revision is superseded, not overwritten | — |
| `Released` | `Superseded` | System | A later revision was released | — | — |
| `Draft` | `Cancelled` | GeneralManager, ProjectManager | Reason recorded; Document not yet released | Any reserved number is cancelled with a reason, never reused | — |
| `PendingTechnicalApproval` | `Cancelled` | GeneralManager | Reason recorded | Reserved number cancelled | — |
| `RevisionRequired` | `Cancelled` | GeneralManager | Reason recorded | Reserved number cancelled | — |

**Explicitly forbidden:**

- Draft -> Released
- TechnicallyApproved -> Released without a release decision (spec 14 criterion 12)
- Release to a recipient not marked IsAuthorizedRecipient
- Editing a released document in place (a new revision is mandatory)

**Terminal states:** `Superseded`, `Cancelled`

## NumberRegister.State

Every number ever reserved, issued or cancelled. A cancelled number is never reused (D-10).

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Reserved` | `Issued` | System | Document created successfully | IssuedAt set | — |
| `Reserved` | `Cancelled` | System | Job failed or was cancelled; Reason recorded | Number never reused; the gap is explainable | — |

**Explicitly forbidden:**

- Issued -> Reserved
- Cancelled -> Reserved or Issued (silent reuse is prohibited, D-10)
- Deleting any row from the register

**Terminal states:** `Issued`, `Cancelled`

## Approvals.Decision

Every approval decision, bound to the exact content approved (ADR-0006, D-09).

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Pending` | `Approved` | GeneralManager, TechnicalReviewer, FinanceReviewer | Acting user is the responsible approver, or holds a valid unrevoked delegation covering this stage, project and moment; Acting user is not the originator where SelfApprovalProhibited is TRUE; ContentHash still matches the entity | DecisionAt and DecisionByUserID recorded; DelegationID recorded when acting as a delegate | — |
| `Pending` | `Rejected` | GeneralManager, TechnicalReviewer, FinanceReviewer | Comment recorded | — | — |
| `Pending` | `Delegated` | GeneralManager, TechnicalReviewer, FinanceReviewer | A delegation exists that is active, unrevoked, inside its window, and covers this stage and project; The delegate is not the originator of the item being approved | Request reassigned to the delegate; the original responsible user is retained | — |
| `Delegated` | `Approved` | GeneralManager, TechnicalReviewer, FinanceReviewer, ProjectManager | Acting user is the named delegate; Delegation still valid at the moment of decision; ContentHash still matches the entity | DecisionByUserID is the delegate; RequestedFromUserID remains the accountable approver; DelegationID recorded | — |
| `Delegated` | `Rejected` | GeneralManager, TechnicalReviewer, FinanceReviewer, ProjectManager | Acting user is the named delegate; Comment recorded | DelegationID recorded | — |
| `Pending` | `Withdrawn` | System | Request superseded | — | — |
| `Approved` | `Void` | System | Entity ContentHash changed after approval | VoidedAt and VoidReason recorded | Every approval downstream of this one |

**Explicitly forbidden:**

- Approving one's own restricted transaction because an approver is unavailable (D-09)
- Approving with an expired, revoked or out-of-scope delegation
- Delegating to the person who originated the item being approved
- Void -> Approved (a fresh approval of the new content is required)

**Terminal states:** `Rejected`, `Withdrawn`, `Void`

## InvoiceRequests.FinanceStatus

A calculated billing request. Drafts only until Phase 7; never posted from Phase 1 or 6.

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Draft` | `PendingFinanceApproval` | System | Every line recalculated from stored inputs; Currency agrees across contract, project and request; Cumulative quantities within contract plus approved variation, or an authorised override exists; Tax rule confirmed in writing by the accountant | Calculation trace frozen with the request | — |
| `PendingFinanceApproval` | `FinanceApproved` | FinanceReviewer, GeneralManager | Approver is not the person who prepared the request; ContentHash of the source document still matches | Approval recorded with hash and the applied tax rule version | — |
| `PendingFinanceApproval` | `Rejected` | FinanceReviewer, GeneralManager | Reason recorded | — | — |
| `Rejected` | `Draft` | System | Recalculated | — | — |
| `FinanceApproved` | `Void` | System | A source record or certificate changed after approval | Finance approval voided | Finance approval; Any accounting posting authorisation |
| `Void` | `Draft` | System | Recalculated from the current inputs | — | — |

**Explicitly forbidden:**

- Draft -> FinanceApproved (finance approval is a separate, recorded decision)
- Any transition to PendingFinanceApproval while the tax treatment is UNDETERMINED (D-08)
- Approval by the person who prepared the request

## InvoiceRequests.QuickBooksStatus

A calculated billing request. Drafts only until Phase 7; never posted from Phase 1 or 6.

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `NotSent` | `Queued` | System | FinanceStatus = FinanceApproved | — | — |
| `Queued` | `SandboxPosted` | System | Sandbox company configured; Customer and item resolved by stored immutable identifier, never by name | Returned identifier recorded | — |
| `SandboxPosted` | `Reconciling` | System | Posted document read back | — | — |
| `Reconciling` | `Posted` | System | Every line, tax, retention, discount and total matches the local calculation exactly; QBO_POSTING_ENABLED is TRUE by written authorisation of the owner | Final invoice number recorded | — |
| `Reconciling` | `ReconciliationFailed` | System | Any difference, however small | Raised for a human. Never auto-corrected in either direction | — |
| `ReconciliationFailed` | `Queued` | FinanceReviewer, GeneralManager | Cause identified and corrected in the source, not in the accounting system | — | — |
| `Queued` | `Failed` | System | Error classified | Retried only if the class is retriable | — |
| `Failed` | `Queued` | System | Retriable class and under the retry cap | — | — |

**Explicitly forbidden:**

- NotSent -> Posted (sandbox and reconciliation are mandatory first)
- Reconciling -> Posted while any figure differs from the local calculation
- Any posting while QBO_POSTING_ENABLED is FALSE
- Creating a customer or item by matching on a similar name

**Terminal states:** `Posted`

## Projects.Status

A project is pure configuration. Adding one never requires changed logic, a cloned app, duplicated scenarios, rewritten prompts or changed code (D-01).

| From | To | Roles | Preconditions | Side effects | Invalidates |
|---|---|---|---|---|---|
| `Draft` | `Active` | SystemAdministrator, BusinessAdministrator, GeneralManager | Client, legal entity, locations, activity rules, approval matrix and template resolved; Residency assignment reviewed or explicitly recorded as unrestricted | Project becomes visible to assigned users | — |
| `Active` | `Suspended` | SystemAdministrator, BusinessAdministrator, GeneralManager | Reason recorded | No new visits; existing records readable | — |
| `Suspended` | `Active` | SystemAdministrator, BusinessAdministrator, GeneralManager | — | — | — |
| `Active` | `Completed` | GeneralManager | Closeout reporting complete | — | — |
| `Completed` | `Archived` | SystemAdministrator, BusinessAdministrator, GeneralManager | Retention review completed | Read-only | — |

**Explicitly forbidden:**

- Draft -> Active while a residency requirement blocks production upload and is unreviewed (D-12)
- Archived -> any state

**Terminal states:** `Archived`

