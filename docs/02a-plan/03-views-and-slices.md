# Views and Slices

**Document ID:** AH-SYS-P2A-003 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Not built, not tested**

> Views and slices control **presentation**. They are never enforcement: a slice that hides a column
> does not stop the data reaching the device. Enforcement is the security filter
> ([`02-security-filter-specification.md`](02-security-filter-specification.md)) plus server-side
> re-validation (P-04).

---

## 1. Design principle: the form must beat the habit

The single largest risk to this system is that a supervisor finds it slower than sending photographs
to a messaging group (R-06). Every decision below follows from that:

- **Choices over typing.** Dropdowns, not free text, wherever a controlled value exists.
- **The shortest possible path to a photograph.** Capture is two taps from the home screen.
- **Nothing on screen that the role cannot act on.** A supervisor never sees a review queue, a
  financial figure, or another project.
- **Defaults that are usually right.** Today's date, the signed-in user, the last project used.
- **The form says what is missing**, in the language the user chose, before they leave site.

## 2. Slices

| Slice | Source | Row filter | Purpose |
|---|---|---|---|
| `MyDrafts` | SiteVisits | `AND([SupervisorUserID] = ME(), [WorkflowStatus] = "Draft")` | The supervisor's unfinished work |
| `MySubmitted` | SiteVisits | `AND([SupervisorUserID] = ME(), IN([WorkflowStatus], LIST("Submitted","UnderTechnicalReview","TechnicallyApproved")))` | What they have sent |
| `NeedsCorrection` | SiteVisits | `AND([SupervisorUserID] = ME(), IN([WorkflowStatus], LIST("ValidationFailed","CorrectionRequired")))` | Returned work, with reasons |
| `ReviewQueue` | SiteVisits | `AND(IN([ProjectID], MY_PROJECTS()), [WorkflowStatus] = "UnderTechnicalReview", [SupervisorUserID] <> ME())` | Reviewer queue. **Excludes the reviewer's own submissions** — self-review is prevented in the slice as well as in the rule |
| `PhotosPendingReview` | Photos | `AND(IN([ProjectID], MY_PROJECTS()), [ReviewerDecision] = "Pending")` | Photograph-level review |
| `ApprovedEvidence` | Photos | `AND(IN([ProjectID], MY_PROJECTS()), [ApprovedForReport] = TRUE)` | What may appear in a report |
| `OpenSnags` | Snags | `AND(IN([ProjectID], MY_PROJECTS()), NOT(IN([Status], LIST("Closed","Rejected"))))` | Open corrective actions |
| `MySnags` | Snags | `AND([RaisedBy] = ME(), NOT(IN([Status], LIST("Closed","Rejected"))))` | A supervisor's own snags |
| `ActiveProjects` | Projects | `AND(IN([ProjectID], MY_PROJECTS()), [Status] = "Active")` | Project picker source |
| `ProjectLocations` | Locations | `AND(IN([ProjectID], MY_PROJECTS()), [IsActive] = TRUE)` | Location picker source |
| `MonthlyCompleteness` | SiteVisits | `AND(IN([ProjectID], MY_PROJECTS()), MONTH([VisitDate]) = MONTH(TODAY()))` | Dashboard source |
| `AdminErrors` | IntegrationJobs | `IN([Status], LIST("Failed","DeadLettered"))` | Administrator error queue |

**Column-level rule.** Field-role slices omit financial and personal columns entirely rather than
hiding them. The strongest form of the control is that the data is not in the slice at all.

## 3. View map by role

### Site supervisor and field user — the only views that must be fast
| View | Type | Source | Notes |
|---|---|---|---|
| Home | Dashboard | — | Four tiles: **New Visit**, My Drafts, Needs Correction, Open Snags |
| New Visit | Form | SiteVisits | Project → Location → date → description. Project defaults to the last used |
| Add Activities | Form (inline) | VisitActivities | Activity filtered by project rules; quantity shown only when the effective rule requires it |
| Add Photos | Form (inline) | Photos | Camera-first. Evidence stage pre-filled from the activity's default stages |
| Photo Gallery | Gallery | Photos | Their own project's evidence, to avoid duplicate captures |
| My Drafts | Deck | `MyDrafts` | Continue or submit |
| Needs Correction | Deck | `NeedsCorrection` | **Shows the reviewer's reason at the top**, not buried in a detail view |
| Open Snags | Deck | `MySnags` | Raise and update |

### Technical reviewer and project manager
| View | Type | Source | Notes |
|---|---|---|---|
| Review Queue | Deck | `ReviewQueue` | Oldest first. Their own submissions are absent |
| Visit Review | Detail | SiteVisits | Approve / Return for correction, with a mandatory reason on return |
| Photo Review | Gallery | `PhotosPendingReview` | Caption, **AI observation shown separately and labelled**, approve / reject / exclude |
| Approved Evidence | Gallery | `ApprovedEvidence` | With report sequence |
| Open Snags | Table | `OpenSnags` | Assign, verify, close |
| Monthly Completeness | Dashboard | `MonthlyCompleteness` | Missing before/after, unreviewed photographs, days with no visit |

### General manager
All of the reviewer views across every project, plus: Documents Pending Approval, Release queue,
Portfolio dashboard, Approval and delegation administration, Access grants.

### Business administrator
Clients, Contacts, Projects, Locations, Activity rules, Templates, Numbering series, Approval matrix,
Residency assignments. **No evidence, no documents, no financial views.**

### System administrator
Users, Roles, Project assignments, Vocabularies, Integration errors, Audit log (read-only), Access
grants (read-only), Recovery plan. **No evidence, no documents, no financial views.**

### Finance reviewer *(Phase 6/7)*
Invoice requests, Invoice lines, Contracts, BOQ, Tax rules, Calculation traces, Finance approval
queue.

### Read-only auditor and break-glass
Both see a banner stating the grant, its reason and its expiry. The auditor's views are read-only
copies of the relevant queues; break-glass sees **only** the administrator views.

## 4. Branding and usability

Professional navy and gold consistent with the company's identity, applied to headers and primary
actions only. No decorative background, no custom fonts on form screens, nothing that costs a
rendering frame on a mid-range Android phone in sunlight. Legibility beats brand expression on a
field device — and a supervisor who cannot read the screen outdoors stops using the app.

## 5. Bilingual behaviour

The interface follows `Users.Language`. Labels and help text are authored in both languages from the
start. Free-text fields accept either language and store what was typed, without transliteration. A
supervisor may write a description in Arabic while the report is generated in English — both are
carried, and the narrative prompt receives both.

## 6. What must be tested before this is believed

Nothing in this document has been built. The Phase 2B gate must record: the review queue genuinely
excludes the reviewer's own submissions; a field role's slice genuinely lacks financial columns
rather than hiding them; and the home screen reaches a photograph in two taps on a real device.
