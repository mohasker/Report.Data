# Change Log

All notable changes to this repository. Dates are ISO 8601.

The system uses phase-based versioning: `0.<phase>.<revision>`. Version `1.0.0` is reserved for the
accepted multi-project MVP (§14).

---

## [0.0.1] — 2026-09-10 — Phase 0 discovery

**Added**

- `MASTER_SPEC.md` — authoritative requirements baseline, v1.0, as supplied by the owner.
- `docs/00-discovery/00-DISCOVERY-SUMMARY.md` — the eight discovery outputs required by §18.
- `docs/00-discovery/01-mvp-boundary.md` — MVP scope, deferrals and acceptance mapping.
- `docs/00-discovery/02-architecture.md` — layer model, four invariants, trust boundaries, failure taxonomy.
- `docs/00-discovery/03-assumptions-register.md` — 20 labelled assumptions and the dependency list.
- `docs/00-discovery/04-open-questions.md` — 10 blocking questions with recommendations, 14 open questions.
- `docs/00-discovery/05-risk-and-controls-register.md` — 32 risks with controls and owners.
- `docs/00-discovery/06-spec-conflicts-and-platform-limits.md` — 12 specification conflicts, 12 platform limitations, 10 simplification opportunities, 7 security observations.
- `docs/00-discovery/07-phase-plan.md` — phases 0–8 with gate evidence requirements.
- `docs/00-discovery/08-phase-1-artifact-manifest.md` — exact Phase 1 deliverables.
- `docs/00-discovery/09-configuration-register.md` — every external value as a named variable, no values recorded.
- `docs/00-discovery/adr/ADR-0001` … `ADR-0008` — architecture decision records, all Proposed.
- `docs/VERSION-MANIFEST.md` — document control register.
- `README.md`, `CHANGELOG.md`, `.gitignore`.

**Not done, recorded deliberately**

- No Google Workspace, Drive, AppSheet, Make, Claude API or QuickBooks account was inspected, created or connected. No access was provided and none was requested in chat.
- No test of any kind was executed. No test result is claimed.
- No credential, key, account ID or other secret was requested, stored or committed.
- No production mutation of any kind was performed — §15 Phase 0 requires owner approval first.

**Status:** awaiting owner approval and answers to BQ-01 … BQ-10.

---

## [0.0.2] — 2026-09-11 — Phase 0 approved, revision 1

**Added**

- `docs/00-discovery/10-owner-decisions.md` — the owner's decisions D-01 … D-15, which govern the Phase 0 documents where they differ.

**Changed — applying the owner's decisions**

- **D-01 scope correction.** The MVP is a *depth* boundary, not a width boundary. The platform is multi-project, multi-client and multi-entity from the first version, sized for dozens or hundreds of projects; three synthetic projects are test fixtures only. Wording corrected in the discovery summary, the MVP boundary and the phase plan.
- **D-02 legal entity.** Conflict C-01 is no longer resolved by choosing "L.L.C." or "W.L.L."; legal identity becomes configurable `LegalEntities` master data with the placeholder `LEGAL_ENTITY_NAME_PENDING_VERIFICATION`. Assumption A-06 superseded.
- **D-04 AppSheet.** No plan or entitlement assumed; a feature-to-plan requirements matrix becomes a Phase 1 deliverable and Phase 1 stays platform-neutral enough to identify anything the platform cannot safely or economically support.
- **D-06 Claude.** ADR-0004 revision 1: AI may pre-analyse **submitted** evidence to assist the reviewer, clearly marked as an AI observation; only **human-approved** evidence may generate an official report, and AI never changes a workflow status.
- **D-07 QuickBooks.** QBO is the accounting system in use. R-02 and P-09 re-scoped from "may not be supported" to "capability for the current company configuration is unverified"; ADR-0008 revision 1 adds mapping fields and a compatibility inspection checklist as a gate.
- **D-08 tax.** The recommendation to configure a "zero-rate" rule is **withdrawn**. No classification may be named — "zero-rated", "exempt", "out of scope" and "no tax configured" are distinct. Assumption A-07 superseded; R-24 and the configuration register updated; the applied rule and its version are preserved on every calculation.
- **D-10 numbering.** ADR-0005 revision 1: one service, many configurable series by legal entity, document type, year, scope, optional client requirement and revision, with an explicit reserved → issued → cancelled lifecycle replacing "never reserved", and migration from the existing manual register.
- **D-11 language.** Bilingual EN/AR is an architectural requirement delivered in Phase 1, not a deferred scope. The earlier claim that Arabic "doubles the work" is withdrawn; it applies to template production only. Assumption A-10 amended; ADR-0007 revision 1 keys templates by type **and** language.
- **D-13 evidence originals.** The enforceable write-once definition is adopted verbatim in C-02 and R-03, with checksum, MIME type, size, received timestamp, source record and uploader recorded, derivatives stored separately, and no "original device image" claim before iOS and Android testing.
- **D-15.** The Phase 1 artifact manifest is rewritten to revision 1 with all seventeen additional deliverables and an explicit coverage table.

**Status:** Phase 0 closed. Phase 1 authorised within the limits of D-14 — repository artifacts, schemas, synthetic data, specifications and documentation only; no production connection, no real data, no external action.

---

## [0.1.0] — 2026-09-11 — Phase 1: data foundation

Phase 1 delivered within the limits of D-14: repository artifacts, schemas, synthetic data,
specifications and documentation only. **No production system was connected, no credential exists,
and no real data was introduced.**

**Added — canonical model and generators**

- `model/model.json` — the single source of truth: 44 tables, 763 columns, 24 bilingual controlled vocabularies, 65 declared status transitions with 29 explicitly forbidden, a role × table × operation matrix of 352 grants with 13 stated exceptions, and the canonical content-hash definition.
- `tools/` — standard-library-only generators (`build_model`, `gen_schemas`, `gen_data_dictionary`, `gen_matrices`), reference implementations (`security`, `evidence`, `contenthash`, `numbering`, `calc`), nine check suites, and `run_validation.py` which regenerates every artifact and records the evidence.
- `schemas/tables/` — 44 generated table schemas. `schemas/ai/` — two closed output contracts for Phase 4 and 5, neither containing any numeric quantity field.
- `seed/` — controlled vocabularies plus three materially different synthetic projects carrying deliberate traps, so a segregation or validation bug is visible rather than subtle.
- `config/` — configuration reference, `.env.example` (names only), rounding policy, tax-rule structure.

**Added — specifications**

Seventeen documents under `docs/01-data-foundation/`, covering the data dictionary, key and hash
strategy, status transitions, the security matrix, evidence rules, naming and numbering, migration
and versioning, the legal-entity and bilingual model, data classification and residency, approval
and delegation, deterministic calculation, the capture-platform requirements matrix, accounting
mapping and inspection, the orchestration contract and operator runbook, the AI prompt and schema
specification, the external-facts register, and the executed validation evidence.

**Executed**

`python3 tools/run_validation.py` — **141 checks across 10 suites, all passing**, recorded in
`docs/01-data-foundation/17-validation-evidence.md` with the evidence each produced.

**Fixed — defects the checks found in the model as it was written**

- `Documents.Cancelled` and `Approvals.Delegated` were unreachable from the transition matrix. Both now have declared transitions, including the delegation path that records the acting delegate and the accountable approver separately.
- A project manager could create rows in the audit log through a group-level grant. Removed; the audit log is now append-only for every role including `SystemAdmin`.
- Six controlled vocabularies carried no change attribution. `CreatedBy`/`UpdatedBy` added — configuration changes need attribution as much as records do under ISO 9001.
- `Clients.LegalNameEN` was required, which made a client registered only in Arabic unsaveable. Changed to "at least one legal name in either language", because forcing an English name would invite an invented transliteration (D-11).
- Column examples in the data dictionary resembled fixture identifiers. Replaced, so no example can be mistaken for real data.
- `SystemAdmin` read access to operational and document tables removed: an administrator configures the system and works the error queue without needing to read client evidence.

**Outstanding**

23 external facts, each named with its owner and the phase it blocks
(`docs/01-data-foundation/16-external-facts-register.md`). None blocks Phase 1; none has been
guessed at.

**Status:** Phase 1 complete, awaiting owner review of the data dictionary, the transition matrix
and the security model. Phase 2 requires EF-01, EF-03, EF-05 and EF-06.

---

## [0.2.0] — 2026-09-11 — Owner review pack, role model, Phase 2A plan

Responds to the owner's Phase 1 review instruction of 2026-09-11. **Phase 1 status corrected to
Completed, Validated Locally, Submitted for Owner Review — it is not production-verified.** No
external service was connected and no real data was introduced.

**Added — owner-facing**

- `docs/OWNER-REVIEW-PACK.md` — the whole design in one document: executive summary, entity-relationship diagrams, all 46 tables grouped into nine business domains, the fields that matter, eight status lifecycles as diagrams, a readable role-permission matrix, the segregation, numbering, approval/hash, financial and bilingual models, the five highest residual risks, the decisions still required, and a recommendation of **conditional approval**.
- `docs/STATUS-DEFINITIONS.md` — the seven acceptance statuses the owner specified, applied consistently across every document header and the version manifest.

**Changed — role model, per the owner's least-privilege decision**

- `SystemAdmin` becomes **`SystemAdministrator`**: technical configuration, integration monitoring, user provisioning and system health, with **no read access to evidence, documents, contracts or financial records**.
- **`BusinessAdministrator`** added: controlled business master-data administration, also with no access to evidence, documents or money.
- **`EmergencyAccess`** added as break-glass. It restores *administrative* capability and never opens client content, because an administrative emergency is not solved by reading a client's photographs.
- `ReadOnlyAuditor` becomes **time-bound**: without a valid grant it reads nothing at all.
- `TemporaryAccessGrants` added — reason, expiry, authoriser, notification and audit reference all mandatory, with a maximum duration. Each precondition is refused separately so a refusal can say why.
- `SystemRecoveryPlan` added, carrying a `GoLiveBlocker` that stays TRUE until either a backup administrator or a documented, tested recovery route exists.
- Two lifecycles declared that were missing: invoice finance status, and accounting synchronisation — the latter forbidding any posting that is not preceded by sandbox posting and exact reconciliation.

**Added — test evidence, expanded to the owner's specification**

`17-validation-evidence.md` now records the commit tested, the exact command, the Python version and
operating environment, the full console output, every individual check with the evidence it
produced, a mapping from all fourteen specification acceptance criteria to the checks that bear on
them, confirmation that regeneration returned byte-identical artifacts, and — most importantly — an
explicit statement of **what these checks are not evidence of**, platform by platform.

**Added — Phase 2A plan (connects nothing)**

`docs/02a-plan/` — AppSheet workbook and security-filter specification (both **generated from the
model**, so the app cannot drift from the data foundation), views and slices, actions and workflow,
the offline and field test plan written against nine user/device profiles, Drive folder-provisioning
design, Make scenario specifications with three **disabled** blueprints containing no URL, secret or
account identifier, deployment and rollback checklists, the cost and licensing matrix, and synthetic
data loading.

**Added — external facts**

- `19-user-and-device-profiles.md` — nine representative profiles (iPhone, Android, weak connectivity, single-project, multi-project, English, Arabic, plus unassigned and expired-assignment negatives) standing in for real people until the owner supplies them (EF-05).
- `12-appsheet-feature-to-plan-matrix.md` rewritten to revision 2 with all sixteen requirements, the verification method for each, and a twenty-minute verification script. **Verification was attempted on 2026-09-11 and failed**: this environment's network egress policy blocks the vendor's own pricing and documentation pages. No tier is recommended by name, and every cost figure is marked unverified.

**Validation**

172 checks across 11 suites, all passing. The 31 new access-control checks confirm that neither
administrator role can read business content, that break-glass restores administration without
opening evidence, that expired and revoked grants stop working immediately, and that a configuration
with neither a backup administrator nor a documented recovery route is detectable as a go-live
blocker.

**Status:** Phase 1 and Phase 2A are **Submitted for Owner Review**. Phase 2B — the first build that
touches a real account — requires written owner approval plus EF-01, EF-03 and EF-06.

---

## [0.3.0] — 2026-09-11 — Lean MVP scope, corrected cost basis

Responds to the owner's simplification and cost corrections of 2026-09-11. No purchase is proposed,
nothing external is connected, and no real data was introduced.

**Corrected — cost basis**

The revision 1 estimate of USD 2,600–5,000 a year is **withdrawn**, not adjusted. It priced AppSheet
as a new per-user subscription when Al-Haram already pays for Google Workspace and AppSheet Core may
be included in it. Pricing an included component as a new purchase inflated the entire figure.

`09-cost-and-licensing-matrix.md` revision 2 rebuilds it in the five categories the owner specified:

- **Existing subscriptions** — Workspace, AppSheet (assumed included, pending an Admin Console check), Drive storage, QuickBooks. **USD 0 incremental.**
- **New mandatory** — none identified. Orchestration may sit inside a free tier at pilot volume.
- **Optional** — the AI API, bounded by a cap the owner sets. Nothing else.
- **Future scaling** — orchestration tier first, then the store migration, each with a numeric trigger.
- **One-time** — no cash outlay; roughly one day of administrator time plus half a day of field testing.

A purchase is proposed only if a specific required feature is proven unavailable **and** Make cannot
handle it safely. Security filters and offline image capture have no fallback — a gap there changes
the capture layer, not the budget. Webhooks and the API both have Make fallbacks that cost nothing.

**Added — lean operational MVP**

The 46-table model stays the long-term reference architecture; the build is a **17-table subset**
covering every capability the owner listed. Defined in `model/model.json` so scope, workbook and
security filters are generated from one source and cannot disagree.

- `11-lean-mvp-scope.md` — the 17 built tables, the 29 deferred ones, six lean replacement columns, and what each deferral actually costs. The largest is delegation: with no delegate, approvals wait while the general manager is away. Stated plainly rather than buried.
- `tools/test_lean_mvp.py` — 13 checks confirming the subset holds together: no lean table requires a deferred one without a declared replacement, every deferred table keeps its schema (620 columns in reserve), and every load-bearing control survives the trim.

**Added — the deliverables requested before any production connection**

- `12-appsheet-entitlement-checklist.md` — 15 minutes in the Admin Console, 8 subscription questions and 8 feature questions, with a decision rule that proposes no purchase under any outcome.
- `13-field-workflow-and-taps.md` — the one-minute target derived tap by tap: **9–13 interface taps plus 6 shutter presses**, with the nine design decisions that get it there and the 35-tap version that would kill adoption. Three multi-photograph capture methods with trade-offs, one recommended, decided by measurement rather than argument.
- `14-storage-and-image-volume.md` — ~332 MB and ~200 rows per project per month, scaled to 3, 10, 20 and 50 projects, with the spreadsheet-migration threshold reached at roughly year 1.4 at 20 projects, and orchestration operations identified as the fastest-growing cost line.

**Fixed — two defects the checks found**

- Six lean tables had required references to deferred tables, which would have made the subset unbuildable. Each now has a declared replacement column with its consequence stated.
- A configurability check flagged any mention of a project count as a limit, and caught a restore trigger that was not one. It now looks for limit constructs specifically.

**Validation:** 185 checks across 12 suites, all passing.

**Status:** Phase 2A is **Completed · Submitted for Owner Review**. Phase 2B requires the owner's
written approval and the Admin Console entitlement check. Nothing is purchased or connected.

---

## [0.4.0] — 2026-09-11 — Verified Make inspection, scope matrix, measured thresholds

Responds to the owner's clarifications of 2026-09-11. **The first verified external fact in this
project** arrives here: the Make account was inspected read-only under explicit authorisation.
Nothing was created, changed, run or purchased.

**Verified — Make account, read-only**

Six read-only calls; four further capabilities deliberately not called and the reasons recorded.
Findings that change the design:

- Plan is **Free**: 1,000 operations a month, **2 active scenarios**, 1 data store of 1 MB, 512 MB transfer, 5 MB maximum file size, 15-minute minimum scheduling interval, no overage — work stops rather than billing. Zone is **us2**, a data-residency fact for the contract review.
- **The design needs five scenarios and the plan allows two.** That is the binding constraint, not operations. Recommendation: start with two — submission validation and evidence registration — and make review notification a daily digest.
- 512 MB of transfer against ~900 MB of photographs a month at three projects turns a design habit into a hard rule: **image bytes must never pass through the orchestration layer.**
- ~800 estimated operations against 1,000 available is 80% of the ceiling with no overage.
- **Every required integration is present**, including a dedicated AppSheet connector, Claude and QuickBooks. The constraint is capacity, not capability.

**Changed — cost statement, revision 3**

Revision 2's "expected pilot cost is USD 0" is withdrawn as an overstatement. The statement is now:
**no new mandatory subscription has been identified before entitlement verification, and variable
automation, AI and storage costs may arise when those capabilities are enabled.** Workspace and
QuickBooks are existing costs; AppSheet Core is assumed USD 0 incremental pending the console check;
Make is potentially free during limited testing but **not confirmed as permanently free**; Claude is
optional for capture and a mandatory usage cost once analysis is enabled; additional storage is a
future conditional cost.

**Changed — migration timing**

The "year 1.4" point is **withdrawn**. It extrapolated one variable and read as a forecast.
`18-migration-threshold-strategy.md` replaces it with nine measured trigger conditions — row count,
cell count, sync time, app open time, update conflicts, automation delay, API limits, error rate and
administrative burden — plus the formula that converts a three-month trailing growth rate into an
estimated date, and a scenario table explicitly labelled as scenarios rather than predictions.

**Changed — volume**

`14-storage-and-image-volume.md` revision 2 states all eleven assumptions with low, expected and
high values, gives three scenarios at 3, 10, 20 and 50 projects, and lists the nine things the
projection must be compared against — none of which is known until the Admin Console storage screen
is read. The "non-issue" framing is withdrawn.

**Changed — the one-minute target**

Recorded in the owner's wording: **no more than 75 seconds, excluding the physical time to position
and take photographs.** `19-real-device-test-protocol.md` defines the full matrix — oldest Android
and iPhone, normal, weak and offline connections, one activity with six photographs and multiple
activities — at least five runs per cell, recording median, 90th percentile, failures, user mistakes
and synchronisation time. Method A is the first test candidate, not the production decision; nine
measurements decide it against Method B.

**Added**

- `17-lean-table-scope-matrix.md` — **generated** one-page matrix: purpose, primary user, field count, expected monthly rows, app visibility, device sync, deferrability and dependencies for each of the 17 tables. Notes that a capture-and-review-only first release is 12 tables.
- `16-admin-console-checklist-owner.md` — click-by-click, six steps, about 15 minutes, written for a non-technical reader, with a fill-in block and what each answer causes.
- `20-administrator-role-placeholders.md` — the three role placeholders with responsibilities, recovery permissions and six separation-of-duties boundaries. **No name or email is invented.**

**Validation:** 185 checks across 12 suites, all passing.

---

## [0.5.0] — 2026-09-11 — Release 1 at twelve tables, image derivative architecture, operations budget

Responds to the owner's clarifications of 2026-09-11. Nothing was activated, connected, purchased or
deployed; the Make account was not touched again beyond the read-only inspection already recorded.

**Corrected — the scenario-count contradiction**

Revision 1 of the inspection record put "seven scenarios exist, all inactive" and "Active scenarios:
2" in different sections. They described different things and reading them together was reasonable.
Stated separately now: **7 exist, 0 are active, 7 are inactive, and 2 is the plan's ceiling on
concurrently active scenarios, not a count.** Since none is running, the allowance is entirely
available.

**Corrected — the "never through Make" rule**

It conflicted with visual AI analysis, which cannot work from metadata. `22-image-derivative-architecture.md`
replaces the absolute with three classes: **original evidence** never leaves the tenant and is never
opened by any processing path; an **AI review derivative** (1024 px, ~400 KB) is created solely for
analysis; a **report derivative** is created for documents. Verified from Anthropic's vision
documentation: base64, URL and Files API sources exist, the per-image limit is 10 MB base64, cost is
`⌈w/28⌉ × ⌈h/28⌉` visual tokens, image metadata is not read, and in-request images are ephemeral and
deleted after processing. The URL source is rejected because it would need a public address. Through
Make the pilot moves ~86 MB/month against the verified 512 MB limit and 8% of the 5 MB file ceiling;
that path breaks somewhere before twenty projects, which is the trigger to move analysis to a
Workspace-side component. Cost is ~$0.021 per analysed photograph, about $4.50/month at pilot volume.

**Corrected — the operations estimate, which was optimistic for a worse reason than headroom**

The earlier ~800 figure counted scenario runs rather than modules. Each module that acts consumes an
operation per bundle, so per-photograph processing costs ~2,160 operations a month at three projects
— twice the entire allowance for one scenario. `23-operations-budget.md` rebuilds the budget by
removing per-photograph orchestration, which release 1 does not need because it produces no
documents. The result is **703 operations, 70% of the verified limit**, on **2 active scenarios**,
with retries, corrections, duplicate triggers and administrative tests all funded — and with
validation, auditability and error handling untouched. Restoring per-photograph processing needs
**≥3,000 operations/month and ≥3 active scenarios**, stated without a price because the price is
unverified.

**Added — release 1 at twelve tables**

`21-release-1-twelve-tables.md`, generated from the model: Users, Projects, ProjectAssignments,
Locations, ActivityTypes, SiteVisits, VisitActivities, Photos, Snags, Approvals, AuditLog,
IntegrationJobs. Four consolidations, each with its rule and its cost. **262 fields in storage, 137
of them generated rather than typed, and 13 on the normal field form** — with an honest caveat that a
row syncs whole, so form size and sync size are different problems with different fixes.

**Added — storage by artifact class**

Original evidence, AI derivatives, report derivatives, generated documents, rejected temporary
derivatives, backups and version history, each counted separately. A single backup copy nearly
doubles the requirement, which makes the backup policy the largest storage decision in the system.
The high scenario now carries its six requirements: retention rules, archive strategy, closeout
procedure, duplicate handling, Workspace storage verification and the possible additional cost.

**Added — scenario ownership convention**

Existing scenarios may belong to unrelated company work and are not to be modified, renamed,
activated, deleted or reused without separate authorisation. Anything created for this project goes
in a dedicated `AHFR` folder, with a naming convention, a label, system-account ownership and
project-only connections.

**Validation:** 191 checks across 12 suites, all passing, including six new release-1 checks.

---

## [0.6.0] — 2026-09-11 — Capture once, use twice, and the portable handoff package

The owner's operational correction, applied to the canonical model first and to every affected
document from there, plus a self-contained handoff package for transfer to another account.

**Owner decisions D-16 to D-21** — recorded in `docs/00-discovery/10-owner-decisions.md`:

- **D-16 Capture once, use twice.** The supervisor never uploads, selects or describes the same
  evidence twice. One capture serves the contractor-group share and every report. Two operating
  modes, Quick Share and AI Reviewed Share, both capturing exactly once. **`CAP-01`: the workflow
  fails acceptance if the supervisor must select or upload the images a second time.**
- **D-17 AI proposes; the supervisor decides.** Eight advisory proposal columns, separate from the
  confirmed values, with the human disposition recorded.
- **D-18 The written description is not mandatory** for a normal photographic submission. An
  optional site note with a ten-value category vocabulary; four named exceptional workflows where a
  reason is still required.
- **D-19 What AI may not infer**, and where trusted context comes from.
- **D-20 No quantitative or contractual field may originate from an image.**
- **D-21 The capture platform is an interface decision, and it is gated** by `CAP-GATE`.

**Added**

- `model/model.json` → `capture_once` — the canonical block: the nine workflow steps, both modes,
  the optional-note rule, what AI proposes, the nine forbidden inferences, sixteen columns closed to
  AI, the sharing rules, and the fifteen-condition platform gate.
- `tools/gen_capture_once.py` → `docs/02a-plan/24-capture-once-workflow.md`, generated.
- `tools/test_capture_once.py` — **28 new checks (`CAP-01` … `CAP-26`)**, including a regression
  guard that fails if any document reintroduces a mandatory work description.
- `docs/00-discovery/adr/ADR-0009-capture-once-native-share.md`.
- `schemas/ai/evidence-analysis-batch.v1.json` — one advisory analysis per **capture batch**.
- Twenty columns: `SiteVisits.CaptureMode`, `ShareStatus`, `SharedAt`, `SharedByUserID`,
  `ShareTargetLabel`, `ShareAttemptCount`, `AdditionalSiteNote`, `SiteNoteCategory`;
  `Photos.CaptureBatchID`, `CaptureSequence`, `AIProposedEvidenceStage`, `AIProposedActivityText`,
  `AIProposedCaptionEN/AR`, `AIVisibleCondition`, `AIPossibleSnag`, `AIImageQualityWarning`,
  `AIUncertaintyNote`, `AIProposalDisposition`, `AIAnalysedAt`. Four new enums.
- Risks **R-33 … R-39**; external facts **EF-24 … EF-26**; open questions **OQ-15 … OQ-19**.
- `docs/02a-plan/19-real-device-test-protocol.md` §4b — the `CAP-GATE` test, fifteen conditions,
  both platforms, both modes, with an explicit blocking rule for each.
- **The portable handoff package:** `START-HERE-NEW-CLAUDE.md`, `MASTER-SPEC-CONSOLIDATED.md`,
  `CURRENT-STATUS-AND-NEXT-PROMPT.md`, `DECISIONS-AND-ASSUMPTIONS.md`, `HANDOFF-MANIFEST.json`,
  `HANDOFF-MANIFEST.md`.

**Changed — and not quietly**

- **AI analysis is re-costed upward.** Every captured photograph is analysed, not only the ~60% a
  reviewer later approves, because a proposal that arrives after the review proposes nothing to
  anybody. Pilot cost rises from ~$4.50 to **~$7.56 a month**; derivative transfer roughly doubles,
  moving the Option A ceiling from twenty projects down to about ten.
- **The AI proposal does not fit the free orchestration tier.** Roughly 1,440 operations a month
  against a 1,000 limit, and a third scenario against a ceiling of two. Four honest responses are
  costed in `23-operations-budget.md` §6b; release 1 ships Quick Share and the capture-once
  guarantee holds regardless.
- `MASTER_SPEC.md` is retained as the **received baseline** and now points at
  `MASTER-SPEC-CONSOLIDATED.md` as the current authority. §3a carries the correction.
- WhatsApp is now explicitly an **output** channel by native share, while remaining out of scope as
  an input channel. Corrected in `01-mvp-boundary.md`, `02-architecture.md` and the discovery
  summary, which previously said only "no WhatsApp automation".
- `21-release-1-twelve-tables.md` now reports **282 fields, 17 on the field form, of which 5 are
  mandatory** — and none of the five is a description.

**Validation:** **219 checks across 13 suites, all passing.** Byte-identical regeneration confirmed.

---

## [0.7.0] — 2026-09-11 — Minimum interaction, a confirmed activity, and filtered analysis

The owner's correction pass on the capture-once implementation. Three things were wrong: it still
asked the supervisor for more than it needed to, it had thrown out the trusted activity
classification along with the untrusted one, and it assumed every photograph needs an immediate
model call.

**Owner decisions D-22 to D-24** — recorded in `docs/00-discovery/10-owner-decisions.md`:

- **D-22 Minimum interaction.** The claim that the supervisor "must supply five fields" is
  **withdrawn**. **Zero fields are mandatory manual inputs on the normal path.** Identity from the
  session; date and time from the device; project from the single active assignment, the last used
  today or the default; location from the project default or the last used; capture mode defaults to
  Quick Share; evidence stage proposed by analysis, pre-tagged, or left `Pending`. **Declaring an
  activity is no longer the price of submitting evidence** — the completeness rule now requires
  *evidence*, not an activity.
- **D-23 A confirmed structured activity.** `Photos.ConfirmedActivityTypeID` is trusted and set only
  by a human; `AIProposedActivityText` and `AIProposedActivityTypeID` are advisory and read by the
  confirmation screen and nothing else; `ClassificationStatus` carries the state, and `Pending` —
  the normal Quick Share outcome — blocks nothing.
- **D-24 Filtered analysis.** Immediate for AI Reviewed Share, deferred and filtered for Quick
  Share. Near-duplicates, unusable images, deletions, exclusions and already-analysed files never
  reach a model call. `PerceptualHash` and `QualityScore` detect them locally, at no cost.

**Added**

- Eight columns: `Photos.AIProposedActivityTypeID`, `ConfirmedActivityTypeID`,
  `ClassificationStatus`, `ConfirmedByUserID`, `ConfirmedAt`, `AnalysisEligibility`,
  `PerceptualHash`, `QualityScore`. Two enums: `ClassificationStatus`, `AnalysisEligibility`.
- Three canonical blocks in `model/model.json` → `capture_once`: `minimum_interaction`,
  `classification`, `ai_analysis_policy`.
- **Twenty new checks (`CAP-27` … `CAP-45`), and `EVD-11b`.** Total **240 across 13 suites.**
  `CAP-29` is the new regression guard: a required, user-typed column with no automatic source on a
  field-path table fails the suite.
- Risks **R-40 … R-43**; open questions **OQ-20 … OQ-22**; assumptions **A-13 … A-15**.
- `tools/run_validation.py --out PATH` writes the evidence document **outside the repository**, so
  an exact commit can be validated without modifying a tracked file.
- `tools/render_review_pack.py` — the review-pack renderer, promoted from a scratch script.
- `dist/DELIVERY-RECEIPT.md` and `.json` carry `SOURCE_COMMIT_SHA` and `PACKAGE_SHA256`. **The
  manifest no longer records the archive's checksum**, and neither file is a member of the archive,
  so nothing attempts to contain a digest of a file containing itself.

**Changed**

- `tools/build_handoff.py` now clones the exact commit, validates it off-tree, checks the clone is
  clean before and after, builds the ZIP **from the clone rather than the working tree**, extracts
  it and re-runs the full suite from the extracted copy.
- The field workflow is rebuilt: **11–14 taps**, down from 16–21, entirely by not asking questions.
- **Costs revised downward, and relabelled as estimates.** Claude ~$6.28/month (Quick Share) and
  ~$6.95 (AI Reviewed) at pilot volume, from ~$7.56. Make ~1,167 and ~1,353 operations a month,
  from ~1,440. **The conclusion is unchanged:** neither policy fits the free orchestration tier,
  because three operations per photograph is irreducible once bytes pass through an orchestrator.
- `evidence.py` — a visit carrying photographs and no activity is a valid photographic submission;
  a visit carrying neither is still refused.

**Validation:** **240 checks across 13 suites, all passing.** Byte-identical regeneration confirmed,
at the packaged commit and from the extracted archive.
