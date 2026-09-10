# Version Manifest — Document Control

**Purpose:** ISO 9001 document control applied to this repository. Every controlled document has an
ID, a revision, a date and an approval status. A document that has not been approved is marked as
such and may not be treated as a decision.

**Repository version:** 0.0.1 (Phase 0) · **Date:** 2026-09-10

| Document ID | Document | Rev | Date | Status |
|---|---|---|---|---|
| — | `MASTER_SPEC.md` | 1.0 | 2026-09-10 | Baseline, supplied by owner |
| AH-SYS-P0-000 | `00-DISCOVERY-SUMMARY.md` | 0 | 2026-09-10 | Awaiting owner approval |
| AH-SYS-P0-001 | `01-mvp-boundary.md` | 0 | 2026-09-10 | Awaiting owner approval |
| AH-SYS-P0-002 | `02-architecture.md` | 0 | 2026-09-10 | Awaiting owner approval |
| AH-SYS-P0-003 | `03-assumptions-register.md` | 0 | 2026-09-10 | Awaiting owner confirmation per assumption |
| AH-SYS-P0-004 | `04-open-questions.md` | 0 | 2026-09-10 | Awaiting owner decisions BQ-01 … BQ-10 |
| AH-SYS-P0-005 | `05-risk-and-controls-register.md` | 0 | 2026-09-10 | Awaiting owner approval |
| AH-SYS-P0-006 | `06-spec-conflicts-and-platform-limits.md` | 0 | 2026-09-10 | Awaiting owner approval |
| AH-SYS-P0-007 | `07-phase-plan.md` | 0 | 2026-09-10 | Awaiting owner approval |
| AH-SYS-P0-008 | `08-phase-1-artifact-manifest.md` | 0 | 2026-09-10 | Awaiting owner approval |
| AH-SYS-P0-009 | `09-configuration-register.md` | 0 | 2026-09-10 | Live register, updated as values are supplied |
| AH-SYS-ADR-0001 | Shared Drive ownership | 0 | 2026-09-10 | Proposed |
| AH-SYS-ADR-0002 | Google Sheets as MVP store | 0 | 2026-09-10 | Proposed |
| AH-SYS-ADR-0003 | Make.com as orchestrator | 0 | 2026-09-10 | Proposed |
| AH-SYS-ADR-0004 | AI is advisory only | 0 | 2026-09-10 | Proposed |
| AH-SYS-ADR-0005 | Central numbering service | 0 | 2026-09-10 | Proposed |
| AH-SYS-ADR-0006 | Approval binds to content hash | 0 | 2026-09-10 | Proposed |
| AH-SYS-ADR-0007 | Single document generation path | 0 | 2026-09-10 | Proposed |
| AH-SYS-ADR-0008 | Defer accounting integration | 0 | 2026-09-10 | Proposed |

## Revision rules

1. A change to an approved document raises its revision and adds a dated entry to `CHANGELOG.md`.
2. `MASTER_SPEC.md` is the requirements baseline. It is not edited to match the implementation; a change to requirements is a dated revision of the baseline, approved by the owner.
3. A document marked "Awaiting owner approval" is a proposal, not a decision, and must not be cited as one.
4. A superseded ADR is marked Superseded with a pointer to the ADR that replaced it. ADRs are never deleted — the record of why a decision was made and later changed is the point of keeping them.
