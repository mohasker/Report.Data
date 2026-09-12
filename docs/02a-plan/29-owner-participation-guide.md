# What the Owner Does on Test Day — One Page

**Document ID:** AH-SYS-P2A-029 · **Revision:** 1 · **Date:** 2026-09-12
**Status:** Completed · **No test is scheduled and none is authorised**
**Time needed:** about 20 minutes of your own, spread across a half-day session

---

## Before the day — four things only you can do

| # | What | Why it must be you |
|---|---|---|
| 1 | **Send the Admin Console answers** (`16-admin-console-checklist-owner.md`) | You are the administrator. About 15 minutes, changes nothing |
| 2 | **Authorise the prototype in writing** | Nothing is built without it, and "go ahead" in conversation is not the same as a written instruction I can point at later |
| 3 | **Provide two phones** — one iPhone, one Android, with standard WhatsApp on one and WhatsApp Business on the other | They must be phones of the kind your supervisors actually carry, not the newest ones in the office. **A test on better phones than the field uses measures nothing** |
| 4 | **Create the test group** with only the two test phones and yourself in it | It must be a group **the company controls**. Never a client group, never a live project group |

## On the day — three moments where you are needed

### Moment 1 — the baseline, before anyone sees the app *(5 minutes)*

Post six photographs to the test group **the way your supervisors do it today**: open WhatsApp,
attach, type the sentence, send. Five times. Someone times it.

**Do this first.** Once people have seen the new app, nobody posts to WhatsApp at a normal pace
again, and the comparison is spoiled for good.

### Moment 2 — revoke the access *(2 minutes, twice)*

When the tester asks, remove the test user's project assignment — **once while the phone is online
and idle, once while it is offline holding six unsent photographs.** Then hand the phone to the
tester and let them inspect what is left.

The second case is the one with no agreed answer yet (`OQ-23`): should the queued evidence be
discarded, or should it complete into a reviewer's queue? **The test shows what the platform does.
You decide what it should do.**

### Moment 3 — the verdict *(3 minutes)*

After five runs, each supervisor is asked one question, and you should hear the answer yourself:

> **"Would you use this instead of WhatsApp?"**

Yes, no, or "only if…". **Their answer outranks the stopwatch.** If the app is eleven seconds faster
and two supervisors say they would not use it, the honest result of this test is a fail, and I would
rather record that than deliver something nobody opens on a hot afternoon.

## What you should refuse to accept from me

- **"It mostly worked."** Every criterion is pass or fail. Twelve of sixteen is a fail.
- **"The share went through."** The application cannot see inside WhatsApp. It can record that the
  share sheet opened and that someone said it completed. **Ask for the screenshot of the received
  message** — that is the only proof.
- **"We can work around the second selection."** No. That is `CAP-01`, and a duplicate-upload
  workaround is exactly the thing this whole design exists to prevent.
- **A pass on one device.** Both devices, both messaging applications, or it is not a pass.

## What a failure costs

**A day, and the capture platform.** The data model, Drive security, orchestration, the AI controls,
approvals and audit rules are all defined independently of the capture interface — that separation
was deliberate, and it is why a failed `CAP-GATE` changes which application the supervisor opens and
almost nothing else.

**Finding out on a test day is the cheap version.** Finding out after three months of building is
the expensive one.

## Status

**Completed.** No test is scheduled, no prototype exists, and nothing in this guide may begin before
your written authorisation.
