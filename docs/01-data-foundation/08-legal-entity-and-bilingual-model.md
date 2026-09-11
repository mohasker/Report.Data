# Legal Entity and Bilingual Model

**Document ID:** AH-SYS-P1-008 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Validated Locally · Submitted for Owner Review
**Delivers:** D-15 items 7 and 10 · **Implements:** D-02, D-11 · **Closes:** C-01
**Evidence:** `17-validation-evidence.md` (LNG-01 … LNG-13, GOV-03)

---

# Part 1 — Legal entity

## 1.1 Why this is master data and not a setting

The specification gives the company's name as "L.L.C."; another internal source gives "W.L.L." for
the same company. Both cannot be right, and the wrong form on an invoice or a completion certificate
submitted to a government client is a documentation defect.

The owner's decision was not to choose. Legal identity becomes configurable master data with a
pending placeholder, and the verified name is taken from the **current Commercial Registration**
before any production document is generated (D-02).

This also makes the platform multi-entity from the first version: a second registered entity is a
row, with its own numbering series, logo, footer and signatories (NUM-05, CFG-09, CFG-12).

## 1.2 What a legal entity carries

`LegalEntityID` · `EntityCode` (used in document numbers) · legal name EN **and** AR · trade name EN
and AR · commercial registration number · establishment/card number · tax registration number and
**status** · registered address EN and AR · country · currency · official email, telephone and
WhatsApp · approved logo reference · document footer EN and AR · authorised signatories ·
`EffectiveFrom` / `EffectiveTo` · `Version`.

## 1.3 Rules

1. **The placeholder is explicit.** Synthetic and pre-verification data reads `LEGAL_ENTITY_NAME_PENDING_VERIFICATION` — a value no one can mistake for a real name. GOV-03 asserts it is still in place.
2. **Versioned, never overwritten.** Correcting the legal name creates a new version. Documents record the version used, so a document issued last year remains explainable even after the name is corrected.
3. **Stored once, referenced everywhere.** Templates reference the entity; they never carry a typed company name. One correction fixes every future document.
4. **Signatories carry no specimen signatures.** Only name, position and scope. A stored signature image is a forgery risk with no operational benefit.
5. **Tax registration status is not a tax position.** Its presence says nothing about what tax applies (D-08).

## 1.4 What is still blocked

Production issue of any invoice, certificate, quotation or external report is blocked until the
verified Commercial Registration details are entered. This blocks **document issue**, not Phase 1,
and not Phase 2 capture and review. Tracked as EF-02.

---

# Part 2 — Bilingual and right-to-left architecture

## 2.1 The decision

English may be the first generated-report language, but **the architecture supports English and
Arabic from Phase 1**, and Arabic must not require redesigning the database, templates, interface or
workflows later (D-11).

The earlier characterisation that Arabic "roughly doubles the work" is withdrawn. It applies to
authoring and visually inspecting an Arabic template set — real work, deferred to Phase 5b — not to
the system.

## 2.2 What is delivered now

| Requirement | How | Check |
|---|---|---|
| Bilingual master-data labels | Every English text column has an Arabic counterpart, with no exceptions | LNG-01 |
| Bilingual free text on operational records | Visit descriptions, activity descriptions, captions, snag descriptions all paired | LNG-12 |
| Bilingual controlled vocabularies | All 24 vocabularies carry an Arabic label for every value | LNG-10 |
| Reference data actually populated in Arabic | Roles, units, disciplines, all 34 activities, document types, classifications | LNG-11 |
| User language preference | `Users.Language`, in use in the fixtures in both values | LNG-03 |
| Text direction as data | `Languages.Direction` (LTR/RTL), and `DocumentTemplates.TextDirection` stored explicitly so RTL is testable rather than inferred | LNG-02, LNG-04 |
| Per-language approved templates | `DocumentTemplates` keyed by type **and** language; an Arabic template already exists in draft | LNG-04 |
| Per-project document language | `Projects.DefaultDocumentLanguage`; one fixture project defaults to Arabic | LNG-05 |
| Unicode integrity end to end | Arabic passes through canonical serialisation unchanged; NFC normalisation alters nothing | LNG-07, LNG-08 |
| Arabic-Indic digits preserved | Never silently converted to Western digits | LNG-09 |

## 2.3 No transliteration, ever

Two rules, both enforced:

1. **An Arabic name is never written into an English column** to satisfy a required field (LNG-13).
2. **A client may be registered only in Arabic.** `Clients.LegalNameEN` is therefore *not* required; the constraint is "at least one legal name in either language" (LNG-06).

The second point is a change made *because* of a fixture. `CLI-0002` was created with an Arabic-only
legal name to see what would break, and the required English column broke. Forcing an English legal
name would have invited an invented transliteration that is not the client's legal name — so the
model changed, not the fixture. That is the right direction for a correction to travel.

## 2.4 What remains deferred

| Deferred | Phase | Why |
|---|---|---|
| Authoring the Arabic template set | 5b | Layout work with its own visual-inspection matrix |
| Page-by-page RTL PDF inspection, including mixed-direction text inside tables | 5b | Genuinely hard, and only testable against real templates (P-10) |
| Arabic narrative generation and its QA pass | 5b | Needs the Arabic templates first |
| Which clients contractually require Arabic | Before 5b | An outstanding external fact, EF-09 |

Deferring template production costs nothing later, because none of it requires a schema, workflow or
interface change. That is the whole point of doing the architecture now.
