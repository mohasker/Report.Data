# Phase 1 Validation Evidence

**Document ID:** AH-SYS-P1-017 · **Revision:** 2 · **Status:** Validated Locally · **Generated from an executed run**

> **This is evidence of locally executed checks against synthetic data. It is not evidence that any external platform works.** See section 3.

## 1. Reproduction record

| | |
|---|---|
| **Commit tested** | `cf9ffed19efe437a305b6d1d68593439e4bb1901` |
| **Commit subject** | Validation evidence: clean-tree reproduction record |
| **Command executed** | `python3 tools/run_validation.py` |
| **Executed at** | 2026-09-11 08:23:03 UTC |
| **Python** | 3.11.15 (CPython, GCC 13.3.0) |
| **Operating system** | Linux 6.18.44-fc-v24 (x86_64) |
| **Environment** | Ephemeral Linux container. This run made no network call, used no credential and contacted no external service |
| **Third-party dependencies** | **None.** Python standard library only |
| **Model version** | 1.0.0 |
| **Working tree before the run** | MODIFIED — see below |

```
M README.md
 M docs/01-data-foundation/17-validation-evidence.md
 M docs/02a-plan/00-PHASE-2A-PLAN.md
 M docs/02a-plan/01-appsheet-workbook.md
 M docs/02a-plan/02-security-filter-specification.md
 M docs/02a-plan/09-cost-and-licensing-matrix.md
 M docs/OWNER-REVIEW-PACK.md
 M docs/VERSION-MANIFEST.md
 M model/model.json
 M tools/build_model.py
 M tools/evidence_meta.py
 M tools/gen_appsheet_workbook.py
 M tools/run_validation.py
 M tools/test_configurability.py
?? docs/02a-plan/11-lean-mvp-scope.md
?? docs/02a-plan/12-appsheet-entitlement-checklist.md
?? docs/02a-plan/13-field-workflow-and-taps.md
?? docs/02a-plan/14-storage-and-image-volume.md
?? tools/test_lean_mvp.py
```

> The run was executed against a working tree containing uncommitted changes. The commit recorded above is the parent commit, not the exact state tested. Re-run after committing to obtain a clean reproduction record.


### Byte-identical regeneration

Every generated artifact was hashed (SHA-256) before regeneration, regenerated from `model/model.json`, and hashed again. **52 artifacts** were compared: 6 generated documents (the canonical model, the data dictionary, the transition matrix, the security matrix, the AppSheet workbook and the security-filter specification) and all 46 table schemas.

**Result: all artifacts came back byte-identical.** Regeneration is deterministic, so the committed artifacts are exactly what the model produces.

## 2. Summary

**185 of 185 checks passed.**

| # | Suite | Kind | Checks | Passed | Failed |
|---|---|---|---|---|---|
| 1 | Seed conformance | structural | 3 | 3 | 0 |
| 2 | Lean operational MVP | structural | 13 | 13 | 0 |
| 3 | Configurability and unbounded width | structural | 12 | 12 | 0 |
| 4 | Project segregation | logic | 12 | 12 | 0 |
| 5 | Role separation, time-bound access and recoverability | logic | 31 | 31 | 0 |
| 6 | Evidence rules | logic | 14 | 14 | 0 |
| 7 | Status transitions, approvals and delegation | structural | 20 | 20 | 0 |
| 8 | Content hashing and approval binding | logic | 14 | 14 | 0 |
| 9 | Document numbering | simulation | 13 | 13 | 0 |
| 10 | Deterministic calculation | logic | 22 | 22 | 0 |
| 11 | Bilingual and right-to-left readiness | structural | 13 | 13 | 0 |
| 12 | Governance and safety rules | structural | 18 | 18 | 0 |
| | **Total** | | **185** | **185** | **0** |

### Console output

```
========================================================================
  Seed conformance                                       3 passed   0 failed
  Lean operational MVP                                  13 passed   0 failed
  Configurability and unbounded width                   12 passed   0 failed
  Project segregation                                   12 passed   0 failed
  Role separation, time-bound access and recoverability  31 passed   0 failed
  Evidence rules                                        14 passed   0 failed
  Status transitions, approvals and delegation          20 passed   0 failed
  Content hashing and approval binding                  14 passed   0 failed
  Document numbering                                    13 passed   0 failed
  Deterministic calculation                             22 passed   0 failed
  Bilingual and right-to-left readiness                 13 passed   0 failed
  Governance and safety rules                           18 passed   0 failed
========================================================================
  TOTAL 185/185 checks passed
```

### Artifact regeneration output

```
$ python3 tools/build_model.py
wrote /home/user/Report.Data/model/model.json
  tables      : 46
  columns     : 829
  enums       : 26
  transitions : 82 allowed, 36 explicitly forbidden
  security    : 10 roles x 46 tables = 460 grants, 20 exceptions
  lean MVP    : 17 tables built first, 29 deferred but designed
$ python3 tools/gen_schemas.py
wrote 46 table schemas to schemas/tables/
$ python3 tools/gen_data_dictionary.py
wrote /home/user/Report.Data/docs/01-data-foundation/01-data-dictionary.md (1808 lines)
$ python3 tools/gen_matrices.py
wrote docs/01-data-foundation/03-status-transition-matrix.md
wrote docs/01-data-foundation/04-security-model.md
$ python3 tools/gen_appsheet_workbook.py
wrote docs/02a-plan/01-appsheet-workbook.md
wrote docs/02a-plan/02-security-filter-specification.md
```

## 3. What these checks are NOT evidence of

Recorded at the owner's instruction. **Local model validation must never be represented as proof that an external platform works.** Nothing below has been tested, because nothing below has been connected (D-14).

| Platform or capability | What remains unproven | Proven in |
|---|---|---|
| **AppSheet** | That security filters, offline capture, image fidelity, dependent dropdowns or sync behave as designed on the real platform or on real devices. | Phase 2 |
| **Google Drive** | That folder provisioning is idempotent, that originals survive registration byte-for-byte, or that permissions are least-privilege in practice. | Phase 3 |
| **Make.com** | That scenarios run, that idempotency keys suppress duplicates in the real data store, or that error routes catch what they are meant to. | Phase 3 |
| **Claude API** | That prompts return schema-valid output, that injection defences hold against a real model, or what analysis actually costs. | Phase 4 |
| **Document rendering** | That any template merges, paginates, or renders Arabic and right-to-left text correctly in a PDF. | Phase 5 |
| **QuickBooks Online** | That the company file supports the required tax codes, classes, currencies or API operations, or that totals reconcile. | Phase 7 |
| **Mobile offline sync** | That a visit captured offline on a real phone syncs completely, in order, with its photographs. | Phase 2 field test |
| **Field usability** | That a supervisor can complete a visit faster than the habit it replaces — the single largest risk to the whole system (R-06). | Phase 2 field test |

### How to read each suite

| Suite | Kind | What it does and does not establish |
|---|---|---|
| Seed conformance | `structural` | Validates the synthetic data against the canonical model. Says nothing about any platform. |
| Lean operational MVP | `structural` | Asserts that the 12-18 table build subset holds together, that no lean table requires a deferred one, and that every deferred table keeps its schema. Says nothing about whether the app built from it is fast enough - that is the Phase 2B field measurement. |
| Configurability and unbounded width | `structural` | Scans the model, schemas, security matrix and logic files for hard-coded identifiers, and exercises the rule engines with a fourth project added in memory. |
| Project segregation | `logic` | Runs the reference access rules against synthetic rows. It proves the RULE is correct. It does NOT prove that AppSheet security filters implement it — that is a Phase 2 integration test on the real platform. |
| Role separation, time-bound access and recoverability | `logic` | Runs the reference access rules and grant validation. Proves the rule, not its enforcement by any platform. |
| Evidence rules | `logic` | Runs the effective-rule resolver and completeness evaluator against synthetic visits. Does NOT prove that a mobile form enforces them, on any device, online or offline. |
| Status transitions, approvals and delegation | `structural` | Asserts the declared transition matrix forbids the dangerous paths and that fixtures sit in reachable states. Does NOT prove a running workflow honours it. |
| Content hashing and approval binding | `logic` | Executes the canonical serialisation and hashing. This one is genuinely complete: the algorithm here is the algorithm. Its INTEGRATION into a workflow is not tested. |
| Document numbering | `simulation` | Exercises a reference numbering service whose atomic counter is a SQLite transaction, standing in for the orchestration platform's atomic data-store update. Proves the CONTRACT holds under concurrency. Does NOT prove Make's data store behaves identically — that is a Phase 3 integration test. |
| Deterministic calculation | `logic` | Executes the calculation engine. The arithmetic and the tax-blocking behaviour are real and complete. Reconciliation against QuickBooks is NOT tested and cannot be until Phase 7. |
| Bilingual and right-to-left readiness | `structural` | Asserts bilingual structure and Unicode integrity through hashing. Does NOT prove that any template, PDF renderer or mobile keyboard handles Arabic or RTL correctly. |
| Governance and safety rules | `structural` | Scans the repository and the model for secrets, non-synthetic identities, AI fields in hashes, delete grants and missing attribution. |

**Kinds.** `structural` — an assertion about the shape of the model or the repository. `logic` — executable rules run against synthetic data. `simulation` — a reference implementation standing in for a platform primitive that does not exist yet.

## 4. Acceptance criteria mapping

The fourteen acceptance criteria in `MASTER_SPEC.md` §14, mapped to the checks that bear on them. **No criterion is claimed as met**: Phase 1 can only establish that the rules behind a criterion are correct, never that a built system satisfies it.

| §14 | Criterion | Phase 1 status | Checks | Note |
|---|---|---|---|---|
| 1 | Visit with multiple activities and unlimited child photo rows | Rule defined and tested | `SEED-01`, `EVD-05` | The model supports it and fixtures exercise it. The practical limit is a Phase 2 measurement. |
| 2 | Project-dependent locations function correctly | Rule defined and tested | `SEG-10`, `SEG-11`, `EVD-02` | Rule proven against synthetic data; the dependent dropdown itself is Phase 2. |
| 3 | No cross-project leakage; multi-project users switch cleanly | Rule defined and tested | `SEG-01`, `SEG-02`, `SEG-03`, `SEG-04`, `SEG-05`, `SEG-06`, `SEG-07`, `SEG-08`, `SEG-09`, `SEG-10`, `SEG-12`, `ACC-02`, `ACC-06`, `ACC-15` | The rule is proven exhaustively. Enforcement by AppSheet security filters is the Phase 2 gate. |
| 4 | Originals in the correct protected location and unchanged | **Not tested in Phase 1** | `GOV-12`, `GOV-13` | The write-once CONTRACT is represented in the model. Nothing has been stored anywhere. |
| 5 | Mandatory evidence rules prevent incomplete submission | Rule defined and tested | `EVD-05`, `EVD-06`, `EVD-07`, `EVD-08`, `EVD-09`, `EVD-10`, `EVD-11`, `EVD-12` | The rules are executable and correct. On-device enforcement is Phase 2. |
| 6 | Reviewers approve/reject visits and individual photographs with comments | Rule defined and tested | `TRN-03`, `TRN-11`, `TRN-19` | Transitions and prohibitions are declared. The review UI is Phase 2. |
| 7 | Duplicate triggers do not create duplicate jobs or documents | Rule defined and tested | `NUM-01`, `NUM-09`, `TRN-07` | Numbering uniqueness is proven under concurrency in a simulation. Webhook idempotency is Phase 3. |
| 8 | Claude produces schema-valid analysis and flags uncertainty | **Not tested in Phase 1** | — | Schemas are written; no API call has been made. Phase 4. |
| 9 | Monthly draft generated from an immutable approved snapshot | Rule defined and tested | `HASH-07`, `HASH-08`, `TRN-05` | Snapshot and hash mechanics are defined and tested. Generation is Phase 5. |
| 10 | Rendered PDF passes visual inspection | **Not tested in Phase 1** | — | No document has been rendered. Phase 5. |
| 11 | Editing approved source data invalidates or versions the approval | Rule proven in logic | `HASH-03`, `HASH-04`, `HASH-05`, `HASH-06`, `HASH-07`, `HASH-08`, `TRN-10` | The hashing algorithm is the real one; this is as close to complete as Phase 1 can get. |
| 12 | No external email or accounting posting without the correct approval | **Not tested in Phase 1** | `TRN-06`, `GOV-05`, `CALC-01` | Neither capability exists. Phase 7. |
| 13 | Tested failures produce actionable logs and recover without data loss | **Not tested in Phase 1** | `NUM-07`, `NUM-08` | The failure taxonomy and error queue are specified; nothing has failed for real. Phase 3. |
| 14 | Operator and administrator guides exist | Rule defined and tested | — | The operator runbook outline exists; it is completed in Phase 3 when the scenarios do. |

## 5. Every check executed

Listed in full so a reviewer can see what was measured rather than taking a summary on trust. The evidence column is the value the check actually produced.

### Seed conformance  ·  `structural`  ·  3/3 passed

Every seed file conforms to the canonical model: columns, types, formats, vocabularies, keys, uniqueness, referential integrity and project consistency.

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `SEED-01` | PASS | Every seed file validates against the model with no error | 31 files, 206 rows, 0 errors |
| `SEED-02` | PASS | Every foreign key resolves within the seeded data | 0 unresolvable-by-design references (tables not built until a later phase) |
| `SEED-03` | PASS | At least three materially different projects are present | 3 projects with 3 clients, 3 reporting frequencies, 3 billing methods, 2 document languages |

### Lean operational MVP  ·  `structural`  ·  13/13 passed

A 12-18 table subset is built first, the 46-table model stays the reference architecture, and every deferred table keeps a schema so adding it later is additive.

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `LEAN-01` | PASS | The lean MVP is within the size the owner asked for | 17 tables (target 12-18); 29 deferred |
| `LEAN-02` | PASS | Every capability the owner listed is carried by a lean table | all 11 listed capabilities covered |
| `LEAN-03` | PASS | Every required reference to a deferred table has a declared lean replacement column | 6 replacements declared: ActivityTypes.DisciplineID -> DisciplineCode; Documents.TemplateID -> TemplateFileKey, LanguageCode; NumberRegister.SeriesID -> SeriesKey; ProjectAssignments.RoleID -> RoleCode; Projects.ClientID -> ClientNameEN, ClientNameAR, ClientKind; Users.RoleID -> RoleCode |
| `LEAN-13` | PASS | Every lean replacement names its column and explains what it carries | 6 overrides, each with a named column and a stated consequence |
| `LEAN-04` | PASS | Optional references to deferred tables are identified, so they can be left empty in the lean build | columns pointing at deferred tables, all optional: ApprovalDelegations, Contracts, DocumentTemplates, Units, WorkOrders |
| `LEAN-05` | PASS | Every deferred table is either folded into a lean table or scheduled to a named phase | 29 deferred tables, all accounted for |
| `LEAN-06` | PASS | Every fold-in states what is lost and when the table returns | 12 fold-ins, each with a stated cost and a restore trigger |
| `LEAN-07` | PASS | Every deferred table keeps its full schema, so returning it is additive | 29 deferred tables retain 452 designed columns |
| `LEAN-08` | PASS | Every load-bearing control survives the trim | segregation, approval binding, audit, numbering register, legal identity, evidence rules and failure visibility all retained |
| `LEAN-09` | PASS | Every project-scoped lean table still carries ProjectID | row-level security is unaffected by the trim |
| `LEAN-10` | PASS | Content hashing survives in the lean subset | hashable lean tables: Photos, SiteVisits, VisitActivities |
| `LEAN-11` | PASS | The cost of deferring delegation is stated plainly, not glossed | **This is the real cost of the lean build.** If the approver is away, approvals stop. Accepted only because no delegate has been named yet. |
| `LEAN-12` | PASS | No table is listed as both built and deferred | the two lists are disjoint |

### Configurability and unbounded width  ·  `structural`  ·  12/12 passed

Adding a project must require only controlled master-data configuration: no modified logic, no cloned application, no duplicated scenario, no rewritten prompt, no changed formula or code (D-01).

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `CFG-01` | PASS | No project, client, contract or user identifier appears in any logic file | 10 logic files scanned, no hard-coded identifier |
| `CFG-02` | PASS | The canonical model names no project, client or contract | identifiers found in model.json: none |
| `CFG-03` | PASS | No generated schema names a project, client or contract | 46 schemas scanned, none names a project |
| `CFG-04` | PASS | Row-level security is expressed in roles and assignments, never in projects | 10 roles x 46 tables, no project named |
| `CFG-05` | PASS | Every project-varying behaviour is a configuration column on Projects | missing: none |
| `CFG-06` | PASS | Behaviour that varies per project has a configuration table of its own | present: ['ApprovalMatrix', 'DocumentTemplates', 'Locations', 'NumberingSeries', 'ProjectActivityRules', 'ProjectAssignments', 'ResidencyAssignments'] |
| `CFG-07` | PASS | A fourth project added as data only is immediately usable, with no code change | USR-0005 now sees 2 projects including PRJ-0004 |
| `CFG-08` | PASS | The new project is invisible to users who are not assigned to it | USR-0006 has no assignment to PRJ-0004 and cannot see it |
| `CFG-09` | PASS | The new project can belong to a different legal entity by configuration | PRJ-0004 issues documents under LE-0002 with its own numbering series |
| `CFG-10` | PASS | The evidence engine serves a brand-new project from the global catalogue | no configuration rows required before a new project can capture evidence |
| `CFG-11` | PASS | Nothing in the model encodes a maximum project count | limit constructs found: none — the model carries no ceiling on how many projects exist |
| `CFG-12` | PASS | Multi-entity operation is structural, not incidental | 2 legal entities across the fixture |

### Project segregation  ·  `logic`  ·  12/12 passed

No data, image, recipient, template, document number or financial record may cross a project boundary (D-15 item 16).

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `SEG-01` | PASS | Field and supervisor roles read only their assigned projects | 6 users x 7 tables checked, no leak |
| `SEG-02` | PASS | A user with no assignment reads nothing at all | rows visible to USR-0011: 0 |
| `SEG-03` | PASS | An expired assignment grants nothing | rows visible to USR-0012 (assignment ended 2026-02-28): 0 |
| `SEG-04` | PASS | A multi-project user sees each assigned project and no others | projects visible to USR-0007: ['PRJ-0002', 'PRJ-0003'] |
| `SEG-05` | PASS | Photographic evidence never crosses a project boundary | no photo visible outside an assignment |
| `SEG-06` | PASS | No field role can read any financial table | 6 users x 5 financial tables, no access |
| `SEG-07` | PASS | Release recipients resolve only to the project's own authorised contacts | 3 projects, recipients confined to their own client |
| `SEG-08` | PASS | A project-specific template is not selectable by another project | TPL-0003 is bound to PRJ-0001 and offered to no other project |
| `SEG-09` | PASS | Project-scoped numbering series are bound to a project | SER-0004 is bound to PRJ-0003; company-wide series carry no project |
| `SEG-10` | PASS | No foreign key references a row belonging to a different project | 206 rows checked, no cross-project reference |
| `SEG-11` | PASS | A location code reused across projects stays distinct because the ID is the key | codes shared across projects: ['BLK-A', 'SITE']; all LocationIDs unique: True |
| `SEG-12` | PASS | A residency restriction disables AI for its own project only | AI disabled: ['PRJ-0003']; AI enabled: ['PRJ-0001', 'PRJ-0002'] |

### Role separation, time-bound access and recoverability  ·  `logic`  ·  31/31 passed

A technical administrator gets no business content; business administration is a separate role; auditor and break-glass access are time-bound and authorised; and the system cannot become unrecoverable.

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `ACC-01` | PASS | All ten roles the owner specified exist in the model | SystemAdministrator, BusinessAdministrator, GeneralManager, TechnicalReviewer, FinanceReviewer, ProjectManager, SiteSupervisor, FieldUser, ReadOnlyAuditor, EmergencyAccess |
| `ACC-02` | PASS | The technical administrator has no read access to evidence, documents, contracts or financial records | tables readable: none (of 11 checked) |
| `ACC-03` | PASS | The technical administrator can still administer technical configuration | vocabularies, roles, units, disciplines, document types and classifications |
| `ACC-04` | PASS | The technical administrator can provision users and project assignments | user provisioning is access administration, not business content |
| `ACC-05` | PASS | The technical administrator can monitor integrations and system health | read-only on both; neither can be altered |
| `ACC-06` | PASS | The business administrator has no access to evidence, documents or financial records either | tables readable: none |
| `ACC-07` | PASS | The business administrator can administer clients, projects and business configuration | clients, projects, locations, activity rules, templates, numbering, legal entities |
| `ACC-08` | PASS | Neither administrator role can create or alter an approval | an administrator must never be able to manufacture an approval |
| `ACC-09` | PASS | Technical and business administration are genuinely different roles | they differ on 31 of 46 tables |
| `ACC-10` | PASS | An auditor reads records while an authorised grant is in force | 16 rows readable inside the grant window |
| `ACC-11` | PASS | The same auditor reads nothing once the grant window closes | 0 rows readable outside the window |
| `ACC-12` | PASS | With no grant at all, the auditor role resolves to no access | 0 rows readable with the grant register emptied |
| `ACC-13` | PASS | An auditor can never write anything | 46 tables, no create or update anywhere |
| `ACC-14` | PASS | Break-glass restores administrative capability | user administration is available under an active emergency grant |
| `ACC-15` | PASS | Break-glass never opens client evidence, documents or financial records | business tables readable under break-glass: none — an administrative emergency is not solved by reading a client's photographs |
| `ACC-16` | PASS | Break-glass access ends when the grant expires | no access outside the grant window |
| `ACC-17` | PASS | A complete emergency grant is accepted | TAG-0003: valid |
| `ACC-18` | PASS | An emergency grant with no reason is refused | a grant without a stated reason is refused |
| `ACC-19` | PASS | An emergency grant with no expiry is refused | a grant without an expiry is refused: no grant is open-ended |
| `ACC-20` | PASS | An emergency grant with no notification sent is refused | break-glass without a sent notification is refused: an unannounced emergency grant is a back door |
| `ACC-21` | PASS | A self-authorised grant is refused | self-authorised grants are refused |
| `ACC-22` | PASS | A grant longer than its configured maximum is refused | grant window of 528h exceeds the configured maximum of 24h |
| `ACC-23` | PASS | A revoked grant stops working immediately | TAG-0004: grant revoked |
| `ACC-24` | PASS | A TechnicalOnly grant is refused for project-scoped content | break-glass is scoped to technical administration and never opens project content |
| `ACC-25` | PASS | Every emergency grant carries a notification recipient and an audit reference | grants missing either: none |
| `ACC-26` | PASS | Every exercised emergency grant is reviewed after use | exercised but unreviewed: none |
| `ACC-27` | PASS | Administrative control cannot rest on a single account | 2 administrator-capable accounts; documented recovery route: TRUE |
| `ACC-28` | PASS | The recovery route is documented with a reference and has been tested | reference recorded, last tested 2026-04-15, result Passed |
| `ACC-29` | PASS | A configuration with neither a backup administrator nor a documented route is detectable as a go-live blocker | the condition is computable from the recovery plan row, so go-live can be blocked on it rather than on someone remembering |
| `ACC-30` | PASS | The recovery plan stores no credential and no route to obtaining one | the plan records whether a route exists and whether it was tested, nothing more |
| `ACC-31` | PASS | No real person is assigned to any role | non-synthetic addresses: none — identities remain pending until the owner supplies them |

### Evidence rules  ·  `logic`  ·  14/14 passed

Evidence requirements are configuration, resolved per project, and a blocked submission always says exactly what to fix (C-07).

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `EVD-01` | PASS | A project with no override inherits the global activity rule | PRJ-0002 / manual weeding inherits RequiresBeforePhoto from the catalogue |
| `EVD-02` | PASS | A project override replaces the global rule and says so | PRJ-0001 requires a quantity for irrigation inspection where the global rule does not |
| `EVD-03` | PASS | The same activity carries different rules on different projects | pesticide application requires 3 photos on PRJ-0001 and 2 on PRJ-0002 |
| `EVD-04` | PASS | An activity can be forbidden on one project and permitted on another | ceiling tile replacement is not permitted on the landscape project |
| `EVD-05` | PASS | A visit meeting every effective rule is judged complete | VIS-0001 complete |
| `EVD-06` | PASS | A snag photograph without a caption blocks submission with a specific reason | VAC-0005: PHO-0007: a caption is mandatory for Snag evidence |
| `EVD-07` | PASS | Removing the required 'After' photograph blocks submission | VAC-0001: An 'After' photograph is required; VAC-0001: At least 3 photographs are required, 2 attached |
| `EVD-08` | PASS | A missing required quantity blocks submission | VAC-0001: A quantity is required for this activity |
| `EVD-09` | PASS | A negative quantity is rejected | VAC-0001: Quantity must not be negative |
| `EVD-10` | PASS | A quantity entered where the rule takes none is rejected | VAC-0007: A 'Before' photograph is required; VAC-0007: An 'After' photograph is required; VAC-0007: At least 2 photographs are required, 0 attached; VAC-0007: A quantity was entered for an activity that does not take one |
| `EVD-11` | PASS | A visit with no activity cannot be submitted | A visit must contain at least one activity |
| `EVD-12` | PASS | Every blocking message names what to fix, never a generic rejection | VAC-0001: A quantity is required for this activity |
| `EVD-13` | PASS | A suspected duplicate is flagged and retained, never deleted or merged | 1 suspected duplicate(s), each pointing at the original and still present |
| `EVD-14` | PASS | Missing GPS never blocks a submission and is recorded as missing, not zero | 6 photographs without GPS, none blocked, none defaulted to 0 |

### Status transitions, approvals and delegation  ·  `structural`  ·  20/20 passed

Work advances only through declared transitions, and an approval is only ever made by an authorised person acting within scope (D-09).

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `TRN-01` | PASS | Every entity with a lifecycle has a declared transition matrix | 11 lifecycles declared: ['Approvals.Decision', 'DocumentJobs.WorkflowStatus', 'Documents.ReleaseStatus', 'InvoiceRequests.FinanceStatus', 'InvoiceRequests.QuickBooksStatus', 'NumberRegister.State', 'Photos.ReviewerDecision', 'Projects.Status', 'SiteVisits.WorkflowStatus', 'Snags.Status', 'VisitActivities.Status'] |
| `TRN-02` | PASS | No declared status is orphaned from the transition matrix | every status appears in the matrix |
| `TRN-03` | PASS | A visit cannot jump from Draft straight to TechnicallyApproved | shortcut absent from the allowed set |
| `TRN-04` | PASS | A visit cannot be approved without passing validation | shortcut absent |
| `TRN-05` | PASS | A document cannot go from Draft to Released | shortcut absent |
| `TRN-06` | PASS | A document cannot be released without an explicit release decision | release requires PendingRelease and a recorded decision |
| `TRN-07` | PASS | A cancelled number can never return to Reserved or Issued | silent reuse is structurally impossible |
| `TRN-08` | PASS | A snag cannot be closed without verification | closure requires evidence and a verifier |
| `TRN-09` | PASS | Terminal states have no outgoing transitions | archive and cancellation are final |
| `TRN-10` | PASS | Transitions that void an approval declare what they invalidate | 1 voiding transitions declared on SiteVisits |
| `TRN-11` | PASS | Every approval route prohibits self-approval | 10 approval routes, all with SelfApprovalProhibited = TRUE |
| `TRN-12` | PASS | Every project resolves an approver at every required stage | 3 projects x 3 stages resolved, project-specific routes overriding the company default |
| `TRN-13` | PASS | A delegation inside its window, stage and project scope is valid | DEL-0001: valid |
| `TRN-14` | PASS | An expired delegation is rejected | DEL-0002: outside the delegation window |
| `TRN-15` | PASS | A revoked delegation is rejected | DEL-0003: delegation revoked |
| `TRN-16` | PASS | A delegation does not cover a stage it was not granted for | DEL-0001 used for Release: stage not covered |
| `TRN-17` | PASS | A project-scoped delegation does not cover another project | DEL-0001 used on PRJ-0002: project not covered |
| `TRN-18` | PASS | No delegation is open-ended | every delegation has an end date |
| `TRN-19` | PASS | AI is structurally barred from deciding a photograph | Any transition performed by AI or by an automation on AI output (ADR-0004, D-06) Any transition that modifies, replaces  |
| `TRN-20` | PASS | Every seeded record sits in a state the matrix can produce | 6 visits in valid states |

### Content hashing and approval binding  ·  `logic`  ·  14/14 passed

An approval is valid only for the exact content it approved, and 'material' has one published definition (C-06).

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `HASH-01` | PASS | A hash is a 64-character SHA-256 hex digest | ba097cc630f0edb43f8ea063ac164a44709994776caff1582a6cf41ecdc84a74 |
| `HASH-02` | PASS | The same content always hashes to the same value | recomputed, identical |
| `HASH-03` | PASS | A material change produces a different hash, voiding the approval | description edited -> hash changed |
| `HASH-04` | PASS | An immaterial change does not void an approval | UpdatedAt and UpdatedBy changed -> hash unchanged |
| `HASH-05` | PASS | Advisory AI output arriving later never voids a human approval | AI observation, confidence and status changed -> photo hash unchanged (C-06) |
| `HASH-06` | PASS | Withdrawing a photograph from the report is material | ApprovedForReport TRUE -> FALSE changed the hash |
| `HASH-07` | PASS | Re-ordering the approved photographs changes the visit hash | report sequence altered -> parent hash changed |
| `HASH-08` | PASS | Approving an additional photograph changes the visit hash | a newly approved child photograph is folded into the parent hash |
| `HASH-09` | PASS | NULL and empty string hash identically, so they never differ by accident | '' and None produce the same canonical value |
| `HASH-10` | PASS | Leading and trailing whitespace does not change a hash | text is trimmed before hashing |
| `HASH-11` | PASS | The same quantity written at different scales hashes identically | 1200 and 1200.000 normalise to the declared scale |
| `HASH-12` | PASS | A quantity that differs at the declared scale changes the hash | 1200.000 vs 1200.001 |
| `HASH-13` | PASS | The canonical field set is published and versioned | version 1.0.0, 10 published rules |
| `HASH-14` | PASS | Every hashable entity declares exactly which fields are material | hashable tables: SiteVisits, VisitActivities, Photos |

### Document numbering  ·  `simulation`  ·  13/13 passed

One service, many configurable series, with a reserved to issued or cancelled lifecycle and no silent reuse (D-10, ADR-0005 rev 1).

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `NUM-01` | PASS | 200 concurrent reservations produce 200 distinct numbers | issued 200, distinct 200, errors 0 |
| `NUM-02` | PASS | Numbers follow the configured pattern for their series | first number: AH-TR-2026-001 |
| `NUM-03` | PASS | A different document type uses a different series and restarts at its own start number | quotation series first number: AH-QT-2026-001 |
| `NUM-04` | PASS | A project-scoped series is partitioned from the company-wide series | project series first number: AH-IRRG-003-TR-2026-001 |
| `NUM-05` | PASS | A second legal entity gets its own independent sequence and its own prefix | second entity first number: AHX-TR-2026-001 (company-wide AH series is unaffected) |
| `NUM-06` | PASS | A reserved number can be issued | AH-CC-2026-001 -> Issued |
| `NUM-07` | PASS | A cancelled number records a reason, so the gap is explainable | AH-CC-2026-002 cancelled: generation failed during template merge |
| `NUM-08` | PASS | Cancelling without a reason is rejected | rejected: a cancellation reason is mandatory: a gap must be explainable |
| `NUM-09` | PASS | Reusing a cancelled sequence value is rejected by the register | rejected: UNIQUE constraint failed: register.series_id, register.year_key, register.scope_key, register.sequence_value |
| `NUM-10` | PASS | An issued number cannot be issued again | rejected: cannot issue a number in state Issued |
| `NUM-11` | PASS | An issued number cannot be cancelled | rejected: cannot cancel a number in state Issued |
| `NUM-12` | PASS | Migration continues the existing manual register instead of restarting it | last manual number 147, next issued AH-TR-2026-148 |
| `NUM-13` | PASS | A new year starts its own sequence where the series resets per year | 2027 first number: AH-TR-2027-001 |

### Deterministic calculation  ·  `logic`  ·  22/22 passed

Every figure is produced by formula from stored inputs, with one rounding policy and a reproducible trace. No figure originates from a language model.

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `CALC-01` | PASS | An unconfirmed tax rule yields UNDETERMINED and blocks, never zero | status=BLOCKED_TAX_UNCONFIRMED tax=None net=None |
| `CALC-02` | PASS | Line amount and subtotal are exact | 1200 x 3.500 = 4200.00 |
| `CALC-03` | PASS | Retention is computed from the configured contract percentage | 5% of 4200.00 = 210.00 |
| `CALC-04` | PASS | Multiple lines sum correctly | subtotal = 6000.00 |
| `CALC-05` | PASS | Tax applies to the taxable base and is rounded once | 5% of 6000.00 = 300.00 |
| `CALC-06` | PASS | Net payable is base + tax - retention - advance recovery | 6000.00 + 300.00 - 300.00 - 0.00 = 6000.00 |
| `CALC-07` | PASS | The applied tax rule and its version are preserved in the result and trace | rule=TAX-SYNTHETIC-TEST version=3 |
| `CALC-08` | PASS | Half-way values round half-up, deterministically | 0.125 -> 0.13 |
| `CALC-09` | PASS | Zero quantity is accepted and yields zero | subtotal = 0.00 |
| `CALC-10` | PASS | Negative quantity is rejected | rejected: line 1: negative quantity is rejected |
| `CALC-11` | PASS | Negative rate is rejected | rejected: line 1: negative rate is rejected |
| `CALC-12` | PASS | A currency mismatch is rejected and never converted | rejected: currency mismatch: contract is QAR, request is USD. No conversion is performed anywhere in this system (C-09). |
| `CALC-13` | PASS | The planted client/project currency mismatch is detectable before billing | client USD vs project QAR — must be resolved before any invoice request is created |
| `CALC-14` | PASS | Certifying beyond contract plus variation is rejected | rejected: cumulative quantity 13000.000 exceeds contract plus approved variation 12000.000 for item 1.01; an authorised override is required |
| `CALC-15` | PASS | Certifying exactly to the contract quantity is permitted | cumulative 12000.000 of permitted 12000.000 |
| `CALC-16` | PASS | An over-contract quantity passes only with a recorded authorised override | override recorded with approver and reason |
| `CALC-17` | PASS | An override without an approver and reason is rejected | rejected: an override must record an approver and a reason |
| `CALC-18` | PASS | An approved variation extends the permitted quantity | 500 contract + 50 variation = 550.000 |
| `CALC-19` | PASS | Advance recovery never exceeds the outstanding advance | 20% of 2650.00 would be 530.00; capped at outstanding 100.00 -> 100.00 |
| `CALC-20` | PASS | A discount larger than the subtotal is rejected | rejected: discount exceeds the subtotal |
| `CALC-21` | PASS | The same inputs always produce the same figures and the same trace | 9 trace steps, byte-identical on repeat |
| `CALC-22` | PASS | Money is decimal end to end, never floating point | all monetary values are decimal strings |

### Bilingual and right-to-left readiness  ·  `structural`  ·  13/13 passed

English and Arabic are supported from Phase 1, with no redesign required to add Arabic documents later (D-11).

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `LNG-01` | PASS | Every English text column has an Arabic counterpart | 35 bilingual pairs, none unpaired |
| `LNG-02` | PASS | Both languages are configured with an explicit text direction | en=LTR, ar=RTL |
| `LNG-03` | PASS | Users carry an individual language preference, and both are in use | preferences present in the fixture: ['ar', 'en'] |
| `LNG-04` | PASS | Templates are keyed by language and carry the correct text direction | 1 Arabic template(s); direction mismatches: none |
| `LNG-05` | PASS | A project can be configured to produce Arabic documents by configuration alone | projects defaulting to Arabic: ['PRJ-0002'] |
| `LNG-06` | PASS | A client registered only in Arabic is accepted without an invented English name | LegalNameEN is empty; LegalNameAR = شركة اصطناعية للمدارس ذ.م.م |
| `LNG-07` | PASS | Arabic text passes through canonical serialisation unchanged | Arabic description preserved verbatim in the canonical string |
| `LNG-08` | PASS | Arabic text is NFC-normalised without alteration | text is already NFC and is unchanged by normalisation |
| `LNG-09` | PASS | Arabic-Indic digits in names are preserved as written | غرفة ١٢ مبنى أ retains Arabic-Indic digits |
| `LNG-10` | PASS | Every controlled vocabulary carries an Arabic label for every value | 26 vocabularies, every value labelled in both languages |
| `LNG-11` | PASS | Seeded reference data is populated in Arabic, not merely capable of it | roles, units, disciplines, activities, document types and classifications all carry Arabic |
| `LNG-12` | PASS | Supervisors can record descriptions and captions in Arabic | 6 visits and 9 photo captions carry Arabic |
| `LNG-13` | PASS | Arabic is never written into an English column to satisfy a requirement | English columns contain no Arabic text |

### Governance and safety rules  ·  `structural`  ·  18/18 passed

The operating rules the owner approved, expressed as assertions so that weakening one of them fails a check rather than passing unnoticed.

| Check | Result | Description | Evidence produced |
|---|---|---|---|
| `GOV-01` | PASS | No credential, key, token or live webhook URL exists anywhere in the repository | every file scanned, nothing matching a secret pattern |
| `GOV-02` | PASS | Every email address is synthetic, or the company's own published address | only @synthetic.example, @pending.example and the published company address appear |
| `GOV-03` | PASS | Legal identity is an explicit pending placeholder, never a guess (D-02) | LegalNameEN = LEGAL_ENTITY_NAME_PENDING_VERIFICATION |
| `GOV-04` | PASS | No tax classification is named before written confirmation (D-08) | classification words found: none; treatment = PENDING_ACCOUNTANT_CONFIRMATION |
| `GOV-05` | PASS | The seeded tax rule is explicitly unconfirmed, so invoicing stays blocked | ConfirmedByAccountant = FALSE |
| `GOV-06` | PASS | No role may delete any row: history is evidence | 460 grants, every delete denied |
| `GOV-07` | PASS | The audit log is append-only for every role, administrators and break-glass included | roles able to alter the audit log: none |
| `GOV-08` | PASS | An administrator cannot create or alter an approval | neither administrator role nor break-glass can create or alter an approval |
| `GOV-09` | PASS | No advisory AI field is part of any content hash (D-06, C-06) | 5 AI fields, 0 in a hash |
| `GOV-10` | PASS | No decision or completion field is sourced from AI | AI-sourced decision fields: none |
| `GOV-11` | PASS | No monetary or measured-quantity field is sourced from AI (invariant I-4) | AI-sourced monetary or quantity fields: none (AIConfidence is advisory metadata, not a measurement) |
| `GOV-12` | PASS | The approved write-once evidence contract is fully represented (D-13) | missing: none |
| `GOV-13` | PASS | No file is described as the original device image before device testing | photographs claiming verification: none |
| `GOV-14` | PASS | Residency assignments exist and are marked unverified until a contract is read | 3 of 3 assignments await contract review |
| `GOV-15` | PASS | A project restricted by a residency rule has AI analysis disabled | restricted: ['PRJ-0003']; disabled: ['PRJ-0003'] |
| `GOV-16` | PASS | Financial tables are declared as such so access rules can act on it | financial tables: TaxRules, Contracts, WorkOrders, BOQItems, InvoiceRequests, InvoiceLines |
| `GOV-17` | PASS | Every table carries creation and update attribution | missing: none |
| `GOV-18` | PASS | The seed directory states plainly that its data is synthetic | stated in seed/README.md |

---

## 6. Reproducing this run

```
git checkout cf9ffed19efe437a305b6d1d68593439e4bb1901
python3 tools/run_validation.py
```

No installation, no dependency, no network access and no credential is required. The run regenerates every artifact and rewrites this document; the only file it modifies is this one, which a reviewer can confirm with `git status` immediately afterwards.
