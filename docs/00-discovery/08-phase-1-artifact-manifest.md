# Phase 1 Artifact Manifest

**Document ID:** AH-SYS-P0-008 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** approved; incorporates the seventeen additional deliverables required by **D-15**

Phase 1 creates **repository artifacts, schemas, synthetic data, specifications, validation rules,
security models, state-transition models, prompt schemas and documentation** — and nothing else
(D-14).

**Phase 1 does not:** connect a production Google account · connect AppSheet production data ·
create production Make scenarios · create or use Claude API credentials · connect QuickBooks ·
upload real client or project photographs · send email or messages · create invoices or accounting
transactions · publish or share external documents.

---

## D-15 deliverable coverage

| # | Required addition | Delivered in |
|---|---|---|
| 1 | Fully normalised multi-project, multi-client data model | `model/model.json`, `schemas/tables/`, `01-data-dictionary.md` |
| 2 | ProjectAssignments supporting multi-project users | `ProjectAssignments` table · `04-security-model.md` · segregation tests |
| 3 | Project-specific locations and hierarchical sublocations | `Locations` (self-referencing `ParentLocationID`) · validation of depth and project consistency |
| 4 | Project-specific activity and evidence rules | `ActivityTypes` + `ProjectActivityRules` override table · `05-evidence-rules.md` |
| 5 | Project-specific templates and reporting frequencies | `DocumentTemplates` (type × language × project) · `Projects.ReportingFrequency` |
| 6 | Project-specific approval matrices | `ApprovalMatrix` + `ApprovalDelegations` · `10-approval-and-delegation-model.md` |
| 7 | Legal-entity configuration | `LegalEntities` · `08-legal-entity-and-bilingual-model.md` |
| 8 | Data classification and residency configuration | `DataClassifications`, `ResidencyRequirements`, `ResidencyAssignments` · `09-data-classification-and-residency.md` |
| 9 | Configurable numbering and migration from existing sequences | `NumberingSeries`, `NumberRegister` · `06-naming-and-numbering.md` · reference implementation and concurrency test |
| 10 | Bilingual / RTL readiness | Paired `*_EN` / `*_AR` columns, `Languages`, `Users.Language` · `08-legal-entity-and-bilingual-model.md` · Unicode integrity test |
| 11 | Complete allowed-status-transition matrix | `03-status-transition-matrix.md` · machine-readable in `model/model.json` · transition tests |
| 12 | Role and row-level security matrix | `04-security-model.md` · security-filter reference implementation · access tests |
| 13 | Deterministic calculation specification | `11-deterministic-calculation-spec.md` · `tools/calc.py` · worked test cases |
| 14 | Audit-log and immutable approval/version model | `AuditLog`, `Approvals`, `EntityVersions` · `02-key-id-and-hash-strategy.md` · content-hash tests |
| 15 | Synthetic seed data for ≥3 materially different projects | `seed/synthetic_projects/` |
| 16 | Tests proving nothing crosses a project boundary | `tools/test_segregation.py` → `17-validation-evidence.md` |
| 17 | Every external fact awaiting confirmation, by blocking phase | `16-external-facts-register.md` |

---

## 1. Canonical model and generators

```
model/model.json          The single source of truth for Phase 1: tables, columns, types,
                          keys, enums, foreign keys, sensitivity, bilingual pairs,
                          ContentHash membership, status-transition rules, and the
                          role × table × operation matrix.
tools/                    Standard-library Python only. No third-party dependency, so the
                          owner can run every check on any machine with Python 3.
  modeldef.py             Model loader and shared helpers.
  gen_schemas.py          Emits schemas/tables/*.schema.json from the model.
  gen_data_dictionary.py  Emits docs/01-data-foundation/01-data-dictionary.md.
  validate_seed.py        Validates every seed file against the model: types, required,
                          enums, uniqueness, referential integrity, project consistency.
  security.py             Reference implementation of row-level access from
                          ProjectAssignments and the role matrix.
  numbering.py            Reference numbering service: reserved → issued → cancelled.
  calc.py                 Deterministic calculation engine (decimal, never float).
  contenthash.py          Canonical serialisation and content hashing.
  test_*.py               Executable checks (segregation, numbering, calculation,
                          transitions, content hash, bilingual integrity).
  run_validation.py       Runs everything and writes the validation evidence document.
```

Generated artifacts are reproducible from the model, so the data dictionary can never drift from
the schemas.

## 2. Documents — `docs/01-data-foundation/`

| File | Content |
|---|---|
| `00-PHASE-1-SUMMARY.md` | What was built, what was executed, what remains open, and the Phase 2 gate request. |
| `01-data-dictionary.md` | **Generated.** Every table and column: type, key, required, default, validation, allowed values, source, sensitivity, read/write roles, ContentHash membership, example. |
| `02-key-id-and-hash-strategy.md` | Identifier generation, immutability, foreign-key conventions, `EntityVersion`, and the canonical serialisation that defines `ContentHash` — closing conflict C-06. |
| `03-status-transition-matrix.md` | Every lifecycle: from-state, to-state, permitted roles, preconditions, side effects, what each transition invalidates, and the forbidden list. |
| `04-security-model.md` | Roles × tables × operations with a justification per grant; security-filter expressions; fields withheld from field roles; tables kept out of the field app entirely. |
| `05-evidence-rules.md` | Per-activity evidence rules and project overrides; on-device vs server-side enforcement (C-07); mandatory captions; old-photo warning; duplicate flagging; GPS as evidence not gate (C-08). |
| `06-naming-and-numbering.md` | File and folder naming, sanitisation, collision handling; the numbering service with per-entity/type/year/scope/client series and the reserved → issued → cancelled lifecycle; migration of the existing manual register (D-10). |
| `07-migration-and-versioning.md` | Schema versioning, additive-change policy, backfill, rollback, and the measurable threshold for migrating off Google Sheets (R-01). |
| `08-legal-entity-and-bilingual-model.md` | `LegalEntities` (D-02) and the bilingual/RTL architecture (D-11). |
| `09-data-classification-and-residency.md` | Classification model, per-client/contract/project residency rules, data-flow map for Google, Make, Claude, AppSheet and QuickBooks, subprocessors and likely processing locations, and the contract-review checklist (D-12). |
| `10-approval-and-delegation-model.md` | Approval stages, delegation with start/end dates, scope and project limits, acting vs original responsible user, self-approval prohibition, audit record (D-09). |
| `11-deterministic-calculation-spec.md` | Calculation order, rounding policy, tax-rule and version preservation, retention, advance recovery, cumulative quantity control, and worked test cases (D-08). |
| `12-appsheet-feature-to-plan-matrix.md` | Requirement-by-requirement matrix with the verification method, plus requirements the platform may not safely or economically support (D-04). |
| `13-quickbooks-mapping-and-inspection.md` | Mapping fields and the compatibility inspection checklist to be executed before the financial phase (D-07). |
| `14-orchestration-contract-and-runbook.md` | Scenario inventory, idempotency keys, correlation IDs, failure classes, retry limits, dead-letter queue, environment separation, connection ownership, and a non-developer operator runbook outline (D-05). |
| `15-claude-prompt-and-schema-spec.md` | Prompt specifications and versioning, output schemas, data-minimisation rules, injection controls, and cost-control design (D-06). |
| `16-external-facts-register.md` | **Every external fact still awaiting confirmation, categorised by the phase it blocks** (D-15 item 17). |
| `17-validation-evidence.md` | **Generated from executed checks.** Results recorded whether they pass or fail. |

## 3. Machine-readable schemas — `schemas/`

Per-table JSON Schema generated from the model, plus the AI output contracts written now and used in
Phase 4: `evidence-analysis.v1.json` and `report-qa.v1.json`. Both are closed schemas
(`additionalProperties: false`) containing **no numeric quantity field**, so a model cannot emit a
quantity even if asked.

## 4. Seed and synthetic data — `seed/`

Controlled vocabularies (roles, units, languages, document types, evidence stages, workflow
statuses, snag categories, data classifications, placeholder tax rules, numbering series) and
synthetic data for **three materially different projects** — different clients, contacts,
disciplines, location hierarchies, activity and evidence rules, assigned users, approval routes,
templates, numbering series, reporting frequencies, billing configuration and residency rules.

Deliberate traps are included so that a segregation or validation bug is visible rather than subtle:
similar location names across projects, a multi-project user, a user with no assignment, a currency
mismatch, and an Arabic-only client name.

**All synthetic. No real client, person, contract, address or contact appears anywhere.**

## 5. Configuration — `config/`

`config.reference.md` (named variables, owners, storage location — **never values**),
`.env.example` (names only), `tax-rules.example.csv` (placeholder, no classification named),
`rounding-policy.md`.

## 6. Phase 1 exit criteria

1. Data dictionary reviewed field by field.
2. Status-transition matrix approved, including what each transition invalidates.
3. Security model reviewed grant by grant.
4. `ContentHash` canonical field list agreed (C-06 closed).
5. Measurable migration threshold defined (R-01).
6. Synthetic projects modelled end to end with **no project-specific logic anywhere in the model**.
7. Configuration register complete, with **no value recorded in this repository**.
8. Validation evidence recorded for schema conformance, referential integrity, segregation, numbering concurrency, deterministic calculation, status transitions, content hashing and bilingual integrity.
9. External-facts register complete and categorised by blocking phase.
