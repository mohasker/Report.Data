# ADR-0004 — AI output is advisory only and never authoritative

**Status:** Accepted (rev 1, amended by D-06) · **Date:** 2026-09-10 · rev 1 2026-09-11
**Relates to:** operating rules 7, 10, 11 · I-4 · R-14, R-18, R-20

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
**Option 1, without exception in the MVP** — advisory only, with the scope of analysis clarified by
owner decision D-06.

**What AI may do (D-06).** Claude **may pre-analyse a submitted image to assist the technical
reviewer**, before any human decision, provided the result is clearly marked as an AI observation.
Pre-analysis is an aid to review, not a substitute for it.

**What remains prohibited.** Only **human-approved** evidence may be used to generate an official
report. AI analysis must never change a workflow approval status. The original caption and the
reviewer's decision are preserved and are never overwritten by AI output. Contradictions and
uncertainty must be flagged. Prompt-injection controls apply to images, captions, PDFs, filenames
and emails.

- AI output is stored only in `AIObservation`, `AIConfidence`, `AIAnalysisStatus` and equivalent advisory fields.
- AI never writes `ApprovedForReport`, `PercentComplete`, `EvidenceStage`, any quantity, any monetary value or any workflow status.
- AI never emits a number that reaches a document unchecked. The §9.1 output schema contains no quantity field at all, so the model has nowhere to put one even if asked.
- Narrative statements of completion must trace to approved evidence or an authorised supervisor confirmation; where the data does not support a statement, the prompt requires an explicit **DATA GAP** item instead of a guess.
- Every generated document records `AIModel` and `PromptVersion`, so any output can be reproduced and explained months later.
- Every AI observation is displayed to the reviewer as an **AI observation**, visually distinct from the supervisor's caption and from the reviewer's own decision.
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
