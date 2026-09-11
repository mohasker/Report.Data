# Orchestration Contract and Operator Runbook

**Document ID:** AH-SYS-P1-014 · **Revision:** 1 · **Date:** 2026-09-11
**Implements:** D-05 · **Relates to:** ADR-0003, spec §8 and §12
**Status:** contract defined in Phase 1. **No scenario is created or connected** (D-14)

---

## 1. Scenario inventory

Each is an independent, reusable workflow with one job. Nothing calls another scenario directly;
they communicate through record state, which means any one can be rebuilt without touching the rest.

| # | Scenario | Trigger | Phase |
|---|---|---|---|
| 01 | Submission validation | Visit becomes `Submitted` | 3 |
| 02 | Evidence registration | New photograph synchronised | 3 |
| 03 | AI evidence analysis | Photograph eligible and project permits it | 4 |
| 04 | Review notification | Submission passes validation | 3 |
| 05 | Report job creation | Authorised user requests a document | 5 |
| 06 | Report generation | Job snapshot frozen | 5 |
| 07 | Approval and release | Technical approval recorded | 5 |
| 08 | Completion certificate | Certificate requested from approved quantities | 6 |
| 09 | Invoice draft | Certificate approved | 6 |
| 10 | Accounting synchronisation | Finance approval recorded | 7 |
| 11 | Approved email delivery | Release recorded | 7 |
| 12 | Scheduled monitoring | Daily, weekly, monthly | 3 |
| 13 | Backup and export | Scheduled | 3 |

## 2. The contract every scenario obeys

### 2.1 Never trust the trigger

A webhook payload is attacker-controllable in principle: it can be replayed or forged (SEC-01). So
every scenario:

1. **Re-reads the authoritative record by identifier.** Payload contents are a notification, never data.
2. **Re-validates authorisation server-side** against `ProjectAssignments` and the role matrix — the client's view of who may do what is irrelevant.
3. **Checks the project is in a state that permits the action.**

### 2.2 Idempotency before any side effect

```
key = {Scenario}:{EntityType}:{EntityID}:{TargetState}

claim(key)  ->  already claimed  ->  log DuplicateSuppressed, stop
            ->  claimed now      ->  perform the side effect
                                 ->  record the outcome against the key
```

A duplicate is **expected and suppressed**, not treated as an error (§14 criterion 7). The
`IntegrationJobs` table carries the key and attempt number with a uniqueness constraint, so a
duplicate cannot be recorded twice either.

### 2.3 Correlation

A correlation identifier is generated at the entry point and carried through every downstream call,
log line and alert. One identifier links a supervisor's submission to its validation, its file
registration, its AI analysis, its notification and any failure in between.

### 2.4 Failure classification and retry

| Class | Retriable | Policy |
|---|---|---|
| Validation | No | Record correctable errors, return to the submitter |
| Authentication / Authorization | No | Alert the administrator. Possible security event |
| RateLimit | Yes | Honour `Retry-After`, capped exponential backoff |
| Network / ProviderUnavailable | Yes | Capped exponential backoff, then dead-letter |
| FileMissing | Once | Sync latency is normal; one delayed retry, then dead-letter |
| SchemaMismatch | No | Dead-letter with the sanitised payload for diagnosis |
| Duplicate | No | Suppress and log |
| Conflict | No | Human resolution. Never auto-overwrite |
| Unknown | No | Dead-letter immediately with full correlation context |

Retries are capped. An exhausted job moves to the dead-letter queue with everything an operator
needs; it never disappears and never loops.

### 2.5 Payload minimisation

Scenarios pass **identifiers and statuses**, not content. The AI scenario is the one exception, and
it sends a **downscaled derivative**, never the original — which also means no processing path ever
opens the write-once file (D-13, P-07).

### 2.6 Secrets

Credentials live only in the platform's connection store. They never appear in a spreadsheet, a log,
an error message, a prompt, a document or this repository (GOV-01). Request and response summaries
recorded in `IntegrationJobs` are sanitised by construction.

### 2.7 Environment separation

Where the licensed plan allows, development and production are separate. Where it does not, the
separation is enforced by data: development scenarios run only against synthetic projects, and every
irreversible action (send, post, share, delete) is disabled by configuration until its phase is
authorised.

### 2.8 Connection ownership

Every connection is owned by the dedicated system account (ADR-0001), never by an individual. The
owner authorises each one personally in the provider's console. A connection owned by a person
leaves with that person.

---

# Operator runbook (outline)

Written for a competent non-developer. Completed in Phase 3, when the scenarios exist.

## A. Daily, five minutes

1. Open the error queue. Anything older than 24 hours is the priority.
2. For each entry, read the recommended action — every entry has one.
3. Validation errors go back to the supervisor, not to the administrator.
4. Authentication or authorisation errors are escalated immediately and never retried.

## B. When a submission will not validate

1. Open the record by its identifier. The specific errors are on the record.
2. Return it for correction with a clear note — the supervisor sees exactly what to fix.
3. If the same error recurs across supervisors, the **rule** is wrong, not the people. Raise it.

## C. When a report will not generate

1. Check the job's validation findings: `DATA GAP` items name what is missing.
2. Missing approvals are the usual cause. Evidence must be human-approved before it can appear.
3. If the job failed after a number was reserved, confirm the number was cancelled **with a reason** — a gap in the register must always be explainable.

## D. When an external service is failing

1. Confirm the class. Rate limits and outages resolve themselves; validation errors do not.
2. Do not re-run a scenario manually to "see if it works". The idempotency key will suppress it, and if it does not, you have created a duplicate.
3. Record what you observed against the correlation identifier.

## E. What an operator must never do

- Edit a record to make a validation error go away. Fix the cause.
- Approve on someone else's behalf. Use a recorded delegation.
- Re-use a cancelled document number.
- Copy a credential out of a connection store for any reason.
- Delete an error-queue entry without recording the resolution.

## F. Monthly

1. Review the oldest pending job and the retry-count dashboard.
2. Review row counts and sync duration against the migration threshold (`07-migration-and-versioning.md` §3).
3. Review AI usage against the spend cap.
4. Confirm the backup export ran, and that a restore has been tested at least once this quarter — an untested backup is a hope, not a control.
