# CAP-GATE Synthetic Prototype — Specification

**Document ID:** AH-SYS-P2A-027 · **Revision:** 1 · **Date:** 2026-09-12
**Status:** Completed · **Nothing built.** No application exists, no account is connected, and
building this prototype needs the owner's separate written authorisation
**Feeds:** `19-real-device-test-protocol.md` §4b and §4c

---

## 1. What this prototype is for, and what it must never become

`CAP-GATE` asks one question: **can the platform share the stored image files themselves, to an
existing group, without the supervisor selecting them a second time?** Everything else in this
project is downstream of the answer.

To ask that question you need the **smallest possible thing that can capture six photographs and open
a share sheet.** Not a pilot. Not a demonstration. Not a first version of the real application.

**The failure mode to avoid is well known:** a prototype built to answer one question becomes the
foundation of the product because it exists and it works. **This one is disposable by design and must
be deleted after the test**, whatever the result. Nothing in the real system is built from it, and
nothing in the real system may reference it.

## 2. The synthetic fixture — no real anything

| Item | Value | Why exactly this |
|---|---|---|
| Project | **`SYN-CAPGATE`**, "Synthetic Capture Test" | Not a real project name, not a real client, not a real site |
| Location | **`SYN-LOC-01`**, "Synthetic Test Location" | One location: the location logic is not what is being tested |
| Users | Two test accounts, labelled **Tester A** and **Tester B** in every record | No supervisor's name appears in a test document |
| Group | A WhatsApp group **the company creates for this test and controls**, containing only the two test phones and the owner | **No client, no main contractor, and no live project group.** A test message in a real contractor group is not a test, it is an incident |
| Photographs | Six, taken during the test, of the numbered cards in §4 | Nothing from a real site. Nothing from anyone's camera roll |

**If any real project, client, contact or photograph appears in the prototype, the run is void** and
is repeated after the data is removed. That is not pedantry: a synthetic test with one real row is
how real data reaches an unsecured place.

## 3. What the prototype must contain — the minimum

| Element | Minimum required | Deliberately excluded |
|---|---|---|
| Tables | **Two:** a visit row and a photograph row, with `CaptureBatchID` and `CaptureSequence` | Every other table of the 46. None is needed to answer the question |
| Fields | Visit: project, location, capture time, share status. Photograph: file, batch, sequence, capture time | Activities, quantities, evidence stages, captions, AI columns, approvals |
| Screens | **Two:** a capture screen and a share action | Reviewer screens, dashboards, reports, settings |
| Rules | **None** | Every validation rule. `CAP-GATE` tests transport, not correctness — and a rule that blocks a test run wastes a device day |
| Security | The two test accounts see the synthetic project and nothing else | Full security-filter testing, which belongs to `P2B-SEG-01 … 14` |
| Storage | A folder the test accounts can write to | Shared-drive structure, folder provisioning, naming conventions |
| Automation | **None. No Make scenario, no webhook, no connection.** | All of it, explicitly |

**If building it takes more than a few hours, it has grown past its purpose.** Stop and re-read §1.

## 4. The six numbered cards — how order and completeness become objective

Print six A5 cards, each carrying **one large number, 1 to 6, in a distinct colour**, plus the word
`SYNTHETIC`. Photograph one card per shot, in order.

This turns three subjective conditions into things anybody can verify from a screenshot of the
received message:

| Condition | Without the cards | With the cards |
|---|---|---|
| §4b-2 all six arrived | Count six similar site photographs and hope | **Numbers 1 to 6 are visible or they are not** |
| §4b-4 order preserved | Compare timestamps afterwards | **1, 2, 3, 4, 5, 6 — or it reordered** |
| §4b-3 orientation | Judgement | Photograph cards 3 and 4 in landscape; **rotation is obvious** |

Card 6 carries a **long Arabic caption** printed on it, so that right-to-left rendering in the shared
summary can be judged from the same photograph.

**Cost: six sheets of paper.** It is the cheapest thing in this protocol and it removes most of the
argument about what the test showed.

## 5. What must exist before the test day

| # | Prerequisite | Owner or tester |
|---|---|---|
| 1 | The Admin Console answers of `16-admin-console-checklist-owner.md` | **Owner** |
| 2 | Written authorisation to build the prototype | **Owner** |
| 3 | Two devices — one iPhone, one Android — with **standard WhatsApp on one and WhatsApp Business on the other**, then swapped for the second pass | Owner arranges |
| 4 | The synthetic group, created and containing only the test phones and the owner | Owner |
| 5 | The six printed cards | Either |
| 6 | Both devices at **more than 50% battery and more than 2 GB free**, recorded | Tester |
| 7 | A stopwatch that is not one of the two test phones | Tester |
| 8 | The results sheet of `28-cap-gate-results-sheet.md`, printed or open | Tester |

## 6. After the test — disposal

1. **Delete the prototype application.** It has answered its question.
2. **Delete the synthetic group**, or empty it and record that it is dormant.
3. **Leave the six photographs in place** until the results sheet is signed off — they are the
   evidence that the evidence arrived.
4. **Record what was deleted and when.** A prototype that quietly survives is the one that gets
   extended.

## 7. Status

**Completed · Nothing built.** This is a specification of a thing that does not exist. Building it
requires the owner's separate written authorisation, which has not been given, and no part of it may
be started on the basis of this document.
