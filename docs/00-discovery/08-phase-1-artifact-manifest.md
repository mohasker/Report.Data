# Phase 1 Artifact Manifest

**Document ID:** AH-SYS-P0-008 · **Revision:** 0 · **Status:** draft for owner approval

Exactly what will be created in Phase 1, and exactly what will not. Phase 1 begins only after the
owner approves the Phase 0 discovery output and answers the blocking questions.

**Phase 1 creates documents, schema definitions and synthetic seed data. Nothing else.**
No Google Sheet, no AppSheet app, no Drive folder, no Make scenario, no API connection, no
credential, no real client data.

---

## 1. Documents — `docs/01-data-foundation/`

### `01-data-dictionary.md`
The complete dictionary for every table in §5. For each column: name · type · required · key role ·
default · validation rule · allowed values · source (user, system, integration, calculation) ·
sensitivity (public / internal / financial / confidential) · which roles may read and write it ·
whether it is included in `ContentHash` · a worked example value.
Covers: Users, Roles, ProjectAssignments, Projects, Clients, Contacts, Locations, ActivityTypes,
Units, SiteVisits, VisitActivities, Photos, Snags, DocumentTemplates, DocumentJobs, Documents,
Approvals, IntegrationJobs, AuditLog, Counters.
Designed but **not built** in the MVP, so that adding them later is additive: Materials,
MaterialUsage, Equipment, VisitEquipment, Employees/Crews, VisitManpower, Contracts, WorkOrders,
BOQItems, InvoiceRequests, InvoiceLines.

### `02-key-and-id-strategy.md`
Identifier generation per table · immutability rules · foreign-key conventions · why display codes
(`ProjectCode`, `LocationCode`) are never keys · the **canonical serialisation** used for
`ContentHash`, including the exact ordered field list per entity and the exclusion list — this
resolves conflict **C-06** · `EntityVersion` increment rules · what a hash change invalidates
downstream.

### `03-status-transition-matrix.md`
For every entity with a lifecycle (SiteVisit, VisitActivity, Photo, Snag, DocumentJob, Document,
Approval, and later InvoiceRequest): the full transition table — from-state, to-state, permitted
actor roles, required preconditions, side effects, what the transition invalidates, and which
transitions are explicitly forbidden. Includes the illegal-transition list that Scenario 01 enforces.

### `04-security-model.md`
Role definitions · the roles × tables × operations matrix with a justification for every grant ·
security-filter expressions per table · the fields that are hidden from field roles and the reason ·
the tables kept entirely out of the field app's data set (SEC-04) · the override-recording rule
(SEC-05) · the security tests each gate must execute.

### `05-evidence-rules.md`
How per-ActivityType rules (`RequiresBeforePhoto`, `RequiresAfterPhoto`, `RequiresQuantity`,
`RequiresMaterial`, `RequiresSnagCheck`) combine into a submission-completeness decision · which
rules are enforced on-device and which server-side, resolving conflict **C-07** · mandatory-caption
stages · the old-photo warning threshold (warn, never auto-reject) · duplicate-detection policy
(flag, never delete) · GPS as evidence rather than a gate, resolving **C-08**.

### `06-naming-and-numbering.md`
Photo and document filename patterns from §6 · character sanitisation rules · collision handling ·
folder naming and the idempotent provisioning algorithm · the numbering-service design (ADR-0005)
with one counter per series, atomic update, no speculative reservation, and the recorded starting
number that continues existing manual series (**BQ-08**, **C-04**).

### `07-migration-and-versioning.md`
Schema version numbering · additive-change policy (new columns permitted, renames and type changes
controlled) · how a schema change is applied without breaking in-flight records · backfill approach ·
rollback approach · the **defined trigger** for migrating off Google Sheets (ADR-0002, **R-01**),
stated as a measurable threshold rather than a feeling.

---

## 2. Machine-readable schemas — `schemas/`

```
schemas/tables/*.schema.json          One JSON Schema per table: columns, types,
                                      required, enums, formats, foreign keys,
                                      and the ContentHash field list.
schemas/ai/evidence-analysis.v1.json  Strict schema for §9.1 output: observable_facts,
                                      likely_activity, evidence_stage_assessment,
                                      visible_condition, potential_snags,
                                      safety_concerns, image_quality,
                                      contradictions_with_caption, uncertainty,
                                      confidence_0_to_1, suggested_professional_caption.
                                      additionalProperties: false. No numeric quantity
                                      fields exist in the schema at all — the model
                                      cannot emit a quantity because there is nowhere
                                      to put one.
schemas/ai/report-qa.v1.json          Strict schema for §9.3 output: issue list with
                                      severity, section, evidence reference,
                                      explanation, proposed correction.
schemas/README.md                     How schemas are versioned and how a version is
                                      retired.
```

Written in Phase 1, used in Phase 4. Defining the contract before the integration is what makes the
integration testable.

---

## 3. Seed and synthetic data — `seed/`

```
seed/roles.csv                    The eight roles from §5.2 with descriptions.
seed/units.csv                    Units of measure (m², m³, lm, no., hr, kg, l …).
seed/activity_types.csv           All landscaping and civil activities listed in §5.7,
                                  with discipline, codes, EN/AR names and evidence and
                                  quantity rules per activity.
seed/workflow_statuses.csv        Status vocabularies with descriptions.
seed/evidence_stages.csv          The nine stages from §5.10.
seed/snag_categories.csv          Category and severity vocabularies.
seed/synthetic_projects/
    clients.csv                   Three fictional clients — different payment terms,
                                  currencies-of-record and contacts.
    projects.csv                  Three fictional projects — different disciplines,
                                  reporting frequencies, templates, approval routes.
    locations.csv                 Hierarchical locations per project, deliberately
                                  including similar names across projects to make a
                                  leakage bug visible rather than subtle.
    users.csv                     Fictional users with non-routable example addresses.
    project_assignments.csv       Deliberately overlapping and non-overlapping
                                  assignments, including one multi-project user, to
                                  exercise the segregation tests.
seed/README.md                    States clearly: SYNTHETIC TEST DATA ONLY. Never load
                                  into a production environment. Contains no real
                                  client, person, contract or contact.
```

All synthetic data uses reserved example domains and obviously fictional names. No real client,
person, address, contract value or contact appears anywhere in this repository (operating rule 2).

---

## 4. Configuration reference — `config/`

```
config/config.reference.md   Every external value the system needs, as a NAMED VARIABLE:
                             variable name · what it is · who owns it · where the real
                             value is stored (Make connection / environment variable /
                             secret manager) · which phase needs it · whether it is a
                             secret. VALUES ARE NEVER RECORDED HERE.
config/.env.example          Variable names with empty values and comments. No secrets,
                             no IDs, no keys — not now, not ever.
config/tax-rules.example.csv Structure of a configuration-driven tax rule, with the
                             named zero-rate rule as the worked example (BQ-06). No
                             assumed rate is stated as fact.
config/rounding-policy.md    The single central rounding policy: decimal places per
                             currency, rounding direction, where rounding is applied
                             in the line → tax → total sequence, and worked examples
                             (§11, R-23).
```

---

## 5. Repository housekeeping

```
README.md          Updated: current phase, status, navigation, and the standing rule
                   that nothing in this repository is a claim of a tested system.
CHANGELOG.md       Dated revision entries per §16 item 16.
docs/VERSION-MANIFEST.md   Document ID, revision, date and approval status for every
                   controlled document — the ISO 9001 document-control habit applied
                   to the repository itself.
.gitignore         Excludes environment files, credentials, exports and local artefacts.
```

---

## 6. Explicitly out of scope for Phase 1

| Not created | Created in |
|---|---|
| Google Sheet workbook | Phase 2 |
| AppSheet application | Phase 2 |
| Google Drive folder structure | Phase 3 |
| Make scenarios | Phase 3 |
| API connections, OAuth authorisations, credentials of any kind | The phase that needs them, authorised by the owner directly in each provider's console |
| Prompt **text** files | Phase 4 (schemas come first, deliberately) |
| Document templates | Phase 5 |
| Financial calculation implementation | Phase 6 |
| Any real client, project, contract or contact record | Phase 8, under controlled import |

---

## Phase 1 exit criteria

1. Data dictionary reviewed field by field with the owner or nominated administrator.
2. Status-transition matrix approved, including what each transition invalidates.
3. Security model reviewed grant by grant.
4. `ContentHash` canonical field list agreed (**C-06** closed).
5. Migration threshold for leaving Google Sheets defined as a measurable number (**R-01**).
6. Three synthetic projects modelled end to end with **no project-specific logic anywhere in the model**.
7. Configuration register complete, with every value owned by a named person and **no value recorded in this repository**.
