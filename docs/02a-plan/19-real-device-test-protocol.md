# Real-Device Test Protocol

**Document ID:** AH-SYS-P2A-019 · **Revision:** 2 · **Date:** 2026-09-11
**Status:** Completed · **Not executed** — no device, no app, no supervisor
**Supersedes the measurement sections of:** `05-offline-test-plan.md`, `13-field-workflow-and-taps.md`
**Revision 2** adds §4b, the `CAP-GATE` native-share test — the pass/fail requirement the
owner set on 2026-09-11. It is the most consequential section in this protocol: a failure
there changes the capture platform, not the form.

> **The target is a design target, not a validated result.** Recorded as the owner specified:
>
> **Target: normal visit submission in no more than 75 seconds, excluding the physical time required
> to position and take photographs.**
>
> No claim that the target is achieved will be made before this protocol has been executed and its
> results recorded — including the failures.

---

## 1. What is being measured

**In the measured time:** opening the app, selecting project and location, choosing activities,
entering a quantity where required, opening the camera, tagging evidence stages or confirming the
AI proposal, submitting, confirming, **and completing the native share to the contractor group**.

A typed description is **not** in the measured flow: it is optional for a normal photographic
submission (D-18). If a supervisor chooses to add a site note, that run is recorded separately.

**Excluded from the measured time:** walking to the subject, positioning the phone, waiting for
focus, the physical act of framing and taking each photograph. These vary with the site, not the
software, and including them would make the software look slower or faster depending on how tidy the
site was that day.

**Recorded separately, not excluded:** time per additional photograph within the capture loop — the
interface cost of taking a sixth photograph rather than a fifth is exactly what decides between
capture methods.

## 2. Devices and conditions — the full matrix

Every cell is measured. There is no "representative device"; the oldest handset is where field apps
fail.

| Condition | Oldest intended Android | iPhone |
|---|---|---|
| Normal connection | ✓ | ✓ |
| Weak connection (one or two bars, fluctuating) | ✓ | ✓ |
| Offline capture, later synchronisation | ✓ | ✓ |

| Visit shape | Both devices, all three connection states |
|---|---|
| **One activity, six photographs** | ✓ |
| **Multiple activities in one visit** (2 activities, 3 photographs each) | ✓ |

**12 device × connection × shape combinations**, each repeated enough times to produce a median and
a 90th percentile — **at least 5 runs per cell, 60 runs total.** Fewer runs produce a number without
a distribution, which is worse than no number.

## 3. What is recorded for every run

| Metric | Why |
|---|---|
| **Median time to submit** | The typical experience |
| **90th percentile time** | The experience people complain about and remember |
| **Failures** | Submission lost, photograph missing, app crash, sync never completed |
| **User mistakes** | Wrong location, wrong activity, forgotten caption, accidental double submission — **a mistake the interface invites is a design defect, not user error** |
| **Synchronisation time** | Submission to server-side acknowledgement |
| Taps actually used | Against the 9–13 budget in `13-field-workflow-and-taps.md` |
| Device model and OS version | The numbers mean nothing without it |
| Battery and storage state | A nearly full device behaves differently |

## 4. Multi-photograph capture — Method A vs Method B

Method A (child rows with "capture again") is the **first test candidate, not the production
decision**. Both methods are measured on the same matrix before choosing.

| # | Measurement | Method A | Method B | Decides |
|---|---|---|---|---|
| M-1 | Number of taps for six photographs | | | Direct comparison |
| M-2 | **Does the camera reopen between photographs?** | | | The single biggest factor in perceived speed |
| M-3 | **Time per additional photograph** (2nd through 6th) | | | Whether the loop degrades as it goes |
| M-4 | Does the camera stay open reliably, or drop out intermittently? | | | Intermittent is worse than never |
| M-5 | Before / during / after classification correct without correction | | | Whether pre-tagging works or creates rework |
| M-6 | **Accidental duplicate submissions** | | | A double-tap that creates two visits is a data-integrity problem |
| M-7 | Offline behaviour: do all six survive a queued submission? | | | Evidence loss is unacceptable at any speed |
| M-8 | **Image quality and re-encoding** — stored file vs camera file | | | The C-02 / D-13 question |
| M-9 | Failed-sync recovery: does a partial sync resume, or duplicate? | | | Determines whether idempotency works in practice |

**Decision rule:** if Method A's median submission exceeds 75 seconds, or M-2 shows the camera
reopening each time, or M-3 shows time per photograph rising, measure Method B on the same matrix
and compare. **Do not switch on impression** — switch on M-1, M-3 and M-9 together, because
Method B trades a faster loop for a more complex failure mode.

## 4b. CAP-GATE — the native share test *(pass/fail, blocking)*

**The question:** can the capture platform reliably share multiple actual image files and formatted
text through the native share sheet to an **existing** WhatsApp or WhatsApp Business group, on iOS
and Android?

**The acceptance rule, before anything else is measured:**

> **CAP-01 — the workflow fails acceptance if the supervisor must select or upload the images a
> second time.**

### The fifteen conditions

| # | Condition | Recorded | Pass |
|---|---|---|---|
| 1 | One photograph | Attached as a file? | File, not a link |
| 2 | Six photographs | All six attached? | All six, none dropped |
| 3 | Portrait and landscape mixed | Orientation preserved? | Preserved, not rotated |
| 4 | Image order | Order as captured? | Matches `CaptureSequence` |
| 5 | Formatted summary | Text arrives with the images? | Text present and legible, Arabic included |
| 6 | Standard WhatsApp | Group reachable from the share sheet? | Existing group appears |
| 7 | WhatsApp Business | Same | Existing group appears |
| 8 | Normal connection | Time to complete | Recorded |
| 9 | Weak connection | Behaviour and time | No silent loss |
| 10 | Offline capture, then synchronisation | Share offered again on reconnect? | Offered, **from stored files** |
| 11 | Images attached, or only links | Which one | **Files. A link-only share is a FAIL** |
| 12 | **Must the user select the images again?** | Yes / no | **No. Yes is a FAIL — this is CAP-01** |
| 13 | Is a public Drive link created? | Yes / no | **No. Yes is a FAIL** |
| 14 | Temporary files left on the device | What, where, how long | Recorded; anything persistent is a finding |
| 15 | Failed or cancelled share recovery | Can it be retried without re-capture? | Retry from stored evidence |

Each condition is run on **both** devices in the §2 matrix, in **both** operating modes (Quick Share
and AI Reviewed Share). Screenshots of the share sheet and of the received group message are part of
the record.

### What a failure means

| Result | Action |
|---|---|
| All fifteen pass on both platforms | **AppSheet is confirmed as the capture platform.** Proceed |
| Condition 12 fails (second selection required) | **Blocking. Do not implement a duplicate-upload workaround.** Produce the capture-platform decision comparison |
| Condition 11 or 13 fails (link instead of files, or a public link) | **Blocking**, for the same reason: it breaks both the evidence-control rule and the capture-once rule |
| Conditions 3, 4, 5, 9, 14 fail | Findings, not blockers. Record, then decide whether they are acceptable |
| Condition 10 or 15 fails | **Blocking for field use.** A supervisor who loses a share after leaving the site re-visits, and the habit dies |

### The comparison that runs if it fails

1. AppSheet with a proven native-share method.
2. A lightweight custom PWA or mobile field application using supported native file sharing.
3. Any other official, policy-compliant approach.

**Forbidden in all three:** unofficial WhatsApp Web automation, group scraping, and any publicly
accessible Drive link.

**What does not change if the platform does:** the canonical data model, Drive security, Make
orchestration, Claude controls, approval rules and audit requirements. They are defined independently
of the capture interface, which is the whole reason this is a survivable failure.

## 5. Image fidelity

| # | Test | Records |
|---|---|---|
| IMG-1 | Capture through the app; separately photograph the same scene with the phone camera; compare | Byte size, pixel dimensions, whether the stored file is a re-encoding |
| IMG-2 | Repeat at the highest available upload-quality setting | Whether the setting changes what is stored |
| IMG-3 | Inspect stored metadata | Capture time preserved? Location preserved or stripped? |
| IMG-4 | Maximum-resolution photograph | Is it downscaled regardless of the setting? |

**`IsOriginalDeviceImageVerified` stays FALSE for every photograph until IMG-1 proves otherwise, per
platform.** If the stored file is a re-encoding, the approved D-13 wording stands unchanged and no
claim about "the original device image" is ever made.

## 6. Segregation on a real device

Security is tested before any real person is added, on synthetic accounts.

| # | Test | Pass |
|---|---|---|
| SEG-D1 | Single-project user searches for another project's location by name | Nothing found |
| SEG-D2 | Single-project user opens a deep link to another project's visit | Refused |
| SEG-D3 | Multi-project user completes a visit on each project in one session | Nothing crosses |
| SEG-D4 | Unassigned account signs in and explores every view | No project data at all |
| SEG-D5 | Expired-assignment account signs in | No access, despite the row existing |
| SEG-D6 | Single-project user calls the API for another project's records | Refused |

SEG-D6 matters most: view filtering can look correct while the delivered data set is not filtered at
all.

## 7. Language and usability

| # | Test | Records |
|---|---|---|
| LNG-D1 | Complete a visit entirely in Arabic | Layout, wrapping, direction, anything unreadable |
| LNG-D2 | Type an Arabic description and caption | Stored exactly, no transliteration, no mangling |
| LNG-D3 | Arabic description with an English activity name | Mixed-direction rendering |
| USE-1 | Outdoor legibility in direct sunlight | Pass / fail, with the screen brightness noted |
| USE-2 | Operation with work gloves on | Pass / fail |
| USE-3 | **First use without training** — a supervisor who has never seen the app completes a visit unaided | Where they hesitate, what they get wrong, what they ask |

USE-3 produces the most useful output of the whole protocol. Every hesitation is a design defect
with a location.

## 8. Reviewer side

| # | Test | Target |
|---|---|---|
| REV-1 | Time to review and approve a clean visit | ≤ 30 seconds |
| REV-2 | Time to return a visit for correction with a reason | ≤ 60 seconds |
| REV-3 | Does the queue exclude the reviewer's own submissions? | Yes |

## 9. Pass, fail, and what happens next

| Outcome | Action |
|---|---|
| Median ≤ 75 s and 90th percentile ≤ 110 s on both devices | Target met. **Record it, with the distribution, not as a single number** |
| Median > 75 s, capture is the cause | Measure Method B, compare on M-1, M-3, M-9, then decide |
| Median > 75 s, the form is the cause | Simplify the form and re-measure **before the phase closes** |
| Any evidence loss, in any run | **Blocking.** Nothing proceeds until the cause is found |
| Photographs re-encoded | Not blocking. Record it and keep the verification flag FALSE |
| Segregation failure | **Blocking, and treated as a security incident** even on synthetic data |
| **CAP-01 fails: a second image selection is required** | **Blocking.** No workaround. The capture-platform comparison runs |
| **A link-only share, or a public link** | **Blocking**, for evidence control as well as usability |
| A share cannot be retried after failure without re-capture | **Blocking for field use** |

## 10. Recording

One row per run, in a results sheet: date, device, OS version, connection state, visit shape,
capture method, operating mode (Quick Share or AI Reviewed Share), elapsed time, taps, **times the
images were selected**, share result, failures, mistakes, sync time, observations.

**Times the images were selected** is the one column that cannot be argued about afterwards. It is
either 1 or it is a failure.

**Failures are recorded as prominently as successes.** A protocol whose results contain only passes
has not been executed honestly, and the numbers that matter here are the ones nobody wanted.
