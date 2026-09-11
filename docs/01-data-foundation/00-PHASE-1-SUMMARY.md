# Phase 1 — Data Foundation: Summary and Gate Request

**Document ID:** AH-SYS-P1-000 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Validated Locally · **Submitted for Owner Review** · **Authorisation:** D-14
**Evidence:** [`17-validation-evidence.md`](17-validation-evidence.md) — **172 checks executed, 172 passed**
**Owner-facing summary:** [`../OWNER-REVIEW-PACK.md`](../OWNER-REVIEW-PACK.md)

---

## 1. What was actually done

Recorded honestly, per operating rule 1.

| | |
|---|---|
| **Built** | A canonical model of 46 tables and 829 columns, with every schema and the data dictionary generated from it; reference implementations of row-level security, evidence rules, content hashing, document numbering and deterministic calculation; synthetic data for three materially different projects; ten executable check suites; nineteen specifications; and the owner review pack |
| **Executed** | `python3 tools/run_validation.py` — 172 checks across 11 suites, all passing. Full reproduction record, including what the checks are **not** evidence of, in `17-validation-evidence.md` |
| **Not done, deliberately** | No Google account connected · no capture application built or connected · no orchestration scenario created · no AI credential created or call made · no accounting system connected · no real photograph, client, project, employee or financial record loaded · no email sent · no invoice or accounting transaction created · no external document published or shared |

Every one of those exclusions is a line in D-14, and every one holds.

## 2. What the validation proves, and what it does not

**It proves** the data foundation is internally consistent and behaves as specified when executed:
the model, the generated schemas and the data dictionary agree; the synthetic data conforms to the
model; and the rules for segregation, evidence, transitions, delegation, hashing, numbering,
calculation, bilingual handling and governance do what the documents claim when run against that
data.

**It does not prove** that any built system works. Nothing has been built. Phase 2 and later carry
their own gates and their own recorded evidence.

| Suite | Checks | What it establishes |
|---|---|---|
| Seed conformance | 3 | 29 files, 196 rows, zero schema or referential errors |
| Configurability | 12 | No project, client or contract identifier appears in any logic file, in the model, in any schema or in the security matrix. A fourth project added **as data only** works immediately and stays segregated |
| Project segregation | 12 | No data, image, recipient, template, numbering series, financial record or foreign key crosses a project boundary |
| Evidence rules | 14 | Per-project rules resolve correctly, incomplete submissions are blocked with specific reasons, duplicates are flagged not deleted, missing GPS never blocks |
| Transitions, approvals, delegation | 20 | Every dangerous shortcut is refused; expired, revoked and out-of-scope delegations are rejected; self-approval is prohibited everywhere |
| Content hashing | 14 | Material changes void an approval, immaterial ones do not, and **a late AI observation never voids a human approval** |
| Document numbering | 13 | 200 concurrent reservations yield 200 distinct numbers; a cancelled number is never reused; migration continues the existing manual register |
| Deterministic calculation | 22 | An unconfirmed tax rule blocks and never yields zero; over-certification is rejected without an authorised override; a currency mismatch is rejected and never converted |
| Bilingual readiness | 13 | Every English column has an Arabic counterpart; Arabic survives hashing unchanged; nothing is transliterated |
| Role separation and recoverability | 31 | Neither administrator reads evidence, documents or money; auditor and break-glass access expire; break-glass restores administration without opening content; the system cannot rest on one administrator |
| Governance | 18 | No secret anywhere; no role can delete; the audit log is append-only for everyone including administrators and break-glass; no AI field reaches a hash or a monetary path |

## 3. How each of your fifteen decisions landed

| | Decision | Where it is now |
|---|---|---|
| D-01 | Not a three-project system | `Projects` carries every project-varying behaviour as a column; seven child tables carry the rest. Twelve configurability checks assert no identifier is in any logic file, and that a fourth project added as data alone works |
| D-02 | Legal entity is master data | `LegalEntities` with 29 fields, EN/AR names, versioning. Placeholder in place and asserted (GOV-03). Two entities in the fixture prove multi-entity numbering |
| D-03 | Google ownership | Folder and permission model designed; nothing provisioned |
| D-04 | No plan assumed | A sixteen-requirement feature-to-plan matrix with a verification method per row, and six named risks the platform may not support safely or economically |
| D-05 | Orchestration | Thirteen scenarios specified with an idempotency contract, failure taxonomy, retry policy and a non-developer runbook. Nothing created |
| D-06 | AI may pre-analyse submitted evidence | ADR-0004 rev 1. Advisory fields excluded from every hash, so a late observation cannot void an approval (HASH-05). Only human-approved evidence generates a report |
| D-07 | QuickBooks is in use | Mapping fields defined; a 24-question compatibility inspection written as a gate. Calculation layer independent of the accounting product |
| D-08 | No tax classification named | `TaxRules` with an explicitly unconfirmed placeholder. The engine returns `UNDETERMINED` and **blocks**; it does not produce zero. Rule and version preserved on every calculation |
| D-09 | Delegation from the start | `ApprovalMatrix` + `ApprovalDelegations`; both identities recorded on a delegated decision; five separate delegation-validity checks |
| D-10 | Numbering by entity, type, year, scope | One service, many series, reserved → issued → cancelled, concurrency-tested, with migration from the manual register |
| D-11 | Bilingual from Phase 1 | Every English column paired; all 24 vocabularies and all reference data populated in Arabic; a fixture client registered **only** in Arabic, which changed the model rather than the fixture |
| D-12 | Residency per project | Classification and residency models, per-project AI disablement, a data-flow map, subprocessor list and a twelve-question contract-review checklist |
| D-13 | Evidence originals | Nine columns implementing the write-once contract; `IsOriginalDeviceImageVerified` stays FALSE until device testing, and GOV-13 asserts no photograph claims otherwise |
| D-14 | Phase 1 limits | Every prohibition holds. GOV-01 and GOV-02 scan the whole repository for secrets and non-synthetic addresses |
| D-15 | Seventeen additions | All seventeen delivered; the coverage table is in `docs/00-discovery/08-phase-1-artifact-manifest.md` |

## 4. Three defects the checks found while the model was being written

Worth recording, because they are the argument for writing the checks at all:

1. **Two statuses were unreachable.** `Documents.Cancelled` and `Approvals.Delegated` existed in the vocabularies with no transition leading to them. Both now have declared transitions, including the delegation path that records the acting delegate and the accountable approver separately.
2. **A project manager could write the audit log.** A group-level grant gave them create access to every control table. They now have none, and the audit log is append-only for every role.
3. **Six controlled vocabularies carried no change attribution.** Languages, roles, units, disciplines, document types and classifications had no `CreatedBy`/`UpdatedBy`. For an ISO 9001 document-control regime, configuration changes need attribution as much as records do.

A fourth correction came from a fixture rather than a check: a client registered only in Arabic could
not be saved, because `LegalNameEN` was required. Forcing an English legal name would have invited an
invented transliteration. The model changed, not the fixture.

## 5. What is still unknown

Twenty-three external facts, each named, each attributed to whoever can supply it, each categorised
by the phase it blocks: [`16-external-facts-register.md`](16-external-facts-register.md).

**None blocks Phase 1, and none has been guessed at.** Two are worth your attention now because they
have long lead times and other people must produce them:

| | What | Who | Blocks |
|---|---|---|---|
| **EF-17** | Written confirmation of the tax treatment applied to these contracts | Accountant | Issue of any invoice (Phase 6) |
| **EF-16** | Contract review for residency, confidentiality and third-party-processing clauses | Owner, from the contracts | Production upload of real data for an affected project |

Neither is urgent this week. Both take longer than expected once started.

## 6. Phase 1 exit criteria

| # | Criterion | Status |
|---|---|---|
| 1 | Data dictionary reviewed field by field | **Awaiting your review** — `01-data-dictionary.md` |
| 2 | Status-transition matrix approved, including what each transition invalidates | **Awaiting your review** — `03-status-transition-matrix.md` |
| 3 | Security model reviewed grant by grant | **Awaiting your review** — `04-security-model.md`, 352 grants and 13 exceptions |
| 4 | `ContentHash` canonical field list agreed (closes C-06) | Defined, published, versioned, tested |
| 5 | Measurable migration threshold defined (R-01) | Defined as five numbered signals |
| 6 | Projects modelled end to end with no project-specific logic | Proven by twelve checks |
| 7 | Configuration register complete, no value in the repository | Complete; asserted by GOV-01 |
| 8 | Validation evidence recorded | 141 of 141 checks, recorded whether passing or failing |
| 9 | External-facts register complete and categorised | 23 facts, by blocking phase |

Criteria 1, 2 and 3 are yours; the rest are done.

## 7. What I recommend you actually read

Not all sixteen documents. In this order, about forty minutes:

1. **This summary** — you are here.
2. **[`17-validation-evidence.md`](17-validation-evidence.md)** — what was actually executed. Skim the evidence column; it says what was measured, not that it passed.
3. **[`04-security-model.md`](04-security-model.md)** §Deliberate exceptions — thirteen decisions about who sees what. The one most likely to provoke disagreement is that the system administrator cannot read evidence or documents at all.
4. **[`16-external-facts-register.md`](16-external-facts-register.md)** — what other people owe the project.
5. **[`11-deterministic-calculation-spec.md`](11-deterministic-calculation-spec.md)** §4 — how the tax decision behaves in practice.

The data dictionary is a reference document. Read the table you are curious about, not all 44.

## 8. Gate request

Phase 1 is complete within its authorisation. To open Phase 2, I need:

1. **Your review of criteria 1, 2 and 3** above — or an instruction to proceed and review in parallel.
2. **EF-01** — the owning Workspace account and the Shared Drive.
3. **EF-03** — the capture-platform plan, verified against the requirements matrix.
4. **EF-05 and EF-06** — real supervisors and devices for the field test, and a named system administrator.

Phase 2 builds the multi-project capture and review application and proves segregation on real
devices with real people. Its gate is the most important in the project: if supervisors find the app
slower than the habit it replaces, nothing downstream matters (R-06).
