# Data Classification, Residency and Data Flows

**Document ID:** AH-SYS-P1-009 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **Contract review not yet executed**
**Delivers:** D-15 item 8 · **Implements:** D-12 · **Relates to:** R-04, P-08, BQ-10
**Evidence:** `17-validation-evidence.md` (GOV-14, GOV-15, SEG-12)

> A contractual restriction blocks **production storage or processing for the affected project** —
> not the generic system design (D-12). This document exists so that when a restriction is found,
> the response is a configuration row and a blocked project, rather than a redesign.

---

## 1. Classification

Six classes, each attached to records and files and each driving concrete behaviour:

| Class | Applies to | May leave the tenant | May be shared externally |
|---|---|---|---|
| `Public` | Already-published material | Yes | Yes |
| `Internal` | Operational data with no client confidentiality | Yes | No |
| `ClientConfidential` | **Default for photographic evidence** and project records | No | No |
| `Personal` | Data identifying an individual | No | No |
| `Financial` | Rates, invoices, accounting identifiers | No | No |
| `GovernmentRestricted` | Handling imposed by a government contract | No | No |

"May leave the tenant" is the switch that governs third-party processing, including AI analysis.
Evidence defaults to `ClientConfidential`, so **AI analysis is an opt-in per project, not a default
for the estate**.

## 2. Residency requirements

A residency requirement is a named rule; a residency assignment binds it to a **client, contract or
project**. Both are master data.

| Rule | Effect |
|---|---|
| `NoRestriction` | Nothing changes. Recorded explicitly so "unrestricted" is a statement, not an absence. |
| `RegionRestricted` | Storage confined to the named regions. |
| `CountryRestricted` | Storage confined to the named country. **Blocks production upload** until a compliant location exists. |
| `NoThirdPartyAI` | Disables AI analysis for the affected project. |
| `NoCloudStorage` | Blocks production upload for the affected project. |

Two enforcement facts, both checked:

- A project bound to a rule that blocks third-party AI has `AIAnalysisEnabled = FALSE` (GOV-15), and only that project — the others are unaffected (SEG-12).
- Every assignment carries `VerifiedFromContract`, which starts `FALSE`. **An unverified assignment means the contract has not been read**, and production upload for that project stays blocked (GOV-14).

Disabling AI removes assistance. It never removes a control: the reviewer still reviews, the
approval still binds to a hash, the report still requires human-approved evidence.

## 3. Data-flow map

What would leave the company's tenant, to where, once each phase is authorised. **In Phase 1 none of
this happens: no service is connected** (D-14).

| Flow | Data | Class | Destination | Phase | Condition |
|---|---|---|---|---|---|
| Capture app → operational store | Structured records, photographs | ClientConfidential | Company Workspace tenant | 2 | Tenant is company-owned; Shared Drive preferred (D-03) |
| Operational store → orchestration | Record identifiers, statuses, **no file content** | Internal | Orchestration platform (EU/US regions) | 3 | Payloads minimised to identifiers |
| Orchestration → storage | File metadata, folder operations | ClientConfidential | Company tenant | 3 | Originals never leave the tenant |
| Orchestration → AI provider | **A downscaled derivative image plus minimal metadata** | ClientConfidential | AI provider | 4 | Only where `AIAnalysisEnabled` and no blocking residency rule |
| Orchestration → AI provider | Structured approved records for narrative drafting | ClientConfidential | AI provider | 5 | Same condition |
| Orchestration → accounting | Invoice lines, customer and item identifiers, totals | Financial | Accounting platform | 7 | After finance approval and reconciliation |
| Release → client | Approved document only | ClientConfidential | Named authorised recipients | 7 | Released status and a recipient snapshot |

Two properties worth stating plainly:

1. **Original evidence never leaves the tenant.** AI analysis receives a *derivative*, which also protects the write-once original from being opened by any processing path at all (P-07, D-13).
2. **Orchestration payloads carry identifiers, not content**, so the workflow layer holds as little client data as the work allows.

## 4. Subprocessors and likely processing locations

Stated as what must be **verified**, not as fact. No provider configuration has been inspected
(D-14).

| Processor | Role | Likely processing location | To verify |
|---|---|---|---|
| Google Workspace | Storage, spreadsheets, documents, capture platform | Provider-selected regions; **no Qatar data region exists** (P-08) | Whether data-region controls are available on the licensed plan, and which regions |
| Make.com | Orchestration | EU or US per organisation setting | Organisation region; what is retained in execution history and for how long |
| Anthropic (Claude API) | Evidence analysis, narrative drafting | Provider infrastructure | Retention and training terms for API traffic; whether they satisfy client contracts |
| Intuit (QuickBooks Online) | Accounting | Provider region for the company file | Region and edition of the existing company file (D-07) |
| Email provider | Notification and release delivery | Company tenant | Whether release delivery is permitted to leave the tenant unencrypted |

## 5. Contract-review checklist

For each client contract, particularly government and semi-government. The answers become
`ResidencyRequirements` and `ResidencyAssignments` rows; until they exist, the project's assignment
stays `VerifiedFromContract = FALSE` and production upload is blocked.

1. Does the contract restrict **where** data may be stored or processed (country, region, on-premise)?
2. Does it restrict **who** may process data — does engaging a subprocessor need written consent?
3. Does it treat photographs of the site as confidential information? Under what conditions may they be transmitted?
4. Does it prohibit or restrict **automated or AI processing** of project data?
5. Does it require data return or destruction at contract end, and on what timetable?
6. Does it impose a retention period that differs from the company's own policy?
7. Does it restrict who may receive reports — named individuals, or a role?
8. Does it require a particular report format, template or language?
9. Does it require notification of a security incident, within what period, to whom?
10. Does it grant audit rights over the company's systems or records?
11. Does it restrict storage on personally-owned devices used in the field?
12. Does it require the company to hold particular certifications, and are any at risk from this system?

## 6. What is blocked until the review happens

| Blocked | Not blocked |
|---|---|
| Uploading real client photographs or records to production storage | Phase 1 schema, security model, synthetic data, documentation, platform evaluation |
| Enabling AI analysis for an affected project | Building the AI integration against synthetic derivatives |
| Releasing a document to a client under an unreviewed contract | Generating drafts internally |

**No real MOEHE, school, government, client, employee or financial data may be uploaded during
Phase 1** (D-12). Nothing in this repository contains any.
