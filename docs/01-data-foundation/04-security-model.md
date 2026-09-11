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
- The audit log is append-only for every role, including both administrator roles and break-glass access.
- A technical administrator can configure the system, provision users and diagnose failures without reading client evidence, documents or financial records: support does not require content access.
- Business master-data administration is a separate role from technical administration, and neither of them opens evidence, documents or money.
- ReadOnlyAuditor and EmergencyAccess function ONLY while a valid, unexpired, authorised TemporaryAccessGrant exists. Without a grant they resolve to no access at all.
- Break-glass restores ADMINISTRATIVE capability. It never opens client evidence, documents or financial records, because an administrative emergency is not solved by reading a client's photographs.
- The system must never become unrecoverable because one administrator is unavailable: either two administrator-capable accounts exist, or a documented and tested recovery route does.
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

| Table | SystemAdministrator | BusinessAdministrator | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor | EmergencyAccess |
|---|---|---|---|---|---|---|---|---|---|---|
| `LegalEntities` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Users` | ALL/ALL/ALL | ALL/-/- \* | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | OWN/-/- \* | ALL/-/- | ALL/ALL/ALL |
| `ActivityTypes` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `DataClassifications` | ALL/ALL/ALL | ALL/-/- | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/ALL/ALL |
| `ResidencyRequirements` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `TaxRules` | — \* | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- | — |
| `NumberingSeries` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `DocumentTemplates` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Clients` | — | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ASG/-/- \* | — | ALL/-/- | — |
| `Contacts` | — | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | — | ALL/-/- | — |
| `Projects` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- | ALL/-/- |
| `ProjectAssignments` | ALL/ALL/ALL \* | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- | ALL/ALL/ALL \* |
| `Locations` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- | ALL/-/- |
| `ProjectActivityRules` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- | ALL/-/- |
| `ApprovalMatrix` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- | ALL/-/- |
| `ApprovalDelegations` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- | ALL/-/- |
| `ResidencyAssignments` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/-/ASG | ASG/-/- | ASG/-/- | ALL/-/- | ALL/-/- |
| `Materials` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Equipment` | ALL/-/- | ALL/ALL/ALL | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- |
| `Employees` | ALL/ALL/ALL | ALL/-/- | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | — | ALL/-/- | ALL/ALL/ALL |

### Vocabulary tables

| Table | SystemAdministrator | BusinessAdministrator | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor | EmergencyAccess |
|---|---|---|---|---|---|---|---|---|---|---|
| `Languages` | ALL/ALL/ALL | ALL/-/- | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/ALL/ALL |
| `Roles` | ALL/ALL/ALL | ALL/-/- | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/ALL/ALL |
| `Units` | ALL/ALL/ALL | ALL/-/- | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/ALL/ALL |
| `Disciplines` | ALL/ALL/ALL | ALL/-/- | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/ALL/ALL |
| `DocumentTypes` | ALL/ALL/ALL | ALL/-/- | ALL/ALL/ALL | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/-/- | ALL/ALL/ALL |

### Operational tables

| Table | SystemAdministrator | BusinessAdministrator | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor | EmergencyAccess |
|---|---|---|---|---|---|---|---|---|---|---|
| `SiteVisits` | — | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- | — |
| `VisitActivities` | — | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- | — |
| `Photos` | — | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN \* | OWN/ASG/OWN | ALL/-/- | — |
| `Snags` | — | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- | — |
| `MaterialUsage` | — | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- | — |
| `VisitEquipment` | — | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- | — |
| `VisitManpower` | — | — | ALL/-/ALL | ASG/-/ASG | ASG/-/- | ASG/ASG/ASG | ASG/ASG/OWN | OWN/ASG/OWN | ALL/-/- | — |

### Document tables

| Table | SystemAdministrator | BusinessAdministrator | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor | EmergencyAccess |
|---|---|---|---|---|---|---|---|---|---|---|
| `DocumentJobs` | — | — | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/ASG/- | — | — | ALL/-/- | — |
| `Documents` | — | — | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/ASG/- | — | — | ALL/-/- | — |
| `NumberRegister` | — | — | ALL/ALL/ALL | ASG/-/- | ALL/-/- | ASG/ASG/- | — | — | ALL/-/- | — |

### Control tables

| Table | SystemAdministrator | BusinessAdministrator | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor | EmergencyAccess |
|---|---|---|---|---|---|---|---|---|---|---|
| `Approvals` | ALL/-/- \* | — | ALL/ALL/ALL | ASG/ALL/ALL | ALL/ALL/ALL | ASG/ALL/ALL \* | — | — | ALL/-/- | ALL/-/- \* |
| `EntityVersions` | ALL/-/- | — | ALL/ALL/ALL | ASG/ALL/ALL | ALL/ALL/ALL | ASG/ALL/- | — | — | ALL/-/- | ALL/-/- |
| `AuditLog` | ALL/-/- \* | — \* | ALL/-/- \* | — \* | ALL/-/- \* | — \* | — | — | ALL/-/- \* | ALL/-/- \* |
| `IntegrationJobs` | ALL/-/- \* | — | ALL/ALL/ALL | ASG/ALL/ALL | ALL/ALL/ALL | ASG/-/- \* | — | — | ALL/-/- | ALL/-/- |
| `TemporaryAccessGrants` | ALL/-/- | — | ALL/ALL/ALL | — | — | — | — | — | ALL/-/- | ALL/-/- |
| `SystemRecoveryPlan` | ALL/-/- | — | ALL/ALL/ALL | — | — | — | — | — | ALL/-/- | ALL/-/- |

### Financial tables

| Table | SystemAdministrator | BusinessAdministrator | GeneralManager | TechnicalReviewer | FinanceReviewer | ProjectManager | SiteSupervisor | FieldUser | ReadOnlyAuditor | EmergencyAccess |
|---|---|---|---|---|---|---|---|---|---|---|
| `Contracts` | — | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- | — |
| `WorkOrders` | — | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- | — |
| `BOQItems` | — | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- | — |
| `InvoiceRequests` | — | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- | — |
| `InvoiceLines` | — | — | ALL/ALL/ALL | — | ALL/ALL/ALL | — | — | — | ALL/-/- | — |

Key: `ALL` every row · `ASG` rows in the user's assigned projects · `OWN` rows the user
created within those projects · `-` denied · `—` no access to the table at all.
`\*` marks a deliberate exception, explained in the next section.

## Deliberate exceptions

Each of these narrows or widens the group default for a stated reason. An exception without a
reason is a bug.

| Role and table | Reason |
|---|---|
| `SystemAdministrator.ProjectAssignments` | User provisioning is a technical-administration task: placing a person into a project is access administration, not business content. |
| `SystemAdministrator.Approvals` | An administrator must never be able to manufacture an approval. |
| `SystemAdministrator.AuditLog` | Append-only for every role. No one may edit or delete the audit trail, including an administrator. |
| `SystemAdministrator.IntegrationJobs` | Integration monitoring and system health are the administrator's job. |
| `SystemAdministrator.TaxRules` | Separation of duties: a technical administrator has no reason to see or change a financial rule. |
| `BusinessAdministrator.Users` | Business administration reads the user register to assign people to projects; creating and disabling accounts stays with technical administration. |
| `BusinessAdministrator.AuditLog` | Least privilege: business master-data administration does not require the audit trail. |
| `GeneralManager.AuditLog` | Append-only for every role. |
| `TechnicalReviewer.AuditLog` | Not needed for the review task; least privilege. |
| `FinanceReviewer.AuditLog` | Append-only for every role. |
| `ProjectManager.Approvals` | Project managers act as first-line reviewers where the approval matrix assigns them. |
| `ProjectManager.AuditLog` | Append-only for every role, and a project manager has no need to read it. |
| `ProjectManager.IntegrationJobs` | Visibility of failures affecting their own projects, without write access. |
| `SiteSupervisor.Clients` | Client display name only, for the projects they are assigned to. |
| `SiteSupervisor.Photos` | Supervisors see all evidence for their projects so they can avoid duplicate captures, but may edit only their own. |
| `FieldUser.Users` | A field user may see their own profile only. |
| `ReadOnlyAuditor.AuditLog` | Read-only, and only while a valid time-bound grant exists. |
| `EmergencyAccess.ProjectAssignments` | Restoring administrative capability means being able to reinstate an administrator. |
| `EmergencyAccess.Approvals` | Break-glass can see that approvals exist and can never create one. |
| `EmergencyAccess.AuditLog` | Break-glass may read the audit trail to diagnose, and may never alter it. |

## What this matrix does not do

It does not enforce anything by itself. It is the specification that the Phase 2 security
filters and the Phase 3 server-side re-validation must both implement, and that
`tools/security.py` implements now so the rule can be tested before anything is built.
Column visibility and view design are presentation, never enforcement (P-04).
