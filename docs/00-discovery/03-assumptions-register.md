# Assumptions Register

**Document ID:** AH-SYS-P0-003 · **Revision:** 0 · **Status:** draft for owner approval

Every item below is an **assumption, not a verified fact**. Nothing here was confirmed against a
live account, because no account access was provided and none was requested in chat (operating
rules 2 and 3).

**How to use this register:** the owner marks each row Confirmed, Corrected or Rejected. An
assumption that reaches its "Must be confirmed by" phase while still unconfirmed becomes a blocker
for that phase.

Legend — **Impact if wrong:** 🔴 redesign · 🟠 significant rework · 🟡 local change

| ID | Assumption | Basis | Impact | Confirm by | Status |
|---|---|---|---|---|---|
| **A-01** | Al-Haram has a **paid Google Workspace** tenant on its own domain (not consumer Gmail), giving Shared Drives, admin control, per-user licensing and audit logging. | The company operates a domain (`alharam.qa`) and a company mailbox. | 🔴 | Phase 1 | ☐ |
| **A-02** | An **AppSheet plan including webhooks and the AppSheet API** will be licensed. Without both, AppSheet cannot trigger Make and Make cannot write status back — the pipeline does not exist. | §4 names AppSheet as the capture layer and §8 requires webhook triggers. | 🔴 | Phase 2 | ☐ |
| **A-03** | A **Make.com organisation** will be available on a plan with Data Stores, error handlers and scheduled scenarios. | §8 requires idempotency stores, error routes and scheduled monitoring. | 🟠 | Phase 3 | ☐ |
| **A-04** | A **Claude API workspace with a hard monthly spend cap** will be provided. | §9 and operating rule 4. | 🟡 | Phase 4 | ☐ |
| **A-05** | Field users have **working smartphones with cameras** and each has an **individual sign-in identity**. Shared logins are not acceptable — they destroy attribution, and attribution is the purpose of the audit trail. | §7.4 requires sign-in and `USEREMAIL()` identity. | 🟠 | Phase 2 | ☐ |
| **A-06** | The **legal name, CR number, logo and contact block** for client documents will be supplied as controlled reference data. The specification says "L.L.C."; another internal company source says "W.L.L." — see conflict **C-01**. Only one can be correct on an invoice or certificate. | §2 vs. internal knowledge base. | 🟠 | Phase 1 | ☐ |
| **A-07** | **No VAT is currently charged** on these Qatar contracts. The system is nonetheless built tax-rule-driven with a named zero-rate rule, so a future tax regime is a configuration change rather than a rebuild. **Must be confirmed in writing by the company's accountant** — the system will not assume a tax position (§11). | §11 explicitly forbids assuming VAT applies or does not. | 🔴 (financial/legal) | Phase 6 | ☐ |
| **A-08** | Default currency is **QAR** and MVP projects are single-currency. Multi-currency inputs are validated and rejected rather than silently mishandled. | §11. | 🟡 | Phase 6 | ☐ |
| **A-09** | MVP reporting frequency is **monthly, calendar-month aligned**, with an agreed cut-off day for late evidence. | §5.3 `ReportingFrequency`; internal knowledge base describes monthly landscape reports. | 🟡 | Phase 2 | ☐ |
| **A-10** | MVP document output language is **English**, with Arabic labels and help text inside the app. Arabic or bilingual client documents are separate, explicitly approved scope. | §7.1; gated by **BQ-09**. | 🟠 | Phase 5 | ☐ |
| **A-11** | Photographic evidence is **client-confidential but not classified**, and may be stored in Google's cloud under the company's Workspace tenant. Government clients may impose stricter terms — see **R-04**, **BQ-10**. | Standard practice; unverified against contracts. | 🔴 | Phase 1 | ☐ |
| **A-12** | The **General Manager may act as sole technical approver** during the MVP, while the approval matrix is designed for delegation so that appointing a delegate later requires no redesign. | §2 approval matrix; **R-07** key-person concentration. | 🟡 | Phase 2 | ☐ |
| **A-13** | **Three synthetic projects** — different clients, disciplines, locations, users, templates and approval routes — are acceptable for proving segregation before real client data is entered. | §15 Phase 2. | 🟡 | Phase 2 | ☐ |
| **A-14** | Project, client and location registers **exist in some exportable form** (spreadsheets, proposals, contracts) and can be imported under control rather than retyped. | §17; A-14 is a schedule risk if false. | 🟠 | Phase 1 | ☐ |
| **A-15** | The company accepts that **offline behaviour is bounded by what AppSheet actually supports on real devices**, and that no offline claim will be made until device testing is executed and recorded. | §7.5 and operating rule 1. | 🟡 | Phase 2 | ☐ |
| **A-16** | Supervisors capturing evidence are **literate in the app's chosen interface language** at the level needed to select values and write a short description. Where they are not, the design leans further on choices over free text. | Adoption risk **R-06**. | 🟠 | Phase 2 | ☐ |
| **A-17** | Photograph volume is on the order of **tens per project per month**, not thousands per day. This determines whether Google Sheets is viable as the MVP store (**R-01**, ADR-0002). | Order-of-magnitude planning estimate only. **Not a measurement.** | 🔴 | Phase 1 | ☐ |
| **A-18** | Existing manual documents already use **some numbering series** (proposals, reports, invoices). The system must continue those series without collision rather than restart them. | **BQ-08**, **R-05**. | 🟠 | Phase 5 | ☐ |
| **A-19** | The company can nominate a **system administrator** (a person, not the GM alone) to maintain master data, onboard projects and work the error queue. | §15 Phase 8 and operational sustainability. | 🟠 | Phase 2 | ☐ |
| **A-20** | Client representatives may **acknowledge work on site informally**; the MVP records this as a claim (`ClientAcknowledgementStatus`, `ClientRepresentative`) and does **not** treat it as a client approval. | §5.8; operating rule 11. | 🟡 | Phase 2 | ☐ |

## Dependency list

External dependencies, with what fails if each is unavailable.

| Dependency | Needed from | If unavailable |
|---|---|---|
| Google Workspace tenant + Shared Drive | Phase 1 | **Stop.** No storage foundation. |
| AppSheet plan with webhook + API | Phase 2 | App can be built; automation cannot trigger. Pipeline stops at capture. |
| Google Drive storage quota | Phase 3 | Evidence registration fails. Quota must be sized against A-17. |
| Make.com organisation | Phase 3 | Fall back to Google Apps Script (ADR-0003) — cheaper in licence, more expensive in maintenance and far less visible to a non-developer. |
| Claude API key + spend cap | Phase 4 | Evidence analysis and narrative drafting unavailable; reports become fully manual to write but the pipeline still functions. |
| Approved document templates + logo | Phase 5 | No document generation. |
| Contract and BOQ source data | Phase 6 | No certificates, no invoices. |
| QuickBooks company + sandbox | Phase 7 | No accounting integration; invoices remain drafts for manual entry. |
| Named approvers with email addresses | Phase 2 | No approval routing; nothing can be released. |
| Real supervisors and devices for field testing | Phase 2 gate | Cannot evidence acceptance criteria or offline behaviour. |
