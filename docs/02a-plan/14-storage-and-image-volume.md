# Storage and Image Volume — Assumptions and Three Scenarios

**Document ID:** AH-SYS-P2A-014 · **Revision:** 2 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review
**Nature:** arithmetic from stated assumptions. **Not a measurement, and not a forecast.**

> Revision 1 described roughly 80 GB a year as "a non-issue". That was withdrawn: whether it is an
> issue depends on the company's actual allocation and current consumption, neither of which is
> known. This revision states every assumption, gives low, expected and high scenarios, and lists
> what the projection must be compared against.

---

## 1. Every assumption, stated

| # | Assumption | Low | **Expected** | High | Where it comes from |
|---|---|---|---|---|---|
| A1 | Visits per project per month | 10 | **20** | 30 | Roughly one per working day at the expected level |
| A2 | Activities per visit | 1 | **2** | 4 | Fixture pattern |
| A3 | Photographs per activity | 2 | **3** | 6 | Before and after, plus an observation |
| A4 | → Photographs per visit (A2 × A3) | 2 | **6** | 24 | Derived |
| A5 | Average original image size | 1.5 MB | **2.5 MB** | 5.0 MB | Modern phone at default quality. **The single most uncertain input** |
| A6 | Derivatives per photograph | 1 | **1** | 2 | Report-ready; a second if AI analysis needs a smaller one |
| A7 | Average derivative size | 150 KB | **250 KB** | 400 KB | Roughly 10:1 downscale |
| A8 | Documents per project per month | 1 | **1** | 3 | Monthly report; more if weekly reporting is enabled |
| A9 | Average document size | 1 MB | **2 MB** | 5 MB | PDF with embedded photographs |
| A10 | Duplicate and re-capture overhead | 0% | **5%** | 15% | Suspected duplicates are flagged and **retained**, never deleted |
| A11 | Retention period | 3 years | **7 years** | 10 years | Classification default; unconfirmed (EF-12) |

**A5 and A4 dominate everything.** If photographs per visit is 24 rather than 6, and images are
5 MB rather than 2.5 MB, the high scenario is **eight times** the expected one.

## 2. Per project per month

| Item | Low | **Expected** | High |
|---|---|---|---|
| Photographs | 20 | **120** | 720 |
| Originals | 30 MB | **300 MB** | 3,600 MB |
| Derivatives | 3 MB | **30 MB** | 576 MB |
| Documents | 1 MB | **2 MB** | 15 MB |
| Duplicate overhead (A10) | 0 MB | **17 MB** | 629 MB |
| **Storage total** | **~34 MB** | **~349 MB** | **~4,820 MB** |
| Rows (visits + activities + photos + snags + approvals + audit) | ~90 | **~624** | ~2,900 |

## 3. Scaling by active projects

### Storage per year

| Active projects | Low | **Expected** | High |
|---|---|---|---|
| 3 | 1.2 GB | **12.6 GB** | 174 GB |
| 10 | 4.1 GB | **41.9 GB** | 578 GB |
| 20 | 8.2 GB | **83.8 GB** | 1,157 GB |
| 50 | 20.4 GB | **209.4 GB** | 2,892 GB |

### Cumulative at the retention period (A11)

| Active projects | Low (3 yr) | **Expected (7 yr)** | High (10 yr) |
|---|---|---|---|
| 3 | 3.7 GB | **88 GB** | 1.7 TB |
| 10 | 12.2 GB | **293 GB** | 5.8 TB |
| 20 | 24.5 GB | **587 GB** | 11.6 TB |
| 50 | 61.2 GB | **1.5 TB** | 28.9 TB |

**The high scenario at scale is a genuine storage problem**, not a rounding error. It is reached by
24 photographs per visit at 5 MB each — which is not implausible if supervisors photograph
generously and nobody constrains image size.

## 4. What this must be compared against — none of it is known yet

The projection alone decides nothing. It has to be set against:

| # | To compare against | How to find it | Why it matters |
|---|---|---|---|
| 1 | **Actual Workspace storage allocation** | Admin Console → Storage (step 5 of the owner checklist) | Determines whether any of the above fits |
| 2 | **Current consumption** | Same screen | Headroom is allocation minus what is already used, not the allocation |
| 3 | **Pooled vs per-user storage** | Depends on the Workspace edition | Pooled storage is shared across the company; per-user is not, and a Shared Drive draws on the pool |
| 4 | Drive upload and sharing limits | Workspace admin documentation | A daily upload ceiling would throttle a bulk month |
| 5 | **Backup and export requirements** | Owner policy (EF-12) | A second copy **doubles** every number above |
| 6 | **Retention period** | Owner policy and client contracts (EF-12, EF-16) | A11 is currently an assumption, not a decision |
| 7 | Duplicate and derived-image overhead | Design, above | Already in A6, A7 and A10 |
| 8 | Report and PDF storage | A8, A9 | Small relative to photographs, and grows with reporting frequency |
| 9 | **Data-residency restrictions** | Contract review (EF-16) | A restriction could force a different storage location entirely, which changes the cost basis rather than the volume |

**Until items 1, 2 and 3 are known, no statement about whether storage is sufficient can be made.**
That is why the owner checklist asks for the storage screen.

## 5. What can be said now

| Statement | Confidence |
|---|---|
| Photographs are ~95% of all storage and ~20% of all rows | **High** — structural, not an estimate |
| The expected scenario adds tens of gigabytes a year at ten to twenty projects | Medium — depends on A4 and A5 |
| The high scenario adds hundreds of gigabytes a year at the same project count | Medium |
| A second backup copy doubles the requirement | **High** |
| Whether any of this fits the existing subscription | **Unknown.** Depends on items 1–3 above |

## 6. Levers, if volume becomes a problem

In the order worth trying:

1. **Cap image upload quality in the app.** Moving A5 from 5 MB to 2.5 MB halves everything. It is one setting, and it is already in the design as the highest fidelity the platform allows — the trade-off against evidence quality is the owner's to make.
2. **Archive closed periods** out of the live store to cold storage. Reduces sync load as well as cost.
3. **Constrain photographs per activity** through the evidence rules — a minimum already exists; a soft maximum with a warning is a one-row change.
4. **Stop generating a second derivative** where AI analysis is disabled for a project.
5. **Review retention** against what contracts actually require, rather than the default.

## 7. When to replace this with measurement

After **one month** of real use. Replace A1, A4 and A5 with observed values and every number here
recomputes. Everything above rests on three inputs; if those three are right, the rest follows, and
if they are wrong, the rest is wrong in exactly the same proportion.
