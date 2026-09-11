# Expected Storage and Image Volume

**Document ID:** AH-SYS-P2A-014 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review
**Nature:** **planning arithmetic from stated assumptions — not a measurement**

> Every input below is an assumption, shown so it can be corrected. One month of real use replaces
> all of it with measurement, and the numbers should be re-run then.

---

## 1. Assumptions

| # | Assumption | Value | Confidence |
|---|---|---|---|
| A1 | Visits per project per month | **20** (roughly one per working day) | Medium — varies by contract |
| A2 | Photographs per visit | **6** | Medium — the fixtures use 4–6 |
| A3 | Original photograph size | **2.5 MB** | Medium — a modern phone at default quality |
| A4 | Derivative (report-ready) size | **250 KB** | Good — a downscale of roughly 10:1 |
| A5 | Activities per visit | **2** | Good |
| A6 | Snags per project per month | **3** | Low |
| A7 | Documents per project per month | **1** monthly report, ~2 MB as PDF | Good |
| A8 | Retention | **7 years** for evidence, per the classification default | To confirm (EF-12) |

## 2. Volume per project per month

| Item | Calculation | Result |
|---|---|---|
| Photographs | 20 visits × 6 | **120** |
| Original storage | 120 × 2.5 MB | **300 MB** |
| Derivative storage | 120 × 250 KB | **30 MB** |
| Document storage | 1 × 2 MB | **2 MB** |
| **Storage per project per month** | | **~332 MB** |
| Spreadsheet rows | 20 visits + 40 activities + 120 photos + 3 snags + ~20 audit/approval | **~200 rows** |

## 3. Scaling

| Active projects | Photographs/month | Storage/month | Storage/year | Rows/month | Rows/year |
|---|---|---|---|---|---|
| **3** (pilot) | 360 | ~1.0 GB | ~12 GB | ~600 | ~7,200 |
| **10** | 1,200 | ~3.3 GB | ~40 GB | ~2,000 | ~24,000 |
| **20** | 2,400 | ~6.6 GB | ~80 GB | ~4,000 | ~48,000 |
| **50** | 6,000 | ~16.6 GB | ~200 GB | ~10,000 | ~120,000 |

### Seven-year retention

| Active projects | Cumulative at 7 years |
|---|---|
| 3 | ~84 GB |
| 10 | ~280 GB |
| 20 | ~560 GB |
| 50 | ~1.4 TB |

## 4. What this means for cost

**Storage is very unlikely to cost anything extra in the near term.** A paid Workspace subscription
carries pooled storage measured in terabytes per licensed user, and at 20 active projects the system
adds roughly 80 GB a year. Even at 50 projects with seven-year retention, the total sits in the low
terabytes.

**What to check** (part of the entitlement checklist, E-7): the subscription's total pooled storage
and how much is already used. The system's growth rate is the number above; whether it fits depends
on what the company is already storing.

**The signal to watch** is not the total. It is the **year-on-year growth rate** once real usage
replaces these assumptions. If photographs per visit turn out to be 15 rather than 6, every number
here multiplies by 2.5.

## 5. What this means for the spreadsheet store

The migration threshold in `../01-data-foundation/07-migration-and-versioning.md` is **40,000 rows
in the Photos table**, or median sync above 15 seconds.

| Active projects | Photos rows/year | Threshold reached |
|---|---|---|
| 3 | ~4,300 | Not within 9 years |
| 10 | ~14,400 | ~year 3 |
| 20 | ~28,800 | **~year 1.4** |
| 50 | ~72,000 | **~month 7** |

**So the spreadsheet store is right for the pilot and for roughly the first year at ten to twenty
projects — and not beyond that.** This is not a surprise; it is why the threshold was defined as a
number in Phase 1 and why monitoring starts in Phase 2 rather than when something slows down.

Archiving closed periods out of the live sheet extends this considerably, and is the cheaper move
before migrating.

## 6. What this means for orchestration operations

Roughly, per visit: 1 validation + 1 notification, plus 2 per photograph (registration, derivative).

| Active projects | Operations/month |
|---|---|
| 3 | ~800 |
| 10 | ~2,600 |
| 20 | ~5,200 |
| 50 | ~13,000 |

Orchestration bills by operation, so **this is the cost line that grows fastest with project count** —
faster than storage, and faster than licences. It is the number to measure first in Phase 3, and the
reason the cost matrix treats orchestration as a scaling cost rather than a fixed one.

Batching derivative creation, and skipping registration work for suspected duplicates, are the
levers if it matters.

## 7. AI cost, if enabled

At 6 photographs per visit and 20 visits per project per month, analysing **approved evidence only**
on downscaled derivatives: roughly 100 images per project per month. At 20 projects that is 2,000
images a month.

Cost is bounded by the owner's hard monthly cap rather than by this estimate (EF-04). Analysis is
per-project configurable and off wherever a residency rule forbids it.

## 8. When to re-run these numbers

After **one month** of real use on the pilot projects. Replace A1, A2 and A3 with measurements, and
the rest of this document recomputes itself. Everything above is arithmetic on three assumptions;
if those three are right, the rest follows.
