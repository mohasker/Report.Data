# Evidence Rules

**Document ID:** AH-SYS-P1-005 · **Revision:** 1 · **Date:** 2026-09-11
**Delivers:** D-15 item 4 (project-specific activity and evidence rules) · **Closes:** C-07, C-08
**Executable statement:** `tools/evidence.py` · **Evidence:** `17-validation-evidence.md` (EVD-01 … EVD-14)

---

## 1. The rule is configuration, resolved per project

Each activity in the catalogue carries default requirements: before photograph, after photograph,
quantity and unit, minimum photograph count, material, snag check. A project that needs something
different gets a `ProjectActivityRules` row — never a code change (D-01).

```
effective rule = global ActivityTypes rule
                 overridden field-by-field by ProjectActivityRules for this project
```

An override is applied only where the project actually supplies a value; an empty override field
inherits. The resolver reports the **source** of every field (`Global` or `ProjectOverride`), so a
supervisor asking "why does this project want three photographs?" gets an answer rather than a
shrug (EVD-01, EVD-02).

Three consequences, each tested:

| Behaviour | Check |
|---|---|
| The same activity carries different requirements on different projects | EVD-03 |
| An activity can be withdrawn from one project while remaining live elsewhere, without deleting history | EVD-04 |
| A brand-new project works immediately from the global catalogue, with no override rows at all | CFG-10 |

## 2. What makes a submission complete

A visit is complete when it has at least one activity and **every** activity satisfies its effective
rule:

1. The activity is permitted on this project.
2. A `Before` photograph exists where required; an `After` photograph exists where required.
3. The photograph count meets the effective minimum.
4. A quantity is present, numeric and non-negative where required — and **absent where the rule does not take one** (a quantity on an activity that has none is a data-entry error, not a bonus).
5. A unit accompanies every quantity.
6. A caption exists on every `Snag`, `Observation`, `Material` and `Safety` photograph, in either language.
7. Any additional project-level caption requirement is met.

## 3. Where each rule is enforced — resolving C-07

A supervisor can complete a visit offline and have it fail validation hours later, after leaving
site. The evidence gap is then unfixable without a return visit. So the rules are split by *where
they can be checked*, not by convenience:

| Enforced on the device, at form level | Enforced server-side, after sync |
|---|---|
| At least one activity | Submitter holds an active assignment with `MaySubmitEvidence` |
| Required before/after photographs | Project is `Active` |
| Minimum photograph count | Location belongs to the selected project |
| Quantity present, numeric, non-negative | Activity is permitted for the project **as configured now** |
| Unit accompanies quantity | Referential integrity of every reference |
| Mandatory captions | Reviewer identity and self-review prohibition |

Everything that *can* be checked while the supervisor is still standing on site, is. Server-side
validation then covers only what genuinely needs authoritative data — and it remains the security
boundary, because a client-side check can never be trusted for security (P-04).

A failure returns the specific correctable errors in `ValidationErrors`, never a generic rejection
(EVD-12).

## 4. Photographs: warn, flag, and never destroy

| Situation | Behaviour | Why |
|---|---|---|
| Capture timestamp much older than the visit date | **Warn**, recorded for the reviewer | Offline capture is legitimate; an automatic rejection would block honest work (spec 7.3) |
| Suspected duplicate | **Flag** with `IsDuplicateSuspected` and a pointer to the original; both rows retained | §5.10 requires flagging, not deletion. Merging loses evidence (EVD-13, S-09) |
| GPS absent or permission denied | Recorded as **missing**, never as zero | Zero is a real coordinate off the coast of Africa. A suspended-ceiling inspection is indoors by definition (C-08, EVD-14) |
| Capture outside the geofence | Flagged for the reviewer | The radius is a hint about attention, not a gate |
| Caption missing on a stage that requires one | **Blocks submission**, naming the photograph | The caption is the evidence's meaning |

## 5. The reviewer is the gate, not the rules

The rules ensure a submission is *complete*. They say nothing about whether it is *true*. Only a
human reviewer decides that:

- `ReviewerDecision` is set by a person and never by AI (GOV-10, TRN-19).
- `ApprovedForReport` follows the reviewer's decision; only human-approved evidence may appear in an official report (D-06).
- The supervisor's caption is preserved exactly. An AI observation is stored separately and displayed as an AI observation, visually distinct from both the caption and the reviewer's decision.
- A reviewer may not approve their own submission; the approval matrix prohibits self-approval on every route (TRN-11).

## 6. Overrides

An evidence rule can be waived, but never quietly. A waiver is an `Approvals` row with
`IsOverride = TRUE`, an `OverrideReason`, and the identity of whoever authorised it. It appears on
the audit dashboard as an override. A rule that can be silently disabled is not a rule (SEC-05,
R-30).
