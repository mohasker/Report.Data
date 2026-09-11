# Store Migration — Threshold-Based Strategy

**Document ID:** AH-SYS-P2A-018 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review
**Withdraws:** the "year 1.4" migration point, which was a single-variable extrapolation presented with more confidence than it deserved

---

## 1. What was withdrawn and why

Revision 1 of the volume document said migration would be needed "at roughly year 1.4 at 20
projects". That came from one variable — row count against a 40,000-row threshold — treated as if it
were a capacity limit. It was not:

- 40,000 rows is a **judgement about when sync becomes uncomfortable**, not a documented platform limit.
- It ignored cell count, sync time, app open time, conflicts, automation delay, API limits, error rate and administrative burden — any of which could bind first.
- It read as a forecast when it was an extrapolation from three assumptions.

**Migration is triggered by measured conditions, not by a date.** A date can still be *estimated*,
but only as a scenario, and only once the growth rate is measured.

## 2. The nine trigger conditions

Migration begins when **any one** holds for **two consecutive weekly measurements**. Two consecutive
readings, because a single bad week is usually a bad network rather than a bad architecture.

| # | Condition | Threshold | Why this number | How measured |
|---|---|---|---|---|
| T1 | **Rows in the largest table** | > 40,000 | Judgement, not a platform limit. Sync cost grows with row count and the Photos table dominates | Row count, weekly |
| T2 | **Workbook cell count** | > 60% of the platform's documented maximum | Leaves room to migrate calmly rather than urgently | Cells = rows × columns, weekly |
| T3 | **Median sync time on a field device** | > 15 seconds | Above this supervisors start avoiding the app, which starves the pipeline | Timed on the oldest handset, weekly |
| T4 | **90th percentile app open time** | > 20 seconds | The slow case is what people remember | Same |
| T5 | **Update conflicts** | > 3 per week | Spreadsheets have no row locking; recurring conflicts mean the store is the wrong shape | Error queue, weekly |
| T6 | **Automation delay** — submission to validation complete | Median > 10 minutes | Beyond this a reviewer cannot work from a live queue | `IntegrationJobs` timestamps |
| T7 | **API or rate-limit rejections** | Any sustained occurrence | A hard ceiling, not a slowdown | Error queue, by failure class |
| T8 | **Integration error rate** | > 2% of runs, excluding suppressed duplicates | Above this, operators stop trusting the queue | `IntegrationJobs`, weekly |
| T9 | **Administrative burden** | > 2 hours a week of manual data correction | The cost has moved from the machine to a person | Administrator's own log |

T1 and T2 are capacity. T3, T4 and T6 are experience. T5, T7 and T8 are correctness. T9 is the one
that usually matters first in practice and is never measured — so it is on the list.

## 3. The formula

To convert measured growth into an estimated date, for any threshold:

```
months_remaining = (threshold - current_value) / monthly_growth_rate

estimated_date  = today + months_remaining

where monthly_growth_rate = (value_this_month - value_three_months_ago) / 3
```

Use a three-month trailing average, because a single month distorted by one busy project is not a
trend. Recompute every month. **The earliest date across all nine thresholds is the one that
matters** — migration is driven by whichever binds first, not by the one being watched.

### Worked example — illustrative only

Suppose after three months of real use the Photos table holds 9,000 rows and is growing by 3,000 a
month:

```
months_remaining = (40,000 - 9,000) / 3,000 = 10.3 months
estimated_date   = today + 10 months
```

**That is a scenario, not a forecast**, and it is valid only for T1. If sync time (T3) is already at
12 seconds and rising by 1.5 seconds a month, T3 binds in two months and T1 never gets the chance.

## 4. Scenario table — what different growth rates imply

Row growth in the Photos table, against T1 only, from zero:

| Photos rows added per month | Months to 40,000 | Scenario label |
|---|---|---|
| 360 (3 projects, expected) | ~111 | Not a concern within the planning horizon |
| 1,200 (10 projects, expected) | ~33 | Comfortable |
| 2,400 (20 projects, expected) | ~17 | Plan the migration in year 1 |
| 6,000 (50 projects, expected) | ~7 | **Do not start at this scale on a spreadsheet** |
| 14,400 (20 projects, high scenario) | ~3 | **Do not start at this scale on a spreadsheet** |

**Every row is a scenario, not a forecast.** None is a prediction until real growth is measured, and
T1 is only one of nine conditions.

## 5. Measurement, from the first week

| Cadence | Measured | By |
|---|---|---|
| Weekly | T1, T2, T5, T7, T8 | Automated count, recorded in the monitoring scenario |
| Weekly | T3, T4 on the oldest handset | Administrator, timed |
| Weekly | T6 from integration timestamps | Automated |
| Monthly | T9, and recompute the formula for all nine | Administrator |
| Monthly | Publish the earliest estimated date, **labelled as a scenario** | Administrator |

Measurement starts in Phase 2B, **before any threshold can be approached**. A threshold discovered
after it is crossed is an outage; discovered on approach, it is a scheduled piece of work.

## 6. What migration involves when triggered

Because every access goes through the table contract in `model/model.json`, and nothing depends on
cell positions, sheet order or in-cell formulas:

1. Create the target store from the generated schemas.
2. Export and load, verifying row counts and checksums.
3. Re-point the capture layer's data source and the orchestration connections.
4. Re-run the full validation suite against the new store.
5. Keep the spreadsheet read-only for one reporting period as a fallback.

**Try archiving first.** Moving closed periods out of the live store addresses T1, T2, T3 and T4 at
once, costs far less than a migration, and is reversible.

## 7. Candidate targets, decided at the time

| Target | Strength | Cost |
|---|---|---|
| The platform's own database | Stronger typing and concurrency, same ecosystem, least disruption | Licence implications to verify at the time |
| Managed SQL | Strongest guarantees, no practical ceiling | Highest operational burden, and a real cost |
| Stay on spreadsheets with aggressive archiving | Cheapest | Only addresses capacity triggers, not conflicts or API limits |

The choice is made from the measurements at the time, against the specific condition that triggered
it. Choosing now would be choosing without the information that decides it.
