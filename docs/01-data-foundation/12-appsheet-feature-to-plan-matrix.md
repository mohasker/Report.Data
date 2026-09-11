# Capture Platform: Feature-to-Plan Requirements Matrix

**Document ID:** AH-SYS-P1-012 · **Revision:** 1 · **Date:** 2026-09-11
**Delivers:** D-04 · **Status:** requirements defined; **entitlements and pricing not yet verified**

> **No plan, feature entitlement or price is assumed or stated here** (D-04, operating rule 2).
> This document states what the system *needs*, how each need will be *verified* against current
> official information, and what happens if a need cannot be met safely or economically.

---

## 1. How to use this

1. Take each requirement below to current official vendor documentation, or to the vendor directly.
2. Record the verified answer in the "Verified" column with the date and source.
3. The lowest plan that satisfies every **Must** requirement is the recommendation.
4. Any **Must** that cannot be satisfied safely or economically goes to §4, which is the reason this document exists.

## 2. Requirements

| # | Requirement | Level | Why the system needs it | How to verify |
|---|---|---|---|---|
| R-01 | **Authenticated individual sign-in** for every user, no shared accounts | Must | Attribution is the point of the audit trail (A-05) | Vendor documentation on sign-in providers and per-user identity |
| R-02 | **Row-level security filters** evaluated server-side | Must | The whole segregation model rests on it. Column hiding is not security (P-04) | Documentation on security filters, and which plans include them |
| R-03 | **Offline capture with delayed sync**, including images | Must | Sites have poor coverage; a supervisor must not be blocked (§7.5) | Documentation, then **real-device testing** in Phase 2 |
| R-04 | **Image capture at the highest available fidelity**, with a configurable upload quality | Must | The write-once original must be as close to the camera file as the platform allows (D-13) | Documentation on image quality settings, then device testing |
| R-05 | **Outbound webhooks** on data change | Must | Without them the app is an island: no validation, no report pipeline (§8) | Documentation on automation tasks by plan |
| R-06 | **Inbound API** to read and write records | Must | Orchestration must write statuses back and re-read authoritative records | Documentation on API availability by plan |
| R-07 | **Per-row change history** retained for a defined period | Must | Supports the audit trail and dispute resolution | Documentation on change history and retention |
| R-08 | **Dependent dropdowns** driven by data | Must | Location filtered by project; activity filtered by project rules | Standard expression capability |
| R-09 | **Parent/child forms** with unlimited child rows within platform limits | Must | Visit → activities → photographs (§14 criterion 1) | Documentation, then measured in Phase 2 (C-11) |
| R-10 | **Deep links to a specific record** | Must | Notifications must link to the record, never to evidence (SEC-03) | Documentation on deep links |
| R-11 | **Governance controls**: who may create apps, where data may live, admin visibility | Must | The company must be able to see and control what exists | Admin console documentation |
| R-12 | **Per-user licensing at a predictable cost** for ~5–10 office users and field users | Must | A recurring per-user cost is a budget decision, not a detail (BQ-02) | Current official pricing, obtained directly |
| R-13 | **Data-region control** for stored data | Should | May be required by a client contract (D-12, P-08) | Admin documentation on data regions |
| R-14 | **External (non-licensed) user access** | Could | Only if a client is ever given direct read access — not in the MVP | Documentation on external users |
| R-15 | **Scheduled reports or bots inside the platform** | Could | The orchestration layer covers this; useful as a fallback | Documentation |
| R-16 | **Barcode/QR scanning** | Could | Would speed location selection on large sites | Documentation |

## 3. Verification record

To be completed before purchase. Empty rows are honest: nothing has been verified yet (D-14).

| # | Verified answer | Plan required | Source | Date | By |
|---|---|---|---|---|---|
| R-01 … R-16 | | | | | |

**Recommendation:** to be stated once the table is filled. It will be *the lowest plan that satisfies
every Must requirement*, with any Should requirement priced separately so the owner can decide
whether it is worth the difference.

## 4. Requirements the platform may not support safely or economically

Phase 1 stays platform-neutral enough to name these now rather than discover them in Phase 2 (D-04).

| Concern | Risk | If it materialises |
|---|---|---|
| **Byte-identical camera originals** | The platform may re-encode images on upload regardless of the quality setting (C-02, R-03) | The approved definition already covers this: write-once from first receipt, with no claim of "original device image" until device testing proves it (D-13) |
| **Per-user cost at field scale** | If every supervisor needs a full licence, cost scales with headcount rather than value | Evaluate a lower tier for capture-only users; or capture through a licensed shared supervisor device **without** shared identity; or reconsider the capture layer entirely |
| **Security-filter performance at volume** | Filters are evaluated per user per sync; large tables can make sync slow (R-01) | The migration threshold in `07-migration-and-versioning.md` triggers before it becomes a field complaint |
| **Practical child-row limits** | "Unlimited photographs" is untested (C-11) | Publish a tested per-visit limit and warn above it, rather than claiming "unlimited" |
| **Offline reliability on specific devices** | Vendor documentation describes the platform, not the company's actual phones | Real-device testing at the Phase 2 gate; document the limitation rather than promising around it (A-15) |
| **Data residency** | No Qatar data region exists at the storage layer (P-08) | Residency model already handles it per project; an affected project is blocked from production upload, not the system (D-12) |

## 5. What this does not do

It does not choose a plan, quote a price, or assert that any capability exists. Those are
verification results, and none has been obtained. The matrix exists so that when someone does the
verification, they know exactly what to ask and what depends on each answer.
