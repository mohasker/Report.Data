# Change Log

All notable changes to this repository. Dates are ISO 8601.

The system uses phase-based versioning: `0.<phase>.<revision>`. Version `1.0.0` is reserved for the
accepted multi-project MVP (§14).

---

## [0.0.1] — 2026-09-10 — Phase 0 discovery

**Added**

- `MASTER_SPEC.md` — authoritative requirements baseline, v1.0, as supplied by the owner.
- `docs/00-discovery/00-DISCOVERY-SUMMARY.md` — the eight discovery outputs required by §18.
- `docs/00-discovery/01-mvp-boundary.md` — MVP scope, deferrals and acceptance mapping.
- `docs/00-discovery/02-architecture.md` — layer model, four invariants, trust boundaries, failure taxonomy.
- `docs/00-discovery/03-assumptions-register.md` — 20 labelled assumptions and the dependency list.
- `docs/00-discovery/04-open-questions.md` — 10 blocking questions with recommendations, 14 open questions.
- `docs/00-discovery/05-risk-and-controls-register.md` — 32 risks with controls and owners.
- `docs/00-discovery/06-spec-conflicts-and-platform-limits.md` — 12 specification conflicts, 12 platform limitations, 10 simplification opportunities, 7 security observations.
- `docs/00-discovery/07-phase-plan.md` — phases 0–8 with gate evidence requirements.
- `docs/00-discovery/08-phase-1-artifact-manifest.md` — exact Phase 1 deliverables.
- `docs/00-discovery/09-configuration-register.md` — every external value as a named variable, no values recorded.
- `docs/00-discovery/adr/ADR-0001` … `ADR-0008` — architecture decision records, all Proposed.
- `docs/VERSION-MANIFEST.md` — document control register.
- `README.md`, `CHANGELOG.md`, `.gitignore`.

**Not done, recorded deliberately**

- No Google Workspace, Drive, AppSheet, Make, Claude API or QuickBooks account was inspected, created or connected. No access was provided and none was requested in chat.
- No test of any kind was executed. No test result is claimed.
- No credential, key, account ID or other secret was requested, stored or committed.
- No production mutation of any kind was performed — §15 Phase 0 requires owner approval first.

**Status:** awaiting owner approval and answers to BQ-01 … BQ-10.
