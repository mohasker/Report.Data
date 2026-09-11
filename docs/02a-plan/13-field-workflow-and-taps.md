# Field Workflow, Tap Count and Multi-Photograph Capture

**Document ID:** AH-SYS-P2A-013 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Target not yet measured on a device**
**Target:** a supervisor submits a normal visit with photographs in **about one minute**

> Every number below is a **design target derived from a tap count**, not a measurement. Nothing has
> been built and nothing has been timed. The Phase 2B field test measures the real figure with a
> real supervisor on a real phone, and the design changes if the measurement disagrees.

---

## 1. What "a normal visit" means

The commonest case, from the synthetic fixtures and the company's own reporting pattern:

| | |
|---|---|
| One location | Block A of a project the supervisor is already assigned to |
| One or two activities | e.g. mowing, plus weeding |
| Four to six photographs | Before, during, after, plus one observation |
| A short description | One line, often in Arabic |
| No snag | Snags are the exception, not the rule |

A visit with a snag, three activities and twenty photographs is a different job and will take longer.
The one-minute target is for the normal case, because that is the case that happens twenty times a
week.

## 2. The flow, tap by tap

| Step | Screen | Taps | Why it is that number |
|---|---|---|---|
| 1 | Open app → **New Visit** | **1** | The home screen is one large button plus three status tiles |
| 2 | Project | **0** | Pre-filled: the only assigned project, or the last one used today. A tap only if they are multi-project and switching |
| 3 | Location | **2** | Open the dropdown, tap the location. Sorted by `DisplayOrder`, and the last location used today is first |
| 4 | Date and supervisor | **0** | Today's date, signed-in identity. Editable only if wrong |
| 5 | Activity | **2** | Open, tap. The list is already filtered to what this project permits |
| 6 | Quantity | **0–2** | Shown **only** when the effective rule requires it; numeric keypad, no unit tap (the unit comes from the rule) |
| 7 | **Camera** | **1** | One tap opens the camera and keeps it open |
| 8 | Capture 6 photographs | **6** | One shutter tap each. The camera does not close between shots — see §3 |
| 9 | Done with photographs | **1** | Returns to the visit |
| 10 | Stage tagging | **0–2** | Pre-tagged from the activity's default stages (Before / During / After in order). A tap only to correct one |
| 11 | Description | **0–1** | Optional for most activities; one line if typed |
| 12 | **Submit** | **1** | |
| 13 | Confirm | **1** | A deliberate second tap, because submission locks the record |
| | **Total** | **15–19 taps**, of which **6 are shutter presses** | |

**Nine to thirteen interface taps plus six photographs.** At roughly three seconds per interface tap
and four seconds per photograph including aiming, that is **55–75 seconds** — which is where the
one-minute target comes from, and why it is a target rather than a promise.

### What makes it short

| Decision | Taps saved |
|---|---|
| Project pre-filled from the assignment or last use | 2 |
| Date and identity never typed | 4+ |
| Location sorted by display order, recent first | 1–2 |
| Activity list pre-filtered to the project's permitted set | 2–4 |
| Quantity field hidden unless the rule requires it | 2 |
| Unit derived from the rule, never chosen | 2 |
| Evidence stage pre-tagged in capture order | 4–6 |
| Camera stays open between shots | 5 per visit at six photographs |
| Description optional | 1 |

Without these the same visit is roughly **35 taps** and two to three minutes — which is slower than
sending photographs to a messaging group, and that is how a field system dies (R-06).

### What the supervisor never does

Type a date · type their own name · choose a unit · type a project or location name · tap through a
menu tree · wait for a round trip between photographs · fill a field the rule does not require.

## 3. Multi-photograph capture — three methods, one recommendation

This is the single most important interaction in the app, and the platform's behaviour here is
**unverified**. So all three methods are specified, with the trade-offs, and the choice is confirmed
by measurement in Phase 2B.

### Method A — child rows with a "capture again" action *(recommended to try first)*

Each photograph is a `Photos` row. After saving, an action re-opens the capture form for the same
activity, so the supervisor stays in a capture loop.

- **Strength:** correct by construction. One row per photograph, unlimited count, every field populated at capture time, no post-processing.
- **Weakness:** each photograph may involve a form save. If the platform makes that feel slow — a visible pause, or a sync round trip — the loop breaks and the target is missed.
- **Taps:** 1 to open, 1 shutter + 1 "another" per photograph, 1 to finish.
- **Verdict:** try first, because it is the honest data model. Measure it on the oldest Android handset in service, not the newest iPhone.

### Method B — fixed image columns, exploded into rows by automation

The activity form carries, say, eight image columns. Automation creates one `Photos` row per
populated column and clears the staging columns.

- **Strength:** fastest possible capture — no save between shots, no round trip.
- **Weakness:** a fixed maximum per activity; automation must run before review, so a photograph exists in a staging column for a short time; a failure mid-explosion needs careful idempotency.
- **Taps:** 1 to open, 1 per photograph, 1 to finish.
- **Verdict:** the fallback if Method A measures too slow. It costs one more moving part and Make operations.

### Method C — device gallery multi-select

The supervisor takes photographs with the phone camera as they work, then selects several at the end.

- **Strength:** matches the existing habit exactly, and the camera app is always faster than any embedded one.
- **Weakness:** weakens evidence freshness — a gallery photograph could be from any day; it needs the old-photograph warning and reviewer attention. Multi-select into separate rows may not be supported natively at all.
- **Verdict:** only if the owner's policy permits gallery upload (OQ-05), and only alongside Method A.

**Decision rule:** build Method A. Measure it at the Phase 2B gate with six photographs on the oldest
handset. If a visit exceeds 90 seconds because of capture, switch to Method B and measure again.
Record both measurements either way.

## 4. What happens when the supervisor is offline

Identical. Every step above is local: the project list, locations and activity rules are already on
the device, the camera is local, and the submit queues. The only difference is that the validation
webhook fires later, when the device syncs.

This is why the completeness rules run **on the device** rather than only on the server (C-07): a
supervisor who submits offline and fails validation an hour later has usually left the site, and the
evidence gap becomes a second visit.

## 5. Review is fast too, or reviewing does not happen

| Reviewer action | Taps |
|---|---|
| Open the queue | 1 |
| Open a visit | 1 |
| Approve every photograph at once, having scrolled the gallery | 1 |
| Approve the visit | 1 |
| **Total for a clean visit** | **4** |

Rejecting anything costs more, deliberately: a rejection requires a typed reason, because a rejection
without a reason is just an obstacle to the supervisor.

## 6. How this gets verified

| Measurement | Where | Pass |
|---|---|---|
| Time to submit a normal visit, real supervisor, oldest handset | Phase 2B gate 6 | **≤ 90 seconds**, target ~60 |
| Time to submit offline | Phase 2B | No worse than online |
| Taps actually used, counted by observation | Phase 2B | Within the range above |
| First use without training | Phase 2B | Completes unaided; note where they hesitate |
| Reviewer time for a clean visit | Phase 2B | ≤ 30 seconds |

**If the measurement misses, the form is simplified before the phase closes.** The target is an
acceptance criterion, not an aspiration — because a field app that is slower than the habit it
replaces will not be used, and everything downstream depends on evidence arriving.
