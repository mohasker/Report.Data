# Phase 2B Platform Test Scripts — Segregation, Evidence Rules, Configurability

**Document ID:** AH-SYS-P2A-026 · **Revision:** 2 · **Date:** 2026-09-12
**Status:** Completed · **Not executed** — no platform exists, and none is authorised
**Companion to:** `19-real-device-test-protocol.md` (device and share), `05-offline-test-plan.md` (offline)

---

## 1. Why these are written before the platform exists

The 257 local checks prove that **the model is right**. They cannot prove that a built system
**enforces** the model, because nothing has been built. That gap is the whole of Phase 2B, and it is
the gap where a design quietly becomes a different design.

These scripts are written now, deliberately, **before any platform is chosen or connected**. A test
written after the platform exists is written against what the platform happens to do; a test written
before it is written against what the system is required to do. When the two disagree — and on at
least one point they will — the disagreement has to be visible as a failure, not absorbed as a
setting.

**Consequently every script here is platform-neutral.** No script names AppSheet, a slice, a view,
a scenario or a webhook. Each one names a role, an input and an observable outcome, so the same
script runs unchanged whichever capture platform the entitlement check and `CAP-GATE` produce.

**Nothing in this document authorises any of it to be run.** Execution needs a platform, and a
platform needs the owner's separate written authorisation. Until then this is a specification of
evidence, not evidence.

## 2. What each suite proves that the local suite cannot

| Local suite | Proves today | The Phase 2B script proves |
|---|---|---|
| `test_segregation.py` — SEG-01 … SEG-12 | The **model** grants no cross-project visibility | The **running system** returns no cross-project row, to a real signed-in identity, through every path it offers — list, search, filter, export, report, notification and link |
| `test_evidence_rules.py` — EVD-01 … EVD-14 | The **rule engine** computes the right effective rule and the right refusal | The **running system** actually refuses, at the moment of submission, with the message the rule produced — and cannot be talked out of it by retry, offline replay or a second device |
| `test_configurability.py` — CFG-01 … CFG-12 | No project, client or contract identifier is compiled into any logic | A **fourth project** can be added as data by an administrator, with **no developer involvement**, and works completely on first use |

**The distinction that matters:** a local check reads a data structure; a platform test drives the
system as a person and observes what the person sees. A system can satisfy every local check and
still leak a photograph through an export button nobody modelled.

## 3. Preconditions — all of them, before any script runs

| # | Precondition | Why it is not optional |
|---|---|---|
| 1 | The Admin Console entitlement check is complete (`16-admin-console-checklist-owner.md`) | Whether **security filters** exist at all decides whether the segregation suite can pass by design or only by view |
| 2 | `CAP-GATE` has been executed (`19-real-device-test-protocol.md` §4b) | A failure there changes the capture platform, and these scripts would be re-run on a different one |
| 3 | The synthetic seed is loaded, unchanged (`10-synthetic-data-loading.md`) | Every expected result below is stated against the seed's own identifiers |
| 4 | **No real project, client, photograph, contact or person is present** | Phase 2B is synthetic. A real row in a test fixture is a data-protection incident, not a shortcut |
| 5 | Test identities are real sign-ins for the synthetic users, not impersonation | A segregation test that bypasses authentication proves nothing about authentication |
| 6 | Each script's result is recorded before the next is run | A suite re-run after a mid-suite fix records the fix, not the failure. The failure is the finding |

**The fixture** is the existing synthetic seed: three projects — `PRJ-0001` landscape and irrigation,
`PRJ-0002` suspended ceiling and civil, `PRJ-0003` irrigation rehabilitation, the last with AI
analysis disabled by a residency rule — and thirteen users, of whom `USR-0011` has **no assignment**
and `USR-0012` has an **expired** one.

---

## 4. Segregation — `P2B-SEG-01` … `P2B-SEG-14`

**The standing rule for this suite: a leak is a stop, not a defect to schedule.** Any script in §4
that fails halts Phase 2B until the cause is understood. No script here has a "minor" outcome.

| Script | Sign in as | Do this | Pass only if | Local check |
|---|---|---|---|---|
| **P2B-SEG-01** | `USR-0005` (supervisor, one project) | Open every list, view and search the application offers | Not one row from a project other than the assigned one is visible anywhere | SEG-01 |
| **P2B-SEG-02** | `USR-0011` (no assignment) | Sign in and attempt to reach any operational screen | The account can sign in and **sees nothing at all** — no project, no visit, no photograph. An empty system, not an error page | SEG-02 |
| **P2B-SEG-03** | `USR-0012` (assignment ended 2026-02-28) | Open the project that was assigned until February | Nothing is visible. **An expired assignment grants exactly what no assignment grants** | SEG-03 |
| **P2B-SEG-04** | `USR-0007` (two projects) | Open every list | `PRJ-0002` and `PRJ-0003` are both fully visible, `PRJ-0001` is not visible at all | SEG-04 |
| **P2B-SEG-05** | `USR-0006` | Attempt to open a photograph belonging to another project **by its direct identifier or link**, not through the interface | Refused. A row hidden from a list but reachable by its key is not segregated, it is merely unlisted | SEG-05 |
| **P2B-SEG-06** | every field role | Attempt to reach any financial table — contracts, BOQ items, invoice requests, invoice lines | No financial row is reachable by any field identity through any path, including search and export | SEG-06 |
| **P2B-SEG-07** | `USR-0004` (project manager) | Begin a release or share to a client recipient | Only the project's own authorised contacts are offered. **No recipient from another project appears in any picker** | SEG-07 |
| **P2B-SEG-08** | `USR-0005` | Attempt to select document template `TPL-0003`, which belongs to `PRJ-0001` | Not offered, and not accepted if supplied directly | SEG-08 |
| **P2B-SEG-09** | `USR-0007` | Trigger anything that issues a document number | Only the project's own series is used. A project-scoped series is never borrowed by another project | SEG-09 |
| **P2B-SEG-10** | any | Export, download or print from every screen that offers it | **Every export obeys the same filter as the screen it came from.** Export is the most common way segregation is lost | SEG-10 |
| **P2B-SEG-11** | `USR-0005`, `USR-0006` | Compare two locations that share a location **code** across projects | They remain distinct records. A reused code never merges two projects' locations | SEG-11 |
| **P2B-SEG-12** | `USR-0007` | Work on `PRJ-0003`, where a residency rule disables AI | **No analysis runs, and no proposal appears**, on that project only. `PRJ-0002` is unaffected in the same session | SEG-12 |
| **P2B-SEG-13** | any assigned user | Receive a notification or alert produced by another project's activity | No notification body, subject, count or preview discloses a row the recipient may not read. **A notification is a read path** | *new — no local equivalent* |
| **P2B-SEG-14** | administrator | Remove a user's assignment while that user is signed in and working | Access to that project ends without a re-install, and **already-cached rows do not remain readable** after the session refreshes | *new — no local equivalent* |

**Two of these fourteen have no local counterpart, by necessity.** Nothing in a data model can
describe what a notification discloses or what a device has cached. They exist only at Phase 2B, and
they are the two most likely to be missed.

## 5. Evidence rules — `P2B-EVD-01` … `P2B-EVD-17`

| Script | Setup | Attempt | Pass only if | Local check |
|---|---|---|---|---|
| **P2B-EVD-01** | `PRJ-0002`, an activity with no project override | Submit without the "Before" photograph | Refused, citing the **global** rule as the source | EVD-01 |
| **P2B-EVD-02** | `PRJ-0001`, an activity the project overrides | Submit against the global rule | Refused, and the message names the **project override**, not the global rule | EVD-02 |
| **P2B-EVD-03** | the same activity on `PRJ-0001` and `PRJ-0003` | Submit the minimum photographs of one on the other | The stricter project refuses, the other accepts. **Identical activity, different outcome, no code difference** | EVD-03 |
| **P2B-EVD-04** | ceiling-tile replacement, forbidden on one project | Select it on the project where it is forbidden | Not offered; and refused if supplied directly | EVD-04 |
| **P2B-EVD-05** | a visit meeting every effective rule | Submit | Accepted, with no warning invented and none suppressed | EVD-05 |
| **P2B-EVD-06** | a snag photograph with no caption | Submit | Refused, and the message says **the caption is mandatory on a snag photograph** — not "invalid input" | EVD-06 |
| **P2B-EVD-07** | remove the required "After" photograph | Submit | Refused, naming the missing stage | EVD-07 |
| **P2B-EVD-08** | an activity requiring a quantity, left empty | Submit | Refused, naming the quantity | EVD-08 |
| **P2B-EVD-09** | a negative quantity | Submit | Refused | EVD-09 |
| **P2B-EVD-10** | a quantity on an activity that takes none | Submit | Refused, saying the activity takes no quantity | EVD-10 |
| **P2B-EVD-11** | photographs, **no declared activity** | Submit | **Accepted.** This is a valid photographic submission (D-22), and classification catches up afterwards. A system that refuses this has reintroduced the obligation the owner removed | EVD-11 |
| **P2B-EVD-12** | neither photograph nor activity | Submit | Refused — there is no evidence to carry | EVD-11b |
| **P2B-EVD-13** | any refusal above | Read every refusal message produced in this suite | **Every one names what to fix.** A generic rejection fails this script even where the refusal itself was correct | EVD-12 |
| **P2B-EVD-14** | two near-identical photographs | Submit both | Both are **retained**, the duplicate is flagged, and neither is deleted or silently merged | EVD-13 |
| **P2B-EVD-15** | a device with location services off | Capture and submit | **Accepted.** GPS is recorded as missing, never as zero, and never blocks | EVD-14 |
| **P2B-EVD-16** | a refused submission | Retry it unchanged; then retry it from a **second device**; then retry after going offline and back online | Refused every time, identically. **A rule that can be outlasted is not a rule** | *new* |
| **P2B-EVD-17** | a submission that was refused, then corrected | Submit the correction | Accepted, and the earlier refusal remains in the record. **A correction is a new version, never an erasure** | *new* |

**P2B-EVD-16 is the script most likely to fail on a real platform.** Client-side validation that
disappears on a replayed or offline submission is an ordinary platform behaviour and a serious
failure here.

## 5b. Revocation and quarantine — `P2B-REV-01` … `P2B-REV-08`

Added by **decision D-25**. The local checks `ACC-32` … `ACC-45` prove the **rule**; these prove the
**running system obeys it**, which is a different claim.

| Script | Setup | Attempt | Pass only if | Local check |
|---|---|---|---|---|
| **P2B-REV-01** | Six photographs captured, queued, unsent. Access revoked while the device is offline | Reconnect | All six complete into **quarantine**. **None is discarded, none reaches the active project register** | ACC-32 |
| **P2B-REV-02** | Access already revoked | Capture and attempt to submit | **Refused.** Not quarantined, not queued, not stored | ACC-33 |
| **P2B-REV-03** | A queued photograph whose capture time is missing or unreadable | Reconnect | **Refused**, and the refusal says why. Unprovable is not treated as early | ACC-34 |
| **P2B-REV-04** | The refusal of `P2B-REV-02` | Retry five times, closing and reopening the app between attempts | Refused every time, identically. **Persistence is not a bypass** | ACC-36 |
| **P2B-REV-05** | The same account signed in on a **second device** after revocation | Capture and submit | Refused. The rule is the capture timestamp against the revocation timestamp, **never the device** | ACC-37 |
| **P2B-REV-06** | The same pre-revocation photograph submitted **twice** | Reconnect | Quarantined **once**, the second flagged as a duplicate. **Not counted twice, not silently dropped** | ACC-38, EVD-13 |
| **P2B-REV-07** | Quarantined items exist | Open every report, calculation, approval and document | **None of them can see a quarantined item.** Only accepted items appear | ACC-39 |
| **P2B-REV-08** | A reviewer rejects a quarantined item | Submit the rejection with the reason left empty | **Refused.** The reason is mandatory, and the audit record is retained either way | ACC-40 |

**And the standing condition, checked throughout §5b:** the revoked user can no longer **view, edit,
delete, share or submit** anything (`ACC-42`). A revocation that leaves any one of those working is a
segregation failure and stops Phase 2B under the §4 rule.

**If the platform cannot enforce this:** `CAP-GATE` fails, and the queued files stay **locally
protected — not deleted, not uploaded** — pending an authorised recovery procedure. That is the
decision, not a fallback invented here.

## 6. Configurability — `P2B-CFG-01` … `P2B-CFG-10`

**The question this suite answers in one sentence:** can the company add its next project without
calling anybody?

| Script | Who does it | What they do | Pass only if | Local check |
|---|---|---|---|---|
| **P2B-CFG-01** | administrator, **unaided** | Add a fourth project, `PRJ-0004`, as data only — no developer, no support request, no new screen | The project is created and usable. **Any step requiring a developer is a failure of this script, however small the step** | CFG-07 |
| **P2B-CFG-02** | `USR-0005`, assigned to the new project | Capture and submit a visit on `PRJ-0004` on the first day | Works completely: rules apply, evidence is accepted, the record is correct | CFG-07, CFG-10 |
| **P2B-CFG-03** | `USR-0006`, not assigned | Look for `PRJ-0004` | Invisible, everywhere, including search and exports | CFG-08 |
| **P2B-CFG-04** | administrator | Give `PRJ-0004` the **second legal entity** | Its documents carry that entity's identity, numbering and tax treatment, without touching another project | CFG-09, CFG-12 |
| **P2B-CFG-05** | administrator | Set a project-specific activity rule on `PRJ-0004` | It takes effect on the next submission, and changes no other project's behaviour | CFG-05, EVD-02 |
| **P2B-CFG-06** | administrator | Change a rule on a project **that already has submitted visits** | The change applies from now on. **Records already submitted keep the rule they were judged under** | *new* |
| **P2B-CFG-07** | administrator | Add projects five through ten as data | All work. No step, limit, warning or degradation appears that depends on the number of projects | CFG-11 |
| **P2B-CFG-08** | administrator | Add a location whose **code** duplicates one in another project | Accepted and distinct | SEG-11, CFG-07 |
| **P2B-CFG-09** | reviewer | Open a report for `PRJ-0004` | The report exists and is correct without a new template being written for it. A project-specific template stays optional | CFG-06 |
| **P2B-CFG-10** | administrator | Read the application's logic — formulas, rules, expressions, scenario contents | **No project, client, contract or person identifier appears anywhere in it** | CFG-01 … CFG-04 |

**P2B-CFG-10 is the one to run last and take seriously.** Every hard-coded identifier this project
has been designed to avoid would show up there, and only there, once a system is actually built.

## 7. What these scripts do not cover

Stated so that a full pass is not mistaken for more than it is.

| Not covered here | Where it lives | Why it cannot be covered here |
|---|---|---|
| Whether the contractor actually received the share | Nowhere — **it is not observable** | The application can record that the share sheet opened and that the supervisor said it completed. It cannot see inside the messaging application, and no document may claim otherwise |
| Capture once, use twice | `19-real-device-test-protocol.md` §4b, `CAP-GATE` | It is a device and platform test, and it gates the platform choice itself |
| Offline capture and deferred submission | `05-offline-test-plan.md` | A network-condition matrix, not a rule test |
| The 75-second target and the tap count | `19-real-device-test-protocol.md`, `13-field-workflow-and-taps.md` | Performance, and **still unmeasured** |
| Make operation consumption against the verified limit | `23-operations-budget.md` | Measured in the first month of running, not in a test |
| AI proposal quality | Nowhere yet | A proposal is advisory by design (D-17, D-23). Its quality changes nothing a rule depends on |

**A full pass of all forty-nine scripts proves the system enforces its own rules. It proves nothing
about delivery, speed, cost or adoption.**

## 8. Pass, fail, and what a failure means

- **Every script is pass or fail.** There is no partial result, and "passed after a small fix" is
  recorded as a failure that was then fixed — with both the failure and the fix in the record.
- **A §4 segregation failure stops Phase 2B** until the cause is understood. It is not scheduled.
- **A §5 failure that can be reproduced offline or by replay is treated as a §4 failure,** because a
  rule that can be bypassed is an access-control problem wearing a validation costume.
- **A §6 failure means the configurability claim is withdrawn** from every document that makes it,
  until it is true again. D-01 is the foundation of this design; if it does not hold in the built
  system, the documents are wrong, not the test.

## 9. What is recorded for every run

For each script: its identifier, the platform and version, the signed-in identity, the exact input,
**what the screen actually showed** — including the wording of any refusal — the result, and the
local check it corresponds to. Failures are recorded in full, with what was expected, what happened,
and what was changed in response.

The record belongs in a Phase 2B evidence document alongside
`docs/01-data-foundation/17-validation-evidence.md`, and carries the same warning: **this is evidence
that a built system enforced a rule on a given day. It is not evidence that the system is secure,
complete, or fit for production.**

## 10. Status

**Completed · Submitted for Owner Review · Not executed.** Forty-nine scripts — fourteen segregation,
seventeen evidence-rule, **eight revocation and quarantine** (D-25), ten configurability — of which **five have no local counterpart** and exist
only because a running system can fail in ways a model cannot describe. No platform exists, none is
authorised, and the local suite stands at **257 of 257 across 13 suites**, unchanged by this
document.
