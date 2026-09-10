# ADR-0002 — Google Sheets as the MVP operational store, behind a table contract

**Status:** Proposed · **Date:** 2026-09-10 · **Relates to:** R-01, P-01, A-17

## Context
§4 directs starting with Google Sheets "unless scale or concurrency testing justifies migration."
Sheets is transparent, editable by a non-developer, natively integrated with the capture layer, and
requires no additional licence. It is also not a database: no transactions, no atomic increment, no
row-level locking, and degrading performance as row counts grow.

The Photos table is the growth risk — several rows per visit, per location, per day, across dozens
of projects. Assumption A-17 (tens of photographs per project per month) is a planning estimate, not
a measurement, and if it is wrong the store is wrong.

## Options
1. **Google Sheets** — fastest, transparent, weakest at scale.
2. **AppSheet Database** — stronger typing and concurrency, still inside the platform, less directly inspectable.
3. **Cloud SQL or another managed database** — strongest guarantees, highest operational burden for a company with one technical decision-maker.

## Decision
**Option 1 for the MVP, with two mandatory conditions:**
1. **A table contract.** Every table's structure, keys and access patterns are defined in the Phase 1 data dictionary and machine-readable schemas. Nothing depends on cell positions, sheet order or formulas embedded in cells. Migration then means pointing the same contract at a different store.
2. **A defined migration trigger.** Phase 1 states a measurable threshold — row counts and sync duration — at which migration to option 2 or 3 begins. Monitoring against that threshold starts in Phase 2, before it is reached.

Two consequences follow immediately and are decided here: sequential numbering does **not** live in
Sheets (ADR-0005), and no cross-table transactional guarantee is assumed anywhere in the design.

## Consequences
**Positive.** Fastest path to a working MVP. The owner can inspect and correct data directly, which
matters during early operation. No additional licence.
**Negative.** Known ceiling. No transactions — every multi-table write must be idempotent and
recoverable rather than atomic. Direct human editing is both a feature and a risk, mitigated by the
audit log and by protected ranges.
**Neutral.** Migration is planned for from day one instead of being an emergency.

## Revisit if
The Phase 1 threshold is crossed, sync duration becomes a field complaint, or concurrent-edit
conflicts appear in the error queue.
