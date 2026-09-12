# CAP-GATE Results Sheet

**Document ID:** AH-SYS-P2A-028 · **Revision:** 2 · **Date:** 2026-09-12
**Status:** Completed · **Empty — not executed.** Every cell below is blank because no test has run
**Fill-in file:** [`cap-gate-results-sheet.csv`](cap-gate-results-sheet.csv)

---

## 1. The run matrix — 16 runs

| Axis | Values |
|---|---|
| Device | **iPhone**, **Android** |
| Messaging application | **Standard WhatsApp**, **WhatsApp Business** |
| Network | **Strong**, **Weak**, **Offline then synchronised** |
| Mode | **Quick Share** on every run; **AI Reviewed Share** on the four strong-network runs only |

2 devices × 2 applications × 3 network states = **12 Quick Share runs**, plus **4 AI Reviewed Share
runs** on strong network = **16 runs**. Each run captures and shares the same six numbered cards.

| Run | Device | Application | Network | Mode |
|---|---|---|---|---|
| R-01 | iPhone | Standard | Strong | Quick Share |
| R-02 | iPhone | Standard | Weak | Quick Share |
| R-03 | iPhone | Standard | Offline → sync | Quick Share |
| R-04 | iPhone | Business | Strong | Quick Share |
| R-05 | iPhone | Business | Weak | Quick Share |
| R-06 | iPhone | Business | Offline → sync | Quick Share |
| R-07 | Android | Standard | Strong | Quick Share |
| R-08 | Android | Standard | Weak | Quick Share |
| R-09 | Android | Standard | Offline → sync | Quick Share |
| R-10 | Android | Business | Strong | Quick Share |
| R-11 | Android | Business | Weak | Quick Share |
| R-12 | Android | Business | Offline → sync | Quick Share |
| R-13 | iPhone | Standard | Strong | AI Reviewed |
| R-14 | iPhone | Business | Strong | AI Reviewed |
| R-15 | Android | Standard | Strong | AI Reviewed |
| R-16 | Android | Business | Strong | AI Reviewed |

**Plus the baselines, which are not runs of the application:** `B-01` iPhone and `B-02` Android —
five WhatsApp postings each, per `19-real-device-test-protocol.md` §4c G-1. **Do the baselines
first**, before anyone has seen the prototype work.

**"Weak network" must be defined the same way every time**, or the numbers cannot be compared. Use
one method for the whole test and record which: the device's own network throttling, a single bar of
mobile signal in a known location, or a deliberately congested connection. **Record the method, not
just the word "weak".**

## 2. The seven pass/fail criteria

| # | Criterion | Passes when | Fails when | Severity |
|---|---|---|---|---|
| **C-1** | **No second image selection** | The supervisor selects or captures the six photographs **once**, and every subsequent step — share, retry, re-share, analysis, report — re-uses the stored files | The picker opens a second time, in any run, on any device | **Blocking — this is CAP-01.** No workaround is acceptable |
| **C-2** | **Actual attachments, not links** | Six image files arrive in the group | Any run delivers a link, a preview, or fewer than six files | **Blocking.** A link is not evidence delivery, and a public link is separately forbidden |
| **C-3** | **No missing or reordered evidence** | Cards 1–6 arrive, all six, in order, orientation preserved | Any card missing, out of order, or rotated | Missing: **blocking**. Reordered or rotated: **finding**, decided by the owner |
| **C-4** | **Speed against WhatsApp** *(owner's threshold, 2026-09-12)* | **Median foreground ≤ baseline + 20 s**, **p90 foreground ≤ baseline + 40 s**, **and both supervisors confirm the workflow is acceptable for daily use** | Either threshold missed, or either supervisor does not confirm | **Blocking, both parts.** The verdict stays blocking even when the numbers pass |
| **C-4b** | **Background synchronisation does not hold the supervisor** | The supervisor can leave the app, lock the phone or start the next visit while the upload continues | Synchronisation blocks further work | **Finding**, and the blocked time is re-counted as **foreground** in C-4, where it may turn a pass into a fail |
| **C-5** | **Storage use and safe cleanup** | Free space returns to within 10 MB of the start, and every remaining copy is accounted for by the census table | Storage climbs run after run, or a copy exists that nobody owns | **Finding**, unless it grows without limit, which is **blocking** |
| **C-6** | **Upload confirmed before cleanup** | No local original is deleted before its upload is confirmed, under **any** interruption | One deletion of one unconfirmed file, once | **Blocking, absolutely.** An application that deletes evidence it has not delivered is worse than none |
| **C-7** | **Revoked access and cached data** *(decision D-25)* | Access ends without a reinstall; nothing cached stays readable after refresh; evidence captured **before** revocation completes into **quarantine**; evidence captured after it, or with no provable capture time, is **refused**; **nothing is ever discarded**; the revoked user can no longer view, edit, delete, share or submit | Cached rows stay readable, queued evidence is discarded, post-revocation evidence is accepted, or a rejection is recorded without a reason | **Blocking.** `OQ-23` is closed by D-25; if the platform cannot enforce it, the files stay locally protected and `CAP-GATE` fails |

**The overall gate:** every blocking criterion passes on **both** devices and **both** messaging
applications. **Twelve of sixteen is a fail**, not a majority.

**Blocking: C-1, C-2, C-3 (missing evidence), C-4 (both the numbers and the verdict), C-6, C-7.**
Findings: C-3 reordering or rotation, C-4b, C-5.

## 3. What is recorded for every run

Per run, into the CSV: run identifier, device model, OS version, application and version, network
method, mode, **foreground seconds and background seconds separately**, whether synchronisation
blocked further work, whether the picker reopened, files versus links, cards received and their
order, storage at S-0/S-1/S-2/S-3, the copy counts for the census, whether cleanup followed
confirmation, the revocation and quarantine outcome, and free-text observations.

**Screenshots per run:** the share sheet, and the received group message. Two images, named
`R-01-sheet.png` and `R-01-received.png`. **The received message is the only proof that the files
arrived as files**, and it is the one screenshot that must never be skipped.

## 4. Signing off

| Field | |
|---|---|
| Test date | ______________________ |
| Devices used (model, OS) | ______________________ |
| Tester | ______________________ |
| Owner present for G-5 | Yes / No |
| Blocking criteria passed | C-1 ☐ C-2 ☐ C-3 ☐ C-4 numbers ☐ C-4 verdict ☐ C-6 ☐ C-7 ☐ |
| Supervisor 1 — acceptable for daily use? | Yes / No — verbatim: ______________________ |
| Supervisor 2 — acceptable for daily use? | Yes / No — verbatim: ______________________ |
| Findings recorded | ______ |
| **Overall** | **PASS / FAIL** |
| Signature | ______________________ |

**A `FAIL` is a legitimate result and changes the capture platform, not the requirements.** The data
model, Drive security, orchestration, AI controls, approvals and audit rules are defined independently
of the capture interface, which is exactly why this is survivable.

## 5. Status

**Completed · Not executed.** No test has been run, no platform exists, and every figure in the CSV
is blank. **A results sheet is not a result.**
