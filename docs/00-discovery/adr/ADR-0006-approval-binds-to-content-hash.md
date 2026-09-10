# ADR-0006 — Approvals bind to a content hash

**Status:** Proposed · **Date:** 2026-09-10 · **Relates to:** §5.18, C-06, I-3, R-30

## Context
§5.18 requires that an approval applies only to the recorded version and hash, and that any material
edit after approval invalidates downstream approvals. Without this, "approved" means only that
someone once clicked approve on something — which is not a control, and would not survive scrutiny
from a client or an auditor.

The specification does not define "material," and the definition is the whole difficulty. Too broad
and reviewers re-approve constantly until they stop reading. Too narrow and content can change
underneath an approval.

## Options
1. **Approve the record identifier only.** Simplest, and worthless — content can change freely afterwards.
2. **Approve a hash over every field.** Strictest, and unusable: a timestamp update or an internal comment would void an approval.
3. **Approve a hash over a canonical serialisation of output-affecting fields.** Requires an explicit, published field list.

## Decision
**Option 3.**

- `ContentHash` is computed over a **canonical serialisation** — a defined field order, defined normalisation of text, dates and numbers, and stable handling of child collections.
- **Included:** quantities, dates, statuses, descriptions, captions, the approved-photo set and its sequence, and every field that appears in or determines generated output.
- **Excluded:** presentation-only and system fields — `UpdatedAt`, UI ordering, internal comments, advisory AI fields.
- The included-field list is **published in the Phase 1 data dictionary and version-controlled**, so "what counts as material" is a documented, reviewable decision rather than an implementation accident.
- Every Approvals row stores `EntityVersion` and `ContentHash`.
- Before any release, posting or send, the hash is recomputed and compared. A mismatch voids the approval and every approval downstream of it, and forces a new revision.

## Consequences
**Positive.** "Approved" becomes a verifiable statement about specific content. Tampering after
approval is detectable rather than assumed impossible. This is what makes §14 criterion 11 testable.
**Negative.** Any change to the canonical field list changes every hash and must be treated as a
schema migration with its own decision record.
**Neutral.** Reviewers see explicitly when a re-approval is required and why — which is better than
never knowing.

## Revisit if
Reviewers report excessive re-approval in practice, in which case the included-field list is
narrowed deliberately and recorded — never by weakening the mechanism.
