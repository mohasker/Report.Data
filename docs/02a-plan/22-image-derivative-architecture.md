# Image Derivative Architecture — Three Classes and How AI Analysis Gets Its Copy

**Document ID:** AH-SYS-P2A-022 · **Revision:** 3 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Nothing connected, no API call made**
**Corrects:** the rule that image bytes must "never" pass through the orchestration layer, which conflicted with visual AI analysis
**Revision 3** applies D-24: not every captured photograph needs a model call. Duplicates, unusable
images, and anything deleted or excluded are filtered out **before** the call, which brings the
volume back down from every captured photograph to roughly 83% of them. Revision 2's figures were
the unfiltered case and are superseded.

---

## 1. The correction

The earlier absolute — *image bytes must never pass through Make* — was wrong as stated. Claude
analyses a photograph by **seeing** it; metadata alone cannot produce a visual observation. The rule
needed to be about *which* image, not about all images.

**Three distinct image classes, each with its own rule:**

| Class | What it is | Where it lives | May it leave the tenant? | May it pass through orchestration? |
|---|---|---|---|---|
| **Original evidence** | The file as first received by the controlled system | `01_Original_Evidence`, write-once | **No** | **No.** Never downloaded, never re-encoded, never opened by any processing path |
| **AI review derivative** | A controlled resized copy made solely for analysis | `02_Derived_Images/ai/` | **Yes**, to the AI provider only, and only when the project permits it | **Yes**, if that transfer path is chosen — see §4 |
| **Report derivative** | A controlled optimised copy placed in generated documents | `02_Derived_Images/report/` | Only inside a released document | Yes, at document-generation time |

**Originals are never compressed.** Both derivatives are produced *from* the original and never
replace it. The original's checksum is recorded at registration and re-verified; a derivative has its
own record and its own lifecycle.

## 2. Derivative specifications

| | AI review derivative | Report derivative |
|---|---|---|
| Purpose | Visual analysis by the model | Printed in a report at readable size |
| Long edge | **1024 px** initially | 1600 px |
| Format | JPEG, quality ~80 | JPEG, quality ~85 |
| Expected size | **~250–600 KB**, inside the owner's 500 KB–1.5 MB target | ~400–800 KB |
| Colour | Unchanged | Unchanged |
| Annotation | **None.** No overlays, no stamps — an annotated image is a different claim | Caption and identifier are page furniture, not burned into the image |
| Retention | **Deleted 7 days after analysis completes** | Retained with the document |
| Reproducible? | Yes, from the original at any time | Yes |

**Why 1024 px.** Claude counts image cost in 28×28-pixel patches: an image costs
`⌈width ÷ 28⌉ × ⌈height ÷ 28⌉` visual tokens. A 1024×768 derivative is
`37 × 28 = 1,036` visual tokens. The same photograph at 2000×1500 costs 3,888 — **3.75× the tokens
for detail a condition assessment rarely needs.** Quality is confirmed by testing before the value is
fixed; 1024 px is the starting point, not a conclusion.

**Why deletion is allowed here.** Nothing in the evidence rules is being deleted. An AI derivative is
a *reproducible artifact* of an original that is itself never deleted, and the analysis result is
stored permanently in the photograph's advisory fields. Deleting the derivative loses nothing that
cannot be regenerated.

## 3. What the AI provider does with the image

Verified from Anthropic's vision documentation:

| Fact | Value |
|---|---|
| Accepted sources | base64 in the request, a **URL**, or a `file_id` from the Files API |
| Maximum image size | **10 MB base64** on the Claude API |
| Maximum dimensions | 8000 × 8000 px |
| Cost model | `⌈w/28⌉ × ⌈h/28⌉` visual tokens; images above the model's resolution tier are downscaled automatically |
| Formats | JPEG, PNG, GIF, WebP |
| **Metadata** | **Not read.** The model receives no EXIF, no location, no capture time |
| **Retention** | **"Image uploads are ephemeral and not stored beyond the duration of the API request. Uploaded images are automatically deleted after they have been processed."** |
| Training | Anthropic does not use uploaded images to train models |

Two consequences for this design:

1. **Send base64 in the request, not a Files API upload.** A `file_id` persists until deleted, which creates a second copy to manage. In-request base64 is ephemeral by construction, which is the retention behaviour this system wants.
2. **The URL source is rejected for this system.** It would require a publicly fetchable address, and evidence is never publicly shared. The owner's instruction and the architecture agree.

## 4. How the derivative reaches Claude — three options

### Option A — through Make *(recommended for the controlled pilot)*

```
Drive (AI derivative)  →  Make: download  →  base64  →  Anthropic API  →  JSON result  →  Sheet
```

| | |
|---|---|
| Strengths | One place to see the whole pipeline; error handling, retries and the idempotency key already live there; nothing new to build |
| Costs | Consumes Make **transfer** and **operations**; subject to Make's **5 MB file-size limit** — a 250–600 KB derivative is comfortably inside it |
| Transfer at pilot volume | See §5 |
| Verdict | **Use for the pilot.** Simple, observable, and inside the verified limits at pilot scale |

### Option B — a processing component inside Workspace *(recommended at scale)*

```
Drive (AI derivative)  →  Apps Script in the company tenant  →  base64  →  Anthropic API
Make orchestrates by passing identifiers only; no image bytes cross it
```

| | |
|---|---|
| Strengths | **Image bytes never touch the orchestration layer at all** — no transfer consumption, no 5 MB ceiling, one fewer processor in the data-flow map |
| Costs | A second component to maintain and monitor; its own execution quotas; its failures must still land in the same error queue |
| Verdict | **The right answer once volume grows**, and the only one that scales past Make's transfer limit |

### Option C — a temporary signed reference

Rejected. The URL source needs a publicly fetchable address; a Drive "anyone with the link" URL is
exactly what the owner forbade and what the evidence rules forbid. Building a signing service to
avoid moving a 400 KB file is more moving parts, not fewer.

**Decision: Option A for the controlled pilot, Option B before the estate grows.** Both keep the
original untouched; they differ only in which component reads the derivative.

## 5. The numbers, under Option A

Assumptions stated: expected scenario, three pilot projects, 120 photographs per project per month,
derivative 400 KB average.

**The volume assumption has moved twice, and this is where it settled.** Revision 1 analysed only
the ~60% of photographs a reviewer later approved — wrong, because a proposal arriving after the
review decision proposes nothing to anybody. Revision 2 therefore analysed *every* captured
photograph — also wrong, in the other direction, because a blurred shot, a near-duplicate and an
image the supervisor deleted are all worth nothing to analyse. **Revision 3 analyses the eligible
ones (D-24).**

**Eligibility, estimated and labelled as such** (`model/model.json` →
`capture_once.ai_analysis_policy`): near-duplicates ~8%, below the quality threshold ~5%, deleted or
excluded before analysis ~4%. **Eligible: ~83%.** Deferred Quick Share applies all three filters;
immediate AI Reviewed Share applies the first two, because it cannot know what the supervisor will
later exclude.

| Quantity | Pilot (3 projects) | 10 projects | 20 projects |
|---|---|---|---|
| Photographs captured per month | 360 | 1,200 | 2,400 |
| *Analysed — rev 1, approved only (~60%)* | *216* | *720* | *1,440* |
| *Analysed — rev 2, every captured photograph* | *360* | *1,200* | *2,400* |
| **Analysed — rev 3, Quick Share (~83%)** | **299** | **996** | **1,992** |
| **Analysed — rev 3, AI Reviewed Share (~92%)** | **331** | **1,104** | **2,208** |
| Average derivative size | 400 KB | 400 KB | 400 KB |
| **Make transfer per month** (Quick Share) | **~120 MB** | **~398 MB** | **~797 MB** |
| Against the verified 512 MB/month limit | **23%** | **78%** | **156% — breached** |
| 5 MB per-file compliance | ✅ 400 KB, 8% of the limit | ✅ | ✅ |

**Option A holds at pilot scale and is uncomfortable by ten projects.** Filtering buys headroom —
78% of the transfer limit at ten projects rather than 94% — but it does not change where the ceiling
is. The threshold to move to Option B, a Workspace-side component that never routes bytes through
the orchestration layer, is **ten projects, or 400 MB of measured monthly transfer, whichever comes
first.**

**And the filters cost nothing to run.** Perceptual hashing for near-duplicates and a blur measure
run locally, with no model call and no transfer. `Photos.PerceptualHash`, `Photos.QualityScore` and
`Photos.AnalysisEligibility` carry the result, and a skipped photograph is **retained as evidence** —
skipping is about waste, never about coverage.

### Claude input cost

Per analysed photograph, at 1024×768 (1,036 visual tokens) plus ~600 tokens of prompt and caption,
returning ~500 output tokens of schema-valid JSON:

| Model | Input | Output | **Per image** | **Pilot, Quick Share (299/mo)** | **Pilot, AI Reviewed (331/mo)** | 20 projects, Quick Share (1,992/mo) |
|---|---|---|---|---|---|---|
| **Claude Opus 5** (default) | ~1,636 tok @ $5/M = $0.0082 | ~500 tok @ $25/M = $0.0125 | **~$0.021** | **~$6.28** | **~$6.95** | ~$42 |
| Claude Haiku 4.5 (owner's choice, if wanted) | @ $1/M = $0.0016 | @ $5/M = $0.0025 | ~$0.004 | ~$1.20 | ~$1.32 | ~$8 |

**Estimates, not measurements.** Every figure rests on the eligibility proportions above and on
360 photographs a month. All of them are replaced by counts in the pilot's first month.

*(Revision 1 quoted ~$4.50 on the approved-only volume; revision 2 quoted ~$7.56 on the unfiltered
volume. Both are superseded rather than wrong — each was right for the workflow as it then stood.)*

**Filtering saves about 17% of the Claude bill** at pilot volume — roughly a dollar a month, which
is not the point. The point is at twenty projects, where it is about eight dollars a month and
growing linearly, and where the transfer ceiling arrives sooner than the money does.

**Batching does not change the per-image cost**, because the images are the tokens. What it changes
is the **orchestration** cost: one request per capture batch rather than one per photograph is the
difference between 703 Make operations and roughly 2,160 (`23-operations-budget.md`).

Opus 5 is the default. Haiku is listed because the owner may reasonably choose it for a per-image
classification task — **that is a decision for the owner, not a change I would make to save money.**
A pilot at roughly five dollars a month is not where cost discipline matters.

If the derivative were left at 2000×1500 instead of 1024×768, the input cost roughly **triples** with
no change to anything else.

**A cap the owner sets still bounds all of this** (EF-04). At pilot volume the cap is not the binding
constraint; at twenty projects it is, and that is the point of having one.

## 6. What is sent, and what is not

| Sent with each analysis | Deliberately withheld |
|---|---|
| One AI derivative (never the original) | The original file |
| The activity name | The client name |
| The recorded evidence stage | The project name |
| The supervisor's caption | The location name |
| The visit date | GPS coordinates |
| | Any user identity |
| | Any rate, quantity or contract value |

Withholding client, project and location names is deliberate: a model that "recognises" a site can
assert things the photograph does not show.

## 7. Pilot policy

| Rule | Status |
|---|---|
| **Only reviewer-approved or reviewer-selected photographs are analysed** | **Default for the pilot**, per the owner |
| Pre-analysis of submitted evidence before review | **Off.** Switching it on roughly doubles the image count and must be costed first |
| Per-project switch | `Projects.AIAnalysisEnabled`, already in the model |
| Residency override | A project whose contract forbids third-party processing is never analysed, whatever the switch says |
| Result storage | Advisory fields on the photograph; never overwrites the caption or the reviewer decision |
| Derivative deletion | 7 days after analysis; the original and the result both persist |

## 8. What must be tested before any of this runs

1. **Image quality at 1024 px** — can a reviewer and the model both still see what matters? Test on real photographs of turf, irrigation fittings and ceiling tiles before fixing the size.
2. **Derivative size distribution** — the 400 KB average is an estimate; measure it.
3. **Transfer consumption** under Option A, measured rather than projected.
4. **Cost per 100 analyses**, measured at the Phase 4 gate.
5. **That the original is untouched** after derivative creation — checksum comparison, recorded.

None of this happens until the owner authorises an AI connection. No API key exists.
