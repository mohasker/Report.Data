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
