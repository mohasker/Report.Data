# ADR-0003 — Make.com as the orchestration layer

**Status:** Proposed · **Date:** 2026-09-10 · **Relates to:** BQ-03, R-07, P-05

## Context
Cross-system work — validation, file routing, AI calls, document generation, notification,
accounting sync — needs an execution layer with retries, error routing and operational visibility.
§4 names Make.com. The realistic alternative is Google Apps Script, which has no licence cost and
runs inside the same Workspace tenant.

The deciding factor is not capability. It is that the company's own assessment names heavy reliance
on one person as a weakness (R-07). An orchestration layer that only a developer can read reproduces
that weakness inside the system itself.

## Options
1. **Make.com.** Visual scenarios, built-in error handlers, data stores, execution history, scheduling. Per-operation billing.
2. **Google Apps Script.** No licence cost, native access, full programmatic control. Orchestration logic invisible to anyone who does not read code; error handling and idempotency must be hand-built; execution quotas apply.
3. **A custom application server.** Maximum control, maximum operational burden. Rejected — every additional runtime is something the company must keep alive.

## Decision
**Option 1.** Make is the orchestration layer, subject to BQ-03 confirming availability.

Every scenario must be: named to a convention · entered through a correlation ID · idempotent via a
Data Store key checked before any side effect · routed to an explicit error handler · classified per
the §12 taxonomy · capped in retries · terminated into a dead-letter queue a human can work from.

If BQ-03 is answered "no Make," the fallback is option 2 with the same guarantees implemented in
code — accepting materially higher build and maintenance cost and materially lower visibility.

## Consequences
**Positive.** Failures are visible to a non-developer. Error handling and retry are first-class
rather than hand-rolled. Execution history is inspectable, which is what makes an integration
supportable rather than mysterious.
**Negative.** Recurring licence cost, billed per operation — and per-photo processing multiplies
operations quickly (P-05). Platform dependency; scenarios are documented module by module so they
can be rebuilt elsewhere.
**Neutral.** Operation consumption must be measured in Phase 3 and the plan sized from measurement.

## Revisit if
Operation costs exceed the value delivered at real volume, or a required capability proves
unavailable on the licensed plan.
