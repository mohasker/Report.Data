# Role and Row-Level Security Matrix

**Document ID:** AH-SYS-P1-004 · **Revision:** 1 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-11 from `model/model.json` by `tools/gen_matrices.py`
**Executable statement:** `tools/security.py` · **Tested by:** `tools/test_segregation.py`
**Evidence:** `17-validation-evidence.md` (SEG-01 … SEG-12, GOV-06 … GOV-08)

## Principles

- Row-level access derives from ProjectAssignments only. Absence of an assignment grants nothing.
- An expired assignment (AssignedTo in the past) grants nothing.
- Field roles have NO access to any financial table: the data is absent from their data set, not merely hidden (SEC-04).
- Delete is 'none' for every role on every table. Rows are deactivated or cancelled, never destroyed, because history is evidence.
- The audit log is append-only for every role including SystemAdmin.
- An administrator can configure the system and diagnose failures without reading client evidence or documents: support does not require content access (spec 7.4).
- View, slice and column visibility are presentation, never enforcement. Every state-changing action is re-validated server-side against the authoritative record (P-04).

## Scopes

| Scope | Meaning |
|---|---|
| `all` | Every row in the table. |
| `assigned` | Only rows whose ProjectID appears in the user's active ProjectAssignments. |
| `own` | Only rows the user created, within their assigned projects. |
| `none` | No access. The table is not present in this role's data set at all. |

## Matrix

Each cell is **read / create / update**. Delete is `none` for every role on every table, so
it is not shown: rows are deactivated or cancelled, never destroyed, because history is
evidence.

### Master tables

| Table | SystemAdmin | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor |
|---|---|---|---|---|---|---|---|---|
| `LegalEntities` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Users` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | OWN/-/- \* | ALL/-/- |
| `ActivityTypes` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- \* | ALL/-/- |
| `DataClassifications` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `ResidencyRequirements` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `TaxRules` | ALL/-/- \* | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- |
| `NumberingSeries` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `DocumentTemplates` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Clients` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ASG/-/- \* | — | ALL/-/- |
| `Contacts` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | — | ALL/-/- |
| `Projects` | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- |
| `ProjectAssignments` | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- |
| `Locations` | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- |
| `ProjectActivityRules` | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- |
| `ApprovalMatrix` | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- |
| `ApprovalDelegations` | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- |
| `ResidencyAssignments` | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- |
| `Materials` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Equipment` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Employees` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | — | ALL/-/- |

### Vocabulary tables

| Table | SystemAdmin | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor |
|---|---|---|---|---|---|---|---|---|
| `Languages` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Roles` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Units` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Disciplines` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `DocumentTypes` | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |

### Operational tables

| Table | SystemAdmin | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor |
|---|---|---|---|---|---|---|---|---|
| `SiteVisits` | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- |
| `VisitActivities` | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- |
| `Photos` | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN \* | OWN/ASG/OWN | ALL/-/- |
| `Snags` | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- |
| `MaterialUsage` | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- |
| `VisitEquipment` | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- |
| `VisitManpower` | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- |

### Document tables

| Table | SystemAdmin | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor |
|---|---|---|---|---|---|---|---|---|
| `DocumentJobs` | — | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/ASG/- | — | — | ALL/-/- |
| `Documents` | — | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/ASG/- | — | — | ALL/-/- |
| `NumberRegister` | ALL/-/- \* | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/ASG/- | — | — | ALL/-/- |

### Control tables

| Table | SystemAdmin | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor |
|---|---|---|---|---|---|---|---|---|
| `Approvals` | ALL/-/- \* | ALL/ALL/ALL | ASG/ALL/ALL | ALL/ALL/ALL | ASG/ALL/ALL \* | — | — | ALL/-/- |
| `EntityVersions` | ALL/-/- | ALL/ALL/ALL | ASG/ALL/ALL | ALL/ALL/ALL | ASG/ALL/- | — | — | ALL/-/- |
| `AuditLog` | ALL/-/- \* | ALL/-/- \* | — \* | ALL/-/- \* | — \* | — | — | ALL/-/- |
| `IntegrationJobs` | ALL/-/- | ALL/ALL/ALL | ASG/ALL/ALL | ALL/ALL/ALL | ASG/-/- \* | — | — | ALL/-/- |

### Financial tables

| Table | SystemAdmin | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor |
|---|---|---|---|---|---|---|---|---|
| `Contracts` | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- |
| `WorkOrders` | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- |
| `BOQItems` | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- |
| `InvoiceRequests` | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- |
| `InvoiceLines` | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- |

Key: `ALL` every row · `ASG` rows in the user's assigned projects · `OWN` rows the user
created within those projects · `-` denied · `—` no access to the table at all.
`\*` marks a deliberate exception, explained in the next section.

## Deliberate exceptions

Each of these narrows or widens the group default for a stated reason. An exception without a
reason is a bug.

| Role and table | Reason |
|---|---|
| `SystemAdmin.NumberRegister` | Administrators must be able to explain a gap in the numbering register without being able to read document content. |
| `SystemAdmin.Approvals` | An administrator must never be able to manufacture an approval. |
| `SystemAdmin.AuditLog` | Append-only for every role. No one may edit or delete the audit trail, including an administrator. |
| `SystemAdmin.TaxRules` | Administrators may see tax configuration to support it, but may not change a financial rule: separation of duties (D-08). |
| `GeneralManager.AuditLog` | Append-only for every role. |
| `TechnicalReviewer.AuditLog` | Not needed for the review task; least privilege. |
| `FinanceReviewer.AuditLog` | Append-only for every role. |
| `ProjectManager.Approvals` | Project managers act as first-line reviewers where the approval matrix assigns them. |
| `ProjectManager.AuditLog` | Append-only for every role, and a project manager has no need to read it. |
| `ProjectManager.IntegrationJobs` | Visibility of failures affecting their own projects, without write access. |
| `SiteSupervisor.Clients` | Client display name only, for the projects they are assigned to. |
| `SiteSupervisor.Photos` | Supervisors see all evidence for their projects so they can avoid duplicate captures, but may edit only their own. |
| `FieldUser.ActivityTypes` | The activity catalogue is not sensitive and is needed to fill the form. |
| `FieldUser.Users` | A field user may see their own profile only. |

## What this matrix does not do

It does not enforce anything by itself. It is the specification that the Phase 2 security
filters and the Phase 3 server-side re-validation must both implement, and that
`tools/security.py` implements now so the rule can be tested before anything is built.
Column visibility and view design are presentation, never enforcement (P-04).
