# AppSheet Implementation Workbook

**Document ID:** AH-SYS-P2A-001 · **Revision:** 1 · **Status:** generated — do not hand-edit
**Generated:** 2026-09-12 from `model/model.json` by `tools/gen_appsheet_workbook.py`

> **Nothing here is connected.** This is the specification an implementer follows in Phase 2,
> derived from the canonical model so the app cannot drift from the data foundation.
> Expressions are written in AppSheet's expression language and have **not** been executed
> on the platform — see `12-appsheet-feature-to-plan-matrix.md`, where the platform's
> capabilities remain UNVERIFIED.

## Workbook structure

One worksheet per table, named exactly as the table. Header row exactly as the column names
in the data dictionary. No formulas in cells: every derivation is an app formula or a
virtual column, so the store stays a store.

**17 worksheets** are built (the lean operational MVP). The remaining
29 tables of the reference architecture are
designed and deferred; adding one later is additive, never a migration. Scope and rationale:
[`11-lean-mvp-scope.md`](11-lean-mvp-scope.md).

### Lean replacements

Where a lean table would otherwise require a deferred one, a replacement column carries the
job instead:

| Reference-architecture column | Lean replacement | Carries |
|---|---|---|
| `Users.RoleID` | `RoleCode` (enum of the ten role codes) | The role vocabulary is fixed for the MVP, so an enum carries it. |
| `ProjectAssignments.RoleID` | `RoleCode` (enum of the ten role codes) | The role held ON THIS PROJECT, which is what the security filter reads. |
| `Projects.ClientID` | `ClientNameEN, ClientNameAR, ClientKind` (text columns on Projects) | Enough for a report header and a dashboard. Billing address, tax number and accounting identifier are absent until Phase 6, where they are needed. |
| `ActivityTypes.DisciplineID` | `DisciplineCode` (enum of six disciplines) | Used to group the activity picker; not referenced anywhere else. |
| `Documents.TemplateID` | `TemplateFileKey, LanguageCode` (columns on Documents, copied from the project at generation) | Records which template file actually produced the document, which is the part that matters for reproducibility. |
| `NumberRegister.SeriesID` | `SeriesKey` (text key composed of entity, document type and year) | The register keeps its reserved/issued/cancelled control; only the series CONFIGURATION moves to the legal entity. |

## Column conventions

| Convention | Rule |
|---|---|
| Key | The table's primary key column. `UNIQUEID()` as initial value, never editable |
| Label | The first bilingual name column, so references display readably |
| `Editable_If` | `FALSE` for every column whose source is system, integration, calculation or AI |
| `Required_If` | Mirrors the model's required flag, plus any conditional rule stated in the dictionary |
| `Valid_If` | Mirrors the model's validation and referential rules |
| Sensitivity | Columns marked financial or personal are omitted entirely from field-role slices, not merely hidden |

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

## SiteVisits

One reporting event at a location on a date. The unit of submission and review.

**Key:** `VisitID` · **Scope:** project · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `VisitID` | Text | Yes | Yes | `UNIQUEID()` — initial value, key, not editable |
| `ProjectID` | Ref → Projects | Yes | No | `IN([_THIS], SELECT(ProjectAssignments[ProjectID],    AND([UserID] = LOOKUP(USEREMAIL(), Users, Email, UserID),        [IsActive] = TRUE,        [MaySubmitEvidence] = TRUE,        [AssignedFrom] <= TODAY(),        OR(ISBLANK([AssignedTo]), [AssignedTo] >= TODAY()))))` — Valid_If. The dropdown offers only projects the signer is actively assigned to, and the same expression re-validates on save |
| `LocationID` | Ref → Locations | Yes | No | `FILTER("Locations", AND([ProjectID] = [_THISROW].[ProjectID], [IsActive] = TRUE))` — Valid_If. Locations depend on the chosen project (spec 7.3) |
| `WorkOrderID` | Ref → WorkOrders |  | Yes |  |
| `VisitDate` | Date | Yes | Yes | `TODAY()` — initial value; editable by an authorised user |
| `StartTime` | Time |  | Yes |  |
| `EndTime` | Time |  | Yes | `OR(ISBLANK([StartTime]), ISBLANK([_THIS]), [_THIS] > [StartTime])` — Valid_If |
| `Weather` | Text |  | Yes |  |
| `SupervisorUserID` | Ref → Users | Yes | No | `LOOKUP(USEREMAIL(), Users, Email, UserID)` — initial value; not editable. Identity comes from the signed-in user, never typed |
| `GPSLatitude` | Decimal |  | Yes |  |
| `GPSLongitude` | Decimal |  | Yes |  |
| `OverallDescriptionEN` | LongText |  | Yes | Optional for a normal photographic submission (D-18) |
| `OverallDescriptionAR` | LongText |  | Yes | Optional for a normal photographic submission (D-18) |
| `AdditionalSiteNote` | LongText |  | Yes | Optional. Mandatory only in the exceptional workflows listed in capture_once.optional_note.mandatory_exceptions |
| `SiteNoteCategory` | Enum (ClientInstruction, AccessRestriction, PermitIssue, HiddenDefect…) |  | Yes |  |
| `CaptureMode` | Enum (QuickShare, AIReviewedShare) | Yes | No | Initial value `QuickShare` |
| `ShareStatus` | Enum (NotShared, ShareInitiated, ShareConfirmed, ShareCancelled…) | Yes | Yes | Initial value `NotShared` |
| `SharedAt` | DateTime |  | No |  |
| `SharedByUserID` | Ref → Users |  | No |  |
| `ShareTargetLabel` | Text |  | Yes |  |
| `ShareAttemptCount` | Number | Yes | No | Initial value `0` |
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
| `VisitActivityID` | Ref → VisitActivities |  | No |  |
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
| `EvidenceStage` | Enum (Before, During, After, Observation…) |  | Yes | Optional at capture (D-22). Never a mandatory manual field before the photograph is taken |
| `CaptionEN` | Text |  | Yes | `OR(IN([_THISROW].[EvidenceStage], LIST("Before","During","After","Equipment","Other")),    NOT(ISBLANK([_THIS])), NOT(ISBLANK([_THISROW].[CaptionAR])))` — Valid_If. A caption is mandatory for Snag, Observation, Material and Safety evidence, in either language |
| `CaptionAR` | Text |  | Yes |  |
| `GPSLatitude` | Decimal |  | Yes |  |
| `GPSLongitude` | Decimal |  | Yes |  |
| `CaptureBatchID` | Text |  | No |  |
| `CaptureSequence` | Number |  | No |  |
| `IsDuplicateSuspected` | Yes/No | Yes | No | Initial value `FALSE` |
| `DuplicateOfPhotoID` | Ref → Photos |  | No |  |
| `AIAnalysisStatus` | Enum (NotRequested, Queued, Completed, Failed…) | Yes | No | Initial value `NotRequested` |
| `AnalysisEligibility` | Enum (Eligible, Analysed, SkippedDuplicate, SkippedQuality…) | Yes | No | Initial value `Eligible` |
| `PerceptualHash` | Text |  | No |  |
| `QualityScore` | Decimal |  | No | 0.00-1.00 |
| `AIObservation` | LongText |  | No |  |
| `AIProposedEvidenceStage` | Enum (Before, During, After, Observation…) |  | No |  |
| `AIProposedActivityText` | Text |  | No |  |
| `AIProposedActivityTypeID` | Ref → ActivityTypes |  | No | Advisory candidate only. No report, rule, calculation, filter or join may read this column |
| `ConfirmedActivityTypeID` | Ref → ActivityTypes |  | Yes | Must be permitted for the project by the effective activity rule |
| `ClassificationStatus` | Enum (Pending, AIProposed, Confirmed, NotApplicable…) | Yes | No | Initial value `Pending` |
| `ConfirmedByUserID` | Ref → Users |  | No |  |
| `ConfirmedAt` | DateTime |  | No |  |
| `QuarantineStatus` | Enum (NotQuarantined, Quarantined, AcceptedIntoProject, Rejected) | Yes | No | Initial value `NotQuarantined` |
| `AccessRevokedAt` | DateTime |  | No |  |
| `UploadCompletedAt` | DateTime |  | No |  |
| `QuarantinedAt` | DateTime |  | No |  |
| `QuarantineReviewedByUserID` | Ref → Users |  | No |  |
| `QuarantineReviewedAt` | DateTime |  | No |  |
| `QuarantineRejectionReason` | LongText |  | Yes |  |
| `AIProposedCaptionEN` | Text |  | No |  |
| `AIProposedCaptionAR` | Text |  | No |  |
| `AIVisibleCondition` | Text |  | No |  |
| `AIPossibleSnag` | Yes/No |  | No |  |
| `AIImageQualityWarning` | Text |  | No |  |
| `AIUncertaintyNote` | Text |  | No |  |
| `AIProposalDisposition` | Enum (NotOffered, Accepted, Corrected, Rejected) | Yes | Yes | Initial value `NotOffered` |
| `AIAnalysedAt` | DateTime |  | No |  |
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

## DocumentJobs

A request to produce a document from a frozen snapshot of approved records.

**Key:** `JobID` · **Scope:** project · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `JobID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `ProjectID` | Ref → Projects | Yes | Yes |  |
| `LegalEntityID` | Ref → LegalEntities | Yes | No |  |
| `DocumentTypeCode` | Enum (DailyReport, WeeklyReport, MonthlyTechnicalReport, InspectionReport…) | Yes | Yes |  |
| `LanguageCode` | Enum (en, ar) | Yes | Yes | Initial value `en` |
| `PeriodStart` | Date | Yes | Yes |  |
| `PeriodEnd` | Date | Yes | Yes | Must be >= PeriodStart |
| `RequestedBy` | Ref → Users | Yes | No | Must hold MayRequestDocuments on ProjectID |
| `RequestedAt` | DateTime | Yes | No |  |
| `InputValidationStatus` | Text | Yes | No | NotRun\|Passed\|Failed |
| `InputValidationFindings` | LongText |  | No |  |
| `SnapshotManifest` | LongText |  | No |  |
| `SnapshotFrozenAt` | DateTime |  | No |  |
| `WorkflowStatus` | Enum (Requested, Validating, InputValidationFailed, SnapshotFrozen…) | Yes | No | Initial value `Requested` |
| `AIModel` | Text |  | No |  |
| `PromptVersion` | Text |  | No |  |
| `ReservedNumberID` | Ref → NumberRegister |  | No |  |
| `StartedAt` | DateTime |  | No |  |
| `FinishedAt` | DateTime |  | No |  |
| `ErrorClass` | Enum (Validation, Authentication, Authorization, RateLimit…) |  | No |  |
| `ErrorMessage` | LongText |  | No |  |
| `RetryCount` | Number | Yes | No | Initial value `0` |
| `CorrelationID` | Text | Yes | No |  |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## Documents

A produced document revision. Approval binds to ContentHash (ADR-0006).

**Key:** `DocumentID` · **Scope:** project · **Sensitivity:** confidential

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `DocumentID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `JobID` | Ref → DocumentJobs | Yes | No |  |
| `ProjectID` | Ref → Projects | Yes | No |  |
| `LegalEntityID` | Ref → LegalEntities | Yes | No |  |
| `DocumentTypeCode` | Enum (DailyReport, WeeklyReport, MonthlyTechnicalReport, InspectionReport…) | Yes | No |  |
| `TemplateID` | Ref → DocumentTemplates | Yes | No |  |
| `LanguageCode` | Enum (en, ar) | Yes | No |  |
| `DocumentNumber` | Text |  | No |  |
| `VersionNumber` | Number | Yes | No | Initial value `1` |
| `RevisionLabel` | Text |  | No |  |
| `DraftFileKey` | Text |  | No |  |
| `PDFFileKey` | Text |  | No |  |
| `ContentHash` | Text | Yes | No |  |
| `TechnicalApprovalStatus` | Text | Yes | No | Pending\|Approved\|Rejected\|Void |
| `FinancialApprovalStatus` | Text | Yes | No | NotRequired\|Pending\|Approved\|Rejected\|Void |
| `ReleaseStatus` | Enum (Draft, PendingTechnicalApproval, TechnicallyApproved, RevisionRequired…) | Yes | No | Initial value `Draft` |
| `ReleasedAt` | DateTime |  | No |  |
| `ReleasedBy` | Ref → Users |  | No |  |
| `RecipientSnapshot` | LongText |  | No |  |
| `SupersedesDocumentID` | Ref → Documents |  | No |  |
| `ClassificationCode` | Enum (Public, Internal, ClientConfidential, Personal…) | Yes | No | Initial value `ClientConfidential` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

## NumberRegister

Every number ever reserved, issued or cancelled. A cancelled number is never reused (D-10).

**Key:** `NumberID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `NumberID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `SeriesID` | Ref → NumberingSeries | Yes | No |  |
| `SequenceValue` | Number | Yes | No |  |
| `FormattedNumber` | Text | Yes | No |  |
| `YearKey` | Text | Yes | No |  |
| `ScopeKey` | Text | Yes | No |  |
| `State` | Enum (Reserved, Issued, Cancelled) | Yes | No | Initial value `Reserved` |
| `ReservedForJobID` | Ref → DocumentJobs |  | No |  |
| `IssuedToDocumentID` | Ref → Documents |  | No |  |
| `ReservedAt` | DateTime | Yes | No |  |
| `IssuedAt` | DateTime |  | No |  |
| `CancelledAt` | DateTime |  | No |  |
| `CancellationReason` | Text |  | No | Required when State = Cancelled |
| `MigratedFromManual` | Yes/No | Yes | No | Initial value `FALSE` |
| `CreatedAt` | DateTime | Yes | No |  |
| `CreatedBy` | Email | Yes | No |  |
| `UpdatedAt` | DateTime | Yes | No |  |
| `UpdatedBy` | Email | Yes | No |  |

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

## IntegrationJobs

One row per external call attempt, with idempotency and failure classification.

**Key:** `IntegrationJobID` · **Scope:** global · **Sensitivity:** internal

| Column | AppSheet type | Required | Editable | Expression / rule |
|---|---|---|---|---|
| `IntegrationJobID` | Text | Yes | Yes | `UNIQUEID()` initial value; key; not editable |
| `SystemName` | Text | Yes | No |  |
| `OperationName` | Text | Yes | No |  |
| `IdempotencyKey` | Text | Yes | No |  |
| `CorrelationID` | Text | Yes | No |  |
| `EntityType` | Text | Yes | No |  |
| `EntityID` | Text | Yes | No |  |
| `ProjectID` | Ref → Projects |  | No |  |
| `AttemptNumber` | Number | Yes | No | Initial value `1` |
| `StartedAt` | DateTime | Yes | No |  |
| `FinishedAt` | DateTime |  | No |  |
| `Status` | Enum (Pending, InProgress, Succeeded, Failed…) | Yes | No | Initial value `Pending` |
| `SanitizedRequestSummary` | Text |  | No |  |
| `SanitizedResponseSummary` | Text |  | No |  |
| `ErrorClass` | Enum (Validation, Authentication, Authorization, RateLimit…) |  | No |  |
| `ErrorCode` | Text |  | No |  |
| `RetryAfter` | DateTime |  | No |  |
| `IsRetriable` | Yes/No | Yes | No | Initial value `FALSE` |

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

