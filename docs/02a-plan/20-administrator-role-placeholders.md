# Administrator Role Placeholders and Separation of Duties

**Document ID:** AH-SYS-P2A-020 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review
**No identity is assigned. No name or email address is invented** (asserted by check ACC-31)

---

## 1. The three placeholders

| Placeholder | Held by | Count required |
|---|---|---|
| `PrimarySystemAdministrator` | To be named | 1 |
| `BackupSystemAdministrator` | To be named | 1 — **or** an approved documented recovery route instead |
| `GeneralManager/SystemOwner` | The owner | 1 |

Until real identities are supplied, the synthetic accounts in the fixtures stand in for them, all on
the reserved `@synthetic.example` domain.

## 2. PrimarySystemAdministrator

**Purpose:** keep the system running. Not to run the business in it.

| Responsibility | Detail |
|---|---|
| Technical configuration | Vocabularies, activity catalogue, system behaviour |
| User provisioning | Create, disable and re-enable accounts; assign users to projects |
| Integration monitoring | Watch the error queue; classify and escalate failures |
| System health | Row counts, sync duration, storage headroom against the migration thresholds |
| Backup verification | Confirm exports ran and that a restore has actually been tested |
| First-line support | Answer "why can't I see this project" — usually an assignment, not a fault |

**Explicitly cannot:**

- Read any site visit, activity, photograph, snag, report or document.
- Read any contract, rate, invoice or tax configuration.
- Create, alter or delete an approval.
- Edit or delete anything in the audit log.
- Delete any row in any table.

**Recovery permissions:** can restore another administrator's access, re-enable a disabled account,
and re-point a broken integration connection. Cannot grant themselves business-content access,
because no role in the matrix carries both.

## 3. BackupSystemAdministrator

**Purpose:** the system must not become unrecoverable because one person is unreachable.

Identical permissions to the primary. The difference is operational, not technical:

| Aspect | Rule |
|---|---|
| Normal use | Dormant. Does not perform day-to-day administration |
| Activation | When the primary is unavailable, or their account is compromised or disabled |
| Credentials | Held separately from the primary's — a second person, or a sealed record the owner controls |
| Verification | Signs in **at least quarterly** to confirm the account still works. An untested recovery account is a hope, not a control |
| Recording | Every use is in the audit log like any other administrator action |

**If no second person can hold this**, the alternative the owner may approve is a **documented
recovery route**: a written procedure, held where the owner can reach it without the administrator,
that restores administrative access. It must be **tested at least once before go-live**, with the
result recorded.

Either the backup account or the tested documented route must exist before go-live. **Neither is
optional** — one of them is.

## 4. GeneralManager / SystemOwner

**Purpose:** the business authority. Approves, releases, and owns the outcome.

| Responsibility | Detail |
|---|---|
| Technical approval | Evidence and documents |
| Financial approval | Invoice requests, from Phase 6 |
| Release | The decision that a document may leave the company |
| Override authorisation | Waiving an evidence rule or a quantity limit — recorded as an override, with a reason |
| Access grants | Authorising time-bound auditor access and break-glass, once those are enabled |
| Business decisions | Which projects exist, who works on them, what is billed |

**Explicitly cannot:** edit the audit log; approve a transaction they originated where the matrix
prohibits self-approval; bypass content hashing to release changed content under an old approval.

## 5. Separation of duties

The point of three placeholders rather than one: **no single account can both do the work and
approve it, or both change the configuration and read the results.**

| Boundary | Enforced how | Why it matters |
|---|---|---|
| **Administration vs business content** | The technical administrator has no read access to evidence, documents or financial records | An administrator troubleshooting a sync fault has no reason to open a client's photographs |
| **Administration vs approval** | Neither administrator can create or alter an approval | An administrator must never be able to manufacture an authorisation |
| **Doing vs approving** | Self-approval is prohibited on every route | The person who submitted evidence cannot approve it |
| **Configuration vs audit** | The audit log is append-only for every role | No one can tidy away what they did |
| **Primary vs backup** | Credentials held separately | A compromise of one account is not a compromise of recovery |
| **Business vs technical authority** | The owner approves; the administrator enables | The owner cannot be locked out by an administrator, and an administrator cannot approve business outcomes |

## 6. What must be decided before go-live

| # | Decision | Blocks |
|---|---|---|
| 1 | Who holds `PrimarySystemAdministrator` | Phase 2B |
| 2 | Who holds `BackupSystemAdministrator`, **or** approval of a documented recovery route instead | **Go-live** |
| 3 | Where backup credentials are held, and who can reach them without the primary | Go-live |
| 4 | Who verifies the backup account quarterly | Go-live |
| 5 | A continuity mechanism for **approvals** — a delegate, or an agreed rule for what waits | **Go-live before any report, certificate or invoice is released operationally** |

Item 5 is the owner's own condition: delegation stays deferred for the controlled field test, and
becomes a go-live requirement before anything is released operationally.

## 7. What is deliberately absent

No name. No email address. No phone number. No credential, and no description of where a credential
is stored. This document says **what each role does and what it must never do**; who fills it is the
owner's decision, and inventing a placeholder name would be inventing a person.
