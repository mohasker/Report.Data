# Blocking Questions and Open Questions

**Document ID:** AH-SYS-P0-004 · **Revision:** 3 · **Status:** all ten answered, decided in principle, or converted to a Phase 1 deliverable on 2026-09-11 · OQ-20 … OQ-22 registered; OQ-15 … OQ-22 carry recommendations in AH-SYS-P2A-025

> **Revision 1.** The owner's decisions are recorded in [`10-owner-decisions.md`](10-owner-decisions.md)
> and summarised in the disposition table below. **The question text is retained unchanged** — the
> record of what was asked, and what was decided, is more useful than a tidied document.
>
> | # | Disposition | What is still outstanding |
> |---|---|---|
> | BQ-01 | Decided in principle (D-03) | Owning account and Shared Drive ID — before production deployment |
> | BQ-02 | Converted to a Phase 1 deliverable (D-04): feature-to-plan requirements matrix | Entitlements and pricing verified from official Google information — before purchase |
> | BQ-03 | Decided (D-05) | Organisation and plan — before Phase 3 |
> | BQ-04 | Decided in principle (D-06), with the correction that AI may pre-analyse **submitted** evidence to assist the reviewer | Monthly spend cap value — before Phase 4 |
> | BQ-05 | **Answered (D-07): QuickBooks Online is in use** | Compatibility inspection checklist — gate before the financial-integration phase |
> | BQ-06 | Open, and correctly so (D-08). **No classification may be named** — "zero-rated", "exempt", "out of scope" and "no tax configured" are not interchangeable | Accountant's written confirmation — before production invoicing |
> | BQ-07 | Decided (D-09): GM as final approver; delegation modelled from the start; no self-approval of a restricted transaction | Delegate identity — before go-live |
> | BQ-08 | Decided (D-10): sequences by entity, type, year, scope, client requirement and revision, with reserved → issued → cancelled states | Review of the existing manual register — before Phase 5 issue |
> | BQ-09 | Decided (D-11): **bilingual EN/AR architecture from Phase 1**; English first for reports; Arabic template production deferred | Which clients require Arabic documents — before Phase 5b |
> | BQ-10 | Converted to a Phase 1 model plus a contract-review checklist (D-12) | Contract review — blocks production upload for an affected project, not the design |
>
> Two recommendations below were **corrected by the owner** and are superseded where they differ
> from the decision record: the BQ-06 suggestion to configure a "zero-rate" rule (D-08 forbids
> naming any classification), and the BQ-09 characterisation of Arabic as roughly doubling the work
> (D-11: bilingual capability is architectural and delivered in Phase 1).

Ten blocking questions, prioritised (§18 allows a maximum of ten). Each carries a **recommendation**
so a decision can be made quickly: *approving the recommendation is a complete answer.*

**Do not send credentials, API keys or passwords in chat.** Answer the *decision*; connection and
OAuth authorisation is performed by the owner directly in each provider's console, following the
secure-connection instructions issued at the start of the relevant phase.

---

## BQ-01 — Which Google account owns the system, and is it a paid Workspace tenant?
**Blocks:** everything from Phase 1.
**Why it matters:** consumer Gmail has no Shared Drives, no admin console, no audit log and no way
to transfer ownership. If the evidence archive lives in one person's personal Drive, it leaves with
that person — and it cannot be handed to an auditor, a client or a successor.

**Recommendation.** Create a dedicated Workspace account on the company domain — for example an
`operations` or `system` mailbox, not an individual's — as the technical owner of the AppSheet app,
the Sheets and the Drive structure. Host all operational data in a **Shared Drive** owned by the
company, with the GM and the system administrator as managers.

**Needed to proceed:** confirmation that the tenant is paid Workspace; the account that will own the
system; the Shared Drive name.
**Consequence if deferred:** Phase 1 cannot close. Building on a personal Drive and migrating later
means re-provisioning every folder and re-pointing every stored file ID.

---

## BQ-02 — Which AppSheet plan, and how many named users in year one?
**Blocks:** Phase 2.
**Why it matters:** AppSheet's lower tiers do not include the webhook and API capabilities this
design depends on. Without them the app is an island: no Make trigger, no status write-back, no
report pipeline. Licensing is also per-user per-month and recurring, so the user count is a real
budget decision, not a technical detail.

**Recommendation.** License the tier that includes **webhooks and the AppSheet API** for the office,
review and administration users (order of 5–10 people), and evaluate the minimum viable tier for
pure field-capture users. **Verify current tier names, feature boundaries and pricing directly with
Google** — this document deliberately states no price (operating rule 2).

**Needed to proceed:** chosen plan; approximate count of field users vs. office users.
**Consequence if deferred:** the app can be built and demonstrated, but nothing downstream of
capture can be built or tested.

---

## BQ-03 — Is a Make.com organisation available, and on which plan?
**Blocks:** Phase 3.
**Why it matters:** Make is the orchestration layer. The design uses Data Stores (idempotency keys),
error handler routes and scheduled scenarios. Operation volume drives the plan tier, and every photo
registration and AI analysis consumes operations.

**Recommendation.** Use Make. The alternative — Google Apps Script — has no licence cost but hides
all orchestration inside code that only a developer can inspect, which is the wrong trade-off for a
company whose stated weakness is reliance on one person (ADR-0003). Start on the lowest plan that
includes Data Stores and error handling; measure real operation consumption in Phase 3 and size up
from measurement rather than from a guess.

**Needed to proceed:** confirmation of Make usage; the organisation and team the scenarios live in.
**Consequence if deferred:** Phase 3 cannot start; capture and review remain unautomated.

---

## BQ-04 — Claude API workspace and monthly spend cap
**Blocks:** Phase 4.
**Why it matters:** cost scales with the number of images analysed and the length of generated
reports. Without a cap, a bulk upload or a retry loop can produce an unexpected bill.

**Recommendation.** Create a dedicated API workspace for this system with a **hard monthly spend
cap** set by the owner. Control cost by design: analyse only reviewer-approved evidence, send
downscaled derivatives rather than full-resolution originals, cap output tokens per call, and record
usage per project so cost can be attributed to the contract that generated it.

**Needed to proceed:** confirmation that an API workspace will exist; the monthly cap figure.
**Consequence if deferred:** Phase 4 is skipped. The pipeline still works; report narrative and
evidence description stay manual.

---

## BQ-05 — Does a usable QuickBooks Online company file exist for the Qatari entity, and is a sandbox available?
**Blocks:** Phases 6–7. **Ask the accountant before any accounting design work.**
**Why it matters:** QuickBooks Online is sold and supported by region, and Qatar is not among its
principal supported markets. Region determines tax handling, numbering, currency behaviour and
whether the product is properly supported at all. Building an integration against an unsupported or
non-existent company file is wasted work with real financial consequences.

**Recommendation.** Confirm with the company's accountant, before Phase 6 design begins: (a) whether
a QBO company file exists and which region/edition it is; (b) whether a sandbox company is
available for testing; (c) if QBO is not properly supported for the Qatari entity, **decide the
accounting target explicitly** rather than defaulting to it (see R-02). Until answered, the system
produces invoice **drafts** and no posting of any kind.

**Needed to proceed:** accountant's written answer to (a)–(c).
**Consequence if deferred:** Phase 6 still delivers certificates and invoice drafts. Only posting is
blocked — which is the correct place to be blocked.

---

## BQ-06 — Confirm the tax treatment actually applied to these contracts today
**Blocks:** Phase 6. **Accountant's answer required, in writing.**
**Why it matters:** §11 forbids assuming a tax position in either direction. An invoice with the
wrong tax treatment is a legal and client-relationship problem, not a software bug.

**Recommendation.** Configure a **named zero-rate tax rule** rather than hard-coding "no tax", so
that if the position changes the system is updated by editing one configuration row. Obtain the
accountant's written confirmation of the current treatment (including any withholding obligations
for particular client types) and file it against assumption **A-07**.

**Needed to proceed:** written statement of current tax treatment for these contracts.
**Consequence if deferred:** invoice drafts cannot be validated as correct, so Phase 6 cannot close.

---

## BQ-07 — Who are the named approvers, and how does approval route per project?
**Blocks:** Phase 2.
**Why it matters:** the approval matrix is the system's control backbone. Every gate — technical
approval, finance approval, release — needs a named, reachable person. It also determines what
happens when that person is travelling, which is an availability question, not a technical one.

**Recommendation.** For the MVP: **GM as technical approver and releaser** across all projects, with
project managers as first-line reviewers where they exist. Before go-live, **nominate at least one
delegate** for each gate, so a single person's absence cannot stop reporting or billing. The
approval matrix is built to support per-project routing from the start, so adding delegates later is
configuration, not redesign (**R-07**).

**Needed to proceed:** names and email addresses for technical reviewer, finance reviewer and
releaser; whether routing differs by project; delegate names.
**Consequence if deferred:** approval routing and notification cannot be configured; nothing can be
approved or released.

---

## BQ-08 — Document numbering scheme, company code, and existing series in use
**Blocks:** Phase 5.
**Why it matters:** §6 specifies the document filename pattern but not the numbering authority. Two
documents carrying the same number, or a system that restarts a series already in use manually, is a
credibility failure in front of a government client and an ISO non-conformity.

**Recommendation.** Adopt **one central numbering service** with an atomic counter (ADR-0005), a
documented format per document type, and a **recorded starting number per series** that continues
existing manual numbering rather than colliding with it. Confirm the company code used in document
numbers.

**Needed to proceed:** the company code; the format per document type; the last number used in each
existing manual series.
**Consequence if deferred:** documents cannot be numbered, so none can be issued.

---

## BQ-09 — Language policy for client-facing documents
**Blocks:** Phase 5.
**Why it matters:** bilingual output is not a formatting toggle. It roughly doubles template work,
QA work and PDF-rendering risk (right-to-left layout, mixed-direction text inside tables, font
embedding), and it needs its own test matrix.

**Recommendation.** **English for the MVP**, with Arabic labels and help text inside the app so
field users are never blocked by language. Treat Arabic or bilingual client documents as a separate,
explicitly approved scope in Phase 5b, prioritised by which clients actually require it.

**Needed to proceed:** which clients require Arabic or bilingual documents, and whether any require
it contractually.
**Consequence if deferred:** English-only templates proceed; adding Arabic later means a second
template set and a second visual-inspection pass, not a rebuild.

---

## BQ-10 — Do any client contracts restrict where evidence and reports may be stored or processed?
**Blocks:** Phase 1 sign-off.
**Why it matters:** government and semi-government clients sometimes impose confidentiality, data
location or third-party-processing conditions. Google Workspace offers data-region controls, but
**Qatar is not an available data region**, and sending images to an AI provider is third-party
processing. Discovering a contractual restriction after go-live is far more expensive than checking
now.

**Recommendation.** The owner reviews the relevant contracts — MOEHE/school contracts first — for
confidentiality, data-location and subcontracting-of-processing clauses. If a restriction exists,
the storage and AI-processing design must be decided around it before Phase 3, not after. Where AI
analysis is contractually problematic for a specific client, the design can disable AI analysis
**per project** as a configuration flag rather than for the whole system.

**Needed to proceed:** confirmation that no restriction exists, or the text of the clauses that do.
**Consequence if deferred:** the system may be built on a storage or processing model a client
contract does not permit.

---

# Non-blocking open questions

To be resolved during the phase noted; none prevent starting Phase 1.

| ID | Question | Needed by |
|---|---|---|
| OQ-01 | Standard working calendar, weekend days and public-holiday handling for reporting periods and target dates. | Phase 2 |
| OQ-02 | Monthly cut-off day: how late can evidence be added before a period is closed? | Phase 2 |
| OQ-03 | Retention policy: how long are originals, derivatives and released documents kept, and what happens at the end of a contract? | Phase 3 |
| OQ-04 | Backup/export cadence and who verifies that a restore actually works. | Phase 3 |
| OQ-05 | Photo gallery upload — permitted, or camera-only? (§7.3 leaves this to policy.) Gallery uploads ease re-submission but weaken evidence freshness. | Phase 2 |
| OQ-06 | Is GPS capture mandatory, and what happens when a device denies location permission? | Phase 2 |
| OQ-07 | Snag severity definitions and target response times per severity. | Phase 2 |
| OQ-08 | Which HSE observations must be recorded to satisfy ISO 45001 obligations. | Phase 5 |
| OQ-09 | Do any clients require a specific report layout or template of their own? | Phase 5 |
| OQ-10 | Should the system record client acknowledgement signatures on site (signature capture)? | Post-MVP |
| OQ-11 | Should manpower and equipment records feed cost control, or reporting only? | Phase 6 |
| OQ-12 | Who receives operational alerts (error queue, overdue corrections) — the administrator alone, or the GM as well? | Phase 3 |
| OQ-13 | Named alternate for the system administrator role (A-19). | Phase 2 |
| OQ-14 | Whether quotations should eventually be generated by this system or remain in the existing proposal process. | Phase 8 |
| OQ-15 | Which operating mode should be the **default** — Quick Share or AI Reviewed Share — and whether a supervisor may choose per visit or the project fixes it (D-16). | Phase 2A |
| OQ-16 | Whether a **formatted summary** should accompany every share, or only shares that carry a snag or a safety observation. More text is not always more useful to a contractor. | Phase 2A |
| OQ-17 | Whether the same share should also reach an **internal** group, and whether that is a second share action or one action with two destinations. | Phase 2B |
| OQ-18 | Whether a supervisor may share a visit that is **still in draft**, or only one they have submitted. Quick Share implies the former; evidence control argues for the latter. | Phase 2A |
| OQ-19 | Whether voice-note capture should write the **audio file** as evidence, or only the transcribed text into `AdditionalSiteNote` (D-18). | Post-MVP |
| OQ-20 | What the **quality threshold** and the **near-duplicate similarity threshold** should be. Both are project configuration, and both trade a saved model call against a missed observation (D-24). | Phase 2B |
| OQ-21 | Whether a **pending classification** should expire into a reviewer task after some number of days, or simply accumulate in a queue (D-23). | Phase 2A |
| OQ-22 | Whether the location prompt, when it does appear, should offer the **nearest location by GPS** rather than the last used (D-22). | Phase 2A |
| OQ-23 | What happens to **evidence still queued on a device when the user's access is revoked** — discarded, or completed into a reviewer's quarantine. Discarding destroys evidence the supervisor believes they submitted; completing lets someone without access write to a project. Surfaced by `CAP-GATE` G-5.3. | Phase 2B |

> **OQ-15 … OQ-22 now have written recommendations.** See
> [`../02a-plan/25-open-question-recommendations.md`](../02a-plan/25-open-question-recommendations.md)
> (AH-SYS-P2A-025). Those are **recommendations submitted for owner review, not decisions**; all
> eight questions remain open until the owner answers.
