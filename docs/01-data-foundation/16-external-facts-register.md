# External Facts Register

**Document ID:** AH-SYS-P1-016 · **Revision:** 1 · **Date:** 2026-09-11
**Delivers:** D-15 item 17 — every external fact still awaiting confirmation, categorised by the phase it blocks

> Each entry is a value or answer that **cannot be invented** (operating rule 2). Each names who can
> supply it, what it blocks, and what happens meanwhile. Nothing here blocks Phase 1, which is
> complete.

---

## Blocks nothing — Phase 1 is complete

Phase 1 ran entirely on local fixtures and synthetic data. No external fact was required, and none
was assumed.

## Blocks Phase 2 — building the capture and review application

| # | Fact | Who supplies it | Meanwhile |
|---|---|---|---|
| **EF-01** | The owning Google Workspace account, confirmation that the tenant is paid Workspace, and the Shared Drive that will hold operational storage (D-03, BQ-01) | Owner | The folder and permission model is designed; nothing is provisioned |
| **EF-03** | Capture platform plan and entitlements, verified from current official vendor information, using the requirements matrix in `12-appsheet-feature-to-plan-matrix.md` (D-04, BQ-02) | Owner, from the vendor | The matrix states what must be true; no plan or price is assumed |
| **EF-05** | Real supervisors and their actual devices for the Phase 2 field test, including both platforms if both are used (A-05, A-15) | Owner | Offline behaviour is claimed nowhere |
| **EF-06** | A named system administrator, and an alternate (A-19) | Owner | The role exists in the model with no one assigned |
| **EF-07** | Named delegates for technical, finance and release approval (D-09, BQ-07) | Owner | The GM is the sole approver; delegation is modelled and tested with synthetic delegations |
| **EF-13** | Working calendar, weekend days, public-holiday handling, and the monthly evidence cut-off day (OQ-01, OQ-02) | Owner | Configuration columns exist and are unset |
| **EF-14** | Whether gallery upload is permitted or capture is camera-only (OQ-05) | Owner | Both are supported by the model; policy decides |

## Blocks Phase 3 — storage and orchestration

| # | Fact | Who supplies it | Meanwhile |
|---|---|---|---|
| **EF-10** | Orchestration organisation and plan, including Data Store availability (D-05, BQ-03) | Owner | The contract in `14-orchestration-contract-and-runbook.md` is platform-independent |
| **EF-11** | Who receives operational alerts — administrator only, or the GM as well (OQ-12) | Owner | Alert recipients are a configuration variable |
| **EF-12** | Retention policy per classification and per project, and backup cadence with a named person to verify a restore (OQ-03, OQ-04) | Owner | Defaults exist in the classification table; nothing is ever auto-deleted |

## Blocks Phase 4 — AI evidence analysis

| # | Fact | Who supplies it | Meanwhile |
|---|---|---|---|
| **EF-04** | AI workspace and the **hard monthly spend cap** the owner authorises (D-06, BQ-04) | Owner | Prompts, schemas, minimisation rules and cost controls are specified; nothing is called |

## Blocks Phase 5 — document generation and issue

| # | Fact | Who supplies it | Meanwhile |
|---|---|---|---|
| **EF-02** | **Verified legal identity** from the current Commercial Registration: legal name EN and AR, CR number, establishment number, registered address, official contacts, authorised signatories, document footer (D-02) | Owner | `LEGAL_ENTITY_NAME_PENDING_VERIFICATION` is in place and asserted by GOV-03. **Blocks issue of any production document** |
| **EF-08** | The **existing manual numbering register**: the last number used in each series, and the company code (D-10, BQ-08) | Owner | Series are configured with illustrative formats; migration is implemented and tested (NUM-12). **No production number may be issued until the register is reviewed** |
| **EF-09** | Which clients contractually require Arabic or bilingual documents (D-11, BQ-09) | Owner | Bilingual architecture is delivered; Arabic template production is deferred |
| **EF-15** | The approved company logo, and any client-specific template requirement (OQ-09) | Owner | Template records exist in draft with no file attached |

## Blocks production upload for an affected project — not the system

| # | Fact | Who supplies it | Meanwhile |
|---|---|---|---|
| **EF-16** | **Contract review** for residency, confidentiality, third-party-processing and retention clauses, using the checklist in `09-data-classification-and-residency.md` §5 (D-12, BQ-10) | Owner, from the contracts | Every residency assignment is `VerifiedFromContract = FALSE`, which blocks production upload for that project. Phase 1, the security model and synthetic testing are unaffected |

## Blocks Phase 6 — certificates and invoice drafts

| # | Fact | Who supplies it | Meanwhile |
|---|---|---|---|
| **EF-17** | **Written confirmation of the tax treatment** applied to these contracts, from the accountant. "Zero-rated", "exempt", "out of scope" and "no tax configured" are distinct and none may be recorded without it (D-08, BQ-06) | Accountant | `TaxRules` holds an explicitly unconfirmed placeholder. The engine returns `UNDETERMINED` and blocks, and does **not** produce zero (CALC-01, GOV-04, GOV-05) |
| **EF-18** | Contract and BOQ source data for real projects | Owner | Synthetic contracts and BOQ items exercise the calculation engine |
| **EF-19** | Per-project payment terms, retention and advance arrangements | Owner | Configuration columns exist and are unset |

## Blocks Phase 7 — accounting synchronisation and release

| # | Fact | Who supplies it | Meanwhile |
|---|---|---|---|
| **EF-20** | The **compatibility inspection** of the current QuickBooks company file — the 24 questions in `13-quickbooks-mapping-and-inspection.md` §2 (D-07, BQ-05) | Accountant | Mapping fields are defined; the calculation layer is independent of the accounting product |
| **EF-21** | Chart-of-accounts, item, tax-code and class mappings | Accountant | Mapping columns exist and are empty |
| **EF-22** | Authorised recipients per client for released documents | Owner | `IsAuthorizedRecipient` exists and is set only in synthetic data |
| **EF-23** | Written authorisation to enable production accounting posting | Owner | `QBO_POSTING_ENABLED` defaults to FALSE (ADR-0008) |

---

## Summary

| Blocks | Count | Can Phase 1 proceed? |
|---|---|---|
| Nothing | — | **Phase 1 is complete** |
| Phase 2 | 7 | Only EF-01 and EF-03 are hard prerequisites for starting |
| Phase 3 | 3 | |
| Phase 4 | 1 | Phase 4 may be skipped entirely; the pipeline works without AI |
| Phase 5 | 4 | EF-02 and EF-08 block **issue**, not build |
| Production upload for a project | 1 | Per project, not system-wide |
| Phase 6 | 3 | EF-17 blocks issue of any invoice |
| Phase 7 | 4 | |

**23 outstanding external facts. None blocks Phase 1, and none has been guessed at.**
