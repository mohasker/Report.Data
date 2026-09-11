# Architecture Decision Records

Each ADR records one decision: its context, the options considered, the decision taken, its
consequences, and what would cause it to be revisited.

Status values: **Proposed** (awaiting owner approval) · **Accepted** · **Superseded** · **Rejected**.

The first eight were **Accepted** on 2026-09-11 with the Phase 0 approval. Four were amended by owner
decisions at the same time; the amendment is shown inside the ADR rather than rewritten over the
original reasoning. **ADR-0009 was accepted later the same day**, with the operational correction.

| ADR | Decision | Status |
|---|---|---|
| [0001](ADR-0001-shared-drive-ownership.md) | Company-owned Shared Drive, system-owned account | Accepted (D-03) |
| [0002](ADR-0002-google-sheets-as-mvp-store.md) | Google Sheets as the MVP store, behind a table contract | Accepted |
| [0003](ADR-0003-make-as-orchestrator.md) | Make.com as the orchestration layer | Accepted (D-05) |
| [0004](ADR-0004-ai-is-advisory-only.md) | AI output is advisory only and never authoritative | Accepted, rev 1 — amended by **D-06**: AI may pre-analyse **submitted** evidence to assist the reviewer; only **human-approved** evidence may generate an official report |
| [0005](ADR-0005-central-numbering-service.md) | One numbering service, many configurable series | Accepted, rev 1 — amended by **D-10**: series by entity/type/year/scope/client/revision, with a reserved → issued → cancelled lifecycle |
| [0006](ADR-0006-approval-binds-to-content-hash.md) | Approvals bind to a content hash | Accepted |
| [0007](ADR-0007-single-document-generation-path.md) | One document generation path (Google Docs → PDF) | Accepted, rev 1 — amended by **D-11**: templates keyed by type **and language**, RTL-capable from the start |
| [0008](ADR-0008-defer-accounting-integration.md) | Deterministic calculation before any accounting posting | Accepted, rev 1 — amended by **D-07**: QuickBooks Online is in use; capability for the current company configuration is inspected, not assumed |
| [0009](ADR-0009-capture-once-native-share.md) | Capture once, use twice, and share through the native share sheet | Accepted, rev 1 (**D-16 to D-24**) — one capture serves the contractor group and every report; **zero mandatory manual inputs** on the normal path; a human-confirmed activity sits beside the advisory one; analysis is filtered before it is paid for; `CAP-GATE` is the unverified platform requirement |
