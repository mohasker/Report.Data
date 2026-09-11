# Field Workflow, Tap Count and Multi-Photograph Capture

**Document ID:** AH-SYS-P2A-013 · **Revision:** 3 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Target not yet measured**
**Revision 3** applies the capture-once correction (D-16 to D-21). The workflow specification is
[`24-capture-once-workflow.md`](24-capture-once-workflow.md); this document is the tap arithmetic
that follows from it.
**Measurement protocol:** [`19-real-device-test-protocol.md`](19-real-device-test-protocol.md)

> **Target: normal visit submission in no more than 75 seconds, excluding the physical time required
> to position and take photographs.**
>
> This is a **design target derived from a tap count, not a validated result.** It will not be
> described as achieved before the real-device protocol has been executed and its median, 90th
> percentile, failures, user mistakes and synchronisation times recorded.

> Nothing has been built and nothing has been timed. The tap counts below are the design; the
> seconds are arithmetic on those taps. Both are replaced by measurement in Phase 2B, and the design
> changes if the measurement disagrees.

---

## 1. What "a normal visit" means

The commonest case, from the synthetic fixtures and the company's own reporting pattern:

| | |
|---|---|
| One location | Block A of a project the supervisor is already assigned to |
| One or two activities | e.g. mowing, plus weeding |
| Four to six photographs | Before, during, after, plus one observation |
| **No typed description** | Optional in every normal case (D-18). The photographs are the submission |
| One share to the contractor group | The same files, through the native share sheet |
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
| 10 | Stage tagging | **0–2** | **AI Reviewed Share:** the proposed stage and caption are already in place; a tap only to correct one. **Quick Share:** pre-tagged from the activity's default stages (Before / During / After in order) |
| 11 | Description | **0** | **Optional (D-18).** A normal photographic submission needs none. `0–1` only if the supervisor chooses to add a site note |
| 12 | **Submit** | **1** | |
| 13 | Confirm | **1** | A deliberate second tap, because submission locks the record |
| 14 | **Share to the contractor group** | **1–2** | One action opens the native share sheet with **the same stored files already attached**. The supervisor picks the group. **No re-selection of images (CAP-01)** |
| | **Total** | **16–21 taps**, of which **6 are shutter presses** | |

**Ten to fifteen interface taps plus six shutter presses.** At roughly three seconds per interface
tap, the interface portion is **30–45 seconds**. Adding the shutter presses themselves — but *not*
the physical time to walk to the subject, position the phone and wait for focus — gives the **75-second
target**, and the target now includes the group share, which today is a separate act of re-selecting
and re-sending the same photographs in a messaging application. Positioning time varies with the
site, not the software, which is why it sits outside the measured figure.

### Quick Share and AI Reviewed Share

| | Quick Share | AI Reviewed Share |
|---|---|---|
| Sequence | capture → store → native share | capture → store → AI proposal → confirm → native share |
| Steps 10 and 11 | after the share, asynchronously | before the share |
| Extra wait for the supervisor | **none** | the analysis round trip |
| Taps | **12–15** | **16–21** |
| Use when | the group must receive the evidence immediately | a reviewed professional caption is wanted first |

**Both capture the photographs exactly once.** The difference is only whether the AI proposal is
waited for. Neither re-opens the camera and neither re-selects a file.

### What makes it short

| Decision | Taps saved |
|---|---|
| Project pre-filled from the assignment or last use | 2 |
| Date and identity never typed | 4+ |
| Location sorted by display order, recent first | 1–2 |
| Activity list pre-filtered to the project's permitted set | 2–4 |
| Quantity field hidden unless the rule requires it | 2 |
| Unit derived from the rule, never chosen | 2 |
| Evidence stage pre-tagged in capture order, or proposed by analysis | 4–6 |
| Camera stays open between shots | 5 per visit at six photographs |
| **Description never required (D-18)** | 1–3 |
| **The share re-uses the stored files (CAP-01)** | **6–8** — the whole of today's second selection |

Without these the same visit is roughly **35 taps** and two to three minutes — which is slower than
sending photographs to a messaging group, and that is how a field system dies (R-06).

### What the supervisor never does

Type a date · type their own name · choose a unit · type a project or location name · tap through a
menu tree · wait for a round trip between photographs · fill a field the rule does not require ·
**write a description of work the photographs already show** · **select, attach or upload the same
photographs a second time to send them to the contractor group (CAP-01)**.

### The second capture that this correction removes

Today a supervisor photographs the work, then opens a messaging application and selects the same
photographs again to send them to the main-contractor group. That second selection is six to eight
taps, a scroll through a gallery, and a real risk of sending the wrong image or missing one. It is
also where the company's evidence currently ends up: in a chat thread rather than in a controlled
store. **Capture once, use twice removes that second selection entirely** — which is the single
largest usability gain in the design, and the reason the share belongs inside the application rather
than beside it.

## 3. Multi-photograph capture — three methods, one recommendation

This is the single most important interaction in the app, and the platform's behaviour here is
**unverified**. So all three methods are specified, with the trade-offs, and the choice is confirmed
by measurement in Phase 2B.

### Method A — child rows with a "capture again" action *(first test candidate, not the production decision)*

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

**Decision rule:** build Method A as the first test candidate. Measure it on the full device matrix
in [`19-real-device-test-protocol.md`](19-real-device-test-protocol.md) §4, which records taps,
whether the camera reopens, time per additional photograph, camera reliability, stage classification,
accidental duplicates, offline behaviour, image re-encoding and failed-sync recovery. **If Method A
misses the target, measure Method B on the same matrix and compare on M-1, M-3 and M-9 before
deciding** — Method B trades a faster capture loop for a more complex failure mode, and that trade
is decided by numbers, not by impression.

## 3b. The share itself — one action, no second selection

| Rule | |
|---|---|
| What is shared | The stored image files themselves, plus a formatted text summary |
| How | **One native operating-system share action.** The supervisor chooses the existing group in the share sheet |
| A public Drive link | **Never created and never required** |
| Re-selecting the images | **Never.** A retry re-uses the stored evidence (`ShareAttemptCount`) |
| What is recorded | `ShareStatus`, `SharedAt`, `ShareAttemptCount` |
| The destination | A **label** in project configuration — never a telephone number or invitation link |
| Forbidden | WhatsApp Web automation, group scraping, any unofficial messaging automation |

**An honest limit.** The application can record that the share sheet was opened and that the
supervisor said it completed. It cannot observe delivery inside the messaging application, and no
document in this repository claims otherwise.

**This is unverified on every platform.** Whether AppSheet can hand several actual image files and
formatted text to the share sheet is `CAP-GATE`, tested in
[`19-real-device-test-protocol.md`](19-real-device-test-protocol.md). If it cannot, no
duplicate-upload workaround is built — the capture-platform comparison runs instead.

## 4. What happens when the supervisor is offline

Identical. Every step above is local: the project list, locations and activity rules are already on
the device, the camera is local, and the submit queues. The only difference is that the validation
webhook fires later, when the device syncs.

This is why the completeness rules run **on the device** rather than only on the server (C-07): a
supervisor who submits offline and fails validation an hour later has usually left the site, and the
evidence gap becomes a second visit.

**The share is the exception.** A native share to a messaging group needs connectivity. Offline, the
visit is captured and queued; the share is offered again when the device reconnects, **from the
stored files**, without re-capture. Whether the platform can hold and re-offer that share is one of
the fifteen `CAP-GATE` conditions.

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
| Median time to submit, excluding photograph positioning | Phase 2B | **≤ 75 seconds** |
| 90th percentile time | Phase 2B | ≤ 110 seconds |
| Time to submit offline | Phase 2B | No worse than online |
| Taps actually used, counted by observation | Phase 2B | Within the 9–13 range |
| Failures and user mistakes | Phase 2B | Recorded; any evidence loss is blocking |
| Synchronisation time | Phase 2B | Recorded |
| First use without training | Phase 2B | Completes unaided; every hesitation noted |
| Reviewer time for a clean visit | Phase 2B | ≤ 30 seconds |
| **Times the supervisor selects the images** | **Phase 2A device test** | **Exactly 1 (CAP-01). More than one fails acceptance** |
| Native share of 6 files with a formatted summary | Phase 2A device test | Attached as files, in order, both platforms |
| AI proposal accepted without correction | Phase 2B | Recorded; a low rate means the prompt is wrong, not the supervisor |

**If the measurement misses, the form is simplified before the phase closes.** The target is an
acceptance criterion, not an aspiration — because a field app that is slower than the habit it
replaces will not be used, and everything downstream depends on evidence arriving.
