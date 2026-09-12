# Security Filter Specification

**Document ID:** AH-SYS-P2A-002 · **Revision:** 1 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-12 from `model/model.json` by `tools/gen_appsheet_workbook.py`

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
| `Users` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("FieldUser"), [UserID] = ME()))` | grant-dependent roles read nothing without an active grant; own rows only |
| `Projects` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"))` | grant-dependent roles read nothing without an active grant |
| `ProjectAssignments` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `Locations` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `ActivityTypes` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `ProjectActivityRules` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `SiteVisits` | `OR(ROLE_IN("GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), IN([ProjectID], MY_PROJECTS())), AND(ROLE_IN("FieldUser"), [SupervisorUserID] = ME()))` | grant-dependent roles read nothing without an active grant; assignment-scoped; own rows only |
| `VisitActivities` | `OR(ROLE_IN("GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), IN([ProjectID], MY_PROJECTS())), AND(ROLE_IN("FieldUser"), [CreatedBy] = ME()))` | grant-dependent roles read nothing without an active grant; assignment-scoped; own rows only |
| `Photos` | `OR(ROLE_IN("GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), IN([ProjectID], MY_PROJECTS())), AND(ROLE_IN("FieldUser"), [CapturedBy] = ME()))` | grant-dependent roles read nothing without an active grant; assignment-scoped; own rows only |
| `Snags` | `OR(ROLE_IN("GeneralManager"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor"), IN([ProjectID], MY_PROJECTS())), AND(ROLE_IN("FieldUser"), [RaisedBy] = ME()))` | grant-dependent roles read nothing without an active grant; assignment-scoped; own rows only |
| `Approvals` | `OR(ROLE_IN("SystemAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `DocumentJobs` | `OR(ROLE_IN("GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `Documents` | `OR(ROLE_IN("GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), AND(ROLE_IN("TechnicalReviewer", "ProjectManager"), IN([ProjectID], MY_PROJECTS())))` | grant-dependent roles read nothing without an active grant; assignment-scoped |
| `NumberRegister` | `OR(ROLE_IN("GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor"), COUNT(MY_GRANT()) > 0), ROLE_IN("TechnicalReviewer", "ProjectManager"))` | grant-dependent roles read nothing without an active grant |
| `LegalEntities` | `OR(ROLE_IN("SystemAdministrator", "BusinessAdministrator", "GeneralManager", "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor", "FieldUser"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `AuditLog` | `OR(ROLE_IN("SystemAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0))` | grant-dependent roles read nothing without an active grant |
| `IntegrationJobs` | `OR(ROLE_IN("SystemAdministrator", "GeneralManager", "FinanceReviewer"), AND(ROLE_IN("ReadOnlyAuditor", "EmergencyAccess"), COUNT(MY_GRANT()) > 0), ROLE_IN("TechnicalReviewer", "ProjectManager"))` | grant-dependent roles read nothing without an active grant |

## Tables deliberately absent from the application

These are not filtered — they are **not present in the app's data set at all**, which is the
strongest form of the control: data that is not there cannot leak.

- `ApprovalDelegations` — Temporary delegation of an approval authority (D-09). Every delegated decision records both the acting user and the original responsible user.
- `ApprovalMatrix` — Who approves what, per project and stage (D-09, D-15 item 6). The GM is the MVP approver, and the structure supports delegation without redesign.
- `BOQItems` — Bill of quantities. Cumulative quantity is controlled, never merely recorded.
- `Clients` — Clients the company works for. Bilingual names preserved exactly (D-11).
- `Contacts` — Client contacts. Only an authorised recipient may receive a released document.
- `Contracts` — Commercial agreement governing a project. Hidden from field roles entirely.
- `DataClassifications` — Sensitivity classes applied to records and files, driving residency and sharing rules (D-12).
- `Disciplines` — Work disciplines. A project may permit one or many.
- `DocumentTemplates` — Approved templates, keyed by document type, language and optionally project or discipline (D-11, ADR-0007).
- `DocumentTypes` — Controlled document types. Adding a type is configuration, not development (D-10).
- `Employees` — Crew register for resource reporting. Payroll data is deliberately excluded (spec 5.13).
- `EntityVersions` — Immutable version history of hashable entities. Supports proving what a decision applied to.
- `Equipment` — Equipment register.
- `InvoiceLines` — Calculated invoice lines. No figure originates from a language model (invariant I-4).
- `InvoiceRequests` — A calculated billing request. Drafts only until Phase 7; never posted from Phase 1 or 6.
- `Languages` — Supported languages and their direction. Bilingual capability is architectural (D-11).
- `MaterialUsage` — Material consumed against a visit activity. Never creates an accounting transaction (spec 5.12).
- `Materials` — Approved materials catalogue.
- `NumberingSeries` — One configurable series per legal entity x document type x year x scope x optional client requirement. Never one undifferentiated sequence (D-10).
- `ResidencyAssignments` — Binds a residency requirement to a client, contract or project (D-12).
- `ResidencyRequirements` — Storage and processing restrictions that may be assigned to a client, contract or project (D-12).
- `Roles` — System roles. Authorisation is enforced by security filters and server-side re-validation, never by view visibility (spec 7.4).
- `SystemRecoveryPlan` — How administrative control is recovered when no administrator is available. The system must not become unrecoverable because one person is unreachable.
- `TaxRules` — Configurable tax rules. NO CLASSIFICATION IS NAMED OR ASSUMED before the accountant confirms it in writing (D-08).
- `TemporaryAccessGrants` — Time-bound, explicitly authorised access. Covers auditor access and break-glass emergency access. Without an active grant, the roles that depend on one resolve to no access at all.
- `Units` — Units of measure for quantities.
- `VisitEquipment` — Equipment present during a visit.
- `VisitManpower` — Manpower present during a visit, for resource summaries only.
- `WorkOrders` — A discrete instruction under a contract, or a one-off job.

## Verification required in Phase 2

Every filter above is a **specification**. None has been executed on AppSheet. The Phase 2
gate must record, for each of these, an attempted access from an unassigned account through
a view, a search, a deep link and the API — with the result recorded either way.
