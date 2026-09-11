# Lean Operational MVP — Scope, and What Is Deferred

**Document ID:** AH-SYS-P2A-011 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review
**Implements:** the owner's simplification instruction of 2026-09-11
**Tested by:** `tools/test_lean_mvp.py` — 13 checks (LEAN-01 … LEAN-13)

> The 46-table model remains the **long-term reference architecture**. What gets *built* is a lean
> subset of **17 tables**. Deferring a table never means losing its design: every deferred table
> keeps its full schema, so adding it later is additive rather than a migration — asserted by
> LEAN-07, which counts 620 designed columns sitting in reserve.

---

**One-page matrix** with purpose, primary user, field count, expected monthly rows, app visibility,
device sync, deferrability and dependencies: [`17-lean-table-scope-matrix.md`](17-lean-table-scope-matrix.md).

## 1. The lean build — 17 tables

| # | Table | Carries | The owner's capability |
|---|---|---|---|
| 1 | `Users` | People who sign in, with `RoleCode` as an enum | Projects and users |
| 2 | `Projects` | Every project-varying behaviour, plus client display name | Projects and users |
| 3 | `ProjectAssignments` | **The only source of row-level access** | Project assignments |
| 4 | `Locations` | Hierarchical, project-scoped | Locations |
| 5 | `ActivityTypes` | The catalogue of 34 activities and default evidence rules | Activities |
| 6 | `ProjectActivityRules` | Per-project overrides of those rules | Activities |
| 7 | `SiteVisits` | The unit of submission and review | Site visits |
| 8 | `VisitActivities` | What was done, quantity, confirmation | Activities |
| 9 | `Photos` | Write-once evidence, reviewer decision, advisory AI fields | Photographs |
| 10 | `Snags` | Raised from evidence, closed with evidence | Snags |
| 11 | `Approvals` | Every decision, bound to a content hash | Reviews and approvals |
| 12 | `DocumentJobs` | A request, with a frozen input snapshot | Document jobs |
| 13 | `Documents` | A produced revision, release-controlled | Generated reports |
| 14 | `NumberRegister` | Reserved / issued / cancelled, with reasons | Generated reports |
| 15 | `LegalEntities` | Company identity on every issued document | Generated reports |
| 16 | `AuditLog` | Append-only, before and after hashes | Audit |
| 17 | `IntegrationJobs` | One row per external call, with failure class | Integration errors |

Every capability on the owner's list is covered (LEAN-02), and every load-bearing control survives
the trim (LEAN-08): segregation, approval binding, audit, the numbering register, legal identity,
per-project evidence rules and failure visibility.

## 2. Lean replacements

Six lean tables would otherwise require a deferred one. Each gets a concrete replacement column —
without these the subset would not actually build, which is what LEAN-03 checks.

| Reference architecture | Lean replacement | What it carries, and what it does not |
|---|---|---|
| `Users.RoleID` → `Roles` | `Users.RoleCode` enum | The ten role codes. Capability flags move to documentation |
| `ProjectAssignments.RoleID` → `Roles` | `ProjectAssignments.RoleCode` enum | The role held **on this project** — what the security filter reads |
| `Projects.ClientID` → `Clients` | `ClientNameEN`, `ClientNameAR`, `ClientKind` | Enough for a report header and a dashboard. No billing address, tax number or accounting identifier — none needed before invoicing |
| `ActivityTypes.DisciplineID` → `Disciplines` | `DisciplineCode` enum | Groups the activity picker; referenced nowhere else |
| `Documents.TemplateID` → `DocumentTemplates` | `TemplateFileKey`, `LanguageCode` | Records which template file actually produced the document — the part that matters for reproducibility |
| `NumberRegister.SeriesID` → `NumberingSeries` | `SeriesKey` text | The register keeps reserved/issued/cancelled; only series *configuration* moves to the legal entity |

## 3. The 29 deferred tables

### Folded into a lean table — the job still gets done

| Deferred | Job now done by | What is lost | Bring it back when |
|---|---|---|---|
| `Roles` | `RoleCode` enums | Editable role capabilities | A role's powers need changing without a rebuild |
| `Units` | `UnitCode` enum | Per-unit decimal places as configuration | A unit needs project-specific rounding |
| `Clients` | Columns on `Projects` | One client with several projects is repeated | Phase 6, or a client holding several projects at once |
| `Contacts` | Nothing — release is manual | No authorised-recipient control in the app | Automated delivery, Phase 7 |
| `DocumentTemplates` | `TemplateFileKey` on `Projects` | Record-level template versioning | A template revision must be provable after issue |
| `NumberingSeries` | Format columns on `LegalEntities` | Per-client and per-project numbering runs | A client requires their own run, or a second entity issues |
| `ApprovalMatrix` | `ReviewerUserID` on `Projects` | Multi-step and per-type routing | A project needs a different approver |
| **`ApprovalDelegations`** | Nothing | **If the approver is away, approvals stop** | **Before go-live if a delegate exists; immediately if approvals ever stall** |
| `EntityVersions` | `EntityVersion` + `ContentHash` on records; `AuditLog` before/after hashes | Version history is reconstructed rather than read | A dispute needs the version chain as a first-class record |
| `TemporaryAccessGrants` | Nothing — auditor and break-glass roles not enabled | Time-bound audit access unavailable | An external audit is scheduled, or break-glass is needed |
| `SystemRecoveryPlan` | **Two administrator accounts + a written runbook** | The go-live blocker lives in the runbook, not in data | The estate is large enough to need recorded test evidence |
| `Languages`, `Disciplines`, `DocumentTypes`, `DataClassifications` | Enums | Vocabularies change by editing the app | A vocabulary changes more than about twice a year |

### Scheduled to a named phase

| Phase | Tables |
|---|---|
| 3 | `ResidencyRequirements`, `ResidencyAssignments` |
| 5 | `Materials`, `MaterialUsage`, `Equipment`, `VisitEquipment`, `Employees`, `VisitManpower` |
| 6 | `Contracts`, `WorkOrders`, `BOQItems`, `TaxRules`, `InvoiceRequests`, `InvoiceLines` |

## 4. The honest cost of the trim

Three things are genuinely weaker in the lean build. They are listed here rather than buried,
because each is a decision the owner is entitled to reverse.

1. **No delegation.** The general manager approves everything, and there is no way to delegate that while they are travelling. Approvals simply wait. This is the single largest operational risk in the lean design, and the fix is one table plus one named delegate.
2. **No auditor or break-glass role.** Time-bound audit access and emergency administrative access are not in the app. Recovery is handled by having **two administrator accounts in the Workspace** and a written runbook — which satisfies the go-live condition, but records nothing about who used what, and when.
3. **No residency enforcement in the app until Phase 3.** The contract-review checklist still gates production upload; it is enforced by procedure rather than by a row.

Each of these can be restored without a migration, because the schema already exists.

## 5. What the trim does **not** cost

| Concern | Still true in the lean build |
|---|---|
| Project segregation | `ProjectAssignments` is retained; every project-scoped table still carries `ProjectID` (LEAN-09) |
| Approval bound to content | `Approvals` retains `ContentHash` and `EntityVersion` (LEAN-10) |
| Audit trail | `AuditLog` retained, append-only, with before and after hashes |
| Numbering integrity | `NumberRegister` retained: a cancelled number is still never reused |
| Per-project evidence rules | `ProjectActivityRules` retained — this is what makes projects genuinely different |
| Multi-project width | Unchanged. Adding a project is still master-data configuration |
| Bilingual capability | Unchanged. The paired columns live on the tables that were kept |
| No AI in a decision or a number | Unchanged |

## 6. Growth path

```
Lean MVP (17)
  + ApprovalDelegations, ApprovalMatrix      when a delegate is named
  + Contacts, DocumentTemplates              when delivery is automated  (Phase 5b/7)
  + ResidencyRequirements/Assignments        when real client data is uploaded  (Phase 3)
  + Materials, Equipment, Manpower           when cost control is wanted  (Phase 5)
  + Contracts, BOQ, Tax, Invoices            when invoicing begins  (Phase 6)
  + Clients, Units, Roles, vocabularies      when configuration churn justifies a table
  = the 46-table reference architecture
```

Each step is additive. No step requires re-modelling what came before, which is the whole reason
the 46-table model was designed before the 17-table build.
