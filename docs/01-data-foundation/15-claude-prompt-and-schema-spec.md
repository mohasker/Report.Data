# AI Prompt and Schema Specification

**Document ID:** AH-SYS-P1-015 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **No API call has been made**
**Implements:** D-06 · **Relates to:** ADR-0004 rev 1, spec §9
**Status:** specifications and schemas defined. **No API credential exists and no call is made** (D-14)

---

## 1. What AI may and may not do

The owner's correction to ADR-0004 defines the boundary precisely:

| Permitted | Prohibited |
|---|---|
| Pre-analyse a **submitted** photograph to assist the technical reviewer, clearly marked as an AI observation | Changing any workflow or approval status |
| Draft narrative prose from structured, already-approved records | Deciding whether evidence is approved |
| Review a draft and report issues | Producing any quantity, measurement, percentage or monetary figure |
| Suggest a professional caption **alongside** the supervisor's own | Overwriting the supervisor's caption or the reviewer's decision |
| Flag a contradiction between a caption and an image | Resolving that contradiction |
| Emit an explicit `DATA GAP` where information is missing | Filling a gap by inference |

Two rules govern everything else:

1. **Only human-approved evidence may generate an official report.** Analysis may run earlier, to help; generation may not.
2. **AI output is stored in advisory fields only**, excluded from every content hash, so an observation arriving after an approval can never void it (GOV-09, HASH-05).

## 2. Prompt set

Four separate, versioned prompts. Never one general-purpose prompt, because the constraints differ
and a shared prompt inherits the loosest of them.

| Prompt | Version | Input | Output | Phase |
|---|---|---|---|---|
| `evidence-analysis` | v1 | One downscaled derivative image, plus minimal metadata | `evidence-analysis.v1.json` | 4 |
| `report-narrative` | v1 | Structured approved records only — **no images** | Structured sections, no numbers | 5 |
| `report-qa` | v1 | The generated draft plus the records it was built from | `report-qa.v1.json` | 5 |
| `invoice-narrative` | v1 | Approved service description fields only | Prose only | 6 |

Every generated document records `AIModel` and `PromptVersion`, so any output can be reproduced and
explained months later.

## 3. Data minimisation

What is sent, and what is deliberately withheld.

| Prompt | Sent | Never sent |
|---|---|---|
| `evidence-analysis` | One downscaled derivative; activity name; recorded evidence stage; the supervisor's caption; visit date | The original file · client name · project name · location name · GPS coordinates · user identities · any rate, quantity or contract value |
| `report-narrative` | Approved activity records, approved captions, snag records, period, project reference | Contract values · rates · invoice figures · client contact details · unapproved evidence |
| `report-qa` | The draft and the records it was built from | Anything not already in the draft |
| `invoice-narrative` | Service description fields | **Every** quantity, rate, tax, retention, discount and total (spec 9.4) |

Three consequences worth stating:

- **The original file never leaves the tenant.** Only a derivative is analysed, which also means no processing path opens the write-once original (D-13, P-07).
- **Location and client names are withheld** so that a model cannot "recognise" a site and assert something about it that the image does not show.
- **The narrative prompt receives no images at all.** It writes from records; the images are evidence for humans.

## 4. Injection defence

Text found in an image, a caption, a filename, a PDF or an email is **untrusted data, never
instruction** (spec 9.5). Controls:

1. Untrusted content is wrapped and labelled as data in every prompt.
2. The system instruction states that embedded instructions are to be ignored and reported.
3. The output schema is closed: there is no field through which an injected instruction could express itself.
4. The model has **no tool access** — it cannot send, write, approve or fetch anything.
5. `prompt_injection_detected` lets the model report an attempt without acting on it.
6. Output is schema-validated before storage; a non-conforming response is dead-lettered, never coerced into shape.

Phase 4's gate requires an executed test: a caption containing an embedded instruction, and an image
containing visible instruction text, must both be ignored, with the result recorded.

## 5. Cost control

| Control | Mechanism |
|---|---|
| Hard monthly cap | Set by the owner on the API workspace (BQ-04, EF-04) |
| Analyse derivatives, not originals | Cost scales with image size; a downscaled derivative is a fraction of the cost |
| One analysis per photograph | Re-analysis requires an explicit request; the result is cached against the photograph |
| Output token cap per call | Configured per prompt |
| Skip ineligible evidence | Suspected duplicates and photographs on AI-disabled projects are never sent |
| Per-project usage recorded | Cost is attributable to the contract that generated it |
| Measured before scaling | Cost per 100 photographs is measured at the Phase 4 gate, not estimated |

## 6. Failure behaviour

AI failure must never block the pipeline, because the pipeline does not depend on AI.

| Failure | Behaviour |
|---|---|
| Provider unavailable or rate-limited | Retriable; capped backoff; `AIAnalysisStatus = Failed` on exhaustion. **Review proceeds without it** |
| Schema-invalid response | `SchemaInvalid`; dead-lettered with the sanitised payload; never coerced |
| Project has AI disabled by a residency rule | `Disabled`; never sent (D-12, SEG-12) |
| Photograph is a suspected duplicate | `Skipped` |
| Response contains a number the schema does not allow | Rejected by schema validation — the field does not exist |

## 7. How AI output reaches a person

In the reviewer's view, three things are visually distinct and never merged:

1. **The supervisor's caption** — their words, unchanged.
2. **The AI observation** — labelled as an AI observation, with its confidence and any flagged contradiction.
3. **The reviewer's own decision and comment** — the only one of the three that has any authority.

A reviewer who disagrees with an AI observation records their decision and moves on. Nothing asks
them to justify disagreeing with a model.

## 8. Schemas

`schemas/ai/evidence-analysis.v1.json` and `schemas/ai/report-qa.v1.json`, both closed
(`additionalProperties: false`).

The evidence schema contains **no numeric quantity, measurement, area, length or count field of any
kind**. A model cannot report a quantity because there is nowhere to put one. That is a structural
control rather than an instruction, and it is why the governance checks can assert that no AI field
ever reaches a content hash or a monetary path (GOV-09, GOV-11).
