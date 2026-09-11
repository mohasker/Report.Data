# ADR-0007 — One document generation path: Google Docs template → PDF

**Status:** Accepted (rev 1, amended by D-11) · **Date:** 2026-09-10 · rev 1 2026-09-11
**Relates to:** C-05, S-02, D-11, §10, P-10

## Context
§3 and §16 refer to "Word/Google Docs and PDF" output. Producing a natively styled `.docx` and
producing a Google Doc from a template are different mechanisms, with different fidelity
characteristics and different failure modes. Building both means maintaining two template sets and
performing the §10 page-by-page visual inspection twice, for every revision, forever.

## Options
1. **Google Docs template → merge → export PDF (and `.docx` on request).** One template, one merge path, one inspection.
2. **Native `.docx` generation → convert to PDF.** Better native Word fidelity; a separate toolchain, separate failure modes, and harder for a non-developer to edit the template.
3. **Both, maintained in parallel.** Double the work for a benefit no client has yet requested.

## Decision
**Option 1.** The controlled template is a Google Docs file, versioned in `DocumentTemplates` and
referenced by Drive file ID. The editable draft is a Google Doc; the PDF is exported from it; a
`.docx` is exported from the same approved Doc when a client requires that format.

## Consequences
**Positive.** One template to control, one merge path to test, one visual inspection per revision.
Templates are editable by the owner without a developer. Revision control fits naturally into
`DocumentTemplates`.
**Negative.** Exported `.docx` styling fidelity is whatever the export produces, not what a native
Word toolchain would author. Complex layouts must be verified against the §10 checklist — which is
required regardless.
**Neutral.** Arabic and right-to-left layout risk (P-10) applies to any generation path.

**Amended by D-11.** Templates are keyed by document type **and language**, and the merge path must
carry right-to-left capability from the start — bilingual placeholders, Unicode throughout, no
transliteration of Arabic names, and per-language approved template records. An Arabic template is
then a new controlled template, not a new mechanism. Only the authoring and visual inspection of the
Arabic template set is deferred to Phase 5b.

## Revisit if
A client contractually requires native Word documents with specific styling that export cannot
achieve.
