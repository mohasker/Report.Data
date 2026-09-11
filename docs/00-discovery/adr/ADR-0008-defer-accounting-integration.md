# ADR-0008 — Defer accounting integration to Phase 7

**Status:** Accepted (rev 1, amended by D-07 and D-08) · **Date:** 2026-09-10 · rev 1 2026-09-11
**Relates to:** BQ-05, BQ-06, D-07, D-08, R-02, R-24, R-25

## Context
§4 names QuickBooks Online as the accounting source of truth, and **Al-Haram currently uses
QuickBooks Online** (D-07). QBO therefore remains the intended accounting system; the question is
not *whether* but *what is actually available*.

Two facts still make immediate integration unwise. First, it is not established that every required
integration, tax setting, project feature, class, currency or API operation is available for the
**current company configuration** — that must be inspected, not assumed (D-07). Second, the tax
treatment applied to these contracts has not been confirmed by the accountant, and no classification
may be named until it is: "zero-rated", "exempt", "out of scope" and "no tax configured" are not
interchangeable (D-08).

Building an accounting integration on either unknown would mean building on invented information,
which operating rule 2 forbids — and errors in this area are financial and legal, not cosmetic.

## Options
1. **Integrate now.** Fastest to a complete-looking system; risks building against an unsupported product and an unconfirmed tax position.
2. **Defer posting to Phase 7; build the deterministic calculation layer first, independent of the accounting product.**
3. **Abandon accounting integration; export invoices for manual entry.** Lower risk, permanent manual step.

## Decision
**Option 2.**

- Phases 1–5 contain no accounting integration of any kind.
- Phase 6 builds contracts, BOQ, certificates and **deterministic financial calculation** with a stored trace, producing invoice **drafts only**. This layer is deliberately independent of the accounting product, so the posting target can change without redesign.
- Phase 7 adds posting, in a **sandbox company first**, with finance approval and reconciliation to the last decimal before anything is marked synchronised.
- **Production posting stays disabled until the owner authorises it in writing**, after sandbox evidence exists.
- Phase 1 defines the **QuickBooks mapping fields** and the **compatibility inspection checklist** — customers, items, tax codes, classes/projects, currencies, terms, numbering and the required API operations — without connecting anything (D-07).
- The inspection checklist is a **gate before the financial-integration phase**. Where it finds a gap, the gap changes the integration, not the system, because the calculation layer is independent of the accounting product.

## Consequences
**Positive.** No work is built on an unconfirmed platform or an unconfirmed tax position. The
highest-consequence irreversible action is the last thing enabled, after everything upstream of it
is proven. The company gets certificates and invoice drafts in Phase 6 regardless of the accounting
answer.
**Negative.** Manual entry into the accounting system continues until Phase 7 closes.
**Neutral.** The deterministic calculation layer is required in every scenario, so no work is
wasted under any outcome of BQ-05.

## Revisit if
The inspection checklist confirms full capability and a sandbox is available, and the owner chooses
to accelerate — which changes the schedule, not the sequence: deterministic calculation still
precedes any posting.
