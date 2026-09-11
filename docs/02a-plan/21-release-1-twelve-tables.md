# Release 1 — Twelve Tables, and What Reaches a Field User

**Document ID:** AH-SYS-P2A-021 · **Revision:** 2 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-11 from `model/model.json` by `tools/gen_release1_scope.py`

> **Storage field counts come from the canonical model.** Exposure counts come from the
> declared form and view design, which is a specification and has not been built.

## 1. The twelve tables

Release 1 is **capture and review only**. It produces no document, so it carries no
document, numbering or legal-entity table.

| # | Table | Fields | Of which generated | Typed by a person |
|---|---|---|---|---|
| 1 | `Users` | 15 | 5 | 10 |
| 2 | `Projects` | 29 | 5 | 24 |
| 3 | `ProjectAssignments` | 14 | 4 | 10 |
| 4 | `Locations` | 16 | 4 | 12 |
| 5 | `ActivityTypes` | 18 | 4 | 14 |
| 6 | `SiteVisits` | 37 | 19 | 18 |
| 7 | `VisitActivities` | 19 | 10 | 9 |
| 8 | `Photos` | 64 | 52 | 12 |
| 9 | `Snags` | 24 | 11 | 13 |
| 10 | `Approvals` | 23 | 19 | 4 |
| 11 | `AuditLog` | 13 | 12 | 1 |
| 12 | `IntegrationJobs` | 18 | 17 | 1 |
| | **Total** | **290** | **162** | **128** |

## 2. Consolidations, and what each costs

| Folded away | Into | The rule | What it costs |
|---|---|---|---|
| `ProjectActivityRules` | ActivityTypes, with an optional ProjectID column | A row with no ProjectID is the global rule; a row with a ProjectID is a project override of it. Same resolution logic, one table. | The override and the rule it overrides share a table, so an administrator reading the catalogue sees both. Acceptable at 34 activities. |
| `Roles` | RoleCode enum on Users and ProjectAssignments | The role vocabulary is fixed at ten for the prototype. | Role capabilities are documentation rather than data. |
| `Clients` | ClientNameEN, ClientNameAR and ClientKind on Projects | Display only; no billing data exists in release 1. | A client with several projects is repeated per project. |
| `LegalEntities, DocumentJobs, Documents, NumberRegister` | Not present. Release 1 produces no document | Reports are produced manually from approved evidence exported from the app. | No document numbering, no release control, no report snapshot. **This is the boundary of release 1** and the first thing release 1b adds. |

**Release 1b adds** `DocumentJobs`, `Documents`, `NumberRegister`, `LegalEntities` — the moment
report generation is switched on.

## 3. Field exposure — the answer to "do not deploy 377 fields to the field interface"

| Measure | Fields | What it means |
|---|---|---|
| **Total in the release-1 storage model** | **290** | Every column across twelve tables, including audit columns |
| Of which **generated, never typed** | **162** | System, integration or AI sourced. A person never sees a keyboard for these |
| **Synchronised to a field device** | **236** | Only from the nine tables a supervisor's phone holds at all |
| **Administrative only** | **54** | Approvals, audit log and integration log. **Absent from the field data set entirely** |
| **On the normal field form** | **15** | What a supervisor can touch, most of it optional |
| **Mandatory to submit a normal photographic visit** | **0** | **None (D-22).** The supervisor supplies the photographs and nothing else |
| Confirmed only when ambiguous | 2 | Project and location, prefilled from the assignment, the default or the last used today. A question only when a genuine choice exists |
| **Visible to a reviewer** | **30** | The supervisor's fields plus the review controls |

**An honest caveat on the sync number.** A row synchronises whole: if a table is in a
user's data set, all its columns travel, which is why 236 is larger than the
15 on the form. Views and slices control what is *shown*, not what is
*delivered*. The two levers that genuinely reduce the sync payload are keeping a table out
of the field role's data set altogether — which is what puts Approvals, the audit log and
the integration log at zero — and keeping row counts down through security filters. The
form size and the sync size are different problems with different fixes.

### The normal field form, in full

**Nothing on this form is mandatory (D-22).** Fields marked * are confirmed only when they
do not resolve automatically; the rest are optional, or a one-tap confirmation of an AI
proposal.

| Screen | Fields the supervisor can touch |
|---|---|
| SiteVisits | **`ProjectID`** \*, **`LocationID`** \*, `AdditionalSiteNote`, `SiteNoteCategory`, `SafetyObservation`, `OverallDescriptionEN`, `OverallDescriptionAR` |
| VisitActivities | `ConfirmedActivityTypeID`, `DescriptionEN`, `Quantity`, `PercentComplete` |
| Photos | `EvidenceStage`, `CaptionEN`, `CaptionAR`, `AIProposalDisposition` |

**15 fields across three screens, of which 0 are mandatory.** The
project comes from the supervisor's assignment, the date and time from the device, the
identity from the session, the capture mode from a default; the Arabic description is an
alternative to the English one rather than an addition; the quantity appears only when an
activity rule requires it; percent complete is optional; the evidence stage is proposed or
left pending; and **the work description is optional in every normal case (D-18)**.

So of **290** fields in storage, a supervisor may touch **15** and **must**
supply **0**. The normal path is: open the app, confirm project and location if
necessary, capture the photographs, save and share.

### Capture once, use twice

The photographs are captured or selected **exactly once** (CAP-01). The same stored files
are handed to the main-contractor group through the native share sheet and re-used by every
later report. `Photos.CaptureBatchID` and `Photos.CaptureSequence` are the mechanism; a
failed or cancelled share is retried from stored evidence and never asks the supervisor to
select the images again. See [`24-capture-once-workflow.md`](24-capture-once-workflow.md).

### Why the storage model is larger than the form

| Category | Example | Why it exists |
|---|---|---|
| Audit columns | `CreatedAt`, `CreatedBy`, `UpdatedAt`, `UpdatedBy` | Four per table, generated. Attribution is the point of the audit trail |
| Keys and references | `VisitID`, `ProjectID`, `LocationID` | Generated or chosen from a dropdown, never typed |
| Integrity fields | `EntityVersion`, `ContentHash` | Generated. What an approval binds to |
| Evidence metadata | `OriginalChecksum`, `OriginalMimeType`, `ReceivedAt` | Captured by the system at registration |
| Advisory AI fields | `AIObservation`, `AIConfidence` | Written by analysis, read by a reviewer, typed by nobody |
| Review fields | `ReviewerDecision`, `ReviewerComment` | A reviewer's screen, not a supervisor's |

## 4. Per-table exposure

| Table | Fields | Syncs to device | Field form | Mandatory | Confirmed if ambiguous | Reviewer view | Admin only |
|---|---|---|---|---|---|---|---|
| `Users` | 15 | Yes | — | — | — | — | No |
| `Projects` | 29 | Yes | — | — | — | — | No |
| `ProjectAssignments` | 14 | Yes | — | — | — | — | No |
| `Locations` | 16 | Yes | — | — | — | — | No |
| `ActivityTypes` | 18 | Yes | — | — | — | — | No |
| `SiteVisits` | 37 | Yes | 7 | — | 2 | 8 | No |
| `VisitActivities` | 19 | Yes | 4 | — | — | 6 | No |
| `Photos` | 64 | Yes | 4 | — | — | 10 | No |
| `Snags` | 24 | Yes | — | — | — | 6 | No |
| `Approvals` | 23 | No | — | — | — | — | **Yes** |
| `AuditLog` | 13 | No | — | — | — | — | **Yes** |
| `IntegrationJobs` | 18 | No | — | — | — | — | **Yes** |

## 5. What release 1 deliberately cannot do

| Cannot | Because | Arrives in |
|---|---|---|
| Generate a report or certificate | No document, numbering or legal-entity table | Release 1b |
| Issue a document number | No numbering register | Release 1b |
| Release anything to a client | Nothing is generated to release | Release 1b |
| Delegate an approval | No delegation table; the general manager approves | Before go-live |
| Enforce residency in the app | Procedural, through the contract-review checklist | Phase 3 |
| Bill anything | No contract, BOQ, tax or invoice table | Phase 6 |

Reports during release 1 are produced **manually from approved evidence**, exactly as they
are today. The system's contribution in release 1 is that the evidence behind them is
captured once, segregated by project, reviewed by a named person and recorded in an audit
trail — which is the part that does not exist today.
