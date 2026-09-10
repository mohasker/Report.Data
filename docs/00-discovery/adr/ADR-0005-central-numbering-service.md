# ADR-0005 — One central atomic numbering service

**Status:** Proposed · **Date:** 2026-09-10 · **Relates to:** C-04, R-05, BQ-08, §14 criterion 7

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
**Option 2.** A single numbering service, used by every document type.

- One counter per series. A series is defined by document type, and where the numbering convention requires it, by project and period.
- Atomic read-and-increment in the orchestration Data Store. No spreadsheet ever performs an increment.
- **Numbers are issued only at the moment a document is actually created** — never reserved in advance. Reserved-then-abandoned numbers leave gaps that look like missing documents to an auditor, which is exactly the suspicion a numbering system exists to prevent.
- Each series records a **starting number** that continues existing manual numbering (BQ-08).
- A uniqueness check runs before issue, and a duplicate is a hard failure — never a silent overwrite.
- Draft numbers and final accounting numbers are separate fields and separate series (§11).

## Consequences
**Positive.** No duplicates. Numbering continues the company's existing series instead of colliding
with it. One place to change the convention.
**Negative.** A single point of dependency; the counter store must be included in backup and
recovery (Scenario 13). Concurrency behaviour must be tested explicitly at the Phase 5 gate.
**Neutral.** Gaps can still occur if a document creation fails after a number is issued. This is
recorded and explainable, which is preferable to reuse.

## Revisit if
The operational store migrates (ADR-0002), in which case the counter moves to whatever atomic
primitive the new store provides.
