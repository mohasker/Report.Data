# Data Dictionary

**Document ID:** AH-SYS-P1-001 · **Revision:** 1 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-11 from `model/model.json` (model version 1.0.0) by `tools/gen_data_dictionary.py`

> This document is produced from the canonical model, as are the JSON Schemas in
> `schemas/tables/`. They cannot drift apart, because both come from the same source.
> To change a column, edit `tools/build_model.py`, rebuild, and regenerate.

## Conventions

- **Scope** — `global` is reference or control data; `project` means every row carries `ProjectID` and is subject to row-level security.
- **Source** — `user` entered by a person · `system` set by the application · `device` from the capturing device · `integration` returned by an external system · `calculation` produced by the deterministic calculation module · `ai` **advisory only, never authoritative** · `config` administrator-maintained configuration.
- **Hash** — ✔ means the column is part of the entity's `ContentHash`, so changing it voids an approval (ADR-0006).
- **Decimal columns are stored as decimal strings, never as floating point** (spec 11).
- Every table carries `CreatedAt`, `CreatedBy`, `UpdatedAt`, `UpdatedBy`; most carry `IsActive`. Rows are deactivated or cancelled, never destroyed, because history is evidence.
- Columns ending `EN` have an `AR` counterpart. Arabic text is stored as given and is never transliterated (D-11).

## Tables at a glance

| Table | Category | Scope | Sensitivity | Built in | Columns | Description |
|---|---|---|---|---|---|---|
| [`LegalEntities`](#legalentities) | master | global | internal | Phase 1–2 (MVP core) | 29 | Registered legal entities that issue documents. Multi-entity from the start (D-02). |
| [`Languages`](#languages) | vocabulary | global | internal | Phase 1–2 (MVP core) | 10 | Supported languages and their direction. Bilingual capability is architectural (D-11). |
| [`Roles`](#roles) | vocabulary | global | internal | Phase 1–2 (MVP core) | 13 | System roles. Authorisation is enforced by security filters and server-side re-validation, never by view visibility (spec 7.4). |
| [`Users`](#users) | master | global | personal | Phase 1–2 (MVP core) | 15 | People who may sign in. One identity per person — shared accounts destroy attribution. |
| [`Units`](#units) | vocabulary | global | internal | Phase 1–2 (MVP core) | 10 | Units of measure for quantities. |
| [`Disciplines`](#disciplines) | vocabulary | global | internal | Phase 1–2 (MVP core) | 9 | Work disciplines. A project may permit one or many. |
| [`ActivityTypes`](#activitytypes) | master | global | internal | Phase 1–2 (MVP core) | 18 | Catalogue of activities with their default evidence and quantity rules. Per-project overrides live in ProjectActivityRules. |
| [`DocumentTypes`](#documenttypes) | vocabulary | global | internal | Phase 1–2 (MVP core) | 13 | Controlled document types. Adding a type is configuration, not development (D-10). |
| [`DataClassifications`](#dataclassifications) | master | global | internal | Phase 1–2 (MVP core) | 12 | Sensitivity classes applied to records and files, driving residency and sharing rules (D-12). |
| [`ResidencyRequirements`](#residencyrequirements) | master | global | internal | Phase 1–2 (MVP core) | 13 | Storage and processing restrictions that may be assigned to a client, contract or project (D-12). |
| [`TaxRules`](#taxrules) | master | global | financial | Phase 6 | 17 | Configurable tax rules. NO CLASSIFICATION IS NAMED OR ASSUMED before the accountant confirms it in writing (D-08). |
| [`NumberingSeries`](#numberingseries) | master | global | internal | Phase 5 | 20 | One configurable series per legal entity x document type x year x scope x optional client requirement. Never one undifferentiated sequence (D-10). |
| [`DocumentTemplates`](#documenttemplates) | master | global | internal | Phase 5 | 20 | Approved templates, keyed by document type, language and optionally project or discipline (D-11, ADR-0007). |
| [`Clients`](#clients) | master | global | confidential | Phase 1–2 (MVP core) | 20 | Clients the company works for. Bilingual names preserved exactly (D-11). |
| [`Contacts`](#contacts) | master | global | personal | Phase 1–2 (MVP core) | 16 | Client contacts. Only an authorised recipient may receive a released document. |
| [`Projects`](#projects) | master | global | confidential | Phase 1–2 (MVP core) | 29 | A project is pure configuration. Adding one never requires changed logic, a cloned app, duplicated scenarios, rewritten prompts or changed code (D-01). |
| [`ProjectAssignments`](#projectassignments) | master | project | internal | Phase 1–2 (MVP core) | 14 | Which users may act on which project, and in what role. A user may be assigned to many projects, and a project may have many users (D-15 item 2). |
| [`Locations`](#locations) | master | project | confidential | Phase 1–2 (MVP core) | 16 | Hierarchical locations within a project. Choices are always filtered by project (spec 7.3). |
| [`ProjectActivityRules`](#projectactivityrules) | master | project | internal | Phase 1–2 (MVP core) | 16 | Per-project overrides of the global activity and evidence rules (D-15 item 4). A project that needs a different rule gets a row, never a code change. |
| [`ApprovalMatrix`](#approvalmatrix) | master | project | internal | Phase 1–2 (MVP core) | 13 | Who approves what, per project and stage (D-09, D-15 item 6). The GM is the MVP approver, and the structure supports delegation without redesign. |
| [`ApprovalDelegations`](#approvaldelegations) | master | global | internal | Phase 1–2 (MVP core) | 17 | Temporary delegation of an approval authority (D-09). Every delegated decision records both the acting user and the original responsible user. |
| [`ResidencyAssignments`](#residencyassignments) | master | project | internal | Phase 1–2 (MVP core) | 14 | Binds a residency requirement to a client, contract or project (D-12). |
| [`SiteVisits`](#sitevisits) | operational | project | confidential | Phase 1–2 (MVP core) | 37 | One reporting event at a location on a date. The unit of submission and review. |
| [`VisitActivities`](#visitactivities) | operational | project | confidential | Phase 1–2 (MVP core) | 19 | What was actually done during a visit. One row per activity. |
| [`Photos`](#photos) | operational | project | confidential | Phase 1–2 (MVP core) | 64 | One photograph per row. The received file is write-once and is never altered (D-13). |
| [`Snags`](#snags) | operational | project | confidential | Phase 1–2 (MVP core) | 24 | Defects and observations tracked to closure with evidence. |
| [`DocumentJobs`](#documentjobs) | document | project | internal | Phase 5 | 27 | A request to produce a document from a frozen snapshot of approved records. |
| [`Documents`](#documents) | document | project | confidential | Phase 5 | 25 | A produced document revision. Approval binds to ContentHash (ADR-0006). |
| [`NumberRegister`](#numberregister) | document | global | internal | Phase 5 | 18 | Every number ever reserved, issued or cancelled. A cancelled number is never reused (D-10). |
| [`Approvals`](#approvals) | control | project | internal | Phase 1–2 (MVP core) | 23 | Every approval decision, bound to the exact content approved (ADR-0006, D-09). |
| [`EntityVersions`](#entityversions) | control | project | internal | Phase 1–2 (MVP core) | 15 | Immutable version history of hashable entities. Supports proving what a decision applied to. |
| [`AuditLog`](#auditlog) | control | global | internal | Phase 1–2 (MVP core) | 13 | Append-only record of every state transition and every consequential action. |
| [`IntegrationJobs`](#integrationjobs) | control | global | internal | Phase 3 | 18 | One row per external call attempt, with idempotency and failure classification. |
| [`TemporaryAccessGrants`](#temporaryaccessgrants) | control | global | internal | Phase 1–2 (MVP core) | 27 | Time-bound, explicitly authorised access. Covers auditor access and break-glass emergency access. Without an active grant, the roles that depend on one resolve to no access at all. |
| [`SystemRecoveryPlan`](#systemrecoveryplan) | control | global | internal | Phase 1–2 (MVP core) | 16 | How administrative control is recovered when no administrator is available. The system must not become unrecoverable because one person is unreachable. |
| [`Contracts`](#contracts) | financial | project | financial | Phase 6 | 23 | Commercial agreement governing a project. Hidden from field roles entirely. |
| [`WorkOrders`](#workorders) | financial | project | financial | Phase 6 | 14 | A discrete instruction under a contract, or a one-off job. |
| [`BOQItems`](#boqitems) | financial | project | financial | Phase 6 | 20 | Bill of quantities. Cumulative quantity is controlled, never merely recorded. |
| [`InvoiceRequests`](#invoicerequests) | financial | project | financial | Phase 6 | 32 | A calculated billing request. Drafts only until Phase 7; never posted from Phase 1 or 6. |
| [`InvoiceLines`](#invoicelines) | financial | project | financial | Phase 6 | 19 | Calculated invoice lines. No figure originates from a language model (invariant I-4). |
| [`Materials`](#materials) | master | global | internal | Phase 5 | 14 | Approved materials catalogue. |
| [`MaterialUsage`](#materialusage) | operational | project | internal | Phase 5 | 11 | Material consumed against a visit activity. Never creates an accounting transaction (spec 5.12). |
| [`Equipment`](#equipment) | master | global | internal | Phase 5 | 10 | Equipment register. |
| [`VisitEquipment`](#visitequipment) | operational | project | internal | Phase 5 | 10 | Equipment present during a visit. |
| [`Employees`](#employees) | master | global | personal | Phase 5 | 12 | Crew register for resource reporting. Payroll data is deliberately excluded (spec 5.13). |
| [`VisitManpower`](#visitmanpower) | operational | project | internal | Phase 5 | 12 | Manpower present during a visit, for resource summaries only. |

**46 tables · 857 columns · 32 controlled vocabularies.**

---

## LegalEntities

Registered legal entities that issue documents. Multi-entity from the start (D-02).

*الكيانات القانونية المسجلة التي تصدر المستندات*

**Primary key:** `LegalEntityID` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `LegalEntityID` | id | ✔ | system |  |  | **PK.** Example: `LE-A7T3R2` |
| `EntityCode` | text | ✔ | user |  |  | **Unique.** 2-6 uppercase letters/digits. Used in document numbers (D-10). Example: `AH` |
| `LegalNameEN` | text | ✔ | user |  |  | From the current Commercial Registration. Placeholder until verified. Example: `LEGAL_ENTITY_NAME_PENDING_VERIFICATION` |
| `LegalNameAR` | text | ✔ | user |  |  | Arabic legal name preserved exactly; never transliterated (D-11). |
| `TradeNameEN` | text |  | user |  |  |  |
| `TradeNameAR` | text |  | user |  |  |  |
| `CommercialRegistrationNumber` | text | ✔ | user |  |  | CR number as registered. Verified before any production document (D-02). |
| `EstablishmentCardNumber` | text |  | user |  |  |  |
| `TaxRegistrationNumber` | text |  | user | financial |  | Presence does not imply any tax treatment (D-08). |
| `TaxRegistrationStatus` | text | ✔ | user |  |  | Default `PENDING_ACCOUNTANT_CONFIRMATION`. Free text placeholder until the accountant confirms in writing (D-08). |
| `RegisteredAddressEN` | longtext | ✔ | user |  |  |  |
| `RegisteredAddressAR` | longtext |  | user |  |  |  |
| `Country` | text | ✔ | user |  |  | Example: `QA` |
| `Currency` | text | ✔ | user |  |  | ISO 4217. Example: `QAR` |
| `OfficialEmail` | email | ✔ | user |  |  |  |
| `OfficialTelephone` | phone | ✔ | user |  |  |  |
| `OfficialWhatsApp` | phone |  | user |  |  |  |
| `LogoFileKey` | filekey |  | config |  |  | Reference to the approved logo. Aspect ratio preserved (spec 10). |
| `DocumentFooterEN` | longtext |  | user |  |  |  |
| `DocumentFooterAR` | longtext |  | user |  |  |  |
| `AuthorisedSignatories` | json |  | user |  |  | List of {name_en, name_ar, position_en, position_ar, scope}. No specimen signatures stored. |
| `EffectiveFrom` | date | ✔ | user |  |  |  |
| `EffectiveTo` | date |  | user |  |  |  |
| `Version` | int | ✔ | system |  |  | Default `1`. A change to legal identity creates a new version; documents record the version used. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> Never edited in place for a legal-name correction: a new version is created so that documents already issued remain explainable.

## Languages

Supported languages and their direction. Bilingual capability is architectural (D-11).

*اللغات المدعومة واتجاه الكتابة*

**Primary key:** `LanguageCode` · **Category:** vocabulary · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `LanguageCode` | enum `Language` | ✔ |  |  |  | **PK.** Example: `en` |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text | ✔ | config |  |  |  |
| `Direction` | text | ✔ | config |  |  | LTR\|RTL. Example: `RTL` |
| `IsDocumentLanguage` | bool | ✔ | config |  |  | Whether approved templates exist for this language. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Roles

System roles. Authorisation is enforced by security filters and server-side re-validation, never by view visibility (spec 7.4).

*أدوار النظام*

**Primary key:** `RoleID` · **Category:** vocabulary · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `RoleID` | id | ✔ |  |  |  | **PK.** Example: `ROLE-FIELDUSER` |
| `RoleCode` | text | ✔ | config |  |  | **Unique.** Example: `FieldUser` |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text | ✔ | config |  |  |  |
| `Description` | longtext | ✔ | config |  |  |  |
| `SeesFinancialData` | bool | ✔ | config |  |  | Default `FALSE`. Field roles are FALSE. Financial tables are kept out of the field app entirely (SEC-04). |
| `MayApprove` | bool | ✔ | config |  |  | Default `FALSE`. |
| `MayAdministerMasterData` | bool | ✔ | config |  |  | Default `FALSE`. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Users

People who may sign in. One identity per person — shared accounts destroy attribution.

*مستخدمو النظام*

**Primary key:** `UserID` · **Category:** master · **Scope:** global · **Sensitivity:** personal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `UserID` | id | ✔ |  |  |  | **PK.** Example: `USR-R6V1N8` |
| `Email` | email | ✔ | user |  |  | **Unique.** Normalised to lowercase. The sign-in identity and the audit key. |
| `FullNameEN` | text | ✔ | user |  |  |  |
| `FullNameAR` | text |  | user |  |  | Arabic name preserved without transliteration loss (D-11). |
| `Mobile` | phone |  | user | personal |  |  |
| `RoleID` | ref → `Roles.RoleID` | ✔ | user |  |  |  |
| `EmployeeID` | text |  | user | personal |  |  |
| `DefaultProjectID` | ref → `Projects.ProjectID` |  | user |  |  | Convenience only. Never a substitute for ProjectAssignments. |
| `Language` | enum `Language` | ✔ | user |  |  | Default `en`. Interface and notification language preference (D-11). |
| `LastLoginAt` | datetime |  | system |  |  |  |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> Payroll and HR attributes are deliberately absent (spec 5.13).

## Units

Units of measure for quantities.

*وحدات القياس*

**Primary key:** `UnitID` · **Category:** vocabulary · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `UnitID` | id | ✔ |  |  |  | **PK.** Example: `UNIT-M2` |
| `UnitCode` | text | ✔ | config |  |  | **Unique.** Example: `m2` |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text | ✔ | config |  |  |  |
| `DecimalPlaces` | int | ✔ | config |  |  | Default `2`. Quantity rounding for this unit. Applied by the calculation module only. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Disciplines

Work disciplines. A project may permit one or many.

*التخصصات*

**Primary key:** `DisciplineID` · **Category:** vocabulary · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `DisciplineID` | id | ✔ |  |  |  | **PK.** Example: `DIS-LAND` |
| `DisciplineCode` | text | ✔ | config |  |  | **Unique.** Example: `LANDSCAPE` |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text | ✔ | config |  |  |  |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## ActivityTypes

Catalogue of activities with their default evidence and quantity rules. Per-project overrides live in ProjectActivityRules.

*أنواع الأنشطة وقواعد الأدلة الافتراضية*

**Primary key:** `ActivityTypeID` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ActivityTypeID` | id | ✔ |  |  |  | **PK.** Example: `ACT-0001` |
| `DisciplineID` | ref → `Disciplines.DisciplineID` | ✔ | config |  |  |  |
| `ActivityCode` | text | ✔ | config |  |  | **Unique.** Example: `TURF-MOW` |
| `ActivityNameEN` | text | ✔ | config |  |  |  |
| `ActivityNameAR` | text | ✔ | config |  |  |  |
| `RequiresBeforePhoto` | bool | ✔ | config |  |  | Default `FALSE`. |
| `RequiresAfterPhoto` | bool | ✔ | config |  |  | Default `FALSE`. |
| `RequiresQuantity` | bool | ✔ | config |  |  | Default `FALSE`. |
| `QuantityUnitID` | ref → `Units.UnitID` |  | config |  |  | Required when RequiresQuantity is TRUE. |
| `RequiresMaterial` | bool | ✔ | config |  |  | Default `FALSE`. |
| `RequiresSnagCheck` | bool | ✔ | config |  |  | Default `FALSE`. |
| `MinPhotos` | int | ✔ | config |  |  | Default `0`. |
| `DefaultEvidenceStages` | text |  | config |  |  | Comma-separated EvidenceStage codes suggested in the form. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## DocumentTypes

Controlled document types. Adding a type is configuration, not development (D-10).

*أنواع المستندات المعتمدة*

**Primary key:** `DocumentTypeCode` · **Category:** vocabulary · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `DocumentTypeCode` | enum `DocumentTypeCode` | ✔ |  |  |  | **PK.** |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text | ✔ | config |  |  |  |
| `RequiresTechnicalApproval` | bool | ✔ | config |  |  | Default `TRUE`. |
| `RequiresFinanceApproval` | bool | ✔ | config |  |  | Default `FALSE`. |
| `RequiresReleaseApproval` | bool | ✔ | config |  |  | Default `TRUE`. |
| `IsExternallyIssued` | bool | ✔ | config |  |  | Default `TRUE`. |
| `BuiltInPhase` | text | ✔ | config |  |  | MonthlyTechnicalReport is the only type produced in the MVP. Example: `5` |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## DataClassifications

Sensitivity classes applied to records and files, driving residency and sharing rules (D-12).

*تصنيفات حساسية البيانات*

**Primary key:** `ClassificationCode` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ClassificationCode` | enum `DataClassificationCode` | ✔ |  |  |  | **PK.** |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text | ✔ | config |  |  |  |
| `Description` | longtext | ✔ | config |  |  |  |
| `MayLeaveTenant` | bool | ✔ | config |  |  | Default `FALSE`. Whether data of this class may be sent to any third-party processor. |
| `MayBeSharedExternally` | bool | ✔ | config |  |  | Default `FALSE`. |
| `DefaultRetentionDays` | int |  | config |  |  | Expiry flags for review. Nothing is ever auto-deleted (C-10). |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## ResidencyRequirements

Storage and processing restrictions that may be assigned to a client, contract or project (D-12).

*متطلبات مكان تخزين ومعالجة البيانات*

**Primary key:** `ResidencyRequirementID` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ResidencyRequirementID` | id | ✔ |  |  |  | **PK.** Example: `RES-G3K9V2` |
| `RuleCode` | enum `ResidencyRuleCode` | ✔ | config |  |  |  |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text | ✔ | config |  |  |  |
| `AllowedRegions` | text |  | config |  |  | Comma-separated region or country codes where storage is permitted. |
| `BlocksProductionUpload` | bool | ✔ | config |  |  | Default `FALSE`. TRUE blocks production upload for the affected project only, not the system (D-12). |
| `BlocksThirdPartyAI` | bool | ✔ | config |  |  | Default `FALSE`. TRUE disables AI analysis for the affected project. |
| `SourceClauseReference` | text |  | user |  |  | Where in the contract the restriction comes from. No contract text is stored. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## TaxRules

Configurable tax rules. NO CLASSIFICATION IS NAMED OR ASSUMED before the accountant confirms it in writing (D-08).

*قواعد الضريبة القابلة للتهيئة*

**Primary key:** `TaxRuleID` · **Category:** master · **Scope:** global · **Sensitivity:** financial · **Built in:** Phase 6

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `TaxRuleID` | id | ✔ |  |  |  | **PK.** Example: `TAX-PLACEHOLDER-PENDING` |
| `TaxRuleCode` | text | ✔ | config |  |  | **Unique.** Example: `PENDING_ACCOUNTANT_CONFIRMATION` |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text | ✔ | config |  |  |  |
| `TreatmentLabel` | enum `TaxTreatmentPlaceholder` | ✔ | config |  |  | 'Zero-rated', 'exempt', 'out of scope' and 'no tax configured' are distinct and non-interchangeable. None may be recorded here without written confirmation (D-08). |
| `RatePercent` | decimal(4) |  | config |  |  | Null until confirmed. Null means 'unknown', never 'zero'.. |
| `AppliesToCountry` | text |  | config |  |  |  |
| `EffectiveFrom` | date | ✔ | config |  |  |  |
| `EffectiveTo` | date |  | config |  |  |  |
| `Version` | int | ✔ | system |  |  | Default `1`. The rule AND its version are preserved on every invoice calculation (D-08). |
| `ConfirmedByAccountant` | bool | ✔ | user |  |  | Default `FALSE`. Production invoicing is blocked while FALSE. |
| `ConfirmationReference` | text |  | user |  |  | Reference to the accountant's written confirmation. No document content stored. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## NumberingSeries

One configurable series per legal entity x document type x year x scope x optional client requirement. Never one undifferentiated sequence (D-10).

*تسلسلات ترقيم المستندات القابلة للتهيئة*

**Primary key:** `SeriesID` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 5

**Unique together:** `LegalEntityID`, `DocumentTypeCode`, `ScopeKind`, `ProjectID`, `ClientID`, `YearBasis`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `SeriesID` | id | ✔ |  |  |  | **PK.** Example: `SER-F9W3C5` |
| `LegalEntityID` | ref → `LegalEntities.LegalEntityID` | ✔ | config |  |  |  |
| `DocumentTypeCode` | enum `DocumentTypeCode` | ✔ | config |  |  |  |
| `ScopeKind` | text | ✔ | config |  |  | CompanyWide\|PerProject\|PerClient. Determines whether the counter is shared or partitioned. |
| `ProjectID` | ref → `Projects.ProjectID` |  | config |  |  | Required when ScopeKind = PerProject. |
| `ClientID` | ref → `Clients.ClientID` |  | config |  |  | Required when ScopeKind = PerClient. |
| `YearBasis` | text | ✔ | config |  |  | Default `Calendar`. Calendar\|Financial\|None. |
| `FinancialYearStartMonth` | int |  | config |  |  | 1-12 when YearBasis=Financial. |
| `FormatPattern` | text | ✔ | config |  |  | Tokens: {ENTITY} {TYPE} {YYYY} {YY} {PROJECT} {CLIENT} {NNN} {REV}. Illustrative only until the existing manual register is reviewed (D-10). Example: `{ENTITY}-TR-{YYYY}-{NNN}` |
| `PadWidth` | int | ✔ | config |  |  | Default `3`. |
| `StartNumber` | int | ✔ | config |  |  | Default `1`. Continues the existing manual register rather than restarting it (A-18). |
| `ResetRule` | text | ✔ | config |  |  | Default `PerYear`. PerYear\|Never. |
| `MigratedFromManualRegister` | bool | ✔ | user |  |  | Default `FALSE`. TRUE once the existing manual series has been reviewed and its last number recorded. |
| `LastManualNumber` | int |  | user |  |  | The final number used manually, so the system continues rather than collides. |
| `AlignedToAccountingProcess` | bool | ✔ | config |  |  | Default `FALSE`. TRUE for invoice-related series: numbering follows the approved accounting process (D-10). |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## DocumentTemplates

Approved templates, keyed by document type, language and optionally project or discipline (D-11, ADR-0007).

*القوالب المعتمدة*

**Primary key:** `TemplateID` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `TemplateID` | id | ✔ |  |  |  | **PK.** Example: `TPL-D8Q2H6` |
| `DocumentTypeCode` | enum `DocumentTypeCode` | ✔ | config |  |  |  |
| `TemplateNameEN` | text | ✔ | config |  |  |  |
| `TemplateNameAR` | text |  | config |  |  |  |
| `LanguageCode` | enum `Language` | ✔ | config |  |  | A template is single-language; bilingual output is two approved templates (D-11). |
| `TextDirection` | text | ✔ | config |  |  | LTR\|RTL. Derived from the language but stored explicitly so RTL is testable. |
| `ProjectID` | ref → `Projects.ProjectID` |  | config |  |  | Null means available to any project. Project-specific templates override (D-15 item 5). |
| `DisciplineID` | ref → `Disciplines.DisciplineID` |  | config |  |  |  |
| `LegalEntityID` | ref → `LegalEntities.LegalEntityID` | ✔ | config |  |  |  |
| `StorageFileKey` | filekey |  | config |  |  | Reference to the controlled template file. No production file ID exists in Phase 1. |
| `Version` | int | ✔ | config |  |  | Default `1`. |
| `EffectiveFrom` | date | ✔ | config |  |  |  |
| `EffectiveTo` | date |  | config |  |  |  |
| `ApprovedByUserID` | ref → `Users.UserID` |  | user |  |  |  |
| `Status` | text | ✔ | config |  |  | Default `Draft`. Draft\|Approved\|Superseded\|Withdrawn. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Clients

Clients the company works for. Bilingual names preserved exactly (D-11).

*العملاء*

**Primary key:** `ClientID` · **Category:** master · **Scope:** global · **Sensitivity:** confidential · **Built in:** Phase 1–2 (MVP core)

**At least one required:** `LegalNameEN`, `LegalNameAR`
**At least one required:** `DisplayNameEN`, `DisplayNameAR`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ClientID` | id | ✔ |  |  |  | **PK.** Example: `CLI-D4F8T2` |
| `LegalNameEN` | text |  | user |  |  | Not required: a client may be registered only in Arabic. At least one legal name must be present (D-11). |
| `LegalNameAR` | text |  | user |  |  | Some clients are known only by an Arabic legal name; it is stored exactly as given and is never transliterated to fill an English column. |
| `DisplayNameEN` | text |  | user |  |  |  |
| `DisplayNameAR` | text |  | user |  |  |  |
| `ClientKind` | text | ✔ | user |  |  | Government\|SemiGovernment\|Private\|MainContractor. |
| `BillingAddressEN` | longtext |  | user | financial |  |  |
| `BillingAddressAR` | longtext |  | user | financial |  |  |
| `TaxRegistrationNumber` | text |  | user | financial |  | Hidden from field roles (spec 7.4). |
| `PrimaryContactID` | ref → `Contacts.ContactID` |  | user |  |  |  |
| `PaymentTermsDays` | int |  | user | financial |  |  |
| `Currency` | text |  | user | financial |  | ISO 4217. |
| `DefaultClassificationCode` | enum `DataClassificationCode` |  | user |  |  | Baseline classification for this client's records (D-12). |
| `QuickBooksCustomerID` | text |  | integration | financial |  | Immutable accounting identifier. Never name-matched (spec 8 scenario 10). |
| `Status` | text | ✔ | user |  |  | Default `Active`. Active\|Suspended\|Closed. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> A client registered only in Arabic is normal in Qatar. Forcing an English legal name would invite a transliteration that is not the client's legal name (D-11).

## Contacts

Client contacts. Only an authorised recipient may receive a released document.

*جهات الاتصال لدى العملاء*

**Primary key:** `ContactID` · **Category:** master · **Scope:** global · **Sensitivity:** personal · **Built in:** Phase 1–2 (MVP core)

**At least one required:** `NameEN`, `NameAR`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ContactID` | id | ✔ |  |  |  | **PK.** Example: `CON-B3H9L5` |
| `ClientID` | ref → `Clients.ClientID` | ✔ | user |  |  |  |
| `NameEN` | text |  | user |  |  |  |
| `NameAR` | text |  | user |  |  |  |
| `PositionEN` | text |  | user |  |  |  |
| `PositionAR` | text |  | user |  |  |  |
| `Email` | email |  | user | personal |  |  |
| `Mobile` | phone |  | user | personal |  |  |
| `PreferredLanguage` | enum `Language` | ✔ | user |  |  | Default `en`. |
| `IsAuthorizedRecipient` | bool | ✔ | user |  |  | Default `FALSE`. Only TRUE contacts may appear in a release recipient snapshot. |
| `Status` | text | ✔ | user |  |  | Default `Active`. Active\|Inactive. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Projects

A project is pure configuration. Adding one never requires changed logic, a cloned app, duplicated scenarios, rewritten prompts or changed code (D-01).

*المشاريع*

**Primary key:** `ProjectID` · **Category:** master · **Scope:** global · **Sensitivity:** confidential · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ProjectID` | id | ✔ |  |  |  | **PK.** Example: `PRJ-K7M2Q1` |
| `ProjectCode` | text | ✔ | user |  |  | **Unique.** Uppercase, no spaces, filename-safe. Used in folder and file names. A display code, never a key. Example: `EXAMPLE-CODE-01` |
| `ProjectNameEN` | text | ✔ | user |  |  |  |
| `ProjectNameAR` | text |  | user |  |  |  |
| `LegalEntityID` | ref → `LegalEntities.LegalEntityID` | ✔ | user |  |  | Which registered entity issues this project's documents (D-02). |
| `ClientID` | ref → `Clients.ClientID` | ✔ | user |  |  |  |
| `ContractID` | ref → `Contracts.ContractID` |  | user | financial |  |  |
| `LocationSummaryEN` | text |  | user |  |  |  |
| `LocationSummaryAR` | text |  | user |  |  |  |
| `StartDate` | date | ✔ | user |  |  |  |
| `EndDate` | date |  | user |  |  | Must be >= StartDate when present. |
| `ReportingFrequency` | enum `ReportingFrequency` | ✔ | user |  |  |  |
| `ReportingCutoffDay` | int |  | user |  |  | 1-28. Latest day evidence may be added to a closing period (OQ-02). |
| `DefaultTemplateID` | ref → `DocumentTemplates.TemplateID` |  | user |  |  |  |
| `DefaultDocumentLanguage` | enum `Language` | ✔ | user |  |  | Default `en`. |
| `ProjectManagerUserID` | ref → `Users.UserID` |  | user |  |  |  |
| `Currency` | text | ✔ | user | financial |  | ISO 4217. Must match the contract currency; a mismatch is a validation failure (C-09). |
| `TimeZone` | text | ✔ | user |  |  | Default `Asia/Qatar`. |
| `BillingMethod` | enum `BillingMethod` |  | user | financial |  |  |
| `PaymentTermsDays` | int |  | user | financial |  |  |
| `AIAnalysisEnabled` | bool | ✔ | user |  |  | Default `TRUE`. Set FALSE where a contract or residency rule forbids third-party AI processing (D-12). |
| `RetentionDays` | int |  | user |  |  | Overrides the classification default. Expiry flags for review, never auto-deletes. |
| `DriveFolderKey` | filekey |  | integration |  |  | Provisioned folder reference. Empty in Phase 1 — nothing is connected (D-14). |
| `Status` | enum `ProjectStatus` | ✔ | user |  |  | Default `Draft`. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> Every project-varying behaviour is a column or a child row here, never a branch in code.

## ProjectAssignments

Which users may act on which project, and in what role. A user may be assigned to many projects, and a project may have many users (D-15 item 2).

*إسناد المستخدمين إلى المشاريع*

**Primary key:** `AssignmentID` · **Category:** master · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

**Unique together:** `ProjectID`, `UserID`, `RoleID`, `AssignedFrom`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `AssignmentID` | id | ✔ |  |  |  | **PK.** Example: `ASG-V7D1G6` |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | user |  |  |  |
| `UserID` | ref → `Users.UserID` | ✔ | user |  |  |  |
| `RoleID` | ref → `Roles.RoleID` | ✔ | user |  |  | The role a user holds ON THIS PROJECT. It may differ from their default role. |
| `AssignedFrom` | date | ✔ | user |  |  |  |
| `AssignedTo` | date |  | user |  |  | Null means open-ended. An expired assignment grants nothing. |
| `MaySubmitEvidence` | bool | ✔ | user |  |  | Default `TRUE`. |
| `MayReviewEvidence` | bool | ✔ | user |  |  | Default `FALSE`. |
| `MayRequestDocuments` | bool | ✔ | user |  |  | Default `FALSE`. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> This table is the sole source of row-level access. Absence of a row means no access, and no view, slice or convenience field may substitute for it.

## Locations

Hierarchical locations within a project. Choices are always filtered by project (spec 7.3).

*المواقع ضمن المشروع*

**Primary key:** `LocationID` · **Category:** master · **Scope:** project · **Sensitivity:** confidential · **Built in:** Phase 1–2 (MVP core)

**Unique together:** `ProjectID`, `LocationCode`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `LocationID` | id | ✔ |  |  |  | **PK.** Example: `LOC-Z5J3D9` |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | user |  |  |  |
| `LocationCode` | text | ✔ | user |  |  | Filename-safe; unique within project. Example: `BLK-A` |
| `LocationNameEN` | text | ✔ | user |  |  |  |
| `LocationNameAR` | text |  | user |  |  |  |
| `ParentLocationID` | ref → `Locations.LocationID` |  | user |  |  | Parent must belong to the SAME project; no cycles; max depth 5. Supports site > building > floor > room hierarchies (D-15 item 3). |
| `LocationKind` | text |  | user |  |  | Site\|Zone\|Building\|Floor\|Room\|Asset. |
| `GPSLatitude` | decimal(7) |  | device |  |  | Evidence, not a gate. Missing is recorded as missing, never as zero (C-08). |
| `GPSLongitude` | decimal(7) |  | device |  |  |  |
| `GeofenceRadiusM` | int |  | user |  |  | Out-of-geofence capture is flagged for the reviewer, never auto-rejected. |
| `DisplayOrder` | int | ✔ | user |  |  | Default `100`. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## ProjectActivityRules

Per-project overrides of the global activity and evidence rules (D-15 item 4). A project that needs a different rule gets a row, never a code change.

*قواعد الأنشطة والأدلة الخاصة بالمشروع*

**Primary key:** `ProjectActivityRuleID` · **Category:** master · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

**Unique together:** `ProjectID`, `ActivityTypeID`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ProjectActivityRuleID` | id | ✔ |  |  |  | **PK.** Example: `PAR-X1B6M7` |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | user |  |  |  |
| `ActivityTypeID` | ref → `ActivityTypes.ActivityTypeID` | ✔ | user |  |  |  |
| `IsPermitted` | bool | ✔ | user |  |  | Default `TRUE`. FALSE removes the activity from this project's form without deleting history. |
| `RequiresBeforePhoto` | bool |  | user |  |  | Null inherits the global rule. |
| `RequiresAfterPhoto` | bool |  | user |  |  | Null inherits the global rule. |
| `RequiresQuantity` | bool |  | user |  |  | Null inherits the global rule. |
| `QuantityUnitID` | ref → `Units.UnitID` |  | user |  |  |  |
| `MinPhotos` | int |  | user |  |  |  |
| `RequiresCaption` | bool |  | user |  |  |  |
| `BOQItemHint` | text |  | user | financial |  | Optional link to the billing item, used from Phase 6. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## ApprovalMatrix

Who approves what, per project and stage (D-09, D-15 item 6). The GM is the MVP approver, and the structure supports delegation without redesign.

*مصفوفة الاعتمادات*

**Primary key:** `ApprovalMatrixID` · **Category:** master · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ApprovalMatrixID` | id | ✔ |  |  |  | **PK.** Example: `APM-C2S9W3` |
| `ProjectID` | ref → `Projects.ProjectID` |  | user |  |  | Null means the company-wide default for this stage. |
| `ApprovalStage` | enum `ApprovalStage` | ✔ | user |  |  |  |
| `DocumentTypeCode` | enum `DocumentTypeCode` |  | user |  |  | Null applies to every document type. |
| `ResponsibleUserID` | ref → `Users.UserID` | ✔ | user |  |  | The accountable approver. A delegate acts FOR this person, never instead of them. |
| `BackupUserID` | ref → `Users.UserID` |  | user |  |  | May remain unassigned until before go-live (D-09). |
| `SequenceNumber` | int | ✔ | user |  |  | Default `1`. Supports multi-step approval within a stage. |
| `SelfApprovalProhibited` | bool | ✔ | config |  |  | Default `TRUE`. No user may approve their own restricted transaction because an approver is unavailable (D-09). This is not configurable to FALSE for financial stages. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## ApprovalDelegations

Temporary delegation of an approval authority (D-09). Every delegated decision records both the acting user and the original responsible user.

*تفويض صلاحيات الاعتماد مؤقتاً*

**Primary key:** `DelegationID` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `DelegationID` | id | ✔ |  |  |  | **PK.** Example: `DEL-N5T8J4` |
| `FromUserID` | ref → `Users.UserID` | ✔ | user |  |  | The original responsible approver. |
| `ToUserID` | ref → `Users.UserID` | ✔ | user |  |  | The acting delegate. May be unassigned until before go-live. |
| `ApprovalStage` | enum `ApprovalStage` |  | user |  |  | Null delegates every stage the delegator holds. |
| `Scope` | enum `DelegationScope` | ✔ | user |  |  |  |
| `ProjectIDs` | text |  | user |  |  | Comma-separated ProjectIDs when Scope = SpecificProjects. |
| `ValidFrom` | datetime | ✔ | user |  |  |  |
| `ValidTo` | datetime | ✔ | user |  |  | Must be after ValidFrom. An open-ended delegation is not permitted.. |
| `Reason` | text | ✔ | user |  |  |  |
| `AuthorisedByUserID` | ref → `Users.UserID` | ✔ | user |  |  |  |
| `RevokedAt` | datetime |  | user |  |  |  |
| `RevokedByUserID` | ref → `Users.UserID` |  | user |  |  |  |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> A delegation is evidence, so it is never deleted — it is revoked, with a timestamp.

## ResidencyAssignments

Binds a residency requirement to a client, contract or project (D-12).

*ربط متطلبات الإقامة بالبيانات*

**Primary key:** `ResidencyAssignmentID` · **Category:** master · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ResidencyAssignmentID` | id | ✔ |  |  |  | **PK.** Example: `RSA-L6P4Z8` |
| `ResidencyRequirementID` | ref → `ResidencyRequirements.ResidencyRequirementID` | ✔ | user |  |  |  |
| `AppliesToKind` | text | ✔ | user |  |  | Client\|Contract\|Project. |
| `ClientID` | ref → `Clients.ClientID` |  | user |  |  |  |
| `ContractID` | ref → `Contracts.ContractID` |  | user |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` |  | user |  |  |  |
| `EffectiveFrom` | date | ✔ | user |  |  |  |
| `EffectiveTo` | date |  | user |  |  |  |
| `VerifiedFromContract` | bool | ✔ | user |  |  | Default `FALSE`. FALSE means the contract has not yet been reviewed — production upload stays blocked. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## SiteVisits

One reporting event at a location on a date. The unit of submission and review.

*زيارة موقع*

**Primary key:** `VisitID` · **Category:** operational · **Scope:** project · **Sensitivity:** confidential · **Built in:** Phase 1–2 (MVP core)

**ContentHash covers:** `ProjectID`, `LocationID`, `WorkOrderID`, `VisitDate`, `StartTime`, `EndTime`, `Weather`, `SupervisorUserID`, `OverallDescriptionEN`, `OverallDescriptionAR`, `SafetyObservation`, `ClientRepresentative`, `ClientAcknowledgementStatus`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `VisitID` | id | ✔ |  |  |  | **PK.** Example: `VIS-Q8C4K1` |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  | ✔ | Required in storage, never a routine question (D-22). Trusted system data; never inferred from a photograph (D-19). |
| `LocationID` | ref → `Locations.LocationID` | ✔ | system |  | ✔ | Location must belong to ProjectID. Required in storage, confirmed rather than typed (D-22). |
| `WorkOrderID` | ref → `WorkOrders.WorkOrderID` |  | user |  | ✔ |  |
| `VisitDate` | date | ✔ | device |  | ✔ | Never typed on the normal path. Correctable by an authorised user (spec 7.3). |
| `StartTime` | time |  | device |  | ✔ |  |
| `EndTime` | time |  | device |  | ✔ | Must be after StartTime. |
| `Weather` | text |  | user |  | ✔ |  |
| `SupervisorUserID` | ref → `Users.UserID` | ✔ | system |  | ✔ | Resolved from the authenticated identity; must hold an active assignment to ProjectID. |
| `GPSLatitude` | decimal(7) |  | device |  |  |  |
| `GPSLongitude` | decimal(7) |  | device |  |  |  |
| `OverallDescriptionEN` | longtext |  | user |  | ✔ | Optional for a normal photographic submission (D-18). NOT mandatory. A normal submission is established by photographs. A written description is required only in the declared exceptional workflows. |
| `OverallDescriptionAR` | longtext |  | user |  | ✔ | Optional for a normal photographic submission (D-18). A supervisor may write in either language; both are carried to the report (D-11). |
| `AdditionalSiteNote` | longtext |  | user |  |  | Optional. Mandatory only in the exceptional workflows listed in capture_once.optional_note.mandatory_exceptions. For facts a photograph cannot establish (D-18). Speech-to-text is a future input method for this field, not a new field. |
| `SiteNoteCategory` | enum `SiteNoteCategory` |  | user |  |  | Classifies the optional note so it can be routed and reported. Never inferred by AI. |
| `CaptureMode` | enum `CaptureMode` | ✔ | system |  |  | Default `QuickShare`. Quick Share is the default so the contractor group is served first and nothing is waited for (D-22). Both modes capture the images exactly once (D-16). |
| `ShareStatus` | enum `ShareStatus` | ✔ | user |  |  | Default `NotShared`. Recorded from the supervisor's confirmation. The app cannot observe delivery inside the messaging application. |
| `SharedAt` | datetime |  | system |  |  |  |
| `SharedByUserID` | ref → `Users.UserID` |  | system |  |  |  |
| `ShareTargetLabel` | text |  | config |  |  | A label for the destination group, held as project configuration. NEVER a telephone number, group invitation link or messaging identifier (D-19). |
| `ShareAttemptCount` | int | ✔ | system |  |  | Default `0`. Incremented on every share attempt. A retry re-uses the stored evidence and must never ask the supervisor to select the images again (CAP-01). |
| `SafetyObservation` | longtext |  | user |  | ✔ |  |
| `ClientRepresentative` | text |  | user | personal | ✔ |  |
| `ClientAcknowledgementStatus` | text |  | user |  | ✔ | NotRequested\|Claimed\|Declined. A CLAIM recorded on site. Never treated as a client approval (A-20). |
| `WorkflowStatus` | enum `WorkflowStatus` | ✔ | system |  |  | Default `Draft`. |
| `SubmittedAt` | datetime |  | system |  |  |  |
| `TechnicalReviewedAt` | datetime |  | system |  |  |  |
| `TechnicalReviewedBy` | ref → `Users.UserID` |  | system |  |  |  |
| `RejectionReason` | longtext |  | user |  |  | Mandatory when returning a record for correction. |
| `ValidationErrors` | json |  | system |  |  | Specific correctable errors from server-side validation, never a generic message. |
| `CorrelationID` | text |  | system |  |  | Links this record to its orchestration jobs and audit entries. |
| `EntityVersion` | int | ✔ | system |  |  | Default `1`. Incremented on every material change. Referenced by Approvals. |
| `ContentHash` | checksum | ✔ | system |  |  | SHA-256 over the canonical serialisation of the fields listed in content_hash_fields. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## VisitActivities

What was actually done during a visit. One row per activity.

*أنشطة الزيارة*

**Primary key:** `VisitActivityID` · **Category:** operational · **Scope:** project · **Sensitivity:** confidential · **Built in:** Phase 1–2 (MVP core)

**ContentHash covers:** `VisitID`, `ActivityTypeID`, `DescriptionEN`, `DescriptionAR`, `Quantity`, `UnitID`, `PercentComplete`, `SupervisorConfirmation`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `VisitActivityID` | id | ✔ |  |  |  | **PK.** Example: `VAC-T3N6B7` |
| `VisitID` | ref → `SiteVisits.VisitID` | ✔ | system |  | ✔ |  |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  | Denormalised for row-level security; must equal the parent visit's project. |
| `ActivityTypeID` | ref → `ActivityTypes.ActivityTypeID` | ✔ | user |  | ✔ | Must be permitted for the project by ProjectActivityRules. |
| `DescriptionEN` | longtext |  | user |  | ✔ |  |
| `DescriptionAR` | longtext |  | user |  | ✔ |  |
| `Quantity` | decimal(3) |  | user |  | ✔ | Numeric, >= 0, present only where the effective rule requires it. |
| `UnitID` | ref → `Units.UnitID` |  | user |  | ✔ |  |
| `PercentComplete` | int |  | user |  | ✔ | 0-100. Entered by a human. NEVER inferred by AI (spec 5.9, ADR-0004). |
| `EvidenceStatus` | text | ✔ | system |  |  | Default `Incomplete`. Incomplete\|Complete\|Waived. Computed from the effective evidence rule, not typed. |
| `SupervisorConfirmation` | bool | ✔ | user |  | ✔ | Default `FALSE`. An authorised human confirmation. One of the only two bases for a completion statement, the other being approved evidence (operating rule 11). |
| `TechnicalReviewerComment` | longtext |  | user |  |  |  |
| `Status` | enum `VisitActivityStatus` | ✔ | system |  |  | Default `Draft`. |
| `EntityVersion` | int | ✔ | system |  |  | Default `1`. Incremented on every material change. Referenced by Approvals. |
| `ContentHash` | checksum | ✔ | system |  |  | SHA-256 over the canonical serialisation of the fields listed in content_hash_fields. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Photos

One photograph per row. The received file is write-once and is never altered (D-13).

*الصور الفوتوغرافية كأدلة*

**Primary key:** `PhotoID` · **Category:** operational · **Scope:** project · **Sensitivity:** confidential · **Built in:** Phase 1–2 (MVP core)

**ContentHash covers:** `VisitID`, `VisitActivityID`, `LocationID`, `EvidenceStage`, `ConfirmedActivityTypeID`, `CaptionEN`, `CaptionAR`, `ApprovedForReport`, `ReportSequence`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `PhotoID` | id | ✔ |  |  |  | **PK.** Example: `PHO-M9F2X5` |
| `VisitID` | ref → `SiteVisits.VisitID` | ✔ | system |  | ✔ |  |
| `VisitActivityID` | ref → `VisitActivities.VisitActivityID` |  | system |  | ✔ | Optional. A photograph belongs to a visit; it is attached to an activity only once one has been confirmed. A photographic submission with no activity at all is valid (D-22). |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  | Denormalised for row-level security and for folder routing. |
| `LocationID` | ref → `Locations.LocationID` | ✔ | system |  | ✔ |  |
| `CapturedAt` | datetime |  | device |  |  | Device capture time where available. Drives the old-photo warning, never a rejection. |
| `ReceivedAt` | datetime | ✔ | system |  |  | When the controlled system first received the file. The anchor of the write-once guarantee (D-13). |
| `UploadedAt` | datetime |  | system |  |  |  |
| `CapturedBy` | ref → `Users.UserID` | ✔ | system |  |  | The uploader identity recorded with the original (D-13). |
| `OriginalFileKey` | filekey | ✔ | system |  |  | WRITE-ONCE. Never overwritten, altered, annotated, resized or deleted. |
| `OriginalChecksum` | checksum |  | integration |  |  | Taken from the storage provider's own file metadata where available (C-03); computed only as a fallback. |
| `ChecksumAlgorithm` | text |  | integration |  |  | Recorded so the value is interpretable years later. Example: `MD5` |
| `OriginalMimeType` | text |  | integration |  |  |  |
| `OriginalWidth` | int |  | integration |  |  |  |
| `OriginalHeight` | int |  | integration |  |  |  |
| `OriginalSizeBytes` | int |  | integration |  |  |  |
| `IsOriginalDeviceImageVerified` | bool | ✔ | system |  |  | Default `FALSE`. Stays FALSE until real-device testing proves no upstream re-encoding. No file may be described as the original device image while this is FALSE (D-13). |
| `EvidenceStage` | enum `EvidenceStage` |  | user |  | ✔ | Optional at capture (D-22). Never a mandatory manual field before the photograph is taken. A supervisor may set it, and often will not. An unclassified photograph is valid evidence and blocks no submission; ClassificationStatus carries how far it has got. |
| `CaptionEN` | text |  | user |  | ✔ | Mandatory for Snag, Observation, Material and Safety stages. The supervisor's own words. Never overwritten by AI (D-06). |
| `CaptionAR` | text |  | user |  | ✔ |  |
| `GPSLatitude` | decimal(7) |  | device |  |  |  |
| `GPSLongitude` | decimal(7) |  | device |  |  |  |
| `CaptureBatchID` | text |  | system |  |  | Groups the photographs captured in one action, so the share and the report both re-use the same stored set. The mechanism behind capture once, use twice (CAP-01). |
| `CaptureSequence` | int |  | system |  |  | Order within the capture batch. Share order and report order derive from this; the supervisor never re-orders by re-selecting files. |
| `IsDuplicateSuspected` | bool | ✔ | system |  |  | Default `FALSE`. Flag only. A suspected duplicate is never deleted or merged (S-09). |
| `DuplicateOfPhotoID` | ref → `Photos.PhotoID` |  | system |  |  |  |
| `AIAnalysisStatus` | enum `AIAnalysisStatus` | ✔ | system |  |  | Default `NotRequested`. |
| `AnalysisEligibility` | enum `AnalysisEligibility` | ✔ | system |  |  | Default `Eligible`. Decided BEFORE any call is made (D-24). A duplicate, an unusable image, a deleted or excluded one, and an already-analysed one all cost nothing. |
| `PerceptualHash` | text |  | system |  |  | Computed at registration for near-duplicate detection. A flag only: a suspected duplicate is never deleted or merged (S-09). |
| `QualityScore` | decimal(2) |  | system |  |  | 0.00-1.00. Local blur/exposure measure computed without a model call. Below the project threshold the photograph is retained as evidence and skipped for analysis. |
| `AIObservation` | json |  | ai |  |  | ADVISORY ONLY. Schema-validated output, displayed as an AI observation, visually distinct from the caption and the reviewer decision (D-06). |
| `AIProposedEvidenceStage` | enum `EvidenceStage` |  | ai |  |  | A PROPOSAL. Never written to EvidenceStage. The supervisor confirms or corrects it (D-17). |
| `AIProposedActivityText` | text |  | ai |  |  | Free text describing the visible activity. Untrusted. Never becomes the structured activity by itself (D-20, D-23). |
| `AIProposedActivityTypeID` | ref → `ActivityTypes.ActivityTypeID` |  | ai |  |  | Advisory candidate only. No report, rule, calculation, filter or join may read this column. A CANDIDATE code the analysis suggests, held in a typed column so it can be shown beside the catalogue entry it points at. It is not the activity: nothing reads it except the confirmation screen, and confirming copies the value into ConfirmedActivityTypeID by an explicit human action (D-23). |
| `ConfirmedActivityTypeID` | ref → `ActivityTypes.ActivityTypeID` |  | user |  | ✔ | Must be permitted for the project by the effective activity rule. **The trusted structured activity.** Set only by a supervisor or reviewer, and only when ClassificationStatus becomes Confirmed. Reports and business rules read this column and no other (D-23). |
| `ClassificationStatus` | enum `ClassificationStatus` | ✔ | system |  |  | Default `Pending`. Pending is normal after a Quick Share and blocks nothing. Only Confirmed makes the activity trusted (D-23). |
| `ConfirmedByUserID` | ref → `Users.UserID` |  | system |  |  | Who confirmed the classification. Attribution is the point. |
| `ConfirmedAt` | datetime |  | system |  |  |  |
| `AIProposedCaptionEN` | text |  | ai |  |  | Proposed professional caption. Copied into CaptionEN only by a human action. |
| `AIProposedCaptionAR` | text |  | ai |  |  |  |
| `AIVisibleCondition` | text |  | ai |  |  | Visible condition only. Never a cause, never a compliance judgement (D-20). |
| `AIPossibleSnag` | bool |  | ai |  |  | Raises a question for the supervisor. Creates no Snag record by itself. |
| `AIImageQualityWarning` | text |  | ai |  |  | Blur, exposure, obstruction, framing. Advisory; never blocks a submission. |
| `AIUncertaintyNote` | text |  | ai |  |  | What the model could not determine. Required by the analysis schema so that uncertainty is stated rather than hidden. |
| `AIProposalDisposition` | enum `AIProposalDisposition` | ✔ | user |  |  | Default `NotOffered`. What the supervisor did with the proposal. Set only by a human (D-17). |
| `AIAnalysedAt` | datetime |  | system |  |  | In Quick Share this is later than SharedAt, by design. |
| `AIConfidence` | decimal(2) |  | ai |  |  | 0.00-1.00. Advisory. Never a threshold for automatic approval. |
| `AIModel` | text |  | ai |  |  | Recorded for reproducibility. |
| `AIPromptVersion` | text |  | ai |  |  |  |
| `AIContradictsCaption` | bool |  | ai |  |  | Raised for the reviewer's attention; resolves nothing by itself. |
| `ReviewerDecision` | enum `ReviewerDecision` | ✔ | user |  |  | Default `Pending`. Set only by a human reviewer. AI may never write this field. |
| `ReviewerComment` | longtext |  | user |  |  |  |
| `ReviewedByUserID` | ref → `Users.UserID` |  | system |  |  |  |
| `ReviewedAt` | datetime |  | system |  |  |  |
| `ApprovedForReport` | bool | ✔ | system |  | ✔ | Default `FALSE`. Derived from ReviewerDecision = Approved. Only human-approved evidence may appear in an official report (D-06). |
| `ReportSequence` | int |  | user |  | ✔ |  |
| `DerivedFileKey` | filekey |  | system |  |  | Report-ready or downscaled derivative, stored SEPARATELY from the original (D-13). |
| `ClassificationCode` | enum `DataClassificationCode` | ✔ | system |  |  | Default `ClientConfidential`. Drives residency and sharing decisions (D-12). |
| `EntityVersion` | int | ✔ | system |  |  | Default `1`. Incremented on every material change. Referenced by Approvals. |
| `ContentHash` | checksum | ✔ | system |  |  | SHA-256 over the canonical serialisation of the fields listed in content_hash_fields. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> Advisory AI fields are deliberately excluded from ContentHash: an AI observation arriving later must not void a human approval (C-06).

## Snags

Defects and observations tracked to closure with evidence.

*الملاحظات وعدم المطابقات*

**Primary key:** `SnagID` · **Category:** operational · **Scope:** project · **Sensitivity:** confidential · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `SnagID` | id | ✔ |  |  |  | **PK.** Example: `SNG-H4L8R2` |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  |  |
| `LocationID` | ref → `Locations.LocationID` | ✔ | user |  |  |  |
| `VisitID` | ref → `SiteVisits.VisitID` |  | system |  |  |  |
| `VisitActivityID` | ref → `VisitActivities.VisitActivityID` |  | system |  |  |  |
| `SourcePhotoID` | ref → `Photos.PhotoID` |  | user |  |  |  |
| `Category` | text | ✔ | user |  |  |  |
| `Severity` | enum `SnagSeverity` | ✔ | user |  |  |  |
| `DescriptionEN` | longtext | ✔ | user |  |  |  |
| `DescriptionAR` | longtext |  | user |  |  |  |
| `RaisedAt` | datetime | ✔ | system |  |  |  |
| `RaisedBy` | ref → `Users.UserID` | ✔ | system |  |  |  |
| `ResponsibleParty` | text |  | user |  |  |  |
| `TargetDate` | date |  | user |  |  |  |
| `Status` | enum `SnagStatus` | ✔ | user |  |  | Default `Open`. |
| `ClosureDate` | date |  | user |  |  | Required when Status = Closed. |
| `ClosureEvidencePhotoID` | ref → `Photos.PhotoID` |  | user |  |  | Required when Status = Closed. A snag cannot be closed on assertion alone. |
| `VerifiedBy` | ref → `Users.UserID` |  | system |  |  | Required when Status = Closed. |
| `VerificationDate` | date |  | system |  |  |  |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## DocumentJobs

A request to produce a document from a frozen snapshot of approved records.

*مهام إنشاء المستندات*

**Primary key:** `JobID` · **Category:** document · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `JobID` | id | ✔ |  |  |  | **PK.** Example: `JOB-S4M7B1` |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | user |  |  |  |
| `LegalEntityID` | ref → `LegalEntities.LegalEntityID` | ✔ | system |  |  |  |
| `DocumentTypeCode` | enum `DocumentTypeCode` | ✔ | user |  |  |  |
| `LanguageCode` | enum `Language` | ✔ | user |  |  | Default `en`. |
| `PeriodStart` | date | ✔ | user |  |  |  |
| `PeriodEnd` | date | ✔ | user |  |  | Must be >= PeriodStart. |
| `RequestedBy` | ref → `Users.UserID` | ✔ | system |  |  | Must hold MayRequestDocuments on ProjectID. |
| `RequestedAt` | datetime | ✔ | system |  |  |  |
| `InputValidationStatus` | text | ✔ | system |  |  | Default `NotRun`. NotRun\|Passed\|Failed. |
| `InputValidationFindings` | json |  | system |  |  | Explicit DATA GAP items rather than silent omissions. |
| `SnapshotManifest` | json |  | system |  |  | Frozen list of included record IDs with their EntityVersion and ContentHash. Later edits cannot silently alter a draft (spec 8 scenario 05). |
| `SnapshotFrozenAt` | datetime |  | system |  |  |  |
| `WorkflowStatus` | enum `JobStatus` | ✔ | system |  |  | Default `Requested`. |
| `AIModel` | text |  | system |  |  |  |
| `PromptVersion` | text |  | system |  |  |  |
| `ReservedNumberID` | ref → `NumberRegister.NumberID` |  | system |  |  | A number reserved for this job; cancelled if the job fails (D-10). |
| `StartedAt` | datetime |  | system |  |  |  |
| `FinishedAt` | datetime |  | system |  |  |  |
| `ErrorClass` | enum `FailureClass` |  | system |  |  |  |
| `ErrorMessage` | longtext |  | system |  |  | Sanitised. Never contains a secret. |
| `RetryCount` | int | ✔ | system |  |  | Default `0`. |
| `CorrelationID` | text | ✔ | system |  |  |  |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Documents

A produced document revision. Approval binds to ContentHash (ADR-0006).

*المستندات المنتجة*

**Primary key:** `DocumentID` · **Category:** document · **Scope:** project · **Sensitivity:** confidential · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `DocumentID` | id | ✔ |  |  |  | **PK.** Example: `DOC-Y2R5T9` |
| `JobID` | ref → `DocumentJobs.JobID` | ✔ | system |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  |  |
| `LegalEntityID` | ref → `LegalEntities.LegalEntityID` | ✔ | system |  |  |  |
| `DocumentTypeCode` | enum `DocumentTypeCode` | ✔ | system |  |  |  |
| `TemplateID` | ref → `DocumentTemplates.TemplateID` | ✔ | system |  |  |  |
| `LanguageCode` | enum `Language` | ✔ | system |  |  |  |
| `DocumentNumber` | text |  | system |  |  | **Unique.** Issued by the numbering service at creation (D-10). |
| `VersionNumber` | int | ✔ | system |  |  | Default `1`. |
| `RevisionLabel` | text |  | system |  |  | Example: `Rev.0` |
| `DraftFileKey` | filekey |  | system |  |  |  |
| `PDFFileKey` | filekey |  | system |  |  |  |
| `ContentHash` | checksum | ✔ | system |  |  | Recomputed and compared before any release, posting or send. |
| `TechnicalApprovalStatus` | text | ✔ | system |  |  | Default `Pending`. Pending\|Approved\|Rejected\|Void. |
| `FinancialApprovalStatus` | text | ✔ | system |  |  | Default `NotRequired`. NotRequired\|Pending\|Approved\|Rejected\|Void. |
| `ReleaseStatus` | enum `DocumentStatus` | ✔ | system |  |  | Default `Draft`. |
| `ReleasedAt` | datetime |  | system |  |  |  |
| `ReleasedBy` | ref → `Users.UserID` |  | system |  |  |  |
| `RecipientSnapshot` | json |  | system |  |  | Authorised recipients as they were AT RELEASE. Later contact edits cannot rewrite history. |
| `SupersedesDocumentID` | ref → `Documents.DocumentID` |  | system |  |  |  |
| `ClassificationCode` | enum `DataClassificationCode` | ✔ | system |  |  | Default `ClientConfidential`. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## NumberRegister

Every number ever reserved, issued or cancelled. A cancelled number is never reused (D-10).

*سجل أرقام المستندات*

**Primary key:** `NumberID` · **Category:** document · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 5

**Unique together:** `SeriesID`, `YearKey`, `ScopeKey`, `SequenceValue`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `NumberID` | id | ✔ |  |  |  | **PK.** Example: `NUM-J7V3F4` |
| `SeriesID` | ref → `NumberingSeries.SeriesID` | ✔ | system |  |  |  |
| `SequenceValue` | int | ✔ | system |  |  |  |
| `FormattedNumber` | text | ✔ | system |  |  | **Unique.** Example: `{ENTITY}-TR-2026-001 (illustrative)` |
| `YearKey` | text | ✔ | system |  |  | Example: `2026` |
| `ScopeKey` | text | ✔ | system |  |  | Partition key: company-wide, project or client, per the series configuration. |
| `State` | enum `NumberState` | ✔ | system |  |  | Default `Reserved`. |
| `ReservedForJobID` | ref → `DocumentJobs.JobID` |  | system |  |  |  |
| `IssuedToDocumentID` | ref → `Documents.DocumentID` |  | system |  |  |  |
| `ReservedAt` | datetime | ✔ | system |  |  |  |
| `IssuedAt` | datetime |  | system |  |  |  |
| `CancelledAt` | datetime |  | system |  |  |  |
| `CancellationReason` | text |  | system |  |  | Required when State = Cancelled. A gap in the register must always be explainable. |
| `MigratedFromManual` | bool | ✔ | system |  |  | Default `FALSE`. TRUE for numbers imported from the existing manual register. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Approvals

Every approval decision, bound to the exact content approved (ADR-0006, D-09).

*قرارات الاعتماد*

**Primary key:** `ApprovalID` · **Category:** control · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ApprovalID` | id | ✔ |  |  |  | **PK.** Example: `APR-B5X8N2` |
| `EntityType` | text | ✔ | system |  |  | Table name. |
| `EntityID` | text | ✔ | system |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` |  | system |  |  | Carried for row-level security even on control records. |
| `ApprovalStage` | enum `ApprovalStage` | ✔ | system |  |  |  |
| `SequenceNumber` | int | ✔ | system |  |  | Default `1`. |
| `RequestedFromUserID` | ref → `Users.UserID` | ✔ | system |  |  | The ACCOUNTABLE approver from the approval matrix. |
| `RequestedAt` | datetime | ✔ | system |  |  |  |
| `Decision` | enum `ApprovalDecision` | ✔ | user |  |  | Default `Pending`. |
| `DecisionAt` | datetime |  | system |  |  |  |
| `DecisionByUserID` | ref → `Users.UserID` |  | system |  |  | The ACTING user. Differs from RequestedFromUserID only under a valid delegation. |
| `DelegationID` | ref → `ApprovalDelegations.DelegationID` |  | system |  |  | Required when DecisionByUserID != RequestedFromUserID. |
| `Comment` | longtext |  | user |  |  |  |
| `EntityVersion` | int | ✔ | system |  |  |  |
| `ContentHash` | checksum | ✔ | system |  |  | The approval applies to THIS hash only. A change voids it and everything downstream. |
| `VoidedAt` | datetime |  | system |  |  |  |
| `VoidReason` | text |  | system |  |  |  |
| `IsOverride` | bool | ✔ | system |  |  | Default `FALSE`. An override is recorded AS an override, with a reason. Never silent (SEC-05). |
| `OverrideReason` | longtext |  | user |  |  | Required when IsOverride. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> Self-approval of a restricted transaction is rejected even when the approver is unavailable; the correct path is a recorded delegation (D-09).

## EntityVersions

Immutable version history of hashable entities. Supports proving what a decision applied to.

*سجل نسخ السجلات*

**Primary key:** `VersionID` · **Category:** control · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

**Unique together:** `EntityType`, `EntityID`, `VersionNumber`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `VersionID` | id | ✔ |  |  |  | **PK.** Example: `VER-K1G6D7` |
| `EntityType` | text | ✔ | system |  |  |  |
| `EntityID` | text | ✔ | system |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` |  | system |  |  |  |
| `VersionNumber` | int | ✔ | system |  |  |  |
| `ContentHash` | checksum | ✔ | system |  |  |  |
| `CanonicalFieldSetVersion` | text | ✔ | system |  |  | Which canonical field list produced this hash. Changing the list is a migration. |
| `ChangedByUserID` | ref → `Users.UserID` | ✔ | system |  |  |  |
| `ChangedAt` | datetime | ✔ | system |  |  |  |
| `ChangeSummary` | text |  | system |  |  | Which hashed fields changed. Never the full payload. |
| `InvalidatedApprovalIDs` | text |  | system |  |  | Approvals voided by this change, recorded at the moment it happened. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## AuditLog

Append-only record of every state transition and every consequential action.

*سجل التدقيق*

**Primary key:** `AuditID` · **Category:** control · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `AuditID` | id | ✔ |  |  |  | **PK.** Example: `AUD-P9C4L3` |
| `TimestampUTC` | datetime | ✔ | system |  |  |  |
| `UserOrService` | text | ✔ | system |  |  |  |
| `Action` | text | ✔ | system |  |  | Example: `SiteVisit.Submit` |
| `EntityType` | text | ✔ | system |  |  |  |
| `EntityID` | text | ✔ | system |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` |  | system |  |  |  |
| `BeforeHash` | checksum |  | system |  |  |  |
| `AfterHash` | checksum |  | system |  |  |  |
| `SourceIPOrDevice` | text |  | system |  |  | Where available. Not fabricated. |
| `CorrelationID` | text |  | system |  |  |  |
| `Result` | text | ✔ | system |  |  | Success\|Failure\|Denied. |
| `Reason` | text |  | system |  |  |  |

> Append-only. No update or delete path exists for any role, including every kind of administrator and break-glass access.
> Never stores an access token, a credential or a full sensitive payload.

## IntegrationJobs

One row per external call attempt, with idempotency and failure classification.

*سجل عمليات التكامل الخارجي*

**Primary key:** `IntegrationJobID` · **Category:** control · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 3

**Unique together:** `IdempotencyKey`, `AttemptNumber`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `IntegrationJobID` | id | ✔ |  |  |  | **PK.** Example: `INT-T6Z2W8` |
| `SystemName` | text | ✔ | system |  |  | Example: `Drive` |
| `OperationName` | text | ✔ | system |  |  |  |
| `IdempotencyKey` | text | ✔ | system |  |  | {Scenario}:{EntityType}:{EntityID}:{TargetState}. Claimed BEFORE any side effect. |
| `CorrelationID` | text | ✔ | system |  |  |  |
| `EntityType` | text | ✔ | system |  |  |  |
| `EntityID` | text | ✔ | system |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` |  | system |  |  |  |
| `AttemptNumber` | int | ✔ | system |  |  | Default `1`. |
| `StartedAt` | datetime | ✔ | system |  |  |  |
| `FinishedAt` | datetime |  | system |  |  |  |
| `Status` | enum `IntegrationStatus` | ✔ | system |  |  | Default `Pending`. |
| `SanitizedRequestSummary` | text |  | system |  |  | Summary only. Never a payload, a credential or a token. |
| `SanitizedResponseSummary` | text |  | system |  |  |  |
| `ErrorClass` | enum `FailureClass` |  | system |  |  |  |
| `ErrorCode` | text |  | system |  |  |  |
| `RetryAfter` | datetime |  | system |  |  |  |
| `IsRetriable` | bool | ✔ | system |  |  | Default `FALSE`. Derived from ErrorClass. Validation and authorisation failures are never retried. |

## TemporaryAccessGrants

Time-bound, explicitly authorised access. Covers auditor access and break-glass emergency access. Without an active grant, the roles that depend on one resolve to no access at all.

*صلاحيات وصول مؤقتة ومحددة بزمن*

**Primary key:** `GrantID` · **Category:** control · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `GrantID` | id | ✔ |  |  |  | **PK.** Example: `TAG-P4K9M2` |
| `GrantKind` | text | ✔ | user |  |  | Audit\|Emergency\|Support. Audit: a time-bound review. Emergency: break-glass. Support: a bounded investigation by an administrator into their own technical scope. |
| `UserID` | ref → `Users.UserID` | ✔ | user |  |  | The individual receiving the grant. A grant is never issued to a shared account. |
| `RoleID` | ref → `Roles.RoleID` | ✔ | user |  |  | The role the grant activates. It can never exceed that role's own matrix. |
| `Scope` | text | ✔ | user |  |  | AllProjects\|SpecificProjects\|TechnicalOnly. TechnicalOnly is the break-glass default: administrative capability, no business content. |
| `ProjectIDs` | text |  | user |  |  | Semicolon-separated, required when Scope = SpecificProjects. |
| `Reason` | longtext | ✔ | user |  |  | MANDATORY. A grant without a stated reason is refused, for every kind. |
| `RequestedByUserID` | ref → `Users.UserID` | ✔ | user |  |  |  |
| `RequestedAt` | datetime | ✔ | system |  |  |  |
| `AuthorisedByUserID` | ref → `Users.UserID` | ✔ | user |  |  | Must be someone other than the recipient. Self-authorisation is refused. |
| `AuthorisedAt` | datetime | ✔ | system |  |  |  |
| `ValidFrom` | datetime | ✔ | user |  |  |  |
| `ValidTo` | datetime | ✔ | user |  |  | Mandatory, after ValidFrom, and within MaxDurationHours. MANDATORY. No grant is open-ended, for any kind. |
| `MaxDurationHours` | int | ✔ | config |  |  | Default `24`. Emergency grants default to 24 hours; audit grants may be configured longer. The ceiling is configuration, never absent. |
| `NotificationRecipients` | text | ✔ | config |  |  | MANDATORY for Emergency. Who was told that break-glass was used. |
| `NotificationSentAt` | datetime |  | system |  |  | Required for GrantKind = Emergency before the grant becomes usable. A break-glass grant that nobody was told about is not break-glass, it is a back door. |
| `AuditReference` | text |  | system |  |  | Correlation identifier linking every action taken under this grant to the audit log. |
| `UsageCount` | int | ✔ | system |  |  | Default `0`. How many times the grant was actually exercised. Zero is worth reviewing too. |
| `RevokedAt` | datetime |  | user |  |  |  |
| `RevokedByUserID` | ref → `Users.UserID` |  | user |  |  |  |
| `ReviewedAt` | datetime |  | user |  |  | Post-use review. Every exercised emergency grant is reviewed after the fact. |
| `ReviewedByUserID` | ref → `Users.UserID` |  | user |  |  |  |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> A grant is evidence. It is revoked, expired or reviewed, and never deleted.
> Actions performed under a grant are tagged with the GrantID in the audit log, so 'what did break-glass actually do' is answerable.

## SystemRecoveryPlan

How administrative control is recovered when no administrator is available. The system must not become unrecoverable because one person is unreachable.

*خطة استعادة السيطرة الإدارية*

**Primary key:** `PlanID` · **Category:** control · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 1–2 (MVP core)

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `PlanID` | id | ✔ |  |  |  | **PK.** Example: `SRP-B7T2X5` |
| `PrimaryAdministratorUserID` | ref → `Users.UserID` |  | user |  |  | Left unassigned until the owner names a person. |
| `BackupAdministratorUserID` | ref → `Users.UserID` |  | user |  |  | The simplest recovery route: a second administrator-capable account. |
| `RecoveryRouteDocumented` | bool | ✔ | user |  |  | Default `FALSE`. TRUE when a written recovery procedure exists and has been located by someone other than the administrator. |
| `RecoveryRouteReference` | text |  | user |  |  | Required when RecoveryRouteDocumented is TRUE. Where the procedure lives. No credential, and no location of a credential. |
| `BreakGlassAccountConfigured` | bool | ✔ | user |  |  | Default `FALSE`. Whether an emergency account exists that can be activated by a grant. |
| `OwnerCanAuthoriseBreakGlass` | bool | ✔ | config |  |  | Default `TRUE`. The system owner can always authorise a break-glass grant. |
| `LastTestedAt` | date |  | user |  |  | An untested recovery route is a hope, not a control. |
| `TestedByUserID` | ref → `Users.UserID` |  | user |  |  |  |
| `TestResult` | text |  | user |  |  | Passed\|Failed\|NotTested. |
| `GoLiveBlocker` | bool | ✔ | system |  |  | Default `TRUE`. Stays TRUE until either a backup administrator exists or a documented recovery route exists. Go-live is blocked while it is TRUE. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> This table holds no credential and no instruction for obtaining one. It records WHETHER a route exists and whether it has been tested.

## Contracts

Commercial agreement governing a project. Hidden from field roles entirely.

*العقود*

**Primary key:** `ContractID` · **Category:** financial · **Scope:** project · **Sensitivity:** financial · **Built in:** Phase 6

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `ContractID` | id | ✔ |  |  |  | **PK.** Example: `CNT-W2Y7P4` |
| `LegalEntityID` | ref → `LegalEntities.LegalEntityID` | ✔ | user |  |  |  |
| `ClientID` | ref → `Clients.ClientID` | ✔ | user |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` |  | user |  |  |  |
| `ContractNumber` | text | ✔ | user |  |  | **Unique.** |
| `EffectiveDate` | date | ✔ | user |  |  |  |
| `ExpiryDate` | date |  | user |  |  |  |
| `Currency` | text | ✔ | user |  |  | ISO 4217; must match the project currency. |
| `PaymentTermsDays` | int | ✔ | user |  |  |  |
| `RetentionPercent` | decimal(4) |  | user |  |  |  |
| `AdvanceAmount` | decimal(3) |  | user |  |  |  |
| `AdvanceRecoveryPercent` | decimal(4) |  | user |  |  |  |
| `TaxRuleID` | ref → `TaxRules.TaxRuleID` |  | user |  |  | The rule AND its version are preserved on every calculation (D-08). |
| `BillingFrequency` | enum `ReportingFrequency` |  | user |  |  |  |
| `BillingMethod` | enum `BillingMethod` | ✔ | user |  |  |  |
| `ContractValue` | decimal(3) |  | user |  |  |  |
| `Status` | text | ✔ | user |  |  | Default `Draft`. Draft\|Active\|Suspended\|Completed\|Terminated. |
| `Version` | int | ✔ | system |  |  | Default `1`. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## WorkOrders

A discrete instruction under a contract, or a one-off job.

*أوامر العمل*

**Primary key:** `WorkOrderID` · **Category:** financial · **Scope:** project · **Sensitivity:** financial · **Built in:** Phase 6

**Unique together:** `ProjectID`, `WorkOrderNumber`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `WorkOrderID` | id | ✔ |  |  |  | **PK.** Example: `WO-H3N7Q5` |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | user |  |  |  |
| `ContractID` | ref → `Contracts.ContractID` |  | user |  |  |  |
| `WorkOrderNumber` | text | ✔ | user |  |  |  |
| `DescriptionEN` | longtext | ✔ | user |  |  |  |
| `DescriptionAR` | longtext |  | user |  |  |  |
| `IssuedDate` | date | ✔ | user |  |  |  |
| `TargetCompletionDate` | date |  | user |  |  |  |
| `Status` | text | ✔ | user |  |  | Default `Open`. Open\|InProgress\|Completed\|Cancelled. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## BOQItems

Bill of quantities. Cumulative quantity is controlled, never merely recorded.

*بنود جدول الكميات*

**Primary key:** `BOQItemID` · **Category:** financial · **Scope:** project · **Sensitivity:** financial · **Built in:** Phase 6

**Unique together:** `ContractID`, `ItemNumber`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `BOQItemID` | id | ✔ |  |  |  | **PK.** Example: `BOQ-M2D9S6` |
| `ContractID` | ref → `Contracts.ContractID` | ✔ | user |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  |  |
| `ItemNumber` | text | ✔ | user |  |  |  |
| `DescriptionEN` | longtext | ✔ | user |  |  |  |
| `DescriptionAR` | longtext |  | user |  |  |  |
| `UnitID` | ref → `Units.UnitID` | ✔ | user |  |  |  |
| `ContractQuantity` | decimal(3) | ✔ | user |  |  | >= 0. |
| `UnitRate` | decimal(3) | ✔ | user |  |  | >= 0. |
| `ApprovedVariationQuantity` | decimal(3) | ✔ | user |  |  | Default `0`. |
| `PreviouslyCertifiedQuantity` | decimal(3) | ✔ | system |  |  | Default `0`. |
| `CurrentQuantity` | decimal(3) | ✔ | system |  |  | Default `0`. |
| `CumulativeQuantity` | decimal(3) | ✔ | system |  |  | Default `0`. Computed. Must not exceed ContractQuantity + ApprovedVariationQuantity without a recorded authorised override (spec 5.17). |
| `RemainingQuantity` | decimal(3) | ✔ | system |  |  | Default `0`. Computed. |
| `QuickBooksItemID` | text |  | integration |  |  | Immutable accounting item identifier. Never name-matched. |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## InvoiceRequests

A calculated billing request. Drafts only until Phase 7; never posted from Phase 1 or 6.

*طلبات إصدار الفواتير*

**Primary key:** `InvoiceRequestID` · **Category:** financial · **Scope:** project · **Sensitivity:** financial · **Built in:** Phase 6

**Unique together:** `ClientID`, `ProjectID`, `ContractID`, `BillingPeriodStart`, `BillingPeriodEnd`, `SourceDocumentID`

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `InvoiceRequestID` | id | ✔ |  |  |  | **PK.** Example: `INV-R8F1V4` |
| `LegalEntityID` | ref → `LegalEntities.LegalEntityID` | ✔ | system |  |  |  |
| `ClientID` | ref → `Clients.ClientID` | ✔ | system |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  |  |
| `ContractID` | ref → `Contracts.ContractID` | ✔ | system |  |  |  |
| `BillingPeriodStart` | date | ✔ | user |  |  |  |
| `BillingPeriodEnd` | date | ✔ | user |  |  |  |
| `Currency` | text | ✔ | system |  |  | From the contract. A mismatch anywhere is a validation failure (C-09). |
| `PaymentTermsDays` | int | ✔ | system |  |  |  |
| `InvoiceDate` | date |  | user |  |  |  |
| `DueDate` | date |  | system |  |  | InvoiceDate + PaymentTermsDays, per contract. |
| `TaxRuleID` | ref → `TaxRules.TaxRuleID` |  | system |  |  |  |
| `TaxRuleVersion` | int |  | system |  |  | The version applied, preserved forever (D-08). |
| `Subtotal` | decimal(3) | ✔ | calculation |  |  | Default `0`. |
| `Discount` | decimal(3) | ✔ | calculation |  |  | Default `0`. |
| `TaxAmount` | decimal(3) | ✔ | calculation |  |  | Default `0`. |
| `RetentionAmount` | decimal(3) | ✔ | calculation |  |  | Default `0`. |
| `AdvanceRecovery` | decimal(3) | ✔ | calculation |  |  | Default `0`. |
| `NetPayable` | decimal(3) | ✔ | calculation |  |  | Default `0`. |
| `CalculationTrace` | json |  | calculation |  |  | Ordered record of every step and rounding decision, reproducible from stored inputs. |
| `SourceDocumentID` | ref → `Documents.DocumentID` |  | system |  |  | The completion certificate or report this billing derives from. |
| `FinanceStatus` | enum `InvoiceFinanceStatus` | ✔ | system |  |  | Default `Draft`. |
| `QuickBooksStatus` | enum `QuickBooksSyncStatus` | ✔ | system |  |  | Default `NotSent`. Production posting is unreachable until QBO_POSTING_ENABLED is set by written authorisation (ADR-0008). |
| `QuickBooksInvoiceID` | text |  | integration |  |  |  |
| `DraftInvoiceNumber` | text |  | system |  |  | Internal. Separate from the final accounting number (spec 11). |
| `FinalInvoiceNumber` | text |  | integration |  |  |  |
| `ContentHash` | checksum | ✔ | system |  |  |  |
| `EntityVersion` | int | ✔ | system |  |  | Default `1`. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> The unique key is the duplicate-billing control (spec 11).

## InvoiceLines

Calculated invoice lines. No figure originates from a language model (invariant I-4).

*بنود الفاتورة*

**Primary key:** `InvoiceLineID` · **Category:** financial · **Scope:** project · **Sensitivity:** financial · **Built in:** Phase 6

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `InvoiceLineID` | id | ✔ |  |  |  | **PK.** Example: `INL-C7J5K9` |
| `InvoiceRequestID` | ref → `InvoiceRequests.InvoiceRequestID` | ✔ | system |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  |  |
| `BOQItemID` | ref → `BOQItems.BOQItemID` |  | system |  |  |  |
| `LineNumber` | int | ✔ | system |  |  |  |
| `DescriptionEN` | longtext | ✔ | user |  |  | AI may draft this human-readable description and nothing else (spec 9.4). |
| `DescriptionAR` | longtext |  | user |  |  |  |
| `Quantity` | decimal(3) | ✔ | system |  |  |  |
| `UnitRate` | decimal(3) | ✔ | system |  |  |  |
| `LineAmount` | decimal(3) | ✔ | calculation |  |  | Computed, never entered. |
| `TaxCode` | text |  | system |  |  |  |
| `TaxAmount` | decimal(3) | ✔ | calculation |  |  | Default `0`. |
| `CostCenter` | text |  | user |  |  |  |
| `Class` | text |  | user |  |  | Maps to an accounting class where available. |
| `ProjectReference` | text |  | system |  |  |  |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Materials

Approved materials catalogue.

*كتالوج المواد*

**Primary key:** `MaterialID` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `MaterialID` | id | ✔ |  |  |  | **PK.** Example: `MAT-W4B2T1` |
| `ItemCode` | text | ✔ | config |  |  | **Unique.** |
| `DescriptionEN` | text | ✔ | config |  |  |  |
| `DescriptionAR` | text |  | config |  |  |  |
| `UnitID` | ref → `Units.UnitID` | ✔ | config |  |  |  |
| `ApprovedSpecification` | longtext |  | config |  |  |  |
| `ApprovedBrand` | text |  | config |  |  |  |
| `Supplier` | text |  | config |  |  |  |
| `QuickBooksItemID` | text |  | integration | financial |  |  |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## MaterialUsage

Material consumed against a visit activity. Never creates an accounting transaction (spec 5.12).

*استهلاك المواد*

**Primary key:** `MaterialUsageID` · **Category:** operational · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `MaterialUsageID` | id | ✔ |  |  |  | **PK.** Example: `MUS-G6L9P3` |
| `VisitActivityID` | ref → `VisitActivities.VisitActivityID` | ✔ | user |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  |  |
| `MaterialID` | ref → `Materials.MaterialID` | ✔ | user |  |  |  |
| `Quantity` | decimal(3) | ✔ | user |  |  | >= 0. |
| `UnitID` | ref → `Units.UnitID` | ✔ | user |  |  |  |
| `Remarks` | text |  | user |  |  |  |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Equipment

Equipment register.

*سجل المعدات*

**Primary key:** `EquipmentID` · **Category:** master · **Scope:** global · **Sensitivity:** internal · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `EquipmentID` | id | ✔ |  |  |  | **PK.** Example: `EQP-N1X7Z5` |
| `EquipmentCode` | text | ✔ | config |  |  | **Unique.** |
| `NameEN` | text | ✔ | config |  |  |  |
| `NameAR` | text |  | config |  |  |  |
| `Category` | text |  | config |  |  |  |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## VisitEquipment

Equipment present during a visit.

*المعدات المستخدمة في الزيارة*

**Primary key:** `VisitEquipmentID` · **Category:** operational · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `VisitEquipmentID` | id | ✔ |  |  |  | **PK.** Example: `VEQ-Q3S8M6` |
| `VisitID` | ref → `SiteVisits.VisitID` | ✔ | user |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  |  |
| `EquipmentID` | ref → `Equipment.EquipmentID` | ✔ | user |  |  |  |
| `Hours` | decimal(2) |  | user |  |  |  |
| `Remarks` | text |  | user |  |  |  |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

## Employees

Crew register for resource reporting. Payroll data is deliberately excluded (spec 5.13).

*سجل العمالة*

**Primary key:** `EmployeeID` · **Category:** master · **Scope:** global · **Sensitivity:** personal · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `EmployeeID` | id | ✔ |  |  |  | **PK.** Example: `EMP-F5D2H4` |
| `EmployeeCode` | text | ✔ | config |  |  | **Unique.** |
| `FullNameEN` | text | ✔ | config |  |  |  |
| `FullNameAR` | text |  | config |  |  |  |
| `TradeEN` | text |  | config |  |  |  |
| `TradeAR` | text |  | config |  |  |  |
| `CrewCode` | text |  | config |  |  |  |
| `IsActive` | bool | ✔ | user |  |  | Default `TRUE`. Soft delete. Rows are never hard-deleted; history is evidence. |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> No salary, rate, passport, visa or personal document field exists in this table.

## VisitManpower

Manpower present during a visit, for resource summaries only.

*العمالة في الزيارة*

**Primary key:** `VisitManpowerID` · **Category:** operational · **Scope:** project · **Sensitivity:** internal · **Built in:** Phase 5

| Column | Type | Req | Source | Sens | Hash | Validation / notes |
|---|---|---|---|---|---|---|
| `VisitManpowerID` | id | ✔ |  |  |  | **PK.** Example: `VMP-V9K1B7` |
| `VisitID` | ref → `SiteVisits.VisitID` | ✔ | user |  |  |  |
| `ProjectID` | ref → `Projects.ProjectID` | ✔ | system |  |  |  |
| `EmployeeID` | ref → `Employees.EmployeeID` |  | user |  |  |  |
| `TradeEN` | text |  | user |  |  |  |
| `TradeAR` | text |  | user |  |  |  |
| `HeadCount` | int |  | user |  |  | >= 0. |
| `Hours` | decimal(2) |  | user |  |  |  |
| `CreatedAt` | datetime | ✔ | system |  |  | UTC. Set once on insert. |
| `CreatedBy` | email | ✔ | system |  |  | USEREMAIL() or the service identity. |
| `UpdatedAt` | datetime | ✔ | system |  |  | UTC. Excluded from ContentHash. |
| `UpdatedBy` | email | ✔ | system |  |  |  |

> Never exposes payroll detail to field roles.

---

## Controlled vocabularies

### Language

Interface and document languages supported from Phase 1 (D-11).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `en` | English | الإنجليزية | Left-to-right. First generated-report language. |
| `ar` | Arabic | العربية | Right-to-left. Capability is architectural from Phase 1. |

### ProjectStatus

Lifecycle of a project. Adding or activating a project is configuration only (D-01).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Draft` | Draft | مسودة | Being configured. Not visible to field users. |
| `Active` | Active | نشط | Accepting site visits. |
| `Suspended` | Suspended | موقوف | No new visits; existing records remain readable. |
| `Completed` | Completed | منجز | Work finished; reporting may continue until closeout. |
| `Archived` | Archived | مؤرشف | Read-only. Retained per the residency and retention rules. |

### ReportingFrequency

Per-project reporting cadence.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Daily` | Daily | يومي |  |
| `Weekly` | Weekly | أسبوعي |  |
| `Monthly` | Monthly | شهري | MVP default. |
| `Quarterly` | Quarterly | ربع سنوي |  |
| `OnCompletion` | On completion | عند الإنجاز | One-off work orders. |
| `OnDemand` | On demand | عند الطلب |  |

### BillingMethod

How a project is billed. Configuration, never logic.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `MonthlyFixed` | Monthly fixed | مقطوع شهري | Recurring maintenance contract. |
| `MeasuredBOQ` | Measured against BOQ | بالكميات المنفذة | Quantities certified per period. |
| `LumpSumMilestone` | Lump sum by milestone | مقطوع بالمراحل |  |
| `OnCompletion` | On completion | عند الإنجاز | One-off work order. |
| `TimeAndMaterial` | Time and material | بالوقت والمواد |  |

### WorkflowStatus

SiteVisit lifecycle. Transitions are restricted (see transitions).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Draft` | Draft | مسودة | Editable by the submitter. Not visible to reviewers. |
| `Submitted` | Submitted | مُرسل | Handed to server-side validation. |
| `ValidationFailed` | Validation failed | فشل التحقق | Specific correctable errors recorded. |
| `UnderTechnicalReview` | Under technical review | قيد المراجعة الفنية | In a reviewer queue. |
| `CorrectionRequired` | Correction required | يتطلب تصحيح | Returned to the submitter with a reason. |
| `TechnicallyApproved` | Technically approved | معتمد فنياً | Evidence may now be used in a report. |
| `ReadyForReport` | Ready for report | جاهز للتقرير | Eligible for a document job snapshot. |
| `IncludedInDraft` | Included in draft | مُدرج في مسودة | Frozen into at least one document snapshot. |
| `Released` | Released | صادر | Part of a released document. |
| `Archived` | Archived | مؤرشف | Read-only. |
| `Cancelled` | Cancelled | ملغي | Cancelled with a recorded reason. Never deleted. |

### VisitActivityStatus

Activity-level lifecycle inside a visit.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Draft` | Draft | مسودة |  |
| `Submitted` | Submitted | مُرسل |  |
| `UnderReview` | Under review | قيد المراجعة |  |
| `Approved` | Approved | معتمد | Approved by the technical reviewer. |
| `Rejected` | Rejected | مرفوض | Excluded from reporting, retained as a record. |
| `CorrectionRequired` | Correction required | يتطلب تصحيح |  |
| `Cancelled` | Cancelled | ملغي |  |

### EvidenceStage

What a photograph is evidence of (spec 5.10).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Before` | Before | قبل |  |
| `During` | During | أثناء |  |
| `After` | After | بعد |  |
| `Observation` | Observation | ملاحظة | Caption mandatory. |
| `Snag` | Snag | ملاحظة عدم مطابقة | Caption mandatory. |
| `Material` | Material | مواد | Caption mandatory. |
| `Equipment` | Equipment | معدات |  |
| `Safety` | Safety | السلامة | Caption mandatory. |
| `Other` | Other | أخرى |  |

### CaptureMode

How a submission reaches the main-contractor group (D-16).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `QuickShare` | Quick share | مشاركة فورية | Capture, store, then open the native share sheet immediately. AI analysis runs afterwards and prepares the internal report metadata. |
| `AIReviewedShare` | AI reviewed share | مشاركة بعد المراجعة | Capture, AI proposal, supervisor confirmation, then the native share sheet. |

### ShareStatus

Outcome of the native share action. Never set by AI (D-16).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `NotShared` | Not shared | لم تتم المشاركة | Default. |
| `ShareInitiated` | Share initiated | بدأت المشاركة | The share sheet was opened. The system cannot observe what happened inside it. |
| `ShareConfirmed` | Share confirmed | تم تأكيد المشاركة | The supervisor confirmed the share completed. A human claim, not a platform receipt. |
| `ShareCancelled` | Share cancelled | أُلغيت المشاركة | Recoverable; the evidence is retained. |
| `ShareFailed` | Share failed | فشلت المشاركة | Recoverable. Re-sharing must never require re-selecting the images (CAP-01). |

### AIProposalDisposition

What the supervisor did with the AI proposal (D-17).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `NotOffered` | Not offered | لم تُعرض | Quick Share, or analysis not yet complete. |
| `Accepted` | Accepted | مقبول | Confirmed unchanged. Still a human decision. |
| `Corrected` | Corrected | مُصحح | The supervisor changed one or more proposed values. |
| `Rejected` | Rejected | مرفوض | The proposal was discarded entirely. |

### ClassificationStatus

How far a photograph's activity classification has got (D-23). Pending is a normal, non-blocking state.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Pending` | Pending | قيد الانتظار | Captured, not yet classified. The normal state immediately after a Quick Share. |
| `AIProposed` | AI proposed | اقتراح من الذكاء الاصطناعي | An advisory proposal exists. **Still untrusted.** No report or business rule may use it. |
| `Confirmed` | Confirmed | مؤكد | A supervisor or reviewer set ConfirmedActivityTypeID. The only trusted state. |
| `NotApplicable` | Not applicable | لا ينطبق | The photograph carries no activity to classify — a safety observation, a material delivery. |
| `Excluded` | Excluded | مستبعد | Deliberately left out: a duplicate, an unusable image, or evidence excluded from this report. |

### AnalysisEligibility

Whether a photograph is worth sending to analysis (D-24). Filtering happens before the call, never after it.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Eligible` | Eligible | مؤهل | Analysis has value and has not run. |
| `Analysed` | Analysed | تم التحليل | Already analysed. Never analysed twice. |
| `SkippedDuplicate` | Skipped — duplicate | تم التخطي - مكرر | A near-identical photograph in the same batch was analysed instead. |
| `SkippedQuality` | Skipped — unusable | تم التخطي - جودة غير كافية | Blurred, dark or obstructed beyond usefulness. Retained as evidence, not analysed. |
| `SkippedExcluded` | Skipped — excluded | تم التخطي - مستبعد | Deleted or explicitly excluded by the supervisor before analysis ran. |
| `SkippedDisabled` | Skipped — analysis off | تم التخطي - التحليل متوقف | Analysis is switched off for this project, or the monthly cap is reached. |

### SiteNoteCategory

Why an optional site note was written (D-18). Facts a photograph cannot establish.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `ClientInstruction` | Client instruction | تعليمات العميل |  |
| `AccessRestriction` | Access restriction | قيود الدخول |  |
| `PermitIssue` | Permit issue | مشكلة تصريح |  |
| `HiddenDefect` | Hidden or underground defect | عيب مخفي أو تحت الأرض |  |
| `MeasuredQuantity` | Measured quantity | كمية مقاسة | Typed by a person. Never proposed by image analysis. |
| `MaterialQuantityOrBatch` | Material quantity or batch | كمية أو دفعة المواد |  |
| `EquipmentFailure` | Equipment failure | عطل معدات |  |
| `NonCompletionReason` | Reason for non-completion | سبب عدم الإنجاز |  |
| `SafetyRestriction` | Safety restriction | قيد يتعلق بالسلامة |  |
| `PostponedByOtherParty` | Work postponed by another party | تأجيل من طرف آخر |  |

### ReviewerDecision

Per-photograph reviewer decision. Only a human sets this (D-06).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Pending` | Pending | قيد الانتظار | Default. Never set by AI. |
| `Approved` | Approved | معتمد | May appear in an official report. |
| `Rejected` | Rejected | مرفوض | Retained as a record, excluded from reporting. |
| `Excluded` | Excluded | مستبعد | Valid evidence deliberately left out of this report. |

### AIAnalysisStatus

State of the advisory AI analysis for one photograph.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `NotRequested` | Not requested | لم يُطلب |  |
| `Queued` | Queued | في الطابور |  |
| `Completed` | Completed | مكتمل | Advisory observation stored. |
| `Failed` | Failed | فشل | Recorded with a failure class. Never blocks review. |
| `SchemaInvalid` | Schema invalid | مخرجات غير مطابقة | Response rejected before storage. |
| `Skipped` | Skipped | متخطى | Ineligible (for example a duplicate). |
| `Disabled` | Disabled for project | معطل للمشروع | Residency or contract rule (D-12). |

### SnagSeverity

Snag severity.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Low` | Low | منخفضة |  |
| `Medium` | Medium | متوسطة |  |
| `High` | High | عالية |  |
| `Critical` | Critical | حرجة |  |

### SnagStatus

Snag lifecycle.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Open` | Open | مفتوح |  |
| `Assigned` | Assigned | مُسند |  |
| `InProgress` | In progress | قيد التنفيذ |  |
| `PendingVerification` | Pending verification | بانتظار التحقق |  |
| `Closed` | Closed | مغلق | Requires closure evidence and a verifier. |
| `Rejected` | Rejected | مرفوض |  |
| `Deferred` | Deferred | مؤجل |  |

### DocumentTypeCode

Controlled document types. Each has its own numbering series (D-10).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `DailyReport` | Daily report | تقرير يومي |  |
| `WeeklyReport` | Weekly report | تقرير أسبوعي |  |
| `MonthlyTechnicalReport` | Monthly technical report | تقرير فني شهري | Only type produced in the MVP. |
| `InspectionReport` | Inspection report | تقرير معاينة |  |
| `CorrectiveActionReport` | Corrective action report | تقرير إجراء تصحيحي |  |
| `Quotation` | Quotation | عرض سعر |  |
| `CompletionCertificate` | Completion certificate | شهادة إنجاز |  |
| `InvoiceCover` | Invoice cover | غلاف فاتورة | Numbering aligned to the accounting process (D-10). |
| `Transmittal` | Transmittal | كتاب إحالة |  |

### JobStatus

DocumentJob lifecycle.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Requested` | Requested | مطلوب |  |
| `Validating` | Validating inputs | تحقق من المدخلات |  |
| `InputValidationFailed` | Input validation failed | فشل تحقق المدخلات | Specific gaps recorded. |
| `SnapshotFrozen` | Snapshot frozen | لقطة مجمدة | Included record IDs and versions fixed. |
| `Generating` | Generating | قيد الإنشاء |  |
| `Generated` | Generated | تم الإنشاء |  |
| `Failed` | Failed | فشل |  |
| `Cancelled` | Cancelled | ملغي | Any reserved number is cancelled, never reused (D-10). |

### DocumentStatus

Document lifecycle. Release is the only externally visible state.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Draft` | Draft | مسودة |  |
| `PendingTechnicalApproval` | Pending technical approval | بانتظار الاعتماد الفني |  |
| `TechnicallyApproved` | Technically approved | معتمد فنياً | Revision locked. |
| `RevisionRequired` | Revision required | يتطلب مراجعة | Content changed; approval void. |
| `PendingRelease` | Pending release | بانتظار الإصدار |  |
| `Released` | Released | صادر | Recipient snapshot recorded. |
| `Superseded` | Superseded | مُستبدل | Replaced by a later revision. |
| `Cancelled` | Cancelled | ملغي |  |

### ApprovalStage

Approval gates. Each is routed by the approval matrix (D-09).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `EvidenceReview` | Evidence review | مراجعة الأدلة | Visit and photograph level. |
| `TechnicalReview` | Technical review | المراجعة الفنية | Document level. |
| `FinanceReview` | Finance review | المراجعة المالية | Phase 6/7. |
| `Release` | Release | الإصدار | Authorises external delivery. |
| `OverrideAuthorisation` | Override authorisation | اعتماد استثناء | Recorded as an override, never silent. |

### ApprovalDecision

Recorded decision. Bound to EntityVersion and ContentHash (ADR-0006).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Pending` | Pending | قيد الانتظار |  |
| `Approved` | Approved | معتمد |  |
| `Rejected` | Rejected | مرفوض |  |
| `Delegated` | Delegated | مفوض | Acted by a delegate; original responsible user recorded. |
| `Withdrawn` | Withdrawn | مسحوب |  |
| `Void` | Void — content changed | لاغٍ لتغير المحتوى | ContentHash no longer matches. |

### NumberState

Document number lifecycle (D-10). A cancelled number is never reused.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Reserved` | Reserved | محجوز | Allocated atomically to a job before generation. |
| `Issued` | Issued | صادر | Bound to a created document. |
| `Cancelled` | Cancelled | ملغي | Job failed or abandoned. Recorded with a reason. |

### FailureClass

Failure taxonomy (spec 12). Determines whether a retry is permitted.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Validation` | Validation | تحقق | Never retried. |
| `Authentication` | Authentication | مصادقة | Never retried. Alert administrator. |
| `Authorization` | Authorization | تخويل | Never retried. Possible security event. |
| `RateLimit` | Rate limit | حد المعدل | Retriable with backoff. |
| `Network` | Network | شبكة | Retriable with backoff. |
| `ProviderUnavailable` | Provider unavailable | المزود غير متاح | Retriable with backoff. |
| `FileMissing` | File missing | ملف مفقود | One delayed retry; sync latency is normal. |
| `SchemaMismatch` | Schema mismatch | عدم تطابق المخطط | Never retried blindly. |
| `Duplicate` | Duplicate | مكرر | Suppressed and logged. Expected, not an error. |
| `Conflict` | Conflict | تعارض | Human resolution. Never auto-overwrite. |
| `Unknown` | Unknown | غير معروف | Dead-letter immediately. |

### IntegrationStatus

Outcome of one external call attempt.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Pending` | Pending | معلق |  |
| `InProgress` | In progress | قيد التنفيذ |  |
| `Succeeded` | Succeeded | نجح |  |
| `Failed` | Failed | فشل |  |
| `DeadLettered` | Dead lettered | في طابور المراجعة | Awaiting an operator. |
| `DuplicateSuppressed` | Duplicate suppressed | تم منع التكرار | Idempotency key already claimed. |

### InvoiceFinanceStatus

Finance lifecycle of an invoice request (Phase 6/7).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Draft` | Draft | مسودة | Calculated but not submitted for finance approval. |
| `PendingFinanceApproval` | Pending finance approval | بانتظار الاعتماد المالي |  |
| `FinanceApproved` | Finance approved | معتمد مالياً | Required before anything may reach the accounting system. |
| `Rejected` | Rejected | مرفوض | Returned with a reason; a new calculation is required. |
| `Void` | Void - inputs changed | لاغٍ لتغير المدخلات | The source content hash changed after approval. |

### QuickBooksSyncStatus

Accounting synchronisation lifecycle (Phase 7). Nothing here is reachable until the owner authorises production posting in writing.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `NotSent` | Not sent | لم يُرسل | Default. The invoice exists only inside this system. |
| `Queued` | Queued for sandbox | في الطابور للبيئة التجريبية | Awaiting a sandbox posting attempt. |
| `SandboxPosted` | Posted to sandbox | مُرحّل في البيئة التجريبية | Posted to a test company only. |
| `Reconciling` | Reconciling | قيد المطابقة | Reading back the posted document to compare totals. |
| `ReconciliationFailed` | Reconciliation failed | فشلت المطابقة | Totals differ. Never auto-corrected in either direction; a human resolves it. |
| `Posted` | Posted to production | مُرحّل للإنتاج | Requires written authorisation to enable. |
| `Failed` | Failed | فشل | Classified failure; retried only when the class is retriable. |

### DataClassificationCode

Sensitivity classes used to drive residency and sharing rules (D-12).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Public` | Public | عام |  |
| `Internal` | Internal | داخلي |  |
| `ClientConfidential` | Client confidential | سري للعميل | Default for photographic evidence. |
| `Personal` | Personal data | بيانات شخصية | Identifiable individuals. |
| `Financial` | Financial | مالي | Rates, invoices, accounting identifiers. |
| `GovernmentRestricted` | Government restricted | مقيد حكومياً | Contract-imposed handling. |

### ResidencyRuleCode

Storage and processing restrictions assignable per client, contract or project (D-12).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `NoRestriction` | No restriction | بدون قيود | Default until a contract says otherwise. |
| `RegionRestricted` | Region restricted | مقيد بالمنطقة | Named region only. |
| `CountryRestricted` | Country restricted | مقيد بالدولة | Named country only. |
| `NoThirdPartyAI` | No third-party AI processing | بدون معالجة ذكاء اصطناعي خارجية | Disables AI analysis for the project. |
| `NoCloudStorage` | No third-party cloud storage | بدون تخزين سحابي خارجي | Blocks production upload for the project. |

### DelegationScope

Breadth of a temporary approval delegation (D-09).

| Code | English | العربية | Meaning |
|---|---|---|---|
| `AllProjects` | All projects | كل المشاريع |  |
| `SpecificProjects` | Specific projects | مشاريع محددة |  |
| `SpecificStage` | Specific stage only | مرحلة محددة فقط |  |

### TaxTreatmentPlaceholder

Placeholder only. NO CLASSIFICATION IS NAMED OR ASSUMED (D-08). 'Zero-rated', 'exempt', 'out of scope' and 'no tax configured' are distinct and non-interchangeable; the real values come from the accountant in writing.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `PENDING_ACCOUNTANT_CONFIRMATION` | Pending accountant confirmation | بانتظار تأكيد المحاسب | The only value permitted in production before written confirmation. |
| `SYNTHETIC_TEST_ONLY` | Synthetic test value — not a tax position | قيمة اختبارية فقط وليست موقفاً ضريبياً | Exists solely so the arithmetic can be tested offline. It asserts nothing about any jurisdiction and must never appear in production data (D-08). |

### EvidenceRuleSource

Where an effective evidence rule came from.

| Code | English | العربية | Meaning |
|---|---|---|---|
| `Global` | Global activity type | نوع النشاط العام |  |
| `ProjectOverride` | Project override | تخصيص للمشروع | Project-specific rule wins. |
