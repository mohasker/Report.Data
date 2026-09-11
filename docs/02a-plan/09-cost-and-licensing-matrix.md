# Cost and Licensing Statement

**Document ID:** AH-SYS-P2A-009 · **Revision:** 4 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review
**Supersedes:** revision 1 (USD 2,600–5,000 annual — withdrawn) and revision 2 ("expected pilot cost is USD 0" — withdrawn as an overstatement)

---

## The statement

> **No new mandatory subscription has been identified before entitlement verification. Variable
> automation, AI and storage costs may arise when those capabilities are enabled.**

That is the whole position. Everything below is the detail behind it.

---

## 1. Existing costs — already paid, not incremental

| Item | Status | Used for | Incremental cost of this project |
|---|---|---|---|
| **Google Workspace** | Active paid subscription | Identity and sign-in, Sheets as the operational store, Drive for evidence and documents, Docs for templates, Gmail for internal notification | **None.** Existing cost |
| **QuickBooks Online** | Active and in use | Accounting, from Phase 7 only | **None.** Existing cost |

## 2. AppSheet Core — assumed USD 0 incremental, pending verification

| | |
|---|---|
| **Assumption** | AppSheet Core is included in the existing Workspace subscription |
| **Status** | **Unverified.** The Admin Console check ([`16-admin-console-checklist-owner.md`](16-admin-console-checklist-owner.md)) settles it in about 15 minutes |
| **Treated as** | **USD 0 incremental** until that check returns |
| **If not included** | A specific, costed option comes back to the owner. **No purchase is assumed, proposed or made without written approval** |

## 3. Make — verified, and not permanently free

The read-only inspection of 2026-09-11 ([`15-make-inspection-record.md`](15-make-inspection-record.md))
established the following **from the live account**:

| Verified fact | Value |
|---|---|
| Current plan | **Free** |
| Operations included | **1,000 per month** |
| Consumed this period | **0** |
| Active scenario limit | **2** |
| Data stores | 1, maximum 1 MB |
| Data transfer | 512 MB/month |
| Maximum file size | 5 MB |
| Minimum scheduling interval | 15 minutes |
| Overage | **None.** Work stops at the ceiling rather than billing |
| Required integrations | **All present**, including AppSheet, Claude and QuickBooks |

**Therefore:**

- **Potentially USD 0 during limited testing.** The rebuilt operations budget lands at **703 operations, 70% of the verified limit**, using **2 active scenarios** — inside the plan, with retries, corrections, duplicates and administrative tests all funded ([`23-operations-budget.md`](23-operations-budget.md)).
- **Not confirmed as permanently free.** That budget only fits because release 1 removes per-photograph orchestration. Restoring it needs **≥3,000 operations/month and ≥3 active scenarios** — the exact paid-plan requirement, stated without a price because the price is unverified.
- **A paid tier is a probable cost at scale**, with a measurable trigger rather than a date. make.com is unreachable from this environment; the owner can read the price on their own billing page.

## 4. Claude API

| | |
|---|---|
| **For the field-capture MVP** | **Optional.** Capture, review, snags and the audit trail work with no AI at all |
| **When automated AI analysis and report drafting are enabled** | **Mandatory incremental usage cost.** There is no free path to automated analysis |
| Cost shape | Usage-based, per image analysed and per report drafted, **bounded by a hard monthly cap the owner sets** (EF-04) |
| **Costed** | ~**$0.021 per analysed photograph** on the default model at a 1024 px derivative — about **$4.50/month** at pilot volume (216 analysed images), ~$30/month at 20 projects. Arithmetic and the cheaper-model option: [`22-image-derivative-architecture.md`](22-image-derivative-architecture.md) §5 |
| Cost controls in the design | Analyse only approved evidence, on downscaled derivatives; one analysis per photograph; output token caps; per-project on/off switch; per-project usage recorded |
| Still to measure | Real cost per 100 photographs, at the Phase 4 gate |

## 5. Additional Drive storage — future conditional

| | |
|---|---|
| **Status** | **Conditional.** Depends on two things that are both unknown |
| Depends on | (a) The company's existing Workspace storage allocation and how much is already used; (b) actual image growth, which depends on photographs per visit and average image size |
| Projection | Expected scenario: ~42 GB/year at 10 projects, ~84 GB/year at 20. High scenario: ~578 GB and ~1.16 TB respectively. Full assumptions and three scenarios: [`14-storage-and-image-volume.md`](14-storage-and-image-volume.md) |
| **Cannot yet be assessed** | Until the Admin Console storage screen is read (step 5 of the owner checklist) |
| Levers before paying | Cap image upload quality; archive closed periods; constrain photographs per activity; review the retention period against what contracts actually require |

## 6. One-time implementation

No external cash outlay identified. The cost is the company's own time.

| Item | Who | Effort |
|---|---|---|
| Admin Console entitlement check | Owner or administrator | ~15 minutes |
| Workspace and Shared Drive setup | Administrator | ~1 hour |
| App build against synthetic data | This workspace | — |
| Report template from the company's existing format | Owner review | ~2 hours |
| Master data for the first three projects | Administrator | ~2–4 hours, then ~20 minutes per project |
| Real-device field testing | 2–3 supervisors | Half a day |
| Legal identity, numbering register, tax confirmation | Owner, accountant | A few hours over weeks |
| Parallel month alongside the manual process | Owner and reviewers | One reporting cycle |

## 7. Summary

| Category | Position |
|---|---|
| **Existing, not incremental** | Google Workspace, QuickBooks Online |
| **Assumed USD 0 incremental, unverified** | AppSheet Core — pending the Admin Console check |
| **Potentially USD 0 during limited testing, not permanently free** | Make — verified Free plan, 1,000 operations, 2 active scenarios. The prototype fits at **70% of the limit**; restoring per-photograph processing needs **≥3,000 ops and ≥3 scenarios** |
| **Optional for the MVP, mandatory when enabled** | Claude API — usage-based, capped by the owner |
| **Future conditional** | Additional Drive storage — depends on the company's existing allocation, current consumption and actual image growth. **Cannot be assessed until the Admin Console storage screen is read** |
| **One-time** | No cash outlay; company time only |

**No new mandatory subscription has been identified before entitlement verification. Variable
automation, AI and storage costs may arise when those capabilities are enabled.**

## 8. What would change this statement

| Finding | Effect |
|---|---|
| AppSheet not included in the Workspace subscription | A costed option comes back for written approval |
| Make's 2-scenario limit proves unworkable even for a 2-scenario pilot | A paid tier becomes a mandatory cost, with a price to verify |
| Photographs per visit much higher than assumed | Storage moves from conditional toward probable |
| Automated AI analysis switched on | A mandatory usage cost begins, bounded by the cap |
| Storage allocation already near full | Additional storage becomes immediate rather than future |

**Nothing is purchased, and no purchase is proposed, until one of these is established in fact.**
