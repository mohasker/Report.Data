# Offline and Field Test Plan

**Document ID:** AH-SYS-P2A-005 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · **Awaiting devices and supervisors (EF-05)** · **Not executed**
**Profiles:** `../01-data-foundation/19-user-and-device-profiles.md`

> **Nothing in this plan has been executed.** Offline behaviour is entirely unknown: the platform's
> documentation describes the platform, not the company's phones. No offline claim will be made
> before these tests are run and recorded (A-15).

---

## 1. What must be true before testing

| Prerequisite | Status |
|---|---|
| Real devices, both platforms, including the oldest handset still in service | **Pending (EF-05)** |
| Real supervisors willing to be observed | **Pending (EF-05)** |
| App built against synthetic data only | Phase 2B |
| Segregation tests already passed on synthetic accounts | Phase 2B gate 1 |
| A site with genuinely poor coverage — a plant room or basement, not airplane mode alone | To arrange |

Airplane mode is not a substitute for bad coverage. The interesting failures happen on a weak,
flapping connection, not a cleanly absent one.

## 2. Test matrix

| # | Test | Profile | Method | Pass criterion |
|---|---|---|---|---|
| **OFF-01** | Cold start offline | P-3 | Force-close, disable data, open the app | App opens with assigned projects and locations available |
| **OFF-02** | Complete a visit offline | P-3 | Full visit, 3 activities, 6 photographs, no connection | All saved locally; nothing lost |
| **OFF-03** | Extended offline | P-3 | Keep the visit queued for 4+ hours, use other apps | Queue intact; no silent discard |
| **OFF-04** | Restart mid-queue | P-3 | Restart the phone with a visit queued | Queue survives the restart |
| **OFF-05** | Sync on reconnection | P-3 | Reconnect | Visit, activities and **every** photograph arrive, correctly related |
| **OFF-06** | Weak, flapping connection | P-3 | Sync where signal comes and goes | No partial visit; no duplicate rows |
| **OFF-07** | Queue size limit | P-3 | Two full visits, 20 photographs, offline | Either both sync, or the app says clearly it cannot hold more |
| **OFF-08** | Low storage | P-2 | Device near full | Clear message; no silent photograph loss |
| **OFF-09** | Battery interruption | P-2 | Device dies with a queue pending | Queue survives to the next charge |
| **OFF-10** | Two devices, one user | P-5 | Same account on two phones, offline edits to different visits | No lost update; conflicts surfaced, never auto-merged |

## 3. Image fidelity — the C-02 question

| # | Test | Profile | Method | Records |
|---|---|---|---|---|
| **IMG-01** | iOS fidelity | P-1 | Capture through the app; separately save the same scene to the camera roll; compare | Byte size, dimensions, whether the stored file is a re-encoding |
| **IMG-02** | Android fidelity | P-2 | As above on a mid-range handset | Same |
| **IMG-03** | Upload quality setting | P-1, P-2 | Repeat at the highest available setting | Does the setting change what is stored? |
| **IMG-04** | Metadata | P-1, P-2 | Inspect the stored file | Is capture time preserved? Is location metadata preserved or stripped? |
| **IMG-05** | Large photograph | P-2 | Maximum camera resolution | Does the platform downscale regardless? |

**The outcome decides the wording, not the other way round.** If the stored file is a re-encoding,
the approved D-13 definition stands as written — write-once from first receipt — and
`IsOriginalDeviceImageVerified` stays FALSE for every photograph. It is only set TRUE if these tests
prove no upstream re-encoding, and only for the platforms tested.

## 4. Segregation on a real device

| # | Test | Profile | Method | Pass criterion |
|---|---|---|---|---|
| **SEG-D1** | Single-project user | P-4 | Search for another project's location by name; open a deep link to another project's visit | Nothing found; deep link refused |
| **SEG-D2** | Multi-project switch | P-5 | Complete a visit on project A, then B, in one session | No record, location, template or photograph crosses |
| **SEG-D3** | Unassigned account | P-8 | Sign in and explore every view | No project data of any kind |
| **SEG-D4** | Expired assignment | P-9 | Sign in after the assignment end date | No access, despite the row existing |
| **SEG-D5** | API attempt | P-4 | Call the API for another project's records | Refused |

SEG-D5 matters most: view-level filtering can look correct while the underlying data set is not
filtered at all (P-04).

## 5. Language and usability

| # | Test | Profile | Records |
|---|---|---|---|
| **LNG-D1** | Arabic interface | P-7 | Complete a visit entirely in Arabic; check layout, wrapping and direction |
| **LNG-D2** | Arabic text entry | P-7 | Type a description and caption in Arabic; verify it is stored exactly |
| **LNG-D3** | Mixed text | P-7 | Arabic description with an English activity name; check rendering |
| **LNG-D4** | English interface | P-6 | Same flows |
| **USE-01** | **Time to complete a typical visit** | P-1, P-2 | Stopwatch, real supervisor, no coaching. **Compare against how long the current habit takes** |
| **USE-02** | Outdoor legibility | P-2 | Direct sunlight |
| **USE-03** | Gloved operation | P-2 | Work gloves on |
| **USE-04** | First use without training | P-4 | A supervisor who has never seen it completes a visit unaided; record where they hesitate |

**USE-01 is an acceptance criterion, not a nice-to-have.** If the app is slower than sending
photographs to a messaging group, the form is simplified before the phase closes. Adoption is the
largest single risk to the whole system (R-06).

## 5b. Offline and the contractor-group share

A native share to a messaging group **needs connectivity**. Offline, the capture, the storage and the
queued submission all work exactly as they do online; the share does not, and pretending otherwise
would be the kind of claim this repository exists to avoid.

| Condition | Expected | Blocking if it fails |
|---|---|---|
| Visit captured offline; photographs stored | Works, identical to online | **Yes** |
| Share attempted offline | Refused clearly, with a reason the supervisor can read | Yes |
| Share re-offered on reconnect, **from the stored files** | Offered in `PendingShare`, no re-capture, no re-selection | **Yes — this is CAP-01 under the hardest condition** |
| Photographs still intact after the reconnect | Byte-identical to what was stored | **Yes. Any evidence loss stops everything** |
| Share attempted on a weak connection | Completes, or fails recoverably. Never silently partial | Yes |

This is condition 10 of the fifteen in
[`19-real-device-test-protocol.md`](19-real-device-test-protocol.md) §4b, and it is the one most
likely to be missed by a test performed at a desk. **It must be executed on a site with genuinely
poor signal, not with aeroplane mode toggled in an office.**

## 6. Recording

For every test: date, device model and OS version, supervisor profile, network conditions, result,
and — where it failed — exactly what was observed. **Failures are recorded as prominently as
passes.** A test plan whose record contains only passes is not evidence, it is marketing.

The results become the offline-behaviour section of the field-user guide. Whatever the platform
actually does is what the guide will say it does.
