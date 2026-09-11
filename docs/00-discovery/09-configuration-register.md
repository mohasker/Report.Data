# Configuration Register

**Document ID:** AH-SYS-P0-009 · **Revision:** 1 · **Status:** live register, updated 2026-09-11 for D-02, D-08, D-10, D-11, D-12

Every external value the system needs, expressed as a **named variable** (operating rule 3).

> **This file records variable NAMES, OWNERS and LOCATIONS — never values.**
> No key, token, password, account ID, folder ID, application ID, webhook URL or company ID is
> written here, in any other file in this repository, in any spreadsheet, in any prompt, or in any
> log (operating rule 4).

## How real values are supplied

| Kind of value | Where it lives | How it is set |
|---|---|---|
| **Secrets** — API keys, tokens, client secrets, webhook signing secrets | The provider's own connection store: Make connections, AppSheet's secure settings, or an environment variable in a secret manager | The **owner authorises OAuth personally in each provider's console.** No credential is ever pasted into chat or into this repository. |
| **Non-secret identifiers** — Drive folder IDs, spreadsheet IDs, app IDs, QuickBooks company ID | A protected configuration table in the operational store, readable only by SystemAdmin | Entered once by the system administrator at provisioning, then referenced by name everywhere. |
| **Business configuration** — payment terms, tax rules, approval routes, templates, recipients, retention | Master-data tables in the application | Maintained by authorised administrators through the app's administration screens — never in code (requirement 14). |

## Register

`SECRET = never leaves its connection store` · `ID = non-secret identifier` · `BUSINESS = master data`

### Google Workspace and Drive

| Variable | Kind | Description | Owner | Needed by | Status |
|---|---|---|---|---|---|
| `GOOGLE_WORKSPACE_DOMAIN` | ID | Company domain of the Workspace tenant | GM | Phase 1 | ☐ |
| `SYSTEM_OWNER_ACCOUNT` | ID | Dedicated system account owning the app, sheets and connections (ADR-0001) | GM | Phase 1 | ☐ |
| `SHARED_DRIVE_ID` | ID | Company-owned Shared Drive holding all operational storage | Administrator | Phase 3 | ☐ |
| `DRIVE_ROOT_FOLDER_ID` | ID | `Al-Haram Operations` root folder ID | Administrator | Phase 3 | ☐ |
| `OPERATIONS_SPREADSHEET_ID` | ID | Operational store workbook | Administrator | Phase 2 | ☐ |
| `GOOGLE_OAUTH_CONNECTION` | SECRET | OAuth connection held in Make | Owner authorises | Phase 3 | ☐ |

### AppSheet

| Variable | Kind | Description | Owner | Needed by | Status |
|---|---|---|---|---|---|
| `APPSHEET_APP_ID` | ID | Application identifier | Administrator | Phase 2 | ☐ |
| `APPSHEET_PLAN_TIER` | ID | Licensed plan (BQ-02) | GM | Phase 2 | ☐ |
| `APPSHEET_API_KEY` | SECRET | Application access key | Owner authorises | Phase 3 | ☐ |
| `APPSHEET_WEBHOOK_SECRET` | SECRET | Shared secret authenticating webhook calls | Owner authorises | Phase 3 | ☐ |
| `APPSHEET_DEEPLINK_BASE` | ID | Base URL for record deep links in notifications | Administrator | Phase 3 | ☐ |

### Make.com

| Variable | Kind | Description | Owner | Needed by | Status |
|---|---|---|---|---|---|
| `MAKE_ORGANIZATION` / `MAKE_TEAM` | ID | Where scenarios live (BQ-03) | GM | Phase 3 | ☐ |
| `MAKE_DATASTORE_IDEMPOTENCY` | ID | Data Store holding idempotency keys | Administrator | Phase 3 | ☐ |
| `MAKE_DATASTORE_COUNTERS` | ID | Data Store holding numbering counters (ADR-0005) | Administrator | Phase 5 | ☐ |
| `MAKE_ERROR_QUEUE_TARGET` | ID | Dead-letter destination | Administrator | Phase 3 | ☐ |
| `MAKE_WEBHOOK_URLS` | SECRET | Scenario webhook endpoints — treated as secrets because possession permits invocation | Owner authorises | Phase 3 | ☐ |

### Claude API

| Variable | Kind | Description | Owner | Needed by | Status |
|---|---|---|---|---|---|
| `CLAUDE_API_KEY` | SECRET | API key, stored only in the Make connection | Owner authorises | Phase 4 | ☐ |
| `CLAUDE_WORKSPACE` | ID | Dedicated workspace for this system (BQ-04) | GM | Phase 4 | ☐ |
| `CLAUDE_MONTHLY_SPEND_CAP` | BUSINESS | Hard monthly cap authorised by the owner | GM | Phase 4 | ☐ |
| `CLAUDE_MODEL_EVIDENCE` / `CLAUDE_MODEL_NARRATIVE` | ID | Models used, recorded on every DocumentJob for reproducibility | Architect | Phase 4 | ☐ |
| `CLAUDE_MAX_OUTPUT_TOKENS` | BUSINESS | Per-call output cap (cost control) | Architect | Phase 4 | ☐ |
| `AI_ANALYSIS_ENABLED_PER_PROJECT` | BUSINESS | Per-project flag to disable AI analysis where a contract or residency rule makes it problematic (D-12, R-04). Disabling it removes assistance, never a control | Administrator | Phase 4 | ☐ |
| `DATA_CLASSIFICATION_RULES` | BUSINESS | Classification of photographs, personal data, contracts, financial data and government/client records (D-12) | Administrator | Phase 1 | ☐ |
| `RESIDENCY_REQUIREMENTS` | BUSINESS | Residency and approved-storage rules assignable per client, contract and project (D-12) | GM | Before production upload | ☐ |

### QuickBooks Online — Phase 7

| Variable | Kind | Description | Owner | Needed by | Status |
|---|---|---|---|---|---|
| `QBO_COMPANY_ID` | ID | Company file (BQ-05) | Accountant | Phase 7 | ☐ |
| `QBO_REGION_EDITION` | ID | Region and edition — determines tax and numbering behaviour | Accountant | Phase 6 | ☐ |
| `QBO_SANDBOX_COMPANY_ID` | ID | Sandbox company for testing | Accountant | Phase 7 | ☐ |
| `QBO_OAUTH_CONNECTION` | SECRET | OAuth connection held in Make | Owner authorises | Phase 7 | ☐ |
| `QBO_INCOME_ACCOUNT_MAP` | BUSINESS | Chart-of-accounts mapping per service | Accountant | Phase 7 | ☐ |
| `QBO_ITEM_MAP` | BUSINESS | Product/service item IDs per BOQ category | Accountant | Phase 7 | ☐ |
| `QBO_TAX_CODE_MAP` | BUSINESS | Tax code mapping (BQ-06) | Accountant | Phase 7 | ☐ |
| `QBO_CLASS_OR_PROJECT_MAP` | BUSINESS | Class/project mapping per project | Accountant | Phase 7 | ☐ |
| `QBO_POSTING_ENABLED` | BUSINESS | **Defaults to FALSE.** Production posting stays disabled until the owner authorises it in writing (ADR-0008) | GM | Phase 7 | ☐ |

### Company and document identity

| Variable | Kind | Description | Owner | Needed by | Status |
|---|---|---|---|---|---|
| `LEGAL_ENTITY_REGISTER` | BUSINESS | **Replaces `COMPANY_LEGAL_NAME` (D-02).** `LegalEntities` master data: EN/AR legal names, CR number, establishment/card number, registered address, country, currency, tax registration status, logo, official email, telephone and WhatsApp, authorised signatories, footer details, effective date, version. Synthetic data uses `LEGAL_ENTITY_NAME_PENDING_VERIFICATION` | GM | Before production documents | ☐ |
| `COMPANY_CODE` | BUSINESS | Code used in document numbers (BQ-08) | GM | Phase 5 | ☐ |
| `COMPANY_CR_NUMBER` | BUSINESS | Commercial registration number for documents | GM | Phase 5 | ☐ |
| `COMPANY_ADDRESS_BLOCK` | BUSINESS | Registered address as printed on documents | GM | Phase 5 | ☐ |
| `COMPANY_LOGO_FILE_ID` | ID | Approved logo, correct aspect ratio (§10) | GM | Phase 5 | ☐ |
| `NUMBERING_SERIES_REGISTER` | BUSINESS | **Replaces a single format list (D-10).** One configurable series per legal entity × document type × year × scope × optional client requirement, each with its format, reset rule and revision handling | GM | Phase 5 | ☐ |
| `DOCUMENT_SERIES_START_NUMBERS` | BUSINESS | Starting number per series, continuing the existing manual register, with that register's migration recorded (A-18, D-10) | GM | Phase 5 | ☐ |
| `DEFAULT_DOCUMENT_LANGUAGE` | BUSINESS | Default generated-report language per project (D-11). Bilingual EN/AR capability is architectural from Phase 1; this value selects the default, not the capability | GM | Phase 5 | ☐ |
| `CONFIDENTIALITY_MARKING` | BUSINESS | Marking applied to client documents where applicable | GM | Phase 5 | ☐ |

### Operational policy

| Variable | Kind | Description | Owner | Needed by | Status |
|---|---|---|---|---|---|
| `DEFAULT_CURRENCY` | BUSINESS | System default, overridden by contract (A-08) | GM | Phase 6 | ☐ |
| `ROUNDING_POLICY` | BUSINESS | Decimal places, direction, and where rounding is applied (R-23) | Architect | Phase 6 | ☐ |
| `TAX_RULES` | BUSINESS | Configurable tax rules (D-08). **No classification may be named** — "zero-rated", "exempt", "out of scope" and "no tax configured" are distinct and non-interchangeable. Seeded with an obviously synthetic placeholder; the applied rule **and its version** are preserved on every invoice calculation | Accountant | Before production invoicing | ☐ |
| `DEFAULT_PAYMENT_TERMS_DAYS` | BUSINESS | Default, overridden per contract | GM | Phase 6 | ☐ |
| `WORKING_CALENDAR` | BUSINESS | Working days, weekend, public holidays (OQ-01) | Administrator | Phase 2 | ☐ |
| `REPORTING_CUTOFF_DAY` | BUSINESS | Latest day evidence may be added to a period (OQ-02) | GM | Phase 2 | ☐ |
| `RETENTION_POLICY_DAYS` | BUSINESS | Per project, with a system default. **Flag for review — never auto-delete** (C-10) | GM | Phase 3 | ☐ |
| `OLD_PHOTO_WARNING_HOURS` | BUSINESS | Threshold for warning about old captures — warn only, never reject (§7.3) | Administrator | Phase 2 | ☐ |
| `MAX_PHOTOS_PER_VISIT_SOFT_LIMIT` | BUSINESS | Tested operational limit (C-11) | Architect | Phase 2 | ☐ |
| `ALERT_RECIPIENTS` | BUSINESS | Who receives error-queue and monitoring alerts (OQ-12) | Administrator | Phase 3 | ☐ |
| `APPROVAL_MATRIX` | BUSINESS | Approver per stage per project, with delegates (BQ-07) | GM | Phase 2 | ☐ |
| `AUTHORIZED_RECIPIENTS` | BUSINESS | Per client, who may receive released documents | GM | Phase 7 | ☐ |
| `BACKUP_SCHEDULE` | BUSINESS | Export cadence and who verifies a restore actually works (OQ-04) | Administrator | Phase 3 | ☐ |

## Rules for this register

1. **No value is ever written into this file.** Names, owners, locations and status only.
2. A variable reaching its "Needed by" phase without a value **blocks that phase** rather than being guessed.
3. Secrets are authorised by the owner directly in the provider's console. They are never requested in chat, never stored in the operational spreadsheet, never printed in a log, and never committed here.
4. Business configuration is maintained through the application's administration screens — never by editing logic, scenarios, prompts or code (requirement 14).
5. Every variable has one named owner. "The system" is not an owner.
