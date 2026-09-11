# Capture Platform: Feature-to-Plan Requirements Matrix (EF-03)

**Document ID:** AH-SYS-P1-012 · **Revision:** 2 · **Date:** 2026-09-11
**Status:** Completed · **Submitted for Owner Review** · **NOT verified against official sources**
**Delivers:** D-04 and the owner's EF-03 request of 2026-09-11

---

## 1. Verification status — read this before anything else

**No tier is recommended by name, because current features and pricing could not be verified from an
official source.**

| | |
|---|---|
| **Attempted** | `about.appsheet.com/pricing`, `cloud.google.com/appsheet/pricing`, `support.google.com/appsheet` |
| **Result** | **Blocked.** The build environment's network egress policy blocks Google-owned domains; one URL returned 404 |
| **Consequence** | Column "Supported?" and column "Minimum plan" below are **UNVERIFIED** throughout |
| **Who can complete it** | The owner, or anyone on an unrestricted network, in about twenty minutes using §5 |

Third-party aggregator pages were reachable and are summarised in §4 **as an indicative cost
assumption only**. They are not official, they may be out of date, and they must not be used to
select or purchase a plan. Operating rule 2 forbids inventing prices, and a third-party figure
repeated confidently is the same failure.

## 2. Requirements matrix

`Level` — **Must**: the design does not function without it · **Should**: significant value ·
**Could**: desirable.

| # | Required capability | Level | Supported? | Min. plan | Official source | Limitation to check | Proposed workaround if unsupported |
|---|---|---|---|---|---|---|---|
| R-01 | Authenticated individual sign-in; no shared accounts | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Which identity providers; whether per-user licensing is enforced | None. Attribution is the audit trail's purpose; shared logins are not acceptable at any price |
| R-02 | Row-level security filters evaluated server-side | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Whether filters run before data reaches the device, or only hide it after | **Blocking.** Without server-side filtering the segregation model cannot be enforced and the platform is unsuitable |
| R-03 | Offline capture with delayed sync, including images | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | How many rows and images are held offline; behaviour when the queue is large | Reduce offline scope to one visit at a time; or reconsider the capture layer |
| R-04 | Image capture at the highest available fidelity, with a configurable upload quality | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Whether the platform re-encodes on upload regardless of setting (C-02) | Already covered by D-13: write-once from first receipt, with no "original device image" claim until device testing |
| R-05 | Outbound webhooks on data change | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Whether webhooks are a licensed automation feature and at which tier | **Blocking for the pipeline.** Fallback: scheduled polling from the orchestration layer, at higher operation cost and with added latency |
| R-06 | Inbound API to read and write records | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Rate limits; whether writes can set status fields | Fallback: write status back to the spreadsheet directly, accepting weaker validation |
| R-07 | Per-row change history retained for a defined period | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Retention period; whether it is exportable | Our own `AuditLog` and `EntityVersions` already carry the authoritative trail; platform history is corroboration |
| R-08 | Dependent dropdowns driven by data | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Expression limits on large reference tables | None needed; this is standard capability |
| R-09 | Parent/child forms with many child rows | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Practical rows per form before the UI degrades (C-11) | Publish a tested per-visit photograph limit and warn above it |
| R-10 | Deep links to a specific record | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Whether a deep link honours security filters for the recipient | Notifications already carry no evidence, only a link (SEC-03) |
| R-11 | Governance: who may create apps, where data lives, admin visibility | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Whether governance is an admin-console or a higher-tier feature | Compensating control: the app is owned by the system account, and creation rights are restricted at the Workspace level |
| R-12 | Per-user licensing at a predictable cost | Must | **UNVERIFIED** | **UNVERIFIED** | *pending* | Whether field users need the same tier as office users | See §3: the user-count model drives the decision more than the tier does |
| R-13 | Data-region control for stored data | Should | **UNVERIFIED** | **UNVERIFIED** | *pending* | Which regions; whether Qatar is available (P-08 says it is not) | Residency model handles it per project: an affected project is blocked from production upload (D-12) |
| R-14 | External (non-licensed) user access | Could | **UNVERIFIED** | **UNVERIFIED** | *pending* | Cost model for client-side viewers | Not required for the MVP; clients receive documents, not app access |
| R-15 | Scheduled bots inside the platform | Could | **UNVERIFIED** | **UNVERIFIED** | *pending* | — | The orchestration layer covers scheduling |
| R-16 | Barcode / QR scanning | Could | **UNVERIFIED** | **UNVERIFIED** | *pending* | — | Manual location selection; a QR shortcut is a later convenience |

**Three of the sixteen are pipeline-blocking if unsupported:** R-02 (security filters), R-05
(webhooks) and R-06 (API). If any is unavailable on an economically acceptable tier, the capture
layer itself should be reconsidered before Phase 2 begins, not after.

## 3. Expected licensed users

Counts are the design's requirement, not an assumption about the company's staffing. Confirm before
purchase.

| Group | Who | Count | Needs the full feature set? |
|---|---|---|---|
| Office and review | General manager, business administrator, technical reviewer, finance reviewer, project manager | **5** | **Yes** — automation, API, review queues, dashboards |
| Technical administration | System administrator + backup administrator | **2** | Yes — governance and user provisioning |
| Field capture | Site supervisors and field users across active projects | **6–15**, scaling with project count | **Possibly not.** Capture, offline and image upload only |
| Break-glass | One emergency account | **1** | Only while a grant is active |
| **Total year one** | | **14–23** | |

**The pricing question that matters is not the tier, it is whether field users need the same tier as
office users.** At 15 field users, a difference of a few dollars per user per month is the difference
between a rounding error and a real annual cost. That is the first thing to establish in §5.

## 4. Cost assumptions — INDICATIVE AND UNVERIFIED

Reproduced only so the owner can size the decision. **Not official. Not to be used for purchase.**

Third-party aggregators consulted on 2026-09-11 describe three paid tiers in the region of
**$5, $10 and $20 per user per month**, with a free development tier limited to a small number of
test users, and Enterprise pricing quoted rather than listed.

Working arithmetic on those unverified figures, for scale only:

| Scenario | Office (7) | Field (15) | Indicative monthly | Indicative annual |
|---|---|---|---|---|
| All users on the middle tier | 7 × $10 | 15 × $10 | ~$220 | ~$2,640 |
| Office on the middle tier, field on the lowest | 7 × $10 | 15 × $5 | ~$145 | ~$1,740 |
| All users on the highest listed tier | 7 × $20 | 15 × $20 | ~$440 | ~$5,280 |

The spread between the first and third row is roughly $2,600 a year — worth twenty minutes of
verification.

**Every figure in this table is unverified and may be wrong.** No purchase decision should rest on
it.

## 5. Verification script for the owner

Twenty minutes, on any unrestricted network. Paste the answers back and this document becomes
verified, after which a tier can be recommended by name.

1. Open the official AppSheet pricing page. Record **each tier name and its exact per-user per-month price**, and whether the price shown is monthly or annual-billed.
2. Open the official plan-comparison or feature-availability documentation. For each of R-01 … R-16, record **the lowest tier** at which it appears, and paste the URL.
3. Answer the three blocking questions specifically:
   - At which tier are **security filters** available?
   - At which tier are **webhooks** available?
   - At which tier is the **API** available?
4. Answer the cost-driving question: **can a capture-only field user sit on a lower tier than an office user**, and does that lower tier still include offline use and image capture?
5. Confirm whether **data-region control** exists and which regions are offered.
6. Confirm the **free development tier** limits, so Phase 2A prototyping costs nothing.

When those six answers exist, the recommendation is mechanical: **the lowest tier satisfying every
Must requirement for office users, plus the lowest tier satisfying R-01, R-03, R-04, R-08 and R-09
for field users if a cheaper split is permitted.**

## 6. Requirements the platform may not support safely or economically

| Concern | Risk | Response if it materialises |
|---|---|---|
| **Byte-identical camera originals** | Re-encoding on upload regardless of quality settings (C-02) | Already covered by the approved D-13 wording; no claim is made before device testing |
| **Per-user cost at field scale** | Cost scales with headcount rather than with value | Lower tier for capture-only users; or a different capture layer |
| **Security-filter performance at volume** | Filters evaluated per user per sync; large tables slow sync | The migration threshold in `07-migration-and-versioning.md` triggers first |
| **Practical child-row limits** | "Unlimited photographs" is untested (C-11) | Publish a tested per-visit limit and warn above it |
| **Offline reliability on specific devices** | Vendor documentation describes the platform, not the company's phones | Real-device testing at the Phase 2 gate, against the profiles in `19-user-and-device-profiles.md` |
| **Data residency** | No Qatar region at the storage layer (P-08) | Per-project residency model blocks an affected project, not the system (D-12) |

## 7. What this document does not do

It does not choose a plan, quote an official price, or assert that any capability exists. Those are
verification results, and none has been obtained from an official source. The matrix exists so that
whoever performs the verification knows exactly what to ask and what each answer decides.
