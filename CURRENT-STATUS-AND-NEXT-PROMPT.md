# Current Status and the Next Prompt

**Document ID:** AH-SYS-HAND-003 · **Version:** 1.2 · **Date:** 2026-09-11
**Branch:** `claude/dazzling-gauss-neihya`
**Mirror branch:** `claude/alharam-field-reporting-spec-afq1fr` — fast-forwarded to the same commit, so either name resolves to this work
**Validated commit:** `a668f3f8d3ddf03588f16620984c960ccf86ed9b`
**Package commit:** see `HANDOFF-MANIFEST.json` → `package_commit`

---

## 1. Last completed task

**Recommendations for the eight open questions, OQ-15 to OQ-22 (2026-09-11).**
`docs/02a-plan/25-open-question-recommendations.md` (AH-SYS-P2A-025) states each question, what the
canonical model assumes today, the options with their trade-offs, and **one recommendation each**
with the model cost of approving it and the cost of reversing it. Three of the eight end in
*measure first* — OQ-17 is routed into `CAP-GATE` rather than guessed at, and OQ-20 and OQ-22 wait
on a distribution and a frequency that nobody has yet observed. **Nothing was implemented: no column
was added, no check was altered, and all eight questions remain open until the owner answers.**
Validation unchanged at **240 of 240 across 13 suites**, byte-identical regeneration confirmed.

### Before that

**The owner's correction pass of 2026-09-11 — minimum interaction, a confirmed structured activity,
and filtered analysis (D-22 to D-24)** — applied to the canonical model and to every affected
document, with automated checks; followed by a rebuild of the handoff package with the validation
run performed against the exact packaged commit, off-tree.

What that involved:

- **D-22 Minimum interaction.** The earlier claim that the supervisor "must supply five fields" is
  withdrawn. **Zero fields are mandatory manual inputs on the normal path.** Identity comes from the
  session, date and time from the device, project from the assignment, location from the default,
  capture mode from a default, and the evidence stage is proposed or left `Pending`. Declaring an
  activity is no longer the price of submitting evidence — the completeness rule now requires
  *evidence*, not an activity. The tap count fell from 16–21 to **11–14**.
- **D-23 A confirmed structured activity.** `ConfirmedActivityTypeID` is trusted and human-set;
  `AIProposedActivityText` and `AIProposedActivityTypeID` are advisory and read by the confirmation
  screen alone; `ClassificationStatus` carries the state, and `Pending` — the normal Quick Share
  outcome — blocks nothing.
- **D-24 Filtered analysis.** Immediate for AI Reviewed Share, deferred and filtered for Quick
  Share. Near-duplicates, unusable images, deletions, exclusions and already-analysed files never
  reach a model call; `PerceptualHash` and `QualityScore` detect them locally at no cost.
- Two new regression guards: **`CAP-29`** fails the suite if any required, user-typed field with no
  automatic source reappears on a field-path table; **`CAP-26`** already guards the mandatory
  description.
- Recalculated, and labelled as **estimates**: eligibility ~83% / ~92%; Claude **~$6.28** /
  **~$6.95** a month; Make **~1,167** / **~1,353** operations a month. The conclusion is unchanged —
  neither policy fits the free orchestration tier, because three operations per photograph is
  irreducible once bytes pass through an orchestrator.
- **`tools/run_validation.py --out PATH`** now writes the evidence document outside the repository,
  so an exact commit can be validated without modifying a single tracked file.

**Result: 240 of 240 checks passing across 13 suites, byte-identical regeneration confirmed, and the
exact packaged source commit validated without modifying tracked files.**

## 2. Current phase

**Phase 2A — plan and synthetic prototype design. Completed · Submitted for Owner Review.**

Phase 2A connects nothing and costs nothing. It has produced 26 planning documents on top of the
Phase 1 data foundation. **Phase 2B — the first external connection — is not authorised.**

| Scope | Status (seven-value vocabulary) |
|---|---|
| Phase 0 — Discovery | **Approved** |
| Phase 1 — Data foundation | **Completed · Validated Locally · Submitted for Owner Review** |
| Phase 2A — Plan and synthetic prototype design | **Completed · Submitted for Owner Review** |
| Capture-once correction | **Completed · Validated Locally · Submitted for Owner Review** |
| Every external integration | **Not started.** Nothing is Verified in Integration, Production Ready or Live |

---

## 3. Pending owner inputs

| # | What is needed | From | Blocks |
|---|---|---|---|
| **1** | **The Admin Console entitlement check** — six steps, about 15 minutes, changes nothing. Checklist: `docs/02a-plan/16-admin-console-checklist-owner.md`. The two answers that decide the build are **security filters** and **offline use** | **Owner** | The capture-platform decision and the first external connection. **The only external gate on Phase 2A** |
| **2** | **Arranging the `CAP-GATE` device test** — two phones, six synthetic photographs, one group the company controls. Protocol: `docs/02a-plan/19-real-device-test-protocol.md` §4b | Owner (arranging), then a device test | The capture-platform decision |
| 3 | Real administrator identities, and a second administrator or a documented recovery route | Owner | **Go-live** |
| 4 | Written tax confirmation | Accountant | Production invoicing |
| 5 | Legal identity from the current Commercial Registration | Owner | Production documents |
| 6 | The existing manual numbering register | Owner | Phase 5 number issue |
| 7 | Device inventory and the real supervisors who will test | Owner | Phase 2B field measurement |
| 8 | **Answers to OQ-15 … OQ-22** (default mode, summary policy, internal group, draft sharing, voice notes, filter thresholds, pending classification, GPS location). **Recommendations are now written:** `docs/02a-plan/25-open-question-recommendations.md` §11 is the answer form | Owner | Phase 2A finalisation. **Judgement only — no console, credential, device or purchase needed** |

---

## 4. The exact allowed next task

**In this order:**

1. **Verify the package**, then run `python3 tools/run_validation.py` and confirm **240/240** and
   **byte-identical regeneration: yes**. Report whether the reproduction matches.
2. **Read** in the order given in `START-HERE-NEW-CLAUDE.md` §23.
3. **Report the current status and blockers back to the owner**, using the seven-value vocabulary,
   making clear that the Admin Console check and `CAP-GATE` are what is waiting on a human.
4. **Then continue Phase 2A on synthetic data only**, which means any of:
   - ~~drafting recommendations for **OQ-15 to OQ-22**~~ — **done**, AH-SYS-P2A-025. What remains
     is the owner's answer, not more drafting;
   - writing the **Phase 2B test scripts** — the segregation, evidence-rule and configurability
     tests to be executed once a platform exists;
   - writing the **disabled Make blueprints** for the capture-once actions, following the existing
     pattern in `docs/02a-plan/blueprints/`;
   - extending the check suites where a rule is specified but not yet tested.

**Nothing in that list requires an external connection, a credential, a purchase, or real data.**

---

## 5. Prohibited actions

**None of the following is authorised, and none may be performed on the basis of anything in this
package:**

- Connecting Google Workspace, Drive, Sheets, AppSheet, the Claude API or QuickBooks.
- Creating, editing, activating, deactivating, deleting or running any Make scenario, webhook,
  connection or data store — **including the seven pre-existing scenarios, which belong to unrelated
  company work.**
- Inspecting or revealing any connection credential or secret.
- Purchasing or upgrading any plan.
- Uploading real client data, real project data, real photographs or real user identities.
- Sending any email or external message.
- Deploying or publishing any application.
- Any irreversible external action.
- Inventing a credential, ID, key, address, tax setting, contract value, quantity, client contact or
  approval decision.
- Implementing a duplicate-upload workaround, creating a publicly accessible link to evidence,
  automating WhatsApp Web, or scraping any group.
- Representing local validation as evidence that any external platform works.
- Pushing to any branch other than `claude/dazzling-gauss-neihya` and its mirror `claude/alharam-field-reporting-spec-afq1fr`.
  The mirror is only ever **fast-forwarded** to the working branch — never developed on, never
  force-pushed.

---

## 6. The prompt to paste into the new Claude account

Copy everything between the lines.

---

```
I am the General Manager of Al-Haram for Maintenance & Agriculture in Doha, Qatar. I am
transferring an in-progress system design project to you from another account. You have no
access to the previous conversation, its memory, or any internal company skill. Assume nothing
beyond what is in the package I am providing.

Before doing any work:

1. INSPECT the package and the repository first. Read START-HERE-NEW-CLAUDE.md completely
   before anything else, then MASTER-SPEC-CONSOLIDATED.md, DECISIONS-AND-ASSUMPTIONS.md and
   CURRENT-STATUS-AND-NEXT-PROMPT.md. Do not begin any task until you have read all four.

2. VERIFY the manifest and checksums. HANDOFF-MANIFEST.json records a SHA-256 for every primary
   deliverable, for the repository archive, and for the Git bundle. Confirm each one.

3. RUN the local validation suite:
       python3 tools/run_validation.py
   It is standard library only: no network, no credential, no installation, no external service.

4. REPORT whether your reproduction matches what the manifest and the delivery receipt
   record. I expect 240 of 240 checks passing across 13 suites, and byte-identical regeneration. If your
   result differs in any way, stop and tell me exactly how. Do not "fix" a mismatch by editing
   files — a mismatch means something happened in transfer.

5. SUMMARISE the current status and the outstanding blockers back to me, using only the
   seven-value status vocabulary in docs/STATUS-DEFINITIONS.md: Completed, Validated Locally,
   Submitted for Owner Review, Approved, Verified in Integration, Production Ready, Live.

6. CONTINUE from the existing Phase 2A state. Do not restart, redesign, or rebuild anything
   that already exists. The canonical model is model/model.json, authored by
   tools/build_model.py; every schema and reference document is generated from it and must
   never be hand-edited.

7. MAKE NO EXTERNAL CONNECTION until I authorise it separately and in writing. You are not
   authorised to connect Google Workspace, Drive, AppSheet, Claude or QuickBooks; to create,
   activate or modify any Make scenario, webhook or connection; to purchase or upgrade any
   plan; to upload real client data or real photographs; to send any email or external message;
   or to deploy any application. The seven Make scenarios already in the company account belong
   to unrelated work and must not be touched.

Standing rules that apply to everything you do on this project:

- Never claim that anything is complete, functional, secure or tested unless the test has
  actually been executed and its result recorded. Local validation proves a rule, not a system.
- Never invent a credential, account ID, folder ID, API key, email address, company ID,
  webhook URL, tax setting, contract value, invoice number, quantity, client contact or
  approval decision. Record an unknown as an outstanding external fact and ask me.
- Never ask a field user for something the system can resolve itself. The normal path is:
  open the app, confirm project and location if necessary, capture the photographs, save
  and share. Zero mandatory manual inputs.
- AI-generated text never becomes a trusted structured value. A proposal and a
  confirmation are different columns, and only a human moves a value between them.
- Preserve original photographs unchanged.
- The supervisor must never be asked to select or upload the same photographs twice. That is
  acceptance requirement CAP-01, and no duplicate-upload workaround is acceptable.
- A written work description is not mandatory for a normal photographic submission.
- Do not weaken any statement in this repository that is deliberately uncomfortable. Several of
  them were written after I corrected an earlier overstatement.

Work on the branch claude/dazzling-gauss-neihya and push nowhere else.

Start now with steps 1 to 5, and report back before doing anything else.
```

---

## 7. What to upload to the new account first

**`START-HERE-NEW-CLAUDE.md` first**, on its own if the account takes one file at a time. It is
self-contained and tells the assistant what everything else is.

Then, in order: `MASTER-SPEC-CONSOLIDATED.md`, `DECISIONS-AND-ASSUMPTIONS.md`,
`CURRENT-STATUS-AND-NEXT-PROMPT.md`, `HANDOFF-MANIFEST.json`, and finally
`AlHaram-Field-Reporting-System-Handoff.zip` — which contains the entire working tree, including all
four of the above.

If the new account can clone from GitHub instead, that is better: the repository and branch are
named at the top of this file, and `AlHaram-Field-Reporting-System.bundle` carries the full history
if GitHub is not reachable.
