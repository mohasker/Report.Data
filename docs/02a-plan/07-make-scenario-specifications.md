# Make Scenario Specifications and Disabled Blueprints

**Document ID:** AH-SYS-P2A-007 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review · **No scenario created, no webhook live**

> The blueprints in `blueprints/` are **specifications in JSON form**, authored here and deliberately
> marked disabled. They are not exports from a live account — no account exists. They describe module
> order, filters, mappings, error routes and idempotency so that a Phase 3 implementer builds the
> same thing that was designed.

---

## 1. Scenarios in scope for Phase 3

| # | Scenario | Trigger | Side effect | Idempotency key |
|---|---|---|---|---|
| 01 | Submission validation | Visit → `Submitted` | Status change, validation findings | `S01:SiteVisit:{VisitID}:Submitted` |
| 02 | Evidence registration | New photograph synced | File routed, checksum recorded | `S02:Photo:{PhotoID}:Registered` |
| 04 | Review notification | Validation passed | One email to the reviewer | `S04:SiteVisit:{VisitID}:Notified` |
| 12 | Daily monitoring | Schedule | Consolidated alert | `S12:Daily:{YYYY-MM-DD}` |
| E | Error queue writer | Any error route | Dead-letter row | `ERR:{CorrelationID}:{AttemptNumber}` |

Scenarios 03, 05–11 and 13 are specified in
`../01-data-foundation/14-orchestration-contract-and-runbook.md` and built in their own phases.

## 2. The contract every scenario obeys

```
1  receive trigger            treat the payload as a NOTIFICATION, never as data
2  re-read the record         by identifier, from the authoritative store
3  re-validate authorisation  server-side, against ProjectAssignments and the role matrix
4  claim the idempotency key  BEFORE any side effect
       already claimed -> log DuplicateSuppressed, stop
5  perform the side effect
6  record the outcome         IntegrationJobs row: correlation ID, sanitised summaries, status
   on error:
       classify -> Validation | Authentication | Authorization | RateLimit | Network |
                   ProviderUnavailable | FileMissing | SchemaMismatch | Duplicate |
                   Conflict | Unknown
       retriable and under cap -> backoff and retry
       otherwise               -> dead-letter with a recommended operator action
```

Step 1 is the security posture: a webhook payload is attacker-controllable in principle, by replay
or forgery (SEC-01). Step 4 is what makes duplicate triggers harmless (§14 criterion 7).

## 3. Scenario 01 — submission validation, module by module

| # | Module | Configuration | Error route |
|---|---|---|---|
| 1 | Custom webhook | Shared secret in the connection store. **Payload used only for `VisitID` and `CorrelationID`** | — |
| 2 | Data store: claim key | `S01:SiteVisit:{VisitID}:Submitted`; if present → route to "duplicate suppressed" | — |
| 3 | Read record | Read `SiteVisits` by `VisitID` from the authoritative store | `FileMissing` → one delayed retry |
| 4 | Filter | `WorkflowStatus = "Submitted"` — a record already moved on is not reprocessed | — |
| 5 | Read children | `VisitActivities` and `Photos` for this visit | — |
| 6 | Validate authorisation | Submitter holds an active assignment with `MaySubmitEvidence` | `Authorization` → **never retried**, alert |
| 7 | Validate project | `Projects.Status = "Active"` | `Validation` → not retried |
| 8 | Validate evidence rules | Effective rule per activity: photographs, quantity, unit, captions | `Validation` |
| 9 | Validate integrity | Location belongs to the project; children carry the same `ProjectID` | `Validation` |
| 10 | Router | Pass → module 11; fail → module 13 | — |
| 11 | Update status | `UnderTechnicalReview`, write `EntityVersion` and `ContentHash` | `Conflict` → dead-letter |
| 12 | Trigger Scenario 04 | Pass `CorrelationID` | — |
| 13 | Record failure | `ValidationFailed` with the specific correctable errors | — |
| 14 | Write `IntegrationJobs` | Sanitised summaries only. **Never a payload, never a credential** | — |

## 4. Scenario 02 — evidence registration

Registers the synced photograph, obtains the storage file ID and metadata, takes the checksum **from
the storage provider's own metadata** rather than downloading the file (C-03), routes the original
into `01_Original_Evidence` without overwriting, and creates a derivative in `02_Derived_Images`.

Two rules that are not negotiable:

- **The original is created, never updated.** If a file with that identifier is already registered, the key is already claimed and the scenario stops.
- **The derivative is a separate file with its own record.** Nothing writes a modified image back over an original.

## 5. Blueprints

| File | Scenario | State |
|---|---|---|
| `blueprints/s01-submission-validation.blueprint.json` | 01 | `"enabled": false` |
| `blueprints/s02-evidence-registration.blueprint.json` | 02 | `"enabled": false` |
| `blueprints/s04-review-notification.blueprint.json` | 04 | `"enabled": false` |

Each carries `"__specification_only": true` and `"__not_connected": true`, contains no URL, no
secret, no account identifier and no connection reference, and will not run if imported without an
implementer completing the connections deliberately.

## 6. What is required before Phase 3

| Requirement | Status |
|---|---|
| Orchestration organisation and plan, with Data Stores | **Pending (EF-10)** |
| Real operation-consumption measurement to size the plan | Phase 3 |
| Workspace and Shared Drive | **Pending (EF-01)** |
| Webhook secrets, authorised by the owner in the provider's console | Phase 3 |
| Alert recipients | **Pending (EF-11)** |

## 7. What Phase 3 must prove

1. A duplicate or replayed trigger produces **one** job — recorded.
2. An original is byte-identical after registration — checksum comparison recorded.
3. Each failure class injected deliberately produces a queue entry with a correlation ID, an entity ID and a recommended action.
4. Provisioning run twice creates no duplicate folder.
5. Real operation consumption measured, so the plan tier is sized from measurement rather than a guess.
6. No evidence folder is publicly accessible — permission audit recorded.
