# Migration and Versioning Strategy

**Document ID:** AH-SYS-P1-007 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Relates to:** ADR-0002, R-01, A-17

---

## 1. Schema versioning

The model carries `model_version` (semantic). Everything downstream is generated from it, so a
version bump regenerates the schemas and the data dictionary together and they cannot disagree.

| Change | Version | Process |
|---|---|---|
| New optional column | patch | Add to the model, regenerate, deploy. Existing rows are valid. |
| New required column **with a default** | minor | Add with default, regenerate, backfill, then enforce. |
| New table | minor | Add, regenerate, seed any vocabulary. |
| New vocabulary value | minor | Add to the enum. Existing rows unaffected. |
| Removing a vocabulary value | **major** | Never delete: mark inactive. Historic rows must remain interpretable. |
| Rename or type change | **major** | Add new, backfill, dual-read, then retire. Never rename in place. |
| Change to a `content_hash_fields` list | **major** | Changes every hash. Requires its own decision record and a `CanonicalFieldSetVersion` increment. |
| Change to the security matrix | **major** | Requires the segregation checks to be re-run and recorded before deployment. |

### Additive-first rule

A change that only adds is safe to deploy while records are in flight. A change that removes or
renames is not, because a record captured offline yesterday may sync tomorrow under the old shape.
Every destructive change therefore goes through add → backfill → dual-read → retire, and the retire
step happens only once no in-flight record can carry the old shape.

## 2. Data migration into the system

| Source | Destination | Controls |
|---|---|---|
| Existing project/client/location registers (spreadsheets, proposals, contracts) | Master data | Validated against the schemas before load; every row attributed to the file and person it came from; loaded in a draft state and activated only after review |
| Existing manual document numbering | `NumberingSeries.LastManualNumber` | See `06-naming-and-numbering.md` §1.3. **Production numbering is blocked until the register is reviewed** |
| Existing contracts and BOQs | Phase 6 tables | Not loaded before Phase 6; quantities are financial and require finance review |
| Historic photographs | Not migrated | Retro-fitting evidence into a controlled pipeline creates records that look reviewed but never were. Historic material stays where it is, referenced if needed |

**No real data is loaded in Phase 1** (D-12, D-14). Everything in the repository is synthetic.

## 3. Leaving Google Sheets — the measurable threshold

ADR-0002 accepted Google Sheets for the MVP on condition that a migration trigger be defined as a
number rather than a feeling. It is:

**Migrate when any one of nine measured conditions holds for two consecutive weekly
measurements.** The full set, the formula that converts measured growth into an estimated date, and
the reason a fixed date was withdrawn are in
[`../02a-plan/18-migration-threshold-strategy.md`](../02a-plan/18-migration-threshold-strategy.md).
The capacity subset is:

| Signal | Threshold | Why this number |
|---|---|---|
| `Photos` row count | **> 40,000** | Well inside the platform's hard limits, but the point where sync duration starts to be felt on a mid-range phone |
| Any single table row count | **> 100,000** | |
| Median app sync duration on a field device | **> 15 seconds** | Above this, supervisors start avoiding the app, which starves the whole pipeline (R-06) |
| Concurrent-edit conflicts in the error queue | **> 3 per week** | Spreadsheets have no row locking; recurring conflicts mean the store is the wrong shape |
| Workbook cell count | **> 60% of the platform limit** | Leaves room to migrate calmly rather than urgently |

Measurement begins in Phase 2 — before the threshold can be reached, not after.

**Assumption A-17** (tens of photographs per project per month) is a planning estimate, not a
measurement. With a platform sized for dozens-to-hundreds of projects (D-01), it may well be wrong.
The threshold exists so that being wrong is a scheduled migration rather than an outage.

### What migration would involve

Because every access goes through the table contract in `model/model.json`, and no logic depends on
cell positions, sheet order or in-cell formulas:

1. Create the target store from the generated schemas.
2. Export and load, verifying row counts and checksums.
3. Re-point the capture layer's data source and the orchestration connections.
4. Re-run the full validation suite against the new store.
5. Keep the spreadsheet read-only for one reporting period as a fallback.

The candidate targets are the platform's own database (stronger typing and concurrency, same
ecosystem) or a managed SQL database (strongest guarantees, highest operational burden). The choice
is made from the measurements at the time, not now.

## 4. Rollback

| Scope | Rollback |
|---|---|
| Model or generated artifact | Revert the commit and regenerate. Everything is reproducible from `model/model.json`. |
| Seed or vocabulary change | Mark the new value inactive; historic rows keep their meaning. |
| Application configuration | Master data is versioned with effective dates; the previous configuration is re-activated rather than re-typed. |
| Document template | Templates are versioned with `EffectiveFrom`/`EffectiveTo`; the prior version is re-activated and documents record which version produced them. |
| A released document | Never rolled back. A superseding revision is issued, and the superseded one is retained and marked. |
| An approval | Never edited. It is voided with a reason, and a fresh approval of the new content is required. |

## 5. What is never migrated or edited

- The original received evidence file. It is write-once (D-13).
- An `AuditLog` row. Append-only for every role (GOV-07).
- An issued document number. It stays issued; a cancelled one stays cancelled (NUM-10, NUM-11).
- A recipient snapshot on a released document. It records who was authorised *at release*, and later contact edits must not rewrite history.
