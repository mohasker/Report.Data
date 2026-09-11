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
