# ADR-0005 — One central atomic numbering service

**Status:** Accepted (rev 1, amended by D-10) · **Date:** 2026-09-10 · rev 1 2026-09-11
**Relates to:** C-04, R-05, BQ-08, D-10, §14 criterion 7

## Context
Reports, completion certificates and invoices carry document numbers that appear in client
correspondence, contracts and accounting records. §2 forbids duplicate numbering across projects.
§14 criterion 7 forbids duplicate jobs and documents.

A spreadsheet cannot guarantee this. Reading "the last number" and writing "the next one" is not
atomic, so two concurrent generations can produce the same number. Manual numbering series also
already exist in the company's current documents (A-18), and a system that restarts a series
already in use is worse than one that has no numbering at all.

## Options
1. **Formula in a sheet** (`MAX + 1`). Simple, and wrong under concurrency.
2. **A central numbering service** with one counter per series in a Data Store, updated atomically.
3. **Random or hash-based identifiers.** Collision-free, and unacceptable — humans and clients need readable, ordered document numbers.

## Decision
**Option 2, as amended by D-10.** One numbering **service**, many configurable **series** — never a
single undifferentiated sequence.

**A series is configured by:** legal entity · document type · calendar or financial year · scope
(project-specific or company-wide, as configured) · optional client-specific requirement · revision
handling. Illustrative formats only, pending review of the existing manual register:
`AH-TR-YYYY-NNN` technical report, `AH-QT-YYYY-NNN` quotation, `AH-CC-YYYY-NNN` completion
certificate, and other controlled types as configured.

**Number lifecycle — reserved → issued → cancelled (D-10).** Revision 0 of this ADR stated that
numbers are never reserved. The owner has replaced that with an explicit, recorded lifecycle:
- **Reserved** — allocated to a specific document job, atomically, before generation.
- **Issued** — bound to a created document.
- **Cancelled** — a reserved number whose job failed or was abandoned. It is recorded as cancelled with a reason and is **never silently reused**, so a gap in the register is always explained rather than merely observed.

**Also required:**
- Atomic read-and-increment. No spreadsheet ever performs an increment. Concurrent requests must not collide, and this is tested, not assumed.
- Each series records a **starting number** that continues the existing manual register, with a documented migration of that register (D-10).
- A uniqueness check before issue; a duplicate is a hard failure, never a silent overwrite.
- Draft numbers and final accounting numbers are separate fields and separate series. **Invoice numbering stays aligned with the approved accounting and QuickBooks process** (§11, D-07).

## Consequences
**Positive.** No duplicates. Numbering continues the company's existing series instead of colliding
with it. One place to change the convention.
**Negative.** A single point of dependency; the counter store must be included in backup and
recovery (Scenario 13). Concurrency behaviour must be tested explicitly at the Phase 5 gate.
**Neutral.** Gaps occur when a reserved number is cancelled. Each is recorded with a reason, so the
register explains itself to an auditor — which is the point, and is preferable to reuse.

## Revisit if
The operational store migrates (ADR-0002), in which case the counter moves to whatever atomic
primitive the new store provides.
