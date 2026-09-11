# AI Prompt and Schema Specification

**Document ID:** AH-SYS-P1-015 · **Revision:** 2 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **No API call has been made**
**Implements:** D-06, **D-17, D-19, D-20** · **Relates to:** ADR-0004 rev 1, ADR-0009, spec §3a, §9
**Revision 2** adds batch analysis for a capture batch, the nine forbidden inferences, and the
separation between a proposal and a confirmed value.
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
| Propose an evidence stage, activity text, caption, visible condition, possible snag, quality warning, uncertainty and confidence — each to its **own advisory column** (D-17) | Writing any of them into the confirmed column. The supervisor confirms or corrects; `AIProposalDisposition` records which |
| Suggest the formatted text that accompanies a native share | Performing the share, choosing the destination, or asserting that it was delivered |

### The nine inferences that are forbidden outright (D-19)

AI may describe only **visually supportable** conditions and activities. It must not infer or
confirm:

1. measured quantity
2. hidden defect, or its cause
3. exact material brand
4. compliance with contract or specification
5. exact completion percentage
6. exact project or location from the photograph alone
7. responsibility or negligence
8. date, unless supplied as trusted metadata
9. that Al-Haram executed the visible work merely because it appears in the photograph

**Project, location, date, assigned user, contract and work-order context come from trusted system
data**, are supplied to the model as context rather than asked of it, and are closed to AI writes by
declaration and by check `CAP-14`. Sixteen columns are closed in total.

Two rules govern everything else:

1. **Only human-approved evidence may generate an official report.** Analysis may run earlier, to help; generation may not.
2. **AI output is stored in advisory fields only**, excluded from every content hash, so an observation arriving after an approval can never void it (GOV-09, HASH-05).

## 2. Prompt set

Four separate, versioned prompts. Never one general-purpose prompt, because the constraints differ
and a shared prompt inherits the loosest of them.

| Prompt | Version | Input | Output | Phase |
|---|---|---|---|---|
| `evidence-analysis` | v1 | One downscaled derivative image, plus minimal metadata | `evidence-analysis.v1.json` | 4 |
| `evidence-analysis-batch` | v1 | **Every derivative in one capture batch**, in capture order, plus minimal metadata | `evidence-analysis-batch.v1.json` | 4 |
| `report-narrative` | v1 | Structured approved records only — **no images** | Structured sections, no numbers | 5 |
| `report-qa` | v1 | The generated draft plus the records it was built from | `report-qa.v1.json` | 5 |
| `invoice-narrative` | v1 | Approved service description fields only | Prose only | 6 |

Every generated document records `AIModel` and `PromptVersion`, so any output can be reproduced and
explained months later.

### Why analysis is batched by capture, not by photograph

The capture-once correction makes the **capture batch** the natural unit: the supervisor captures
once, so the set is analysed once. It is also the only affordable unit. A six-module per-photograph
scenario costs six Make operations per photograph — roughly **2,160 operations a month at three
projects, more than twice the entire allowance**
([`../02a-plan/23-operations-budget.md`](../02a-plan/23-operations-budget.md)). One request per
capture batch replaces that with one.

In **Quick Share** the batch request runs *after* the share and nobody waits for it. In **AI Reviewed
Share** it runs before, and its latency is the supervisor's latency — which is why it must be one
request rather than six.

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

`schemas/ai/evidence-analysis.v1.json`, `schemas/ai/evidence-analysis-batch.v1.json` and
`schemas/ai/report-qa.v1.json`, all closed (`additionalProperties: false`).

The evidence schemas contain **no numeric quantity, measurement, area, length, count, brand,
compliance, responsibility or completion-percentage field of any kind**. A model cannot report a
quantity because there is nowhere to put one. That is a structural control rather than an
instruction, and it is why the governance checks can assert that no AI field ever reaches a content
hash or a monetary path (GOV-09, GOV-11), and why `CAP-13` can assert that no quantitative or
contractual column is AI-sourced.

The batch schema adds three things and no new authority: `capture_batch_id` and `capture_sequence`,
echoed rather than chosen, so the analysis binds to evidence captured once; `batch_observations`,
for what is only visible across a set — an apparent Before/During/After sequence, an apparent
duplicate, a gap in coverage — which creates nothing, merges nothing and deletes nothing; and
`suggested_group_summary`, a **suggestion** for the text accompanying a native share, shown to the
supervisor for confirmation and never sent by the system.

`photo_ref` is deliberately an opaque reference: **never a Drive file identifier, never a URL, never
a public link.**
