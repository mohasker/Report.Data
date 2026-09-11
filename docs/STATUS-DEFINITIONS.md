# Acceptance Status Definitions

**Document ID:** AH-SYS-GOV-001 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Approved — set by the owner on 2026-09-11

These seven statuses are the only ones used to describe the maturity of any artifact in this
repository. They are applied consistently in document headers, the version manifest, the change log
and every progress report.

| Status | Means | Does **not** mean |
|---|---|---|
| **Completed** | The artifact has been created. | That it works, that it is correct, or that anyone has looked at it. |
| **Validated Locally** | Internal automated checks passed against synthetic data in this repository. | That any external platform works. Local checks prove a rule, not a system. |
| **Submitted for Owner Review** | Awaiting business and design acceptance by the owner. | Approved. |
| **Approved** | Expressly accepted by the owner. | That it has been built, connected or tested against a real platform. |
| **Verified in Integration** | Tested against the actual external platform it depends on. | Production ready — integration success is not the same as operational readiness. |
| **Production Ready** | All applicable security, field, integration, recovery and acceptance tests have passed. | Live. |
| **Live** | Explicitly deployed and authorised for real use. | — |

## Rules

1. **A status is never claimed without the evidence that supports it.** "Validated Locally" points to an executed run; "Verified in Integration" points to a recorded integration test; "Approved" points to a written owner decision.
2. **A status never skips forward.** Nothing is Production Ready without having been Verified in Integration first.
3. **Local validation is never reported as integration verification.** This is the failure mode the vocabulary exists to prevent: a passing local check suite says a *rule* is right, not that AppSheet, Drive, Make, the Claude API, QuickBooks, a phone or a PDF renderer behaves as designed.
4. **A regression moves the status back.** An artifact that was Approved and has since changed materially returns to Submitted for Owner Review.

## Current position

| Scope | Status | Evidence |
|---|---|---|
| Phase 0 — Discovery | **Approved** | Owner decision, 2026-09-11 (`00-discovery/10-owner-decisions.md`) |
| Phase 0 revision 1 | **Approved** | Owner acceptance, 2026-09-11 |
| **Phase 1 — Data foundation** | **Completed, Validated Locally, Submitted for Owner Review** | `01-data-foundation/17-validation-evidence.md` — 172 checks executed |
| Phase 2A — Plan and synthetic prototype design | **Completed, Submitted for Owner Review** | `docs/02a-plan/` |
| Everything requiring an external platform | **Not started** | No connection exists (D-14) |

**Nothing in this repository is Verified in Integration, Production Ready, or Live.**
