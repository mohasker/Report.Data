# Capture Once, Use Twice — Field Workflow Specification

**Document ID:** AH-SYS-P2A-024 · **Revision:** 2 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-12 from `model/model.json` by `tools/gen_capture_once.py`
**Authority:** the owner's operational corrections of 2026-09-11 (decisions D-16 to D-24)

> This document is generated from the canonical model. The automated checks in
> `tools/test_capture_once.py` test the same block, so the specification and the tests
> cannot disagree.

## 1. The principle

**Capture once, use twice. The supervisor captures or selects the photographs exactly once. The same stored files serve the contractor group share and every internal report.**

### CAP-01 — the acceptance requirement

> **The workflow fails acceptance if the supervisor must select or upload the images a second time.**

It applies to every one of these, not only the first share:

- first share
- retry after a failed or cancelled share
- AI analysis
- reviewer correction
- every report that re-uses the evidence

**If the platform cannot meet it:** Do not implement a duplicate-upload workaround. Produce the capture-platform decision comparison instead.

## 2. The workflow

| Step | Actor | Action | Where the fact comes from |
|---|---|---|---|
| 1 | Supervisor | Opens the field application. |  |
| 2 | System | Project, location, date, time, supervisor and capture mode are populated automatically. The supervisor is asked nothing unless a genuine choice exists. | ProjectAssignments, the device clock and the authenticated identity — trusted system data, never the photograph (D-22). |
| 3 | Supervisor | Confirms the location — and only when it does not resolve automatically. | Locations — prefilled from the project default or the last location used today. A trusted structured reference, never inferred from the photograph. |
| 4 | Supervisor | Captures or selects the photographs ONCE. | Device camera or gallery. This is the only file selection in the workflow. |
| 5 | System | The photographs are stored in the controlled system, unchanged, and grouped under one CaptureBatchID. |  |
| 6 | AI (advisory) | Analyses the ELIGIBLE photographs and PROPOSES the advisory fields below — immediately in AI Reviewed Share, after the share in Quick Share (D-24). | Advisory only. Binds nothing, approves nothing. |
| 7 | Supervisor | Confirms or corrects the proposal with minimum interaction. In Quick Share this happens later; classification stays Pending and blocks nothing (D-23). | The human decision. This is what the record carries. |
| 8 | Supervisor | Shares the same image files and a formatted summary to the existing main-contractor group through ONE native share action. | Native share sheet only. No public link, no re-selection, no web automation. |
| 9 | System | The same stored evidence is re-used in daily, weekly, monthly, corrective-action, inspection and completion reports. |  |

**Step 4 is the only file selection in the entire workflow.** Steps 8 and 9 both re-use
what step 5 stored.

## 3. The two operating modes

| Mode | Sequence | AI | Use when | Times the evidence is captured |
|---|---|---|---|---|
| **QuickShare** | capture → store → native share | deferred and filtered: after the share, once duplicates, unusable images and exclusions have been removed (D-24) | The default. The contractor group is served first and nothing is waited for. | **1** |
| **AIReviewedShare** | capture → store → AI proposal → supervisor confirmation → native share | immediate, before the share, on the batch's eligible photographs | A reviewed professional caption is wanted before group submission. | **1** |

Both modes end at the native share sheet, and both capture exactly once. The difference is
only whether the AI proposal is waited for.

## 3b. Minimum interaction — what the supervisor actually supplies

**Minimum interaction. On the normal path the supervisor supplies the photographs and nothing else. Every other value is populated automatically, and a question is asked only when a genuine choice exists.**

### The normal path

```
   open the app  ->  confirm project and location only if necessary  ->  capture the photographs  ->  save and share
```

**Mandatory manual inputs on that path: 0.** The supervisor supplies the photographs and nothing else.

### What is populated automatically

| Field | Where the value comes from | When the supervisor is asked |
|---|---|---|
| `SiteVisits.SupervisorUserID` | the authenticated identity | never |
| `SiteVisits.VisitDate` | the device date | never |
| `SiteVisits.StartTime` | the device time at first capture | never |
| `SiteVisits.EndTime` | the device time at last capture | never |
| `SiteVisits.ProjectID` | the single active assignment, else the last project used today, else the project default | only when several assignments are active and none resolves |
| `SiteVisits.LocationID` | the project's default location, else the last location used today | only when several active locations exist and none resolves |
| `SiteVisits.CaptureMode` | defaults to QuickShare | never on the normal path |
| `Photos.EvidenceStage` | proposed by analysis, or pre-tagged from the activity rule, or left pending | never before capture |
| `Photos.CaptureBatchID` | generated at capture | never |
| `Photos.CaptureSequence` | the order the device captured them | never |

### Required in storage is not the same as required of the supervisor

These fields are required for the record to mean anything, and none of them is a question
on the normal path:

- `SiteVisits.ProjectID`
- `SiteVisits.LocationID`
- `SiteVisits.VisitDate`
- `SiteVisits.SupervisorUserID`
- `SiteVisits.CaptureMode`
- `SiteVisits.ShareStatus`
- `SiteVisits.ShareAttemptCount`
- `Photos.ClassificationStatus`
- `Photos.AnalysisEligibility`

> Required in storage and required of the supervisor are different things. Every field above is required for the record to be meaningful, and none of them is a question on the normal path.

### What is not required at all

**`VisitActivities`** — Declaring an activity is not the price of submitting evidence (D-22). A visit carrying photographs and no activity is a valid photographic submission; the classification catches up afterwards. An activity that DOES exist still satisfies its effective rule in full — quantity, caption and minimum photographs are unchanged.

### Optional, and genuinely optional

`SiteVisits.AdditionalSiteNote`, `SiteVisits.SiteNoteCategory`, `SiteVisits.SafetyObservation`, `SiteVisits.OverallDescriptionEN`, `SiteVisits.OverallDescriptionAR`, `Photos.CaptionEN`, `Photos.CaptionAR`, `Photos.EvidenceStage`.

## 3c. Classification — a proposal is not a fact

**AI-generated free text never becomes the trusted structured activity. A proposal and a confirmation are different columns, and only the confirmation is read by anything.**

| Column | Standing |
|---|---|
| `Photos.AIProposedActivityText` | **Advisory.** Untrusted. Read by the confirmation screen and nothing else |
| `Photos.AIProposedActivityTypeID` | **Advisory.** Untrusted. Read by the confirmation screen and nothing else |
| `Photos.ConfirmedActivityTypeID` | **Trusted.** The structured activity a report may use |
| `Photos.ClassificationStatus` | How far the classification has got |
| `Photos.AIProposalDisposition` | What the supervisor did with the proposal |

**The rule.** Only ClassificationStatus = Confirmed makes ConfirmedActivityTypeID readable by a report, a rule, a calculation or a filter. Pending is the normal state immediately after a Quick Share and blocks nothing.

**In Quick Share.** Classification stays Pending and is reviewed later. The share has already happened; the record catches up.

**Barred from reading the candidate:** reports, business rules, calculations, filters, joins, approvals.

| Classification state | Meaning |
|---|---|
| `Pending` | Captured, not yet classified. The normal state immediately after a Quick Share. |
| `AIProposed` | An advisory proposal exists. **Still untrusted.** No report or business rule may use it. |
| `Confirmed` | A supervisor or reviewer set ConfirmedActivityTypeID. The only trusted state. |
| `NotApplicable` | The photograph carries no activity to classify — a safety observation, a material delivery. |
| `Excluded` | Deliberately left out: a duplicate, an unusable image, or evidence excluded from this report. |

## 3d. When analysis runs, and when it does not

**Not every captured photograph needs an immediate model call. Filtering happens before the call, never after it, and reports still use every relevant approved photograph.**

| | **AIReviewedShare** | **QuickShare** |
|---|---|---|
| Timing | immediate, before the share | deferred, after the share |
| Unit | one request per capture batch | one request per capture batch, batched again across visits where the queue allows |
| Filtered | local duplicate and quality checks run first; the rest of the batch is analysed | duplicates, unusable images, deleted and explicitly excluded images are removed first; only then is a request made |
| Why | the supervisor is waiting, so the proposal has to exist now | nothing is waiting, so the cheapest correct moment is after the supervisor has finished and the obvious waste has been removed |

### Never analysed

- a near-duplicate of a photograph already analysed in the same batch
- an image below the project's quality threshold
- an image deleted or explicitly excluded before analysis ran
- an image already analysed — analysis never runs twice on the same file
- any image in a project where analysis is switched off, or after the monthly cap

**Still analysed:** every photograph a reviewer may approve for a report. Skipping is about waste, never about coverage: an excluded image is one nobody will report on.

**Perceptual hashing and the blur measure run locally, without a model call.**

### Estimated eligibility

> **Every eligibility proportion below is an ESTIMATE from the stated assumptions. None has been measured. The pilot's first month replaces them with counts.**

| Class | Estimated share | Basis |
|---|---|---|
| near-duplicate | 8% | supervisors take two or three of the same subject to be sure |
| below quality threshold | 5% | movement, low light, an obstructed lens |
| deleted or excluded before analysis | 4% | wrong subject, accidental capture |
| **Eligible** | **83%** | the remainder |

At the pilot's **360** photographs a month, that is about
**299** analysed under Quick Share and
**331** under AI Reviewed Share.

Immediate mode filters duplicates and unusable images locally but cannot know what the supervisor will later exclude, so its eligible count is higher.

## 4. The written description is optional

> **A written description of completed work must not be mandatory for a normal photographic submission.**

These fields are optional by design, and the checks fail if any of them becomes required:

- `SiteVisits.OverallDescriptionEN`
- `SiteVisits.OverallDescriptionAR`
- `SiteVisits.AdditionalSiteNote`
- `VisitActivities.DescriptionEN`
- `VisitActivities.DescriptionAR`
- `Photos.CaptionEN`
- `Photos.CaptionAR`

### What the optional note is for

Facts a photograph cannot establish. `SiteVisits.SiteNoteCategory` carries the vocabulary:

| Code | Meaning |
|---|---|
| `ClientInstruction` | Client instruction |
| `AccessRestriction` | Access restriction |
| `PermitIssue` | Permit issue |
| `HiddenDefect` | Hidden or underground defect |
| `MeasuredQuantity` | Measured quantity — Typed by a person. Never proposed by image analysis. |
| `MaterialQuantityOrBatch` | Material quantity or batch |
| `EquipmentFailure` | Equipment failure |
| `NonCompletionReason` | Reason for non-completion |
| `SafetyRestriction` | Safety restriction |
| `PostponedByOtherParty` | Work postponed by another party |

**Future input methods** for the same field, not new fields: voice note, speech to text.

### The exceptional workflows that DO require a written reason

- A record returned for correction — RejectionReason stays mandatory.
- A visit reporting non-completion — the reason cannot be photographed.
- A caption on an Observation, Snag, Material or Safety photograph — the stage itself asserts a fact the image alone does not name.
- A measured quantity claimed without a photographed measurement.

Everything outside this list is a normal photographic submission, and a normal
photographic submission needs no typed description.

## 5. What the AI proposes

Every item below is a **proposal** written to its own advisory column. None of them is
ever written to the confirmed field, and none enters a content hash, so an analysis
arriving later can never void a human approval.

| What is proposed | Advisory column |
|---|---|
| visible activity | `Photos.AIProposedActivityText` |
| evidence stage | `Photos.AIProposedEvidenceStage` |
| professional caption | `Photos.AIProposedCaptionEN` |
| visible condition | `Photos.AIVisibleCondition` |
| possible snag | `Photos.AIPossibleSnag` |
| image quality warning | `Photos.AIImageQualityWarning` |
| uncertainty | `Photos.AIUncertaintyNote` |
| confidence | `Photos.AIConfidence` |

**Evidence stage vocabulary:** `Before`, `During`, `After`, `Observation`, `Snag`, `Material`, `Equipment`, `Safety`, `Other`.

The supervisor's response is recorded in `Photos.AIProposalDisposition` — `NotOffered`, `Accepted`, `Corrected`, `Rejected` — so a confirmation is always distinguishable from a correction.

## 6. What the AI must not infer

AI may describe only visually supportable conditions and activities. It must not infer or
confirm:

- measured quantity
- hidden defect or its cause
- exact material brand
- compliance with contract or specification
- exact completion percentage
- exact project or location from the photograph alone
- responsibility or negligence
- date, unless supplied as trusted metadata
- that Al-Haram executed the visible work merely because it appears in the photograph

### Trusted context comes from system data, never from the photograph

- `SiteVisits.ProjectID`
- `SiteVisits.LocationID`
- `SiteVisits.VisitDate`
- `SiteVisits.SupervisorUserID`
- `SiteVisits.WorkOrderID`
- `VisitActivities.ActivityTypeID`
- `Photos.LocationID`

### The 18 columns closed to AI by declaration

Checked by `CAP-14`. If any of these is ever changed to an AI source, the validation suite
fails:

| Column | Why it is closed |
|---|---|
| `SiteVisits.ProjectID` | Contractual identity. Comes from the assignment. |
| `SiteVisits.LocationID` | Structured reference. A photograph cannot name a location reliably. |
| `SiteVisits.VisitDate` | Trusted metadata or a human correction, never a guess. |
| `SiteVisits.SupervisorUserID` | Attribution. Comes from the signed-in user. |
| `SiteVisits.WorkflowStatus` | A state machine, not an opinion. |
| `VisitActivities.ActivityTypeID` | A contractual activity. Advisory text exists separately. |
| `VisitActivities.Quantity` | Quantitative. Feeds a certificate and eventually an invoice. |
| `VisitActivities.PercentComplete` | Quantitative and contractual. |
| `VisitActivities.UnitID` | Determines what a quantity means. |
| `Photos.EvidenceStage` | The supervisor's assertion about what the photograph shows. |
| `Photos.CaptionEN` | The supervisor's own words. |
| `Photos.CaptionAR` | The supervisor's own words. |
| `Photos.ReviewerDecision` | A human review decision. |
| `Photos.ApprovedForReport` | Derived from a human decision. |
| `Photos.ConfirmedActivityTypeID` | Trusted structured data. |
| `Photos.ClassificationStatus` | Trusted structured data. |
| `Snags.Severity` | A judgement with commercial consequence. |
| `Approvals.Decision` | An approval. Only a named person approves. |

## 7. Sharing to the main-contractor group

**Method:** native operating-system share sheet. **Payload:** the stored image files themselves, plus a formatted text summary.

| Rule | Value |
|---|---|
| A public link is required | **No** |
| A public link is permitted | **No** |

**Forbidden methods:**

- WhatsApp Web automation
- group scraping
- any unofficial messaging automation
- a publicly accessible Drive link
- any flow that asks the supervisor to select the files again

**Recorded as:** `SiteVisits.ShareStatus`, `SiteVisits.SharedAt`, `SiteVisits.ShareAttemptCount`.

> **An honest limit.** The application can record that the share sheet was opened and that the supervisor said it completed. It cannot observe delivery inside the messaging application, and no document may claim otherwise.

## 8. The platform gate — unverified

**CAP-GATE:** Can AppSheet reliably share multiple actual image files and formatted text through the native share sheet to an existing WhatsApp or WhatsApp Business group, on iOS and Android?

**Status: UNVERIFIED — requires real-device testing in Phase 2A**

### The 15 conditions that must be tested on real devices

| # | Condition |
|---|---|
| 1 | one photograph |
| 2 | six photographs |
| 3 | portrait and landscape images |
| 4 | image order |
| 5 | formatted summary |
| 6 | standard WhatsApp |
| 7 | WhatsApp Business |
| 8 | normal connection |
| 9 | weak connection |
| 10 | offline capture followed by synchronisation |
| 11 | images attached or only links |
| 12 | whether the user must select the images again |
| 13 | whether a public Drive link is created |
| 14 | whether temporary files remain on the device |
| 15 | failed or cancelled share recovery |

**The workflow fails acceptance if the supervisor must select or upload the images a
second time.** No duplicate-upload workaround will be implemented. If AppSheet cannot meet
the requirement, the decision comparison is between:

1. AppSheet with a proven native-share method
2. A lightweight custom PWA or mobile field application using supported native file sharing
3. Any other official, policy-compliant approach

> **The data model, Drive security, Make orchestration, Claude controls, approval rules and audit requirements must remain re-usable if the capture interface changes.**

This is why the capture platform is an interface decision and not an architecture
decision: the canonical model, the security filters, the approval binding, the numbering
contract and the audit trail are all defined independently of it.
