# AppSheet Implementation Workbook

**Document ID:** AH-SYS-P2A-001 · **Revision:** 1 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-11 from `model/model.json` by `tools/gen_appsheet_workbook.py`

> **Nothing here is connected.** This is the specification an implementer follows in Phase 2,
> derived from the canonical model so the app cannot drift from the data foundation.
> Expressions are written in AppSheet's expression language and have **not** been executed
> on the platform — see `12-appsheet-feature-to-plan-matrix.md`, where the platform's
> capabilities remain UNVERIFIED.

## Workbook structure

One worksheet per table, named exactly as the table. Header row exactly as the column names
in the data dictionary. No formulas in cells: every derivation is an app formula or a
virtual column, so the store stays a store.

**28 worksheets** are built for the MVP application. The remaining
18 tables are designed and will be added in their own
phase without a migration, because their schemas already exist.

## Column conventions

| Convention | Rule |
|---|---|
| Key | The table's primary key column. `UNIQUEID()` as initial value, never editable |
| Label | The first bilingual name column, so references display readably |
| `Editable_If` | `FALSE` for every column whose source is system, integration, calculation or AI |
| `Required_If` | Mirrors the model's required flag, plus any conditional rule stated in the dictionary |
| `Valid_If` | Mirrors the model's validation and referential rules |
| Sensitivity | Columns marked financial or personal are omitted entirely from field-role slices, not merely hidden |

## LegalEntities

Registered legal entities that issue documents. Multi-entity from the start (D-02).

**Key:** `LegalEntityID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `LegalEntityID` | Text | Yes | No | `UNIQUEID()` initial value; key; not editable |
| `EntityCode` | Text | Yes | Yes | 2-6 uppercase letters/digits |
| `LegalNameEN` | Text | Yes | Yes |  |
| `LegalNameAR` | Text | Yes | Yes |  |
| `TradeNameEN` | Text |  | Yes |  |
| `TradeNameAR` | Text |  | Yes |  |
| `CommercialRegistrationNumber` | Text | Yes | Yes |  |
| `EstablishmentCardNumber` | Text |  | Yes |  |
| `TaxRegistrationNumber` | Text |  | Yes | **[financial]** |
| `TaxRegistrationStatus` | Text | Yes | Yes | Initial value `PENDING_ACCOUNTANT_CONFIRMATION` |
| `RegisteredAddressEN` | LongText | Yes | Yes |  |
| `RegisteredAddressAR` | LongText |  | Yes |  |
| `Country` | Text | Yes | Yes |  |
| `Currency` | Text | Yes | Yes | ISO 4217 |
| `OfficialEmail` | Email | Yes | Yes |  |
| `OfficialTelephone` | Phone | Yes | Yes |  |
| `OfficialWhatsApp` | Phone |  | Yes |  |
| `LogoFileKey` | Text |  | Yes |  |
| `DocumentFooterEN` | LongText |  | Yes |  |
| `DocumentFooterAR` | LongText |  | Yes |  |
| `AuthorisedSignatories` | LongText |  | Yes |  |
| `EffectiveFrom` | Date | Yes | Yes |  |
| `EffectiveTo` | Date |  | Yes |  |
| `Version` | Number | Yes | No | Initial value `1` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Languages

Supported languages and their direction. Bilingual capability is architectural (D-11).

**Key:** `LanguageCode` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `LanguageCode` | Enum (en, ar) | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `NameEN` | Text | Yes | Yes |  |
| `NameAR` | Text | Yes | Yes |  |
| `Direction` | Text | Yes | Yes | LTR\|RTL |
| `IsDocumentLanguage` | Yes/No | Yes | Yes |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Roles

System roles. Authorisation is enforced by security filters and server-side re-validation, never by view visibility (spec 7.4).

**Key:** `RoleID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `RoleID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `RoleCode` | Text | Yes | Yes |  |
| `NameEN` | Text | Yes | Yes |  |
| `NameAR` | Text | Yes | Yes |  |
| `Description` | LongText | Yes | Yes |  |
| `SeesFinancialData` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `MayApprove` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `MayAdministerMasterData` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Users

People who may sign in. One identity per person — shared accounts destroy attribution.

**Key:** `UserID` · **Scope:** global · **Sensitivity:** personal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `UserID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `Email` | Email | Yes | Yes |  |
| `FullNameEN` | Text | Yes | Yes |  |
| `FullNameAR` | Text |  | Yes |  |
| `Mobile` | Phone |  | Yes | **[personal]** |
| `RoleID` | Ref → Roles | Yes | Yes |  |
| `EmployeeID` | Text |  | Yes | **[personal]** |
| `DefaultProjectID` | Ref → Projects |  | Yes |  |
| `Language` | Enum (en, ar) | Yes | Yes | Initial value `en` |
| `LastLoginAt` | DateTime |  | No |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Units

Units of measure for quantities.

**Key:** `UnitID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `UnitID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `UnitCode` | Text | Yes | Yes |  |
| `NameEN` | Text | Yes | Yes |  |
| `NameAR` | Text | Yes | Yes |  |
| `DecimalPlaces` | Number | Yes | Yes | Initial value `2` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Disciplines

Work disciplines. A project may permit one or many.

**Key:** `DisciplineID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `DisciplineID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `DisciplineCode` | Text | Yes | Yes |  |
| `NameEN` | Text | Yes | Yes |  |
| `NameAR` | Text | Yes | Yes |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## ActivityTypes

Catalogue of activities with their default evidence and quantity rules. Per-project overrides live in ProjectActivityRules.

**Key:** `ActivityTypeID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ActivityTypeID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `DisciplineID` | Ref → Disciplines | Yes | Yes |  |
| `ActivityCode` | Text | Yes | Yes |  |
| `ActivityNameEN` | Text | Yes | Yes |  |
| `ActivityNameAR` | Text | Yes | Yes |  |
| `RequiresBeforePhoto` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `RequiresAfterPhoto` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `RequiresQuantity` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `QuantityUnitID` | Ref → Units |  | Yes | Required when RequiresQuantity is TRUE |
| `RequiresMaterial` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `RequiresSnagCheck` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `MinPhotos` | Number | Yes | Yes | Initial value `0` |
| `DefaultEvidenceStages` | Text |  | Yes |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## DocumentTypes

Controlled document types. Adding a type is configuration, not development (D-10).

**Key:** `DocumentTypeCode` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `DocumentTypeCode` | Enum (DailyReport, WeeklyReport, MonthlyTechnicalReport, InspectionReport…) | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `NameEN` | Text | Yes | Yes |  |
| `NameAR` | Text | Yes | Yes |  |
| `RequiresTechnicalApproval` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `RequiresFinanceApproval` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `RequiresReleaseApproval` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `IsExternallyIssued` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `BuiltInPhase` | Text | Yes | Yes |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## DataClassifications

Sensitivity classes applied to records and files, driving residency and sharing rules (D-12).

**Key:** `ClassificationCode` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ClassificationCode` | Enum (Public, Internal, ClientConfidential, Personal…) | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `NameEN` | Text | Yes | Yes |  |
| `NameAR` | Text | Yes | Yes |  |
| `Description` | LongText | Yes | Yes |  |
| `MayLeaveTenant` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `MayBeSharedExternally` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `DefaultRetentionDays` | Number |  | Yes |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## ResidencyRequirements

Storage and processing restrictions that may be assigned to a client, contract or project (D-12).

**Key:** `ResidencyRequirementID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ResidencyRequirementID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `RuleCode` | Enum (NoRestriction, RegionRestricted, CountryRestricted, NoThirdPartyAI…) | Yes | Yes |  |
| `NameEN` | Text | Yes | Yes |  |
| `NameAR` | Text | Yes | Yes |  |
| `AllowedRegions` | Text |  | Yes |  |
| `BlocksProductionUpload` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `BlocksThirdPartyAI` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `SourceClauseReference` | Text |  | Yes |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Clients

Clients the company works for. Bilingual names preserved exactly (D-11).

**Key:** `ClientID` · **Scope:** global · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ClientID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `LegalNameEN` | Text |  | Yes |  |
| `LegalNameAR` | Text |  | Yes |  |
| `DisplayNameEN` | Text |  | Yes |  |
| `DisplayNameAR` | Text |  | Yes |  |
| `ClientKind` | Text | Yes | Yes | Government\|SemiGovernment\|Private\|MainContractor |
| `BillingAddressEN` | LongText |  | Yes | **[financial]** |
| `BillingAddressAR` | LongText |  | Yes | **[financial]** |
| `TaxRegistrationNumber` | Text |  | Yes | **[financial]** |
| `PrimaryContactID` | Ref → Contacts |  | Yes |  |
| `PaymentTermsDays` | Number |  | Yes | **[financial]** |
| `Currency` | Text |  | Yes | ISO 4217 **[financial]** |
| `DefaultClassificationCode` | Enum (Public, Internal, ClientConfidential, Personal…) |  | Yes |  |
| `QuickBooksCustomerID` | Text |  | No | **[financial]** |
| `Status` | Text | Yes | Yes | Active\|Suspended\|Closed |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Contacts

Client contacts. Only an authorised recipient may receive a released document.

**Key:** `ContactID` · **Scope:** global · **Sensitivity:** personal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ContactID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ClientID` | Ref → Clients | Yes | Yes |  |
| `NameEN` | Text |  | Yes |  |
| `NameAR` | Text |  | Yes |  |
| `PositionEN` | Text |  | Yes |  |
| `PositionAR` | Text |  | Yes |  |
| `Email` | Email |  | Yes | **[personal]** |
| `Mobile` | Phone |  | Yes | **[personal]** |
| `PreferredLanguage` | Enum (en, ar) | Yes | Yes | Initial value `en` |
| `IsAuthorizedRecipient` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `Status` | Text | Yes | Yes | Active\|Inactive |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Projects

A project is pure configuration. Adding one never requires changed logic, a cloned app, duplicated scenarios, rewritten prompts or changed code (D-01).

**Key:** `ProjectID` · **Scope:** global · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ProjectID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ProjectCode` | Text | Yes | Yes | Uppercase, no spaces, filename-safe |
| `ProjectNameEN` | Text | Yes | Yes |  |
| `ProjectNameAR` | Text |  | Yes |  |
| `LegalEntityID` | Ref → LegalEntities | Yes | Yes |  |
| `ClientID` | Ref → Clients | Yes | Yes |  |
| `ContractID` | Ref → Contracts |  | Yes | **[financial]** |
| `LocationSummaryEN` | Text |  | Yes |  |
| `LocationSummaryAR` | Text |  | Yes |  |
| `StartDate` | Date | Yes | Yes |  |
| `EndDate` | Date |  | Yes | Must be >= StartDate when present |
| `ReportingFrequency` | Enum (Daily, Weekly, Monthly, Quarterly…) | Yes | Yes |  |
| `ReportingCutoffDay` | Number |  | Yes | 1-28 |
| `DefaultTemplateID` | Ref → DocumentTemplates |  | Yes |  |
| `DefaultDocumentLanguage` | Enum (en, ar) | Yes | Yes | Initial value `en` |
| `ProjectManagerUserID` | Ref → Users |  | Yes |  |
| `Currency` | Text | Yes | Yes | ISO 4217 **[financial]** |
| `TimeZone` | Text | Yes | Yes | Initial value `Asia/Qatar` |
| `BillingMethod` | Enum (MonthlyFixed, MeasuredBOQ, LumpSumMilestone, OnCompletion…) |  | Yes | **[financial]** |
| `PaymentTermsDays` | Number |  | Yes | **[financial]** |
| `AIAnalysisEnabled` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `RetentionDays` | Number |  | Yes |  |
| `DriveFolderKey` | Text |  | No |  |
| `Status` | Enum (Draft, Active, Suspended, Completed…) | Yes | Yes | Initial value `Draft` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## ProjectAssignments

Which users may act on which project, and in what role. A user may be assigned to many projects, and a project may have many users (D-15 item 2).

**Key:** `AssignmentID` · **Scope:** project · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `AssignmentID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ProjectID` | Ref → Projects | Yes | Yes |  |
| `UserID` | Ref → Users | Yes | Yes |  |
| `RoleID` | Ref → Roles | Yes | Yes |  |
| `AssignedFrom` | Date | Yes | Yes |  |
| `AssignedTo` | Date |  | Yes |  |
| `MaySubmitEvidence` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `MayReviewEvidence` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `MayRequestDocuments` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Locations

Hierarchical locations within a project. Choices are always filtered by project (spec 7.3).

**Key:** `LocationID` · **Scope:** project · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `LocationID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ProjectID` | Ref → Projects | Yes | Yes |  |
| `LocationCode` | Text | Yes | Yes | Filename-safe; unique within project |
| `LocationNameEN` | Text | Yes | Yes |  |
| `LocationNameAR` | Text |  | Yes |  |
| `ParentLocationID` | Ref → Locations |  | Yes | Parent must belong to the SAME project; no cycles; max depth 5 |
| `LocationKind` | Text |  | Yes | Site\|Zone\|Building\|Floor\|Room\|Asset |
| `GPSLatitude` | Decimal |  | Yes |  |
| `GPSLongitude` | Decimal |  | Yes |  |
| `GeofenceRadiusM` | Number |  | Yes |  |
| `DisplayOrder` | Number | Yes | Yes | Initial value `100` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## ProjectActivityRules

Per-project overrides of the global activity and evidence rules (D-15 item 4). A project that needs a different rule gets a row, never a code change.

**Key:** `ProjectActivityRuleID` · **Scope:** project · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ProjectActivityRuleID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ProjectID` | Ref → Projects | Yes | Yes |  |
| `ActivityTypeID` | Ref → ActivityTypes | Yes | Yes |  |
| `IsPermitted` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `RequiresBeforePhoto` | Yes/No |  | Yes |  |
| `RequiresAfterPhoto` | Yes/No |  | Yes |  |
| `RequiresQuantity` | Yes/No |  | Yes |  |
| `QuantityUnitID` | Ref → Units |  | Yes |  |
| `MinPhotos` | Number |  | Yes |  |
| `RequiresCaption` | Yes/No |  | Yes |  |
| `BOQItemHint` | Text |  | Yes | **[financial]** |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## ApprovalMatrix

Who approves what, per project and stage (D-09, D-15 item 6). The GM is the MVP approver, and the structure supports delegation without redesign.

**Key:** `ApprovalMatrixID` · **Scope:** project · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ApprovalMatrixID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ProjectID` | Ref → Projects |  | Yes |  |
| `ApprovalStage` | Enum (EvidenceReview, TechnicalReview, FinanceReview, Release…) | Yes | Yes |  |
| `DocumentTypeCode` | Enum (DailyReport, WeeklyReport, MonthlyTechnicalReport, InspectionReport…) |  | Yes |  |
| `ResponsibleUserID` | Ref → Users | Yes | Yes |  |
| `BackupUserID` | Ref → Users |  | Yes |  |
| `SequenceNumber` | Number | Yes | Yes | Initial value `1` |
| `SelfApprovalProhibited` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## ApprovalDelegations

Temporary delegation of an approval authority (D-09). Every delegated decision records both the acting user and the original responsible user.

**Key:** `DelegationID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `DelegationID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `FromUserID` | Ref → Users | Yes | Yes |  |
| `ToUserID` | Ref → Users | Yes | Yes |  |
| `ApprovalStage` | Enum (EvidenceReview, TechnicalReview, FinanceReview, Release…) |  | Yes |  |
| `Scope` | Enum (AllProjects, SpecificProjects, SpecificStage) | Yes | Yes |  |
| `ProjectIDs` | Text |  | Yes |  |
| `ValidFrom` | DateTime | Yes | Yes |  |
| `ValidTo` | DateTime | Yes | Yes | Must be after ValidFrom. An open-ended delegation is not permitted. |
| `Reason` | Text | Yes | Yes |  |
| `AuthorisedByUserID` | Ref → Users | Yes | Yes |  |
| `RevokedAt` | DateTime |  | Yes |  |
| `RevokedByUserID` | Ref → Users |  | Yes |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## ResidencyAssignments

Binds a residency requirement to a client, contract or project (D-12).

**Key:** `ResidencyAssignmentID` · **Scope:** project · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ResidencyAssignmentID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ResidencyRequirementID` | Ref → ResidencyRequirements | Yes | Yes |  |
| `AppliesToKind` | Text | Yes | Yes | Client\|Contract\|Project |
| `ClientID` | Ref → Clients |  | Yes |  |
| `ContractID` | Ref → Contracts |  | Yes |  |
| `ProjectID` | Ref → Projects |  | Yes |  |
| `EffectiveFrom` | Date | Yes | Yes |  |
| `EffectiveTo` | Date |  | Yes |  |
| `VerifiedFromContract` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## TemporaryAccessGrants

Time-bound, explicitly authorised access. Covers auditor access and break-glass emergency access. Without an active grant, the roles that depend on one resolve to no access at all.

**Key:** `GrantID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `GrantID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `GrantKind` | Text | Yes | Yes | Audit\|Emergency\|Support |
| `UserID` | Ref → Users | Yes | Yes |  |
| `RoleID` | Ref → Roles | Yes | Yes |  |
| `Scope` | Text | Yes | Yes | AllProjects\|SpecificProjects\|TechnicalOnly |
| `ProjectIDs` | Text |  | Yes |  |
| `Reason` | LongText | Yes | Yes |  |
| `RequestedByUserID` | Ref → Users | Yes | Yes |  |
| `RequestedAt` | DateTime | Yes | No |  |
| `AuthorisedByUserID` | Ref → Users | Yes | Yes |  |
| `AuthorisedAt` | DateTime | Yes | No |  |
| `ValidFrom` | DateTime | Yes | Yes |  |
| `ValidTo` | DateTime | Yes | Yes | Mandatory, after ValidFrom, and within MaxDurationHours |
| `MaxDurationHours` | Number | Yes | Yes | Initial value `24` |
| `NotificationRecipients` | Text | Yes | Yes |  |
| `NotificationSentAt` | DateTime |  | No | Required for GrantKind = Emergency before the grant becomes usable |
| `AuditReference` | Text |  | No |  |
| `UsageCount` | Number | Yes | No | Initial value `0` |
| `RevokedAt` | DateTime |  | Yes |  |
| `RevokedByUserID` | Ref → Users |  | Yes |  |
| `ReviewedAt` | DateTime |  | Yes |  |
| `ReviewedByUserID` | Ref → Users |  | Yes |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## SystemRecoveryPlan

How administrative control is recovered when no administrator is available. The system must not become unrecoverable because one person is unreachable.

**Key:** `PlanID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `PlanID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `PrimaryAdministratorUserID` | Ref → Users |  | Yes |  |
| `BackupAdministratorUserID` | Ref → Users |  | Yes |  |
| `RecoveryRouteDocumented` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `RecoveryRouteReference` | Text |  | Yes | Required when RecoveryRouteDocumented is TRUE |
| `BreakGlassAccountConfigured` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `OwnerCanAuthoriseBreakGlass` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `LastTestedAt` | Date |  | Yes |  |
| `TestedByUserID` | Ref → Users |  | Yes |  |
| `TestResult` | Text |  | Yes | Passed\|Failed\|NotTested |
| `GoLiveBlocker` | Yes/No | Yes | No | Initial value `TRUE` |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## SiteVisits

One reporting event at a location on a date. The unit of submission and review.

**Key:** `VisitID` · **Scope:** project · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `VisitID` | Text | Yes | Yes | `UNIQUEID()` — initial value, key, not editable |
| `ProjectID` | Ref → Projects | Yes | Yes | `IN([_THIS], SELECT(ProjectAssignments[ProjectID],    AND([UserID] = LOOKUP(USEREMAIL(), Users, Email, UserID),        [IsActive] = TRUE,        [MaySubmitEvidence] = TRUE,        [AssignedFrom] <= TODAY(),        OR(ISBLANK([AssignedTo]), [AssignedTo] >= TODAY()))))` — Valid_If. The dropdown offers only projects the signer is actively assigned to, and the same expression re-validates on save |
| `LocationID` | Ref → Locations | Yes | Yes | `FILTER("Locations", AND([ProjectID] = [_THISROW].[ProjectID], [IsActive] = TRUE))` — Valid_If. Locations depend on the chosen project (spec 7.3) |
| `WorkOrderID` | Ref → WorkOrders |  | Yes |  |
| `VisitDate` | Date | Yes | Yes | `TODAY()` — initial value; editable by an authorised user |
| `StartTime` | Time |  | Yes |  |
| `EndTime` | Time |  | Yes | `OR(ISBLANK([StartTime]), ISBLANK([_THIS]), [_THIS] > [StartTime])` — Valid_If |
| `Weather` | Text |  | Yes |  |
| `SupervisorUserID` | Ref → Users | Yes | No | `LOOKUP(USEREMAIL(), Users, Email, UserID)` — initial value; not editable. Identity comes from the signed-in user, never typed |
| `GPSLatitude` | Decimal |  | Yes |  |
| `GPSLongitude` | Decimal |  | Yes |  |
| `OverallDescriptionEN` | LongText |  | Yes |  |
| `OverallDescriptionAR` | LongText |  | Yes |  |
| `SafetyObservation` | LongText |  | Yes |  |
| `ClientRepresentative` | Text |  | Yes | **[personal]** |
| `ClientAcknowledgementStatus` | Text |  | Yes | NotRequested\|Claimed\|Declined |
| `WorkflowStatus` | Enum (Draft, Submitted, ValidationFailed, UnderTechnicalReview…) | Yes | No | `"Draft"` — initial value; not editable by a field role. Status moves only through actions |
| `SubmittedAt` | DateTime |  | No |  |
| `TechnicalReviewedAt` | DateTime |  | No |  |
| `TechnicalReviewedBy` | Ref → Users |  | No |  |
| `RejectionReason` | LongText |  | Yes |  |
| `ValidationErrors` | LongText |  | No |  |
| `CorrelationID` | Text |  | No |  |
| `EntityVersion` | Number | Yes | No | Initial value `1` |
| `ContentHash` | Text | Yes | No |  |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## VisitActivities

What was actually done during a visit. One row per activity.

**Key:** `VisitActivityID` · **Scope:** project · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `VisitActivityID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `VisitID` | Ref → SiteVisits | Yes | No |  |
| `ProjectID` | Ref → Projects | Yes | No |  |
| `ActivityTypeID` | Ref → ActivityTypes | Yes | Yes | `FILTER("ActivityTypes",    IN([ActivityTypeID], SELECT(ProjectActivityRules[ActivityTypeID],       AND([ProjectID] = [_THISROW].[ProjectID], [IsPermitted] = TRUE)))) + FILTER("ActivityTypes",    NOT(IN([ActivityTypeID], SELECT(ProjectActivityRules[ActivityTypeID],       [ProjectID] = [_THISROW].[ProjectID]))))` — Valid_If. Activities explicitly permitted for the project, plus any with no project rule at all (which inherit the global catalogue) |
| `DescriptionEN` | LongText |  | Yes |  |
| `DescriptionAR` | LongText |  | Yes |  |
| `Quantity` | Decimal |  | Yes | `OR(ISBLANK([_THIS]), [_THIS] >= 0)` — Valid_If. Non-negative |
| `UnitID` | Ref → Units |  | Yes |  |
| `PercentComplete` | Number |  | Yes | `OR(ISBLANK([_THIS]), AND([_THIS] >= 0, [_THIS] <= 100))` — Valid_If |
| `EvidenceStatus` | Text | Yes | No | Incomplete\|Complete\|Waived |
| `SupervisorConfirmation` | Yes/No | Yes | Yes | Initial value `FALSE` |
| `TechnicalReviewerComment` | LongText |  | Yes |  |
| `Status` | Enum (Draft, Submitted, UnderReview, Approved…) | Yes | No | Initial value `Draft` |
| `EntityVersion` | Number | Yes | No | Initial value `1` |
| `ContentHash` | Text | Yes | No |  |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Photos

One photograph per row. The received file is write-once and is never altered (D-13).

**Key:** `PhotoID` · **Scope:** project · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `PhotoID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `VisitID` | Ref → SiteVisits | Yes | No |  |
| `VisitActivityID` | Ref → VisitActivities |  | Yes |  |
| `ProjectID` | Ref → Projects | Yes | No |  |
| `LocationID` | Ref → Locations | Yes | No |  |
| `CapturedAt` | DateTime |  | Yes |  |
| `ReceivedAt` | DateTime | Yes | No | `NOW()` — initial value; not editable. Anchors the write-once guarantee |
| `UploadedAt` | DateTime |  | No |  |
| `CapturedBy` | Ref → Users | Yes | No | `LOOKUP(USEREMAIL(), Users, Email, UserID)` — initial value; not editable |
| `OriginalFileKey` | Text | Yes | No |  |
| `OriginalChecksum` | Text |  | No |  |
| `ChecksumAlgorithm` | Text |  | No |  |
| `OriginalMimeType` | Text |  | No |  |
| `OriginalWidth` | Number |  | No |  |
| `OriginalHeight` | Number |  | No |  |
| `OriginalSizeBytes` | Number |  | No |  |
| `IsOriginalDeviceImageVerified` | Yes/No | Yes | No | Initial value `FALSE` |
| `EvidenceStage` | Enum (Before, During, After, Observation…) | Yes | Yes |  |
| `CaptionEN` | Text |  | Yes | `OR(IN([_THISROW].[EvidenceStage], LIST("Before","During","After","Equipment","Other")),    NOT(ISBLANK([_THIS])), NOT(ISBLANK([_THISROW].[CaptionAR])))` — Valid_If. A caption is mandatory for Snag, Observation, Material and Safety evidence, in either language |
| `CaptionAR` | Text |  | Yes |  |
| `GPSLatitude` | Decimal |  | Yes |  |
| `GPSLongitude` | Decimal |  | Yes |  |
| `IsDuplicateSuspected` | Yes/No | Yes | No | Initial value `FALSE` |
| `DuplicateOfPhotoID` | Ref → Photos |  | No |  |
| `AIAnalysisStatus` | Enum (NotRequested, Queued, Completed, Failed…) | Yes | No | Initial value `NotRequested` |
| `AIObservation` | LongText |  | No |  |
| `AIConfidence` | Decimal |  | No | 0.00-1.00 |
| `AIModel` | Text |  | No |  |
| `AIPromptVersion` | Text |  | No |  |
| `AIContradictsCaption` | Yes/No |  | No |  |
| `ReviewerDecision` | Enum (Pending, Approved, Rejected, Excluded) | Yes | Yes | `"Pending"` — initial value. Editable ONLY by a reviewer role; never by AI and never by the uploader |
| `ReviewerComment` | LongText |  | Yes |  |
| `ReviewedByUserID` | Ref → Users |  | No |  |
| `ReviewedAt` | DateTime |  | No |  |
| `ApprovedForReport` | Yes/No | Yes | No | `([ReviewerDecision] = "Approved")` — app formula, so it can never be set independently of the human decision |
| `ReportSequence` | Number |  | Yes |  |
| `DerivedFileKey` | Text |  | No |  |
| `ClassificationCode` | Enum (Public, Internal, ClientConfidential, Personal…) | Yes | No | Initial value `ClientConfidential` |
| `EntityVersion` | Number | Yes | No | Initial value `1` |
| `ContentHash` | Text | Yes | No |  |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Snags

Defects and observations tracked to closure with evidence.

**Key:** `SnagID` · **Scope:** project · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `SnagID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ProjectID` | Ref → Projects | Yes | No |  |
| `LocationID` | Ref → Locations | Yes | Yes |  |
| `VisitID` | Ref → SiteVisits |  | No |  |
| `VisitActivityID` | Ref → VisitActivities |  | No |  |
| `SourcePhotoID` | Ref → Photos |  | Yes |  |
| `Category` | Text | Yes | Yes |  |
| `Severity` | Enum (Low, Medium, High, Critical) | Yes | Yes |  |
| `DescriptionEN` | LongText | Yes | Yes |  |
| `DescriptionAR` | LongText |  | Yes |  |
| `RaisedAt` | DateTime | Yes | No |  |
| `RaisedBy` | Ref → Users | Yes | No |  |
| `ResponsibleParty` | Text |  | Yes |  |
| `TargetDate` | Date |  | Yes |  |
| `Status` | Enum (Open, Assigned, InProgress, PendingVerification…) | Yes | Yes | Initial value `Open` |
| `ClosureDate` | Date |  | Yes | Required when Status = Closed |
| `ClosureEvidencePhotoID` | Ref → Photos |  | Yes | `OR([Status] <> "Closed", NOT(ISBLANK([_THIS])))` — Required_If equivalent. A snag cannot be closed on assertion alone |
| `VerifiedBy` | Ref → Users |  | No | Required when Status = Closed |
| `VerificationDate` | Date |  | No |  |
| `IsActive` | Yes/No | Yes | Yes | Initial value `TRUE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Approvals

Every approval decision, bound to the exact content approved (ADR-0006, D-09).

**Key:** `ApprovalID` · **Scope:** project · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `ApprovalID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `EntityType` | Text | Yes | No | Table name |
| `EntityID` | Text | Yes | No |  |
| `ProjectID` | Ref → Projects |  | No |  |
| `ApprovalStage` | Enum (EvidenceReview, TechnicalReview, FinanceReview, Release…) | Yes | No |  |
| `SequenceNumber` | Number | Yes | No | Initial value `1` |
| `RequestedFromUserID` | Ref → Users | Yes | No |  |
| `RequestedAt` | DateTime | Yes | No |  |
| `Decision` | Enum (Pending, Approved, Rejected, Delegated…) | Yes | Yes | Initial value `Pending` |
| `DecisionAt` | DateTime |  | No |  |
| `DecisionByUserID` | Ref → Users |  | No |  |
| `DelegationID` | Ref → ApprovalDelegations |  | No | Required when DecisionByUserID != RequestedFromUserID |
| `Comment` | LongText |  | Yes |  |
| `EntityVersion` | Number | Yes | No |  |
| `ContentHash` | Text | Yes | No |  |
| `VoidedAt` | DateTime |  | No |  |
| `VoidReason` | Text |  | No |  |
| `IsOverride` | Yes/No | Yes | No | Initial value `FALSE` |
| `OverrideReason` | LongText |  | Yes | Required when IsOverride |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## EntityVersions

Immutable version history of hashable entities. Supports proving what a decision applied to.

**Key:** `VersionID` · **Scope:** project · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `VersionID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `EntityType` | Text | Yes | No |  |
| `EntityID` | Text | Yes | No |  |
| `ProjectID` | Ref → Projects |  | No |  |
| `VersionNumber` | Number | Yes | No |  |
| `ContentHash` | Text | Yes | No |  |
| `CanonicalFieldSetVersion` | Text | Yes | No |  |
| `ChangedByUserID` | Ref → Users | Yes | No |  |
| `ChangedAt` | DateTime | Yes | No |  |
| `ChangeSummary` | Text |  | No |  |
| `InvalidatedApprovalIDs` | Text |  | No |  |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## AuditLog

Append-only record of every state transition and every consequential action.

**Key:** `AuditID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `AuditID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `TimestampUTC` | DateTime | Yes | No |  |
| `UserOrService` | Text | Yes | No |  |
| `Action` | Text | Yes | No |  |
| `EntityType` | Text | Yes | No |  |
| `EntityID` | Text | Yes | No |  |
| `ProjectID` | Ref → Projects |  | No |  |
| `BeforeHash` | Text |  | No |  |
| `AfterHash` | Text |  | No |  |
| `SourceIPOrDevice` | Text |  | No |  |
| `CorrelationID` | Text |  | No |  |
| `Result` | Text | Yes | No | Success\|Failure\|Denied |
| `Reason` | Text |  | No |  |

---

## Key expressions in full

Reproduced unwrapped, because these are the ones where a transcription error would be a
security or data-integrity defect rather than a cosmetic one.

### `SiteVisits.VisitID`

*initial value, key, not editable*

```
UNIQUEID()
```

### `SiteVisits.ProjectID`

*Valid_If. The dropdown offers only projects the signer is actively assigned to, and the same expression re-validates on save*

```
IN([_THIS], SELECT(ProjectAssignments[ProjectID],
   AND([UserID] = LOOKUP(USEREMAIL(), Users, Email, UserID),
       [IsActive] = TRUE,
       [MaySubmitEvidence] = TRUE,
       [AssignedFrom] <= TODAY(),
       OR(ISBLANK([AssignedTo]), [AssignedTo] >= TODAY()))))
```

### `SiteVisits.LocationID`

*Valid_If. Locations depend on the chosen project (spec 7.3)*

```
FILTER("Locations", AND([ProjectID] = [_THISROW].[ProjectID], [IsActive] = TRUE))
```

### `SiteVisits.VisitDate`

*initial value; editable by an authorised user*

```
TODAY()
```

### `SiteVisits.SupervisorUserID`

*initial value; not editable. Identity comes from the signed-in user, never typed*

```
LOOKUP(USEREMAIL(), Users, Email, UserID)
```

### `SiteVisits.WorkflowStatus`

*initial value; not editable by a field role. Status moves only through actions*

```
"Draft"
```

### `SiteVisits.EndTime`

*Valid_If*

```
OR(ISBLANK([StartTime]), ISBLANK([_THIS]), [_THIS] > [StartTime])
```

### `VisitActivities.ActivityTypeID`

*Valid_If. Activities explicitly permitted for the project, plus any with no project rule at all (which inherit the global catalogue)*

```
FILTER("ActivityTypes",
   IN([ActivityTypeID], SELECT(ProjectActivityRules[ActivityTypeID],
      AND([ProjectID] = [_THISROW].[ProjectID], [IsPermitted] = TRUE))))
+ FILTER("ActivityTypes",
   NOT(IN([ActivityTypeID], SELECT(ProjectActivityRules[ActivityTypeID],
      [ProjectID] = [_THISROW].[ProjectID]))))
```

### `VisitActivities.Quantity`

*Valid_If. Non-negative*

```
OR(ISBLANK([_THIS]), [_THIS] >= 0)
```

### `VisitActivities.PercentComplete`

*Valid_If*

```
OR(ISBLANK([_THIS]), AND([_THIS] >= 0, [_THIS] <= 100))
```

### `Photos.CaptionEN`

*Valid_If. A caption is mandatory for Snag, Observation, Material and Safety evidence, in either language*

```
OR(IN([_THISROW].[EvidenceStage], LIST("Before","During","After","Equipment","Other")),
   NOT(ISBLANK([_THIS])), NOT(ISBLANK([_THISROW].[CaptionAR])))
```

### `Photos.ReceivedAt`

*initial value; not editable. Anchors the write-once guarantee*

```
NOW()
```

### `Photos.CapturedBy`

*initial value; not editable*

```
LOOKUP(USEREMAIL(), Users, Email, UserID)
```

### `Photos.ReviewerDecision`

*initial value. Editable ONLY by a reviewer role; never by AI and never by the uploader*

```
"Pending"
```

### `Photos.ApprovedForReport`

*app formula, so it can never be set independently of the human decision*

```
([ReviewerDecision] = "Approved")
```

### `Snags.ClosureEvidencePhotoID`

*Required_If equivalent. A snag cannot be closed on assertion alone*

```
OR([Status] <> "Closed", NOT(ISBLANK([_THIS])))
```

