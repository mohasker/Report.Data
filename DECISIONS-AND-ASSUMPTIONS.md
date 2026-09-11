# Decisions, Withdrawals, Assumptions and Open Questions

**Document ID:** AH-SYS-HAND-004 · **Version:** 1.0 · **Date:** 2026-09-11

**Read this before proposing any change to the design.** Most things that look wrong in this
repository are decisions taken deliberately, with the reasoning recorded. This file is the
consolidated record: what the owner decided, what was withdrawn, what is merely assumed, what is
still unknown, and which phase each item blocks.

Source documents, if you want the full reasoning: `docs/00-discovery/10-owner-decisions.md`,
`docs/00-discovery/03-assumptions-register.md`, `docs/00-discovery/04-open-questions.md`,
`docs/00-discovery/adr/`, `docs/01-data-foundation/16-external-facts-register.md`.

---

## 1. Owner-approved decisions

### Phase 0 approval, 2026-09-11 — D-01 to D-15

| # | Decision | Consequence |
|---|---|---|
| **D-01** | **This is not a three-project system.** Designed from the first version for dozens or hundreds of projects. Three synthetic projects are **test fixtures only** | Adding a project must be master-data configuration only — never modified logic, a cloned app, duplicated scenarios, rewritten prompts or changed formulas. Enforced by 12 automated checks |
| **D-02** | **Legal identity is configurable master data**, not a choice between "L.L.C." and "W.L.L." | `LegalEntities` carries EN/AR names, CR number, address, currency, tax status, signatories, footer, effective date and version. Synthetic data uses an explicit pending-verification placeholder |
| **D-03** | Google ownership decided **in principle**: company-owned Shared Drive, system-owned account | Account and Shared Drive IDs remain configuration values due before production |
| **D-04** | The AppSheet plan question becomes a **Phase 1 deliverable**: a feature-to-plan requirements matrix, then verification | The matrix exists; verification was attempted and blocked by network egress, recorded honestly |
| **D-05** | Make.com is the orchestration layer | Organisation and plan are configuration values. The account was later inspected read-only |
| **D-06** | **AI may pre-analyse submitted evidence to assist the reviewer**, clearly marked. **Only human-approved evidence may generate an official report.** AI may never change an approval status or overwrite a caption | Advisory fields only, excluded from every content hash |
| **D-07** | QuickBooks Online is in use | Capability is **inspected, not assumed** — 24 questions, outstanding |
| **D-08** | **"Zero-rated" is withdrawn.** The tax treatment is unconfirmed | The engine returns `UNDETERMINED` and **blocks**. It never produces zero |
| **D-09** | The General Manager is the final approver; **delegation is modelled from the start** | Delegate identity due before go-live |
| **D-10** | Numbering series configurable by entity, type, year, scope, client and revision, with a reserved → issued → cancelled lifecycle | The existing manual register must still be reviewed before Phase 5 issue |
| **D-11** | **Bilingual architecture from Phase 1.** "Arabic doubles the work" is withdrawn | Paired columns, `at_least_one`, NFC, no transliteration. Arabic *template production* is deferred; the architecture is not |
| **D-12** | Data residency becomes a **model plus a contract-review checklist** | Blocks production upload for an affected project, not the design |
| **D-13** | **Evidence-original wording must be exact** | No file may be described as "the original device image" while `IsOriginalDeviceImageVerified` is FALSE, which it stays until a real device proves no upstream re-encoding |
| **D-14** | **Phase 1 authorisation boundary** | No production Google account, AppSheet data, Make scenario, Claude credential, QuickBooks connection, real photograph, email, invoice or published document |
| **D-15** | Seventeen required additions to the Phase 1 deliverables | All delivered |

### Cost, scope and process corrections, 2026-09-11

| # | Decision | Consequence |
|---|---|---|
| **D-A** | **Workspace is already paid; AppSheet Core is assumed USD 0 incremental pending verification.** The USD 2,600–5,000 estimate is withdrawn | Five cost categories, each stated separately. **No purchase without written approval** |
| **D-B** | **The Admin Console entitlement check is the only external gate** on Phase 2A | A 15-minute, click-by-click checklist for the owner |
| **D-C** | **A lean MVP of 12–18 tables** is built first; the 46-table model remains the reference architecture | 17 lean, 12 in release 1, 29 deferred but schema'd |
| **D-D** | **Recoverability is a go-live blocker**, not a note | Computable in the model: no go-live without a second administrator or a documented, tested recovery route |
| **D-E** | **Read-only Make inspection authorised**, with an explicit allowed/forbidden list | Six read-only calls made; everything adjacent to credentials, webhooks or business content deliberately not called |
| **D-F** | **Migration is threshold-triggered.** "Year 1.4" is withdrawn | Row counts, sync times and concurrent writers — measured, not predicted |
| **D-G** | **A seven-value acceptance vocabulary** governs every status claim | Completed · Validated Locally · Submitted for Owner Review · Approved · Verified in Integration · Production Ready · Live |
| **D-H** | **Design to 60–70% of the verified orchestration limit**, without removing validation, auditability or error handling | 703 operations, 70%, 2 scenarios |
| **D-I** | **Release 1 is the twelve-table capture-and-review release** | No document, no numbering, no legal entity. Reports are produced manually from approved evidence |
| **D-J** | **Three image classes**, replacing the "never through Make" absolute | Original never; AI derivative yes at pilot volume; report derivative at generation time |

### The operational correction, 2026-09-11 — D-16 to D-21

| # | Decision | Consequence |
|---|---|---|
| **D-16** | **Capture once, use twice.** The supervisor never uploads, selects or describes the same evidence twice. Two modes: Quick Share and AI Reviewed Share | **`CAP-01`: the workflow fails acceptance if the supervisor must select or upload the images a second time.** Eight new columns on `SiteVisits`, two on `Photos` |
| **D-17** | **AI proposes; the supervisor decides, with minimum interaction** | Eight advisory proposal columns separate from the confirmed values; `AIProposalDisposition` records accept or correct. **Analysis now runs on every captured photograph**, which raises the cost |
| **D-18** | **A written description is not mandatory for a normal photographic submission** | Optional site note with a ten-value category vocabulary; four named exceptional workflows; voice input is a future *input method* for the same field. Regression-guarded by `CAP-26` |
| **D-19** | **Nine inferences AI may never make**, and trusted context comes from system data | Sixteen columns closed to AI by declaration and by check. The share destination is a **label**, never a telephone number or invitation link |
| **D-20** | **No quantitative or contractual field may originate from an image** | The AI's activity assessment is free text, deliberately **not** a reference to `ActivityTypes` |
| **D-21** | **The capture platform is an interface decision, and it is gated** | `CAP-GATE`, fifteen conditions on real devices. **No duplicate-upload workaround.** The backend is re-usable if the interface changes |

---

## 2. Withdrawn and superseded — do not reintroduce

| # | Statement | Status |
|---|---|---|
| W-01 | "Annual cost of USD 2,600–5,000" | **Withdrawn — invented figure** |
| W-02 | "Expected pilot cost is USD 0" | **Withdrawn — asserts an unverified entitlement** |
| W-03 | "Migration at year 1.4" | **Withdrawn — false precision.** Thresholds, not dates |
| W-04 | "Image bytes must never pass through Make" | **Superseded** — three image classes; visual analysis requires the model to see an image |
| W-05 | A written work description is required on a visit | **Superseded by D-18** |
| W-06 | Any workflow requiring a second image selection | **Forbidden by `CAP-01`** |
| W-07 | "Three pilot projects" as a system property | **Withdrawn by D-01** — they are fixtures |
| W-08 | "The contracts are zero-rated" | **Withdrawn by D-08** |
| W-09 | "Arabic doubles the work" | **Withdrawn by D-11** |
| W-10 | "80 GB a year is a non-issue" | **Withdrawn** — depends on an unknown allocation |
| W-11 | Any claim that local validation proves a platform works | **Forbidden** |
| W-12 | "Active scenarios: 2" read as a count | **Clarified** — 7 exist, 0 active, 2 is the ceiling |
| W-13 | "WhatsApp is not in scope", unqualified | **Clarified by D-16** — not an input channel; an output channel by native share only |
| W-14 | AI analysis runs only on approved photographs | **Superseded by D-17** — every captured photograph |
| W-15 | "A capture-and-review release is 12 tables" arrived at as 17 - 3 | **Corrected** — an arithmetic error of mine; the twelve are named explicitly |

### Corrections made to my own work, recorded because they matter

Five defects were found by the checks and fixed as they were found: two unreachable statuses; a
project manager who could write the audit log; six vocabularies with no change attribution; an
unpaired Arabic column; and six lean tables that depended on deferred ones without a declared
replacement. A sixth came from a fixture: an Arabic-only client could not be saved because the
English legal name was required — **the model was changed, not the fixture.**

---

## 3. Current assumptions

Assumptions are not facts. Each is labelled, each has a consequence if it is wrong, and none is
load-bearing without being written down.

| # | Assumption | If it is wrong |
|---|---|---|
| **A-01** | In Make, **each module that acts consumes one operation per bundle**; filters and routers do not | **The entire operations budget is wrong in the same proportion.** The first week of real running replaces it with measurement |
| **A-02** | AppSheet Core is included in the existing Workspace subscription | A specific costed option goes to the owner. No purchase is assumed |
| **A-03** | The capture platform provides security filters and offline use | **No workaround exists.** The capture tool is reconsidered — a licence would not fix a missing capability |
| **A-04** | 120 photographs per project per month, averaging 2.5 MB | Storage, transfer and AI cost all scale with it. Low, expected and high scenarios are stated separately |
| **A-05** | A supervisor performs ~20 visits per project per month | The operations budget scales linearly |
| **A-06** | Photographs are not re-encoded between camera and store | `IsOriginalDeviceImageVerified` stays FALSE until a device proves otherwise. **No document calls a file "the original device image" meanwhile** |
| **A-07** | ~3 seconds per interface tap | The 75-second target is arithmetic on taps, not a measurement. **Never describe it as achieved** |
| **A-08** | 15% of visits are returned for correction; 10% of runs retry | Both are funded allowances in the budget, and both are measured in Phase 3 |
| **A-09** | A 1024 px derivative is sufficient for useful visual analysis | A larger derivative roughly triples the input cost with no other change |
| **A-10** | The nine representative user and device profiles are broadly right | They stand in for real people until the owner supplies identities and an inventory |
| **A-11** | The company will accept that neither administrator can read evidence or documents | This is the exception most likely to provoke disagreement, and it is flagged as such in the review pack |
| **A-12** | Quick Share sending evidence before review is acceptable because it matches what already happens | If the owner disagrees, AI Reviewed Share becomes mandatory and Quick Share is removed. **The capture-once guarantee is unaffected either way** |

---

## 4. Open questions

| # | Question | Blocks |
|---|---|---|
| OQ-05 | Whether gallery upload is permitted at all, given it weakens evidence freshness | Phase 2 capture method |
| OQ-09 | Whether any client requires a report layout of their own | Phase 5 |
| OQ-10 | Whether client acknowledgement signatures should be captured on site | Post-MVP |
| OQ-11 | Whether manpower and equipment feed cost control or reporting only | Phase 6 |
| OQ-12 | Who receives operational alerts — the administrator alone, or the GM too | Phase 3 |
| OQ-13 | The named alternate for the system administrator role | Phase 2 |
| OQ-14 | Whether quotations are eventually generated by this system | Phase 8 |
| **OQ-15** | **Which mode is the default** — Quick Share or AI Reviewed Share — and whether the supervisor chooses per visit or the project fixes it | Phase 2A |
| **OQ-16** | Whether a **formatted summary** accompanies every share, or only those carrying a snag or safety observation | Phase 2A |
| **OQ-17** | Whether the same share should also reach an **internal** group, and whether that is one action or two | Phase 2B |
| **OQ-18** | Whether a supervisor may share a visit **still in draft**. Quick Share implies yes; evidence control argues no | Phase 2A |
| **OQ-19** | Whether voice capture stores the **audio** as evidence, or only the transcript | Post-MVP |

**OQ-15 to OQ-19 need no external access.** They are the natural next work for a new account.

---

## 5. External facts register

**26 outstanding. None has been guessed at.**

| ID | Fact needed | From | Blocks |
|---|---|---|---|
| **EF-24** | **`CAP-GATE`** — whether the capture platform can share several stored image files and formatted text through the native share sheet to an existing WhatsApp group, iOS and Android, **without a second selection** | **A real-device test. Nobody can supply it as an answer** | The capture-platform decision |
| **EF-01** | Google Workspace account, Shared Drive ownership and IDs | Owner | First external connection |
| **EF-03** | AppSheet entitlement: does the tier provide **security filters** and **offline use** | Owner, Admin Console | **The build itself** |
| **EF-25** | Whether AppSheet has **API access or webhook automation** | Owner, Admin Console step 4 | Whether the AI proposal costs anything to run |
| **EF-26** | The **label** of each project's existing contractor group — never a number or link | Owner | The share configuration |
| **EF-04** | The hard monthly AI spend cap | Owner | Phase 4 |
| **EF-05** | Real user identities and a device inventory | Owner | Phase 2B field test |
| **EF-06** | A second administrator, or an approved recovery route | Owner | **Go-live** |
| **EF-07** | Named approval delegates | Owner | Go-live |
| **EF-09** | Which clients require Arabic documents | Owner | Phase 5 |
| **EF-10** | The orchestration organisation and plan decision | Owner | Phase 3 |
| **EF-11** | Alert recipients | Owner | Phase 3 |
| **EF-12** | Retention and backup policy | Owner | **The largest storage decision in the system** |
| **EF-13** | Working calendar and reporting cut-off | Owner | Phase 3 |
| **EF-14** | Gallery upload policy | Owner | Phase 2 |
| **EF-15** | Approved logo and any client templates | Owner | Phase 5 |
| **EF-16** | Contract review for data residency — orchestration runs in the **United States** | Owner / legal | Production upload for an affected project |
| **EF-17** | **Written tax confirmation from the accountant** | Accountant | **Production invoicing** |
| **EF-18/19** | Contract and BOQ data; payment terms, retention, advances | Owner | Phase 6 |
| **EF-02/08** | Legal identity from the current CR; the existing manual numbering register | Owner | Production documents; Phase 5 issue |
| **EF-20/21** | QuickBooks company-file inspection and mappings | Accountant | Phase 7 |
| **EF-22/23** | Authorised recipients; written authorisation for production posting | Owner | Phase 7 |

**EF-24 is different in kind from every other entry.** The rest are facts somebody knows and has not
yet told us. **EF-24 is a fact nobody knows.** It is not documented anywhere, and only running the
test on two real phones answers it.

---

## 6. Verified external facts

**Exactly two things in this project have been verified externally.**

**1. The Make.com account**, inspected read-only on 2026-09-11 with written owner authorisation:
zone `us2.make.com` (United States — a residency fact); Free plan; 1,000 operations a month, 0
consumed; **7 scenarios present, 0 active, a plan ceiling of 2**; 1 data store of 1 MB; 512 MB
transfer; 5 MB maximum file size; 15-minute minimum interval; 5-minute maximum execution; **no
overage — work stops rather than billing**; and every required integration present, including
AppSheet, Anthropic Claude and QuickBooks. Six read-only calls were made; everything adjacent to
credentials, webhooks, connections or business content was deliberately **not** called. The seven
existing scenarios belong to unrelated company work and were listed and nothing more.

**2. Claude vision capability**, from official documentation: three source types (base64, URL,
file_id), a 10 MB base64 limit, visual tokens ≈ ⌈w/28⌉ × ⌈h/28⌉, image metadata **not** read by the
model, and in-request images ephemeral and auto-deleted — which is why in-request base64 was chosen
over any stored or publicly linked copy.

**Recorded as blocked, honestly rather than substituted:** `about.appsheet.com`, `cloud.google.com`,
`support.google.com` and `make.com` were unreachable from the build environment. No third-party
figure was used in their place. Re-check if your environment differs, but do not treat the gap as an
oversight — it is a recorded finding.

---

## 7. What blocks what — the summary

| Item | Blocks |
|---|---|
| **Admin Console entitlement check** (owner, 15 min) | The capture-platform decision and the first external connection. **The only external gate on Phase 2A** |
| **`CAP-GATE` device test** | The capture-platform decision |
| Real administrator identities + a recovery route | **Go-live** |
| Written tax confirmation | Production invoicing only |
| Legal identity from the CR | Production documents only |
| Manual numbering register | Phase 5 number issue |
| Device inventory and real supervisors | The Phase 2B field measurement |
| Contract review (US orchestration residency) | Production upload for an affected project |

**Nothing blocks continued Phase 2A work on synthetic data.**
