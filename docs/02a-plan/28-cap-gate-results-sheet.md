# CAP-GATE Results Sheet

**Document ID:** AH-SYS-P2A-028 · **Revision:** 1 · **Date:** 2026-09-12
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
| **C-4** | **Speed against WhatsApp** | Median ≤ baseline + 40 s **and** slowest ≤ baseline + 75 s **and** the supervisors' own verdict is yes | Either threshold missed, or a supervisor says they would not use it | **Blocking on the verdict**, finding on the seconds. A number cannot overrule the people who must use it |
| **C-5** | **Storage use and safe cleanup** | Free space returns to within 10 MB of the start, and every remaining copy is accounted for by the census table | Storage climbs run after run, or a copy exists that nobody owns | **Finding**, unless it grows without limit, which is **blocking** |
| **C-6** | **Upload confirmed before cleanup** | No local original is deleted before its upload is confirmed, under **any** interruption | One deletion of one unconfirmed file, once | **Blocking, absolutely.** An application that deletes evidence it has not delivered is worse than none |
| **C-7** | **Revoked access and cached data** | Access ends without a reinstall; nothing cached stays readable after refresh; **queued evidence is never silently lost** | Cached rows stay readable, or queued evidence disappears without a record | **Blocking on silent loss.** The correct handling of a queued submission is `OQ-23`, still open |

**The overall gate:** every blocking criterion passes on **both** devices and **both** messaging
applications. **Twelve of sixteen is a fail**, not a majority.

## 3. What is recorded for every run

Per run, into the CSV: run identifier, device model, OS version, application and version, network
method, mode, start and end time in seconds, whether the picker reopened, files versus links, cards
received and their order, storage at S-0/S-1/S-2/S-3, the copy counts for the census, whether cleanup
followed confirmation, and free-text observations.

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
| Blocking criteria passed | C-1 ☐ C-2 ☐ C-3 ☐ C-4 ☐ C-6 ☐ C-7 ☐ |
| Findings recorded | ______ |
| **Overall** | **PASS / FAIL** |
| Signature | ______________________ |

**A `FAIL` is a legitimate result and changes the capture platform, not the requirements.** The data
model, Drive security, orchestration, AI controls, approvals and audit rules are defined independently
of the capture interface, which is exactly why this is survivable.

## 5. Status

**Completed · Not executed.** No test has been run, no platform exists, and every figure in the CSV
is blank. **A results sheet is not a result.**
