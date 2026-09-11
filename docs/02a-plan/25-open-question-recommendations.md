# Recommendations for the Eight Open Questions — OQ-15 to OQ-22

**Document ID:** AH-SYS-P2A-025 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Nothing built, nothing connected, nothing decided**

---

## 1. What this document is, and what it is not

Eight questions have been open since the capture-once correction pass. None of them needs an external
connection, a credential, a purchase or real data to *answer* — they need the owner's judgement.
This document states each question, what the canonical model assumes today, the options with their
real trade-offs, and **one recommendation with its reasoning**.

**A recommendation is not a decision.** Nothing here may be cited as settled, implemented, or built
against until the owner answers. Until then every one of the eight remains open, and the model stays
as it is. Where a recommendation would change `model/model.json`, the change is named exactly —
including the columns it would add — so the cost of saying yes is visible before it is paid.

Three of the eight (**OQ-17, OQ-20, OQ-22**) end in *measure first, decide after*. That is a real
answer, not an evasion: each one depends on a fact nobody in this project has yet observed, and the
honest move is to name the measurement rather than pick a number that would then be quoted as though
it had been verified.

## 2. Summary — the eight recommendations

| # | Question | Recommendation | Model cost if approved | Reversal cost |
|---|---|---|---|---|
| **OQ-15** | Default capture mode, and who chooses | **Quick Share stays the default; the project may override it; the supervisor may switch by an explicit action, never by a question** | 1 column on `Projects` | Low — the column is ignored |
| **OQ-16** | A formatted summary with every share? | **Always, in two lengths: a short constant block, extended only when a snag or safety observation exists** | None | None |
| **OQ-17** | Should the share also reach an internal group? | **Two explicit share actions, not one. Not in release 1. Add the "can one share reach two groups?" question to `CAP-GATE` and measure it** | None now — deliberately | None |
| **OQ-18** | May a supervisor share a visit still in draft? | **Yes — permitted, and recorded. A reviewer view shows what left before review; a shared draft is corrected by a new version, never erased** | None — a view over existing columns | Low |
| **OQ-19** | Voice: keep the audio, or only the transcript? | **Transcript only, with the input method recorded so a transcript is never mistaken for typed text. Post-MVP** | 1 column + 1 enum, Post-MVP | Low |
| **OQ-20** | Quality and near-duplicate thresholds | **Start conservative and relative, not absolute: Hamming ≤ 5 within one batch; no absolute quality cutoff until the distribution is measured. Both as project configuration** | 2 columns on `Projects` | Low |
| **OQ-21** | Should a pending classification expire? | **It accumulates and ages. It never expires into a value. Older than 7 days it appears in the reviewer's overdue view and the weekly digest** | 1 column on `Projects` | Low |
| **OQ-22** | Should the location prompt offer the nearest location by GPS? | **Not now. Measure how often the prompt appears at all first; revisit only if it is frequent, and then GPS may order the list, never select the value** | None | None |

**If all eight were approved: four columns on `Projects`, one on `SiteVisits` (Post-MVP), one new
enum, no new table, and no change to the twelve tables of release 1.**

---

## 3. OQ-15 — Which mode is the default, and who chooses it

**The question.** Which operating mode is the default — Quick Share or AI Reviewed Share — and
whether the supervisor chooses per visit or the project fixes it.

**What the model assumes today.** `capture_once.modes.QuickShare.default = true`.
`SiteVisits.CaptureMode` defaults to `QuickShare` and, under D-22, the supervisor is **never asked**
for it on the normal path. AI Reviewed Share is chosen "by an explicit action, never a routine
question". **There is no per-project setting** — no `Projects` column carries a default mode, so
today every project behaves identically.

| Option | What it means | Against it |
|---|---|---|
| A | Quick Share everywhere; supervisor switches per visit | A client who wants reviewed captions before anything reaches their group cannot be accommodated without code — which breaks D-01 |
| B | AI Reviewed Share everywhere | Every submission then waits on a model call. The contractor group is served last. This is the behaviour the capture-once correction removed |
| C | The project fixes the mode; the supervisor cannot switch | Removes the supervisor's judgement on the one visit where a reviewed caption matters |
| **D** | **The project sets the default; the supervisor may switch by explicit action** | One column, and a default that differs between projects is one more thing to explain |

**Recommendation: D.** It is option A plus a single column. Quick Share remains the default because
the contractor group is served first and nothing waits on a model — and because under D-23 a
`Pending` classification blocks nothing, so deferring analysis costs the record nothing. But "a
project is pure configuration" (D-01) is the load-bearing principle of this whole system, and a
capture mode that cannot vary by project is a policy hard-coded into the app.

**What approval would change.** One column on `Projects`: `DefaultCaptureMode` (enum `CaptureMode`,
required, default `QuickShare`), authored in `tools/build_model.py`. One line in
`capture_once.minimum_interaction.auto_populated` — the source of `SiteVisits.CaptureMode` becomes
"the project default, else Quick Share". **The tap count does not change:** the supervisor is still
never asked, because a default that comes from the project is still a default.

**What it must not become.** A per-visit *question*. Switching mode stays an explicit action the
supervisor takes when they want it, exactly as D-22 requires.

## 4. OQ-16 — Does a formatted summary accompany every share

**The question.** Whether a formatted summary accompanies every share, or only those carrying a snag
or a safety observation. More text is not always more useful to a contractor.

**The fact that settles half of it.** The summary costs the supervisor nothing. It is composed from
values already populated — project, location, date, photograph count — so "always" and "sometimes"
are the same number of taps. The question is only what serves the reader.

**Recommendation: always, in two lengths.**

- **Always, short:** project, location, date, the number of photographs, and the visit reference once
  numbering exists (Phase 5). This constant header is what makes a message findable in a group six
  months later, and losing that is precisely what the current practice costs the company.
- **Extended only when there is something to say:** the snag or safety lines are added when such an
  observation exists on the visit. A message that says nothing every day teaches its readers not to
  read it.

**One consequence the owner should see plainly.** The summary may contain only **confirmed**
structured values. Under D-23, `AIProposedActivityText` and `AIProposedActivityTypeID` are advisory
and are read by the confirmation screen and nothing else — a share message is neither. So **the
summary of a Quick Share carries no activity names**, because at that moment classification is still
`Pending`. The share says where, when, and how many photographs; it does not say what was done. That
is the honest price of sharing before review, and it should not be worked around by quietly letting
a proposal into the text.

**What approval would change.** Nothing in the model. The template belongs in
`docs/02a-plan/04-actions-and-workflow.md`, and in `DocumentTemplates` once templates are built.

## 5. OQ-17 — Should the same share also reach an internal group

**The question.** Whether the same share should also reach an internal group, and whether that is a
second share action or one action with two destinations. *(Phase 2B)*

**What is not known.** Whether one invocation of the native share sheet can reach two destinations
**has not been verified**. It is platform behaviour, the vendor documentation was unreachable from
this build environment, and no device test has been run. The assumption — that the sheet returns to
the application after one destination, and a second group is a second invocation — is an assumption
and is recorded as one.

**Recommendation: two explicit share actions, the internal one optional, and none of it in release
1. Add the question to the `CAP-GATE` device protocol and measure it.**

Reasoning: the internal share is a convenience; the contractor share is the product. Building a
"one action, two destinations" flow on an unverified platform capability risks discovering at the
device test that it cannot be done — after it has been designed around. `CAP-GATE`
(`docs/02a-plan/19-real-device-test-protocol.md` §4b) already puts two phones and six synthetic
photographs in front of a human. One more condition costs that test nothing:

> **Can a single share invocation reach two separate groups, on Android and on iOS?
> If not, how many taps is the second share?**

**The rule that applies either way.** CAP-01 governs the second share exactly as it governs the
first: **the supervisor must never be asked to select the photographs again.** An internal share that
re-opens the picker fails acceptance, and no duplicate-upload workaround is acceptable.

**What approval would change.** Nothing yet — deliberately. `SiteVisits.ShareTargetLabel` is
single-valued today; a second destination needs either a second label column or a small child table,
and **modelling a capability that may not exist is the error to avoid.** Decide the shape after the
device test says what is possible.

## 6. OQ-18 — May a supervisor share a visit that is still in draft

**The question.** Quick Share implies yes; evidence control argues no.

**The uncomfortable statement this touches.** *Quick Share sends evidence before review.* That
sentence was written deliberately and must not be softened. The question is not whether that is
uncomfortable — it is — but whether the discomfort is worth what Quick Share buys.

| Option | Consequence |
|---|---|
| A — permitted and unrecorded | The reviewer cannot tell which evidence the client has already seen. Unacceptable |
| B — forbidden; submit first | Deletes Quick Share, and with it the only part of this system that matches what supervisors already do today. Every submission then waits for a reviewer |
| **C — permitted, and recorded** | The contractor is served immediately; the reviewer can see exactly what left before anyone checked it |

**Recommendation: C.** Permitted, because forbidding it would trade the system's single biggest
adoption advantage for a control that arrives too late anyway — the photographs are already in the
group before any reviewer could have opened the record. Recorded, because a reviewer who does not
know what the client has seen cannot review anything meaningfully.

**How, with no new column.** `ShareStatus` moves to `ShareInitiated` / `ShareConfirmed` while the
visit is still a draft; `SharedAt` is populated. "Shared before review" is therefore a **filter over
existing columns** — `SharedAt` is not null and the visit has not been submitted — and belongs in the
reviewer's view list in `docs/02a-plan/03-views-and-slices.md`, not in the model.

**The rule that has to come with it.** **A shared visit may be corrected, never erased.** Once
evidence has left, a correction is a new version recorded in `EntityVersions` — because the
contractor already holds the photographs, and a record that quietly differs from what the client
received is worse than no record. This follows from the existing write-once and versioning rules; it
is stated here because draft sharing is where someone will first be tempted to delete something.

## 7. OQ-19 — Voice capture: the audio, or only the transcript

**The question.** Whether voice capture stores the audio as evidence, or only the transcript into
`AdditionalSiteNote`. *(Post-MVP — D-18 lists voice as a future input method for an existing field,
not a new kind of evidence.)*

**Recommendation: the transcript only, with the input method recorded, and the transcript editable
by its author before it is saved.**

Three reasons, in order of weight:

1. **Consent.** A recording made on a site captures whoever is speaking nearby — a client's
   employee, another contractor's foreman, a passer-by. Nobody in this project has asked whether
   that is permitted, and it is not a question to answer by inference. Recorded here as an open
   matter, not resolved.
2. **Classification and residency.** An audio file is evidence in the same sense a photograph is: it
   would fall under `DataClassifications` and `ResidencyRequirements`, needing storage, retention,
   access control and a residency answer. That is a substantially larger commitment than text in a
   note field, for a benefit nobody has yet asked for.
3. **The dangerous outcome is a transcript nobody can identify as one.** Speech-to-text output reads
   exactly like typed text. If a transcription error later appears in a report, no one will be able
   to tell whether a supervisor wrote it or a model heard it.

**What approval would change.** One enum (`NoteInputMethod`: `Typed`, `Speech`) and one column,
`SiteVisits.NoteInputMethod`, Post-MVP. Nothing in release 1. And one rule, consistent with D-23:
machine-produced text is advisory until a human saves it — so the supervisor sees and may edit the
transcript before it becomes the note.

## 8. OQ-20 — The quality and near-duplicate thresholds

**The question.** What the quality threshold and the near-duplicate similarity threshold should be.
Both are project configuration, and both trade a saved model call against a missed observation.
*(Phase 2B)*

**The asymmetry that should decide it.** A false skip loses an observation, permanently and
invisibly — nobody ever learns what the photograph would have shown. A false analysis costs about
**$0.021** on Claude Opus 5, or about **$0.004** on Haiku 4.5 (estimates, from
`docs/02a-plan/22-image-derivative-architecture.md`). **The two errors are not comparable in cost, so
the thresholds should be conservative and should fail towards analysing.**

**Recommendation — starting values, to be replaced by measurement:**

| Setting | Recommended start | Why |
|---|---|---|
| **Near-duplicate** | 64-bit perceptual hash, **Hamming distance ≤ 5**, and only within the **same `CaptureBatchID` and the same `LocationID`** | Conservative: two shots of the same subject, seconds apart, typically differ by far less. Restricting it to one batch and one location means a genuinely similar wall in another building is never silently dropped. Never across visits, never across projects |
| **Quality** | **No absolute cutoff yet.** Skip on quality only when the photograph is below the project threshold **and** an eligible near-duplicate of the same subject scores higher | A blur measure is device- and scene-dependent; an absolute number chosen before any measurement would be quoted later as though it had been verified. A photograph that is the only record of its subject is analysed however poor it is |
| **Where they live** | `Projects`, as configuration | So that a project may loosen, tighten or switch off filtering without code (D-01) |
| **What makes it safe** | A **monthly count of skips by class** — `SkippedDuplicate`, `SkippedQuality`, `SkippedExcluded` | A threshold that is silently discarding work must be visible. Without the count, no threshold is safe at any value |

**What approval would change.** Two columns on `Projects`: `NearDuplicateHammingMax` (int, default 5)
and `QualityScoreMin` (decimal, nullable — **null means no absolute cutoff**, which is the
recommended pilot setting). Both authored in `tools/build_model.py`. The skip counts come from
`AnalysisEligibility`, which already exists, and belong in the weekly digest.

**The measurement that replaces this.** The six synthetic photographs of `CAP-GATE`, then the first
pilot month: a distribution of `QualityScore` and of pairwise Hamming distances within real batches.
**Until then, every number in this section is a starting point, not a setting.**

## 9. OQ-21 — Should a pending classification expire

**The question.** Whether a pending classification should expire into a reviewer task after some
number of days, or simply accumulate in a queue. *(Phase 2A)*

**One thing is not open.** `Pending` and `AIProposed` must **never** become `Confirmed` by the
passage of time. A timeout that promotes a proposal is an AI-written trusted value arriving by the
back door, and D-23 forbids it in every form. No number of days changes that.

**Recommendation: it accumulates, and it ages.**

- A photograph whose classification is still `Pending` or `AIProposed` after **7 days**
  (project-configurable) appears in the reviewer's **overdue classification** view and is counted in
  the **weekly monitoring digest** — scenario S12, already budgeted at three modules in
  `docs/02a-plan/23-operations-budget.md`, so this costs no additional operations.
- **It blocks nothing.** Under D-22 and D-23 an unclassified photograph is valid evidence and appears
  in a photographic report as an uncaptioned photograph. A queue that blocks submissions would
  reintroduce exactly the obligation the correction pass removed.
- **No new column on `Photos`.** The age is derived from `CapturedAt`, which already exists.

**One sub-question for the owner, because it is a policy and not a mechanism.** May an unclassified
photograph appear in a **client-facing** document? Recommended answer: **yes** for a daily or weekly
photographic report, which asserts only that the photograph was taken at that place on that date;
**no** for a completion certificate or anything asserting a quantity, because a quantity claim rests
on the confirmed activity. Owner to confirm.

**What approval would change.** One column on `Projects`: `PendingClassificationDays` (int, default
7). The view belongs in `03-views-and-slices.md`.

## 10. OQ-22 — Should the location prompt offer the nearest location by GPS

**The question.** Whether the location prompt, when it does appear, should offer the nearest location
by GPS rather than the last used. *(Phase 2A)*

**Recommendation: not now. Measure how often the prompt appears at all, first.**

Three reasons:

1. **The prompt may be rare.** Under D-22 it appears only when several active locations exist and
   none resolves from the project default or the last location used today. The entire point of the
   minimum-interaction pass was to make that uncommon — and **nobody has measured how uncommon.**
   Optimising a prompt that appears twice a month is the wrong work.
2. **A permission prompt is itself an interaction.** Asking for location access adds a question to a
   workflow whose stated goal is zero mandatory questions, and a supervisor who denies it once
   creates a support problem that outlives the visit.
3. **GPS can be confidently wrong.** Inside a building, between blocks of a school, or in a walled
   compound, the error is routinely larger than the distance between two locations in the same
   project. Location is a **trusted structured reference** (D-22) — not something to infer, and least
   of all something to infer from a signal that is wrong exactly where this company works.

**The revisit trigger, recorded now.** If the Phase 2B field measurement shows the location prompt
appearing on more than **one visit in five**, revisit under one rule: **GPS may order the list; it
may never select the value.** What the supervisor taps is what is stored.

**What approval would change.** Nothing. The cost of deferring is zero, and the decision improves
with one number that Phase 2B produces anyway.

---

## 11. What the owner is being asked to do

Answer eight questions. Nothing here needs a console, a credential, a device or a purchase — this is
the one piece of outstanding work that waits only on judgement.

```
OQ-15  Default capture mode        agreed / instead: ______________________
OQ-16  Summary with every share    agreed / instead: ______________________
OQ-17  Internal group              agreed / instead: ______________________
OQ-18  Sharing a draft             agreed / instead: ______________________
OQ-19  Voice: transcript only      agreed / instead: ______________________
OQ-20  Thresholds                  agreed / instead: ______________________
OQ-21  Pending classification      agreed / instead: ______________________
       — and: may an unclassified photograph appear in a client-facing
         photographic report?      yes / no
OQ-22  GPS location ordering       agreed / instead: ______________________
```

**These eight are independent of the two human gates.** The Admin Console entitlement check
(`16-admin-console-checklist-owner.md`) and the `CAP-GATE` device test
(`19-real-device-test-protocol.md` §4b) remain the only external things blocking Phase 2A, and
answering these questions neither replaces them nor waits for them — except for OQ-17, which is
deliberately routed into `CAP-GATE` rather than guessed at.

## 12. Status of this document

**Completed · Submitted for Owner Review.** No model file has been changed, no column has been added,
no check has been altered, and no recommendation in this document has been implemented. The
validation suite stands at **240 of 240 across 13 suites**, unchanged by this document.
