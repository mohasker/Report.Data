# Approval and Delegation Model

**Document ID:** AH-SYS-P1-010 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Validated Locally · Submitted for Owner Review
**Delivers:** D-15 items 6 and 14 · **Implements:** D-09 · **Relates to:** ADR-0006, R-07
**Evidence:** `17-validation-evidence.md` (TRN-11 … TRN-20, GOV-08)

---

## 1. Stages

| Stage | What it authorises | MVP approver |
|---|---|---|
| `EvidenceReview` | A visit and its individual photographs become usable in a report | Technical reviewer or project manager, per project |
| `TechnicalReview` | A generated document is technically correct | **General Manager** |
| `FinanceReview` | A financial calculation is correct (Phase 6/7) | **General Manager**, with a finance reviewer as backup |
| `Release` | A document may leave the company | **General Manager** |
| `OverrideAuthorisation` | A rule is deliberately waived | **General Manager** |

The General Manager is the final technical, financial and release approver for the MVP (D-09). The
structure supports delegation from the start, so appointing a delegate later needs no redesign —
which matters, because the company's own assessment names reliance on one person as a weakness
(R-07).

## 2. Routing

`ApprovalMatrix` rows resolve an approver from **project × stage × document type**, most specific
first:

```
project + stage + document type  →  project + stage  →  company default for stage
```

Every project resolves an approver at every required stage, or the configuration is incomplete —
asserted by TRN-12 across every fixture project. `BackupUserID` may remain unassigned until before
go-live (D-09), and is tracked as EF-07.

## 3. Delegation

A delegation is a **temporary, bounded transfer of the right to act**, never a transfer of
accountability. The accountable approver remains the person the matrix names.

| Field | Rule |
|---|---|
| `FromUserID` | The accountable approver |
| `ToUserID` | The acting delegate. May be unassigned until before go-live |
| `ApprovalStage` | A single stage, or null for every stage the delegator holds |
| `Scope` | All projects, specific projects, or a specific stage |
| `ProjectIDs` | Required when the scope is specific projects |
| `ValidFrom` / `ValidTo` | Both mandatory. **No delegation is open-ended** (TRN-18) |
| `Reason` | Mandatory |
| `AuthorisedByUserID` | Who authorised the delegation |
| `RevokedAt` / `RevokedByUserID` | Revocation is recorded, never deleted |

A delegation is valid only when it is active, unrevoked, inside its window, and covers this stage
and this project. Each of those four conditions is tested separately, because each fails
differently:

| Condition | Check |
|---|---|
| Valid inside window, stage and project | TRN-13 |
| Expired | TRN-14 |
| Revoked | TRN-15 |
| Used for a stage it does not cover | TRN-16 |
| Used on a project it does not cover | TRN-17 |

When a delegate decides, the `Approvals` row records **both** identities: `RequestedFromUserID` (the
accountable approver) and `DecisionByUserID` (who actually acted), plus the `DelegationID` that
permitted it. The decision reads as `Delegated`, so the audit trail says exactly what happened
rather than implying the accountable person was present.

## 4. What no one may do

1. **Approve their own restricted transaction because an approver is unavailable** (D-09). Every approval route carries `SelfApprovalProhibited = TRUE` (TRN-11), and it is not configurable to `FALSE` for financial stages. The correct answer to an absent approver is a recorded delegation, not a shortcut.
2. **Approve evidence they submitted.** Enforced as a precondition on the transition, not as a convention.
3. **Manufacture an approval.** Neither administrator role, nor break-glass access, has create or update access to `Approvals` (GOV-08).
4. **Approve with an expired, revoked or out-of-scope delegation** (TRN-14 … TRN-17).
5. **Delegate to the person who originated the item being approved** — otherwise delegation becomes a route around rule 2.

## 5. Approval binds to content

Every `Approvals` row stores `EntityVersion` and `ContentHash`. Before any release, posting or send,
the hash is recomputed and compared.

A mismatch voids the approval **and every approval downstream of it**, with `VoidedAt` and
`VoidReason` recorded. The document returns to `RevisionRequired` and a new revision is created; the
superseded revision is retained. Full mechanics in `02-key-id-and-hash-strategy.md` §3.

The practical effect: *"approved"* is a verifiable statement about specific content, not a record
that someone once clicked a button.

## 6. Overrides

An override waives a rule — an evidence requirement, a cumulative-quantity limit. It is an
`Approvals` row with `IsOverride = TRUE`, an `OverrideReason` and an authoriser, surfaced on the
audit dashboard as an override.

The calculation engine enforces the same thing in code: certifying beyond contract plus approved
variation raises an error unless an override carrying **both** an approver and a reason is supplied
(CALC-14, CALC-16, CALC-17).

## 7. What still has to be decided

| Item | Needed by | Tracked as |
|---|---|---|
| Named delegate for each gate | Before go-live | EF-07 |
| Whether any project needs a two-step technical approval | Phase 2 configuration | Configuration, not a blocker |
| Whether a client's acceptance should ever be recorded as an approval stage | Post-MVP | Today it is recorded as a *claim*, never an approval (A-20) |
