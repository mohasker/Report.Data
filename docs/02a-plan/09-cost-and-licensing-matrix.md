# Cost and Licensing Matrix

**Document ID:** AH-SYS-P2A-009 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **EVERY FIGURE IS UNVERIFIED**

> **No price in this document has been verified against an official source.** The build environment's
> network egress policy blocks the vendors' own pricing pages. Third-party aggregator figures are
> reproduced only so the owner can size the decision, and **must not be used to purchase anything.**
> Operating rule 2 forbids inventing prices, and repeating an unofficial figure confidently is the
> same failure.

---

## 1. What the system needs a licence for

| Component | Licensing model | Needed from | Verified? |
|---|---|---|---|
| Google Workspace | Per user per month; Shared Drive capability depends on the edition | Phase 2 | **No** |
| Capture platform (AppSheet) | Per user per month; features gated by tier | Phase 2 | **No** — see `12-appsheet-feature-to-plan-matrix.md` |
| Orchestration (Make) | Per operation, tiered; Data Stores may be tier-gated | Phase 3 | **No** |
| AI (Claude API) | Per token consumed, with a hard monthly cap set by the owner | Phase 4 | **No** — cap not yet set (EF-04) |
| Accounting (QuickBooks Online) | Already licensed and in use | Phase 7 | Existing cost, unchanged |
| Storage | Included in the Workspace edition up to a quota | Phase 3 | **No** |

## 2. User counts — the number that actually drives cost

| Group | Count | Why |
|---|---|---|
| Office and review | 5 | GM, business administrator, technical reviewer, finance reviewer, project manager |
| Technical administration | 2 | Administrator plus the backup that the recovery plan requires |
| Field capture | 6–15 | Scales with active projects |
| Break-glass | 1 | Licensed only if the platform requires a licence for a dormant account |
| **Total** | **14–23** | |

**The decisive question is not the tier, it is whether a capture-only field user can sit on a cheaper
tier than an office user.** At fifteen field users, a few dollars a month each is the difference
between a rounding error and a real annual line item. It is the first question in the verification
script.

## 3. Indicative annual cost — UNVERIFIED

Third-party aggregators consulted on 2026-09-11 describe capture-platform tiers in the region of
**$5, $10 and $20 per user per month**. Working arithmetic on those unverified figures, for scale
only:

| Scenario | Capture platform | Workspace | Orchestration | AI | Indicative annual |
|---|---|---|---|---|---|
| **Lean** — office on a middle tier, field on the lowest | ~$1,740 | existing | lowest tier | capped low | **~$2,000–3,000 + orchestration** |
| **Uniform** — everyone on a middle tier | ~$2,640 | existing | lowest tier | capped low | **~$3,000–4,000 + orchestration** |
| **Premium** — everyone on the highest listed tier | ~$5,280 | existing | mid tier | capped | **~$6,000–8,000** |

Orchestration is deliberately left as a range: it bills per operation, and per-photograph processing
multiplies operations quickly (P-05). **The only honest way to size it is to measure real
consumption in Phase 3 and then choose a tier**, not to guess now.

AI cost is bounded by construction: a hard monthly cap, analysis of downscaled derivatives only,
one analysis per photograph, and per-project usage tracking. The cap is the number, not the estimate.

## 4. Cost controls built into the design

| Control | Effect |
|---|---|
| Field users may sit on a cheaper tier if the platform permits | Largest single lever |
| AI analyses derivatives, never originals | Vision cost scales with image size |
| One analysis per photograph, cached | No re-analysis without an explicit request |
| Ineligible evidence never sent | Duplicates and AI-disabled projects cost nothing |
| Hard monthly AI cap | A bulk upload cannot produce a surprise bill |
| Batch orchestration where safe; no per-row polling | Operation consumption |
| Google Sheets as the MVP store | No database licence until the migration threshold is crossed |
| Per-project usage tracking | Cost is attributable to the contract that generated it |

## 5. Cost of *not* verifying

The spread between the lean and premium scenarios is roughly **$2,600–5,000 a year**. The
verification script in `12-appsheet-feature-to-plan-matrix.md` §5 takes about twenty minutes. It is
the highest-return twenty minutes available in this phase.

## 6. What must happen before any purchase

1. Complete the verification script; record each answer with its official URL and the date.
2. Confirm whether capture-only users can sit on a cheaper tier, and whether that tier still includes offline use and image capture.
3. Confirm the free development tier's limits, so Phase 2A prototyping costs nothing.
4. Set the AI monthly cap (EF-04).
5. Re-run the arithmetic above with verified figures; only then does a recommendation by tier name become legitimate.
