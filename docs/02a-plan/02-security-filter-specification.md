# Security Filter Specification

**Document ID:** AH-SYS-P2A-002 · **Revision:** 1 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-11 from `model/model.json` by `tools/gen_appsheet_workbook.py`

> Security filters are the **enforcement** layer, not the presentation layer. Views, slices
> and column visibility control what is shown; a security filter controls what is delivered
> to the device at all. Every state-changing automation re-validates the same rule
> server-side, because a client-side check can never be trusted for security (P-04).

## The building blocks

```
ME()            = LOOKUP(USEREMAIL(), Users, Email, UserID)
MY_ROLE()       = LOOKUP(USEREMAIL(), Users, Email, RoleID)
MY_PROJECTS()   = SELECT(ProjectAssignments[ProjectID],
                     AND([UserID] = ME(),
                         [IsActive] = TRUE,
                         [AssignedFrom] <= TODAY(),
                         OR(ISBLANK([AssignedTo]), [AssignedTo] >= TODAY())))
MY_GRANT()      = SELECT(TemporaryAccessGrants[GrantID],
                     AND([UserID] = ME(), [IsActive] = TRUE,
                         ISBLANK([RevokedAt]),
                         [ValidFrom] <= NOW(), [ValidTo] >= NOW(),
                         NOT(ISBLANK([Reason])),
                         OR([GrantKind] <> "Emergency",
                            NOT(ISBLANK([NotificationSentAt])))))
```

`MY_PROJECTS()` is the whole access model in five lines: an assignment that is inactive, has
not started, or has ended contributes nothing.

## Filter per table

`ROLE_IN(...)` abbreviates `IN(LOOKUP(USEREMAIL(), Users, Email, RoleID), LIST(...))`.

| Table | Security filter | Rationale |
|---|---|---|
| `LegalEntities` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `Languages` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `Roles` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `Users` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("FieldUser"), [UserID] = ME()))` | grant-dependent roles read nothing without an active grant; own rows only |
| `Units` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `Disciplines` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `ActivityTypes` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `DocumentTypes` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `DataClassifications` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `ResidencyRequirements` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `Clients` | `OR(ROLE_IN("BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), ROLE_IN("SiteSupervisor"))` | grant-dependent roles read nothing without an active grant |
| `Contacts` | `OR(ROLE_IN("BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `Projects` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"))` | grant-dependent roles read nothing without an active grant |
| `ProjectAssignments` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `Locations` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `ProjectActivityRules` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `ApprovalMatrix` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `ApprovalDelegations` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"))` | grant-dependent roles read nothing without an active grant |
| `ResidencyAssignments` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `TemporaryAccessGrants` | `OR(ROLE_IN("SystemAdministrator", "GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `SystemRecoveryPlan` | `OR(ROLE_IN("SystemAdministrator", "GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `SiteVisits` | `OR(ROLE_IN("GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), IN([ProjectID], MY_PROJECTS())), AND(ROLE_IN("FieldUser"), [SupervisorUserID] = ME()))` | grant-dependent roles read nothing without an active grant; assignment-scoped; own rows only |
| `VisitActivities` | `OR(ROLE_IN("GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), IN([ProjectID], MY_PROJECTS())), AND(ROLE_IN("FieldUser"), [CreatedBy] = ME()))` | grant-dependent roles read nothing without an active grant; assignment-scoped; own rows only |
| `Photos` | `OR(ROLE_IN("GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), IN([ProjectID], MY_PROJECTS())), AND(ROLE_IN("FieldUser"), [CapturedBy] = ME()))` | grant-dependent roles read nothing without an active grant; assignment-scoped; own rows only |
| `Snags` | `OR(ROLE_IN("GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), IN([ProjectID], MY_PROJECTS())), AND(ROLE_IN("FieldUser"), [RaisedBy] = ME()))` | grant-dependent roles read nothing without an active grant; assignment-scoped; own rows only |
| `Approvals` | `OR(ROLE_IN("SystemAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `EntityVersions` | `OR(ROLE_IN("SystemAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `AuditLog` | `OR(ROLE_IN("SystemAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |

## Tables deliberately absent from the application

These are not filtered — they are **not present in the app's data set at all**, which is the
strongest form of the control: data that is not there cannot leak.

- `BOQItems` — Bill of quantities. Cumulative quantity is controlled, never merely recorded.
- `Contracts` — Commercial agreement governing a project. Hidden from field roles entirely.
- `DocumentJobs` — A request to produce a document from a frozen snapshot of approved records.
- `DocumentTemplates` — Approved templates, keyed by document type, language and optionally project or discipline (D-11, ADR-0007).
- `Documents` — A produced document revision. Approval binds to ContentHash (ADR-0006).
- `Employees` — Crew register for resource reporting. Payroll data is deliberately excluded (spec 5.13).
- `Equipment` — Equipment register.
- `IntegrationJobs` — One row per external call attempt, with idempotency and failure classification.
- `InvoiceLines` — Calculated invoice lines. No figure originates from a language model (invariant I-4).
- `InvoiceRequests` — A calculated billing request. Drafts only until Phase 7; never posted from Phase 1 or 6.
- `MaterialUsage` — Material consumed against a visit activity. Never creates an accounting transaction (spec 5.12).
- `Materials` — Approved materials catalogue.
- `NumberRegister` — Every number ever reserved, issued or cancelled. A cancelled number is never reused (D-10).
- `NumberingSeries` — One configurable series per legal entity x document type x year x scope x optional client requirement. Never one undifferentiated sequence (D-10).
- `TaxRules` — Configurable tax rules. NO CLASSIFICATION IS NAMED OR ASSUMED before the accountant confirms it in writing (D-08).
- `VisitEquipment` — Equipment present during a visit.
- `VisitManpower` — Manpower present during a visit, for resource summaries only.
- `WorkOrders` — A discrete instruction under a contract, or a one-off job.

## Verification required in Phase 2

Every filter above is a **specification**. None has been executed on AppSheet. The Phase 2
gate must record, for each of these, an attempted access from an unassigned account through
a view, a search, a deep link and the API — with the result recorded either way.
