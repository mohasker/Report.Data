# Phase 1 Validation Evidence

**Document ID:** AH-SYS-P1-017 · **Revision:** 1 · **Status:** generated from an executed run
**Executed:** 2026-09-11 00:59 UTC · **Model version:** 1.0.0 · **Python:** 3.11.15

> Produced by `python3 tools/run_validation.py`. Every result below comes from code that
> actually ran; nothing here is asserted by hand. Re-run the command to reproduce it.

## What this run does and does not prove

**It proves** that the Phase 1 data foundation is internally consistent: the model, the
generated schemas and the data dictionary agree; the synthetic data conforms; the rules for
segregation, evidence, transitions, delegation, hashing, numbering, calculation and
bilingual handling behave as specified when executed against that data.

**It does not prove** that any built system works. No AppSheet app, Google Drive folder,
Make scenario, Claude call or QuickBooks connection exists or was contacted. Those are
Phase 2 and later, and will carry their own recorded evidence (D-14).

## Summary — 141 of 141 checks passed

| Suite | Checks | Passed | Failed |
|---|---|---|---|
| Seed conformance | 3 | 3 | 0 |
| Configurability and unbounded width | 12 | 12 | 0 |
| Project segregation | 12 | 12 | 0 |
| Evidence rules | 14 | 14 | 0 |
| Status transitions, approvals and delegation | 20 | 20 | 0 |
| Content hashing and approval binding | 14 | 14 | 0 |
| Document numbering | 13 | 13 | 0 |
| Deterministic calculation | 22 | 22 | 0 |
| Bilingual and right-to-left readiness | 13 | 13 | 0 |
| Governance and safety rules | 18 | 18 | 0 |
| **Total** | **141** | **141** | **0** |

> Every check passed. Each is listed below with the evidence it produced, so a reviewer
> can see what was actually measured rather than taking a summary on trust.

## Artifact regeneration

| Step | Result | Output |
|---|---|---|
| `build_model.py` | ok | wrote /home/user/Report.Data/model/model.json;   tables      : 44;   columns     : 786;   enums       : 24;   transitions : 68 allowed, 29 explicitly forbidden;   security    : 8 roles x 44 tables = 352 grants, 14 exceptions |
| `gen_schemas.py` | ok | wrote 44 table schemas to schemas/tables/ |
| `gen_data_dictionary.py` | ok | wrote /home/user/Report.Data/docs/01-data-foundation/01-data-dictionary.md (1710 lines) |

## Seed conformance

Every seed file conforms to the canonical model: columns, types, formats, vocabularies, keys, uniqueness, referential integrity and project consistency.

| Check | Result | Description | Evidence |
|---|---|---|---|
| `SEED-01` | PASS | Every seed file validates against the model with no error | 29 files, 196 rows, 0 errors |
| `SEED-02` | PASS | Every foreign key resolves within the seeded data | 0 unresolvable-by-design references (tables not built until a later phase) |
| `SEED-03` | PASS | At least three materially different projects are present | 3 projects with 3 clients, 3 reporting frequencies, 3 billing methods, 2 document languages |

## Configurability and unbounded width

Adding a project must require only controlled master-data configuration: no modified logic, no cloned application, no duplicated scenario, no rewritten prompt, no changed formula or code (D-01).

| Check | Result | Description | Evidence |
|---|---|---|---|
| `CFG-01` | PASS | No project, client, contract or user identifier appears in any logic file | 10 logic files scanned, no hard-coded identifier |
| `CFG-02` | PASS | The canonical model names no project, client or contract | identifiers found in model.json: none |
| `CFG-03` | PASS | No generated schema names a project, client or contract | 44 schemas scanned, none names a project |
| `CFG-04` | PASS | Row-level security is expressed in roles and assignments, never in projects | 8 roles x 44 tables, no project named |
| `CFG-05` | PASS | Every project-varying behaviour is a configuration column on Projects | missing: none |
| `CFG-06` | PASS | Behaviour that varies per project has a configuration table of its own | present: ['ApprovalMatrix', 'DocumentTemplates', 'Locations', 'NumberingSeries', 'ProjectActivityRules', 'ProjectAssignments', 'ResidencyAssignments'] |
| `CFG-07` | PASS | A fourth project added as data only is immediately usable, with no code change | USR-0005 now sees 2 projects including PRJ-0004 |
| `CFG-08` | PASS | The new project is invisible to users who are not assigned to it | USR-0006 has no assignment to PRJ-0004 and cannot see it |
| `CFG-09` | PASS | The new project can belong to a different legal entity by configuration | PRJ-0004 issues documents under LE-0002 with its own numbering series |
| `CFG-10` | PASS | The evidence engine serves a brand-new project from the global catalogue | no configuration rows required before a new project can capture evidence |
| `CFG-11` | PASS | Nothing in the model encodes a project count or limit | no project-count assumption anywhere in the canonical model |
| `CFG-12` | PASS | Multi-entity operation is structural, not incidental | 2 legal entities across the fixture |

## Project segregation

No data, image, recipient, template, document number or financial record may cross a project boundary (D-15 item 16).

| Check | Result | Description | Evidence |
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
| `SEG-10` | PASS | No foreign key references a row belonging to a different project | 196 rows checked, no cross-project reference |
| `SEG-11` | PASS | A location code reused across projects stays distinct because the ID is the key | codes shared across projects: ['BLK-A', 'SITE']; all LocationIDs unique: True |
| `SEG-12` | PASS | A residency restriction disables AI for its own project only | AI disabled: ['PRJ-0003']; AI enabled: ['PRJ-0001', 'PRJ-0002'] |

## Evidence rules

Evidence requirements are configuration, resolved per project, and a blocked submission always says exactly what to fix (C-07).

| Check | Result | Description | Evidence |
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

## Status transitions, approvals and delegation

Work advances only through declared transitions, and an approval is only ever made by an authorised person acting within scope (D-09).

| Check | Result | Description | Evidence |
|---|---|---|---|
| `TRN-01` | PASS | Every entity with a lifecycle has a declared transition matrix | declared: ['Approvals', 'DocumentJobs', 'Documents', 'NumberRegister', 'Photos', 'Projects', 'SiteVisits', 'Snags', 'VisitActivities'] |
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

## Content hashing and approval binding

An approval is valid only for the exact content it approved, and 'material' has one published definition (C-06).

| Check | Result | Description | Evidence |
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

## Document numbering

One service, many configurable series, with a reserved to issued or cancelled lifecycle and no silent reuse (D-10, ADR-0005 rev 1).

| Check | Result | Description | Evidence |
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

## Deterministic calculation

Every figure is produced by formula from stored inputs, with one rounding policy and a reproducible trace. No figure originates from a language model.

| Check | Result | Description | Evidence |
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

## Bilingual and right-to-left readiness

English and Arabic are supported from Phase 1, with no redesign required to add Arabic documents later (D-11).

| Check | Result | Description | Evidence |
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
| `LNG-10` | PASS | Every controlled vocabulary carries an Arabic label for every value | 24 vocabularies, every value labelled in both languages |
| `LNG-11` | PASS | Seeded reference data is populated in Arabic, not merely capable of it | roles, units, disciplines, activities, document types and classifications all carry Arabic |
| `LNG-12` | PASS | Supervisors can record descriptions and captions in Arabic | 6 visits and 9 photo captions carry Arabic |
| `LNG-13` | PASS | Arabic is never written into an English column to satisfy a requirement | English columns contain no Arabic text |

## Governance and safety rules

The operating rules the owner approved, expressed as assertions so that weakening one of them fails a check rather than passing unnoticed.

| Check | Result | Description | Evidence |
|---|---|---|---|
| `GOV-01` | PASS | No credential, key, token or live webhook URL exists anywhere in the repository | every file scanned, nothing matching a secret pattern |
| `GOV-02` | PASS | Every email address is synthetic, or the company's own published address | only @synthetic.example, @pending.example and the published company address appear |
| `GOV-03` | PASS | Legal identity is an explicit pending placeholder, never a guess (D-02) | LegalNameEN = LEGAL_ENTITY_NAME_PENDING_VERIFICATION |
| `GOV-04` | PASS | No tax classification is named before written confirmation (D-08) | classification words found: none; treatment = PENDING_ACCOUNTANT_CONFIRMATION |
| `GOV-05` | PASS | The seeded tax rule is explicitly unconfirmed, so invoicing stays blocked | ConfirmedByAccountant = FALSE |
| `GOV-06` | PASS | No role may delete any row: history is evidence | 352 grants, every delete denied |
| `GOV-07` | PASS | The audit log is append-only for every role including SystemAdmin | roles able to alter the audit log: none |
| `GOV-08` | PASS | An administrator cannot create or alter an approval | SystemAdmin holds read-only access to Approvals |
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

## Reproducing this run

```
python3 tools/run_validation.py
```

No installation, no dependency, no network access and no credential is required.
