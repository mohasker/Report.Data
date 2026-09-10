# ADR-0008 — Defer accounting integration to Phase 7

**Status:** Proposed · **Date:** 2026-09-10 · **Relates to:** BQ-05, BQ-06, R-02, R-24, R-25

## Context
§4 names QuickBooks Online as the accounting source of truth. Two facts make immediate integration
unwise. First, QuickBooks Online is sold and supported by region, and Qatar is not among its
principal supported markets — so it is not yet established that a properly supported company file
exists for the Qatari entity (BQ-05). Second, the tax treatment actually applied to these contracts
has not been confirmed by the company's accountant, and §11 forbids assuming a tax position in
either direction (BQ-06).

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
- If BQ-05 establishes that QuickBooks Online is not properly usable for the Qatari entity, the accounting target is chosen explicitly at that point. Because the calculation layer is independent, that decision changes the integration, not the system.

## Consequences
**Positive.** No work is built on an unconfirmed platform or an unconfirmed tax position. The
highest-consequence irreversible action is the last thing enabled, after everything upstream of it
is proven. The company gets certificates and invoice drafts in Phase 6 regardless of the accounting
answer.
**Negative.** Manual entry into the accounting system continues until Phase 7 closes.
**Neutral.** The deterministic calculation layer is required in every scenario, so no work is
wasted under any outcome of BQ-05.

## Revisit if
BQ-05 confirms a fully supported company file and sandbox, and the owner chooses to accelerate —
which changes the schedule, not the sequence: calculation still precedes posting.
