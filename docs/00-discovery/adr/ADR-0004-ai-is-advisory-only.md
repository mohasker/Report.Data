# ADR-0004 — AI output is advisory only and never authoritative

**Status:** Proposed · **Date:** 2026-09-10 · **Relates to:** operating rules 7, 10, 11 · I-4 · R-14, R-18, R-20

## Context
Claude is used for evidence description, narrative drafting and QA review. The temptation in every
such system is to let confident model output flow into operational fields — auto-classifying an
evidence stage, auto-approving a clear "after" photograph, filling in a quantity that appears
obvious from an image.

Every one of those shortcuts converts a probabilistic statement into a company record. If a monthly
report tells a government client that work was completed, that statement must trace to evidence a
named person approved — not to a model's confidence score.

## Options
1. **Advisory only.** AI writes to dedicated advisory fields. A human decides everything that matters.
2. **Advisory with auto-approval above a confidence threshold.** Less reviewer effort. Requires threshold tuning, a false-positive policy, and an answer to who is accountable when a threshold misfires.
3. **AI as classifier of record.** Rejected outright — it contradicts operating rules 7, 10 and 11.

## Decision
**Option 1, without exception in the MVP.**

- AI output is stored only in `AIObservation`, `AIConfidence`, `AIAnalysisStatus` and equivalent advisory fields.
- AI never writes `ApprovedForReport`, `PercentComplete`, `EvidenceStage`, any quantity, any monetary value or any workflow status.
- AI never emits a number that reaches a document unchecked. The §9.1 output schema contains no quantity field at all, so the model has nowhere to put one even if asked.
- Narrative statements of completion must trace to approved evidence or an authorised supervisor confirmation; where the data does not support a statement, the prompt requires an explicit **DATA GAP** item instead of a guess.
- Every generated document records `AIModel` and `PromptVersion`, so any output can be reproduced and explained months later.
- All text originating from captions, filenames, images and client documents is untrusted data, never instruction (§9.5).

## Consequences
**Positive.** The audit trail stays defensible. A model change cannot silently alter company records.
Accountability stays with named people, which is what a government client or an ISO auditor asks for.
**Negative.** Reviewers do more work — every photograph still needs a human decision. This is the
intended cost, and it is what the specification requires.
**Neutral.** Automation value comes from drafting and summarising rather than from deciding, which
is where language models are actually reliable.

## Revisit if
Reviewer workload proves unsustainable at portfolio scale — and then only by proposing a specific,
bounded, separately approved exception with its own accountability answer, never by relaxing the
principle generally.
