# Make Account Inspection — Read-Only Record

**Document ID:** AH-SYS-P2A-015 · **Revision:** 2 · **Date:** 2026-09-11
**Status:** Completed · **Verified from the live account** — the first verified external fact in this project
**Authorisation:** the owner's read-only inspection authorisation of 2026-09-11

---

## 1. What was inspected, and what was not

**Read-only calls executed — six:**

| # | Call | Purpose | Result |
|---|---|---|---|
| 1 | `environment_get` | Zone, organisations, teams | Returned |
| 2 | `organizations_get` | Plan, limits, consumption | Returned in full |
| 3 | `scenarios_list` | Active scenarios | Returned 7 |
| 4 | `data-stores_list` | Existing data stores | Returned empty |
| 5 | `apps_list` | Available integrations | Returned 60 |
| 6 | `apps_recommend` | Whether an AppSheet connector exists | Returned |

**Deliberately not called**, although the connector offers them:

| Not called | Why |
|---|---|
| `connections_list` | Edges toward connection inspection, which the authorisation restricts. `apps_list` answers the integration question without touching the company's configured connections |
| `hooks_list`, `keys_list` | Not needed; both are adjacent to credentials and webhooks |
| `executions_list`, `executions_get` | Would read the content of past runs, which is business data |
| Anything that creates, edits, activates, deactivates, deletes, runs, or changes billing | Explicitly prohibited |

**Nothing was created, changed, activated, run or deleted. No credential or secret was read or
revealed.** Personal identifiers returned by the API are deliberately not reproduced in this
repository.

## 1b. Scenario counts — the ambiguity corrected

Revision 1 put "seven scenarios exist, all inactive" in one section and "Active scenarios: 2" in
another. Those described **different things** and reading them together was reasonable and wrong.
Stated separately, from the same inspection:

| # | Question | Answer | Source field |
|---|---|---|---|
| 1 | **Total scenarios present in the account** | **7** | `scenarios_list` returned 7 records |
| 2 | **Currently active** | **0** | Every record has `isActive: false`; the organisation reports `activeScenarios: 0` |
| 3 | **Currently inactive** | **7** | All of them |
| 4 | **Maximum active scenarios allowed by the Free plan** | **2** | `license.scenarios: 2` |
| 5 | **What "2" describes** | **The plan limit — a ceiling, not a count.** Nothing is running | `license.scenarios` is a licence field, not a usage field |

So: **7 exist, 0 run, and at most 2 may run at once.** The design needs five, which is why the
prototype is reduced to two ([`23-operations-budget.md`](23-operations-budget.md) §5).

Nothing was activated, deactivated or changed. The account is exactly as it was found.

## 1c. Boundary maintained, and the convention for anything new

The existing scenarios were listed and nothing more. **They may belong to unrelated company work and
must not be modified, renamed, activated, deleted or reused without separate authorisation.** None
was opened, no execution history was read, and no connection, key or webhook was inspected.

Any future Al-Haram Field Reporting scenario will be created under a convention that keeps it
visibly separate from existing work:

| Rule | Value |
|---|---|
| **Folder** | A dedicated folder, `AHFR` — nothing outside it belongs to this project |
| **Naming** | `AHFR-S01 Submission validation`, `AHFR-S12 Monitoring digest` — the prefix, the scenario number from the design, then the purpose |
| **Ownership** | Owned by the dedicated system account, never by an individual |
| **Description** | Each scenario's description names this project, the design document it implements, and the date it was created |
| **Labels** | A scenario label `al-haram-field-reporting`, so the set can be listed and audited as a group |
| **Connections** | New connections created for this project only; existing connections are never reused |
| **Change rule** | Nothing outside the `AHFR` folder is touched, for any reason, without separate written authorisation |

## 2. Organisation and plan — verified

| Item | Value |
|---|---|
| Zone | **`us2.make.com`** — United States |
| Organisations | 1 |
| Teams | 1 |
| **Plan** | **Free** |
| Created | December 2024 |
| Billing period | Monthly; last reset 11 August 2026, next reset **11 September 2026 (today)** |
| Auto-purchase of extra operations | **Disabled** |

**The zone is a data-residency fact.** Orchestration runs in the United States. It belongs in the
contract review (EF-16), because payloads pass through that region even though, by design, they
carry identifiers rather than file content.

## 3. Plan limits — verified

| Limit | Value | Consequence for this design |
|---|---|---|
| **Operations per month** | **1,000** | The design's estimate at three pilot projects is ~800/month. **Too close to the ceiling to be safe** |
| **Active scenarios** | **2** | The Phase 3 design needs five. **This is the binding constraint** |
| **Data stores** | **1**, maximum **1 MB** | Idempotency keys fit (~10,000 at ~100 bytes), but need a purge policy. One store must serve both keys and counters |
| **Data transfer** | **512 MB/month** | **Routing image bytes through Make would breach this immediately** — 360 photographs at 2.5 MB is ~900 MB |
| **Maximum file size** | **5 MB** | A 2.5 MB photograph is fine. Some phones produce 5–8 MB files, which would fail |
| **Minimum scheduling interval** | **15 minutes** | If webhooks are unavailable and Make must poll, notification latency is up to 15 minutes |
| **Maximum execution time** | **5 minutes** | Report generation must stay inside this, or be split |
| API rate limit | 30 | Adequate |
| Execution log retention | **7 days** | Our own `IntegrationJobs` table is the authoritative record — already designed that way |
| Webhook log retention | 3 days | Same |
| Dead-letter queue storage | 1 MB | Needs monitoring |
| Execution priority | Low | Queue delay under load |
| Overage | **None on this plan** — auto-purchase disabled | Work **stops** at the ceiling; it does not silently bill |

## 4. Current usage — verified

| Item | Value |
|---|---|
| Operations consumed this period | **0** of 1,000 |
| Data transfer consumed | **0** of 512 MB |
| **Scenarios that exist** | **7** |
| **Currently active** | **0** |
| **Currently inactive** | **7** |
| **Plan ceiling on active scenarios** | **2** |
| Data stores | **0** |

Seven scenarios exist from earlier experiments — email monitoring, a Sheets-to-Canva-to-Drive flow,
a Telegram-to-Drive flow, a WhatsApp gateway, a Sheets-to-Gmail flow, an image-generation test. All
are switched off and none has consumed operations this period. The account is, in effect, dormant.

Since none is running, the two-scenario allowance is entirely available to this project today.
**If any existing scenario is ever switched back on, it consumes one of the two slots** — which is a
reason for the dedicated folder and labelling convention in §1c, so the set in use is always
visible.

## 5. Integration availability — verified

Every integration the design needs exists on this account:

| Needed for | Connector | Available |
|---|---|---|
| Operational store | Google Sheets | **Yes** |
| Evidence and document storage | Google Drive | **Yes** |
| Report generation | Google Docs | **Yes** |
| Notification | Gmail, and a generic Email connector | **Yes** |
| Capture platform triggers | Webhooks | **Yes** |
| **Capture platform read/write** | **AppSheet** — create, get, edit, search, delete record, plus a generic API call | **Yes** |
| Idempotency and counters | Data store | **Yes** (1 store, 1 MB) |
| AI analysis and drafting | Anthropic Claude | **Yes** |
| Accounting | QuickBooks | **Yes** |
| Supporting | HTTP, JSON, Tools, Flow Control | **Yes** |

**No integration gap.** The constraint is capacity, not capability.

## 6. What this changes in the design

Four findings, in order of consequence.

### 6.1 Two active scenarios is the binding constraint

The Phase 3 design has five scenarios. Three responses:

| Option | Effect | Cost |
|---|---|---|
| **Consolidate into one scenario with a router** | All five paths in one scenario, branching on the trigger type | Harder to read and to debug; a fault in one path stops the others. Contradicts "independent, reusable scenarios" |
| **Build only two: validation and evidence registration** | Notification, reporting and monitoring stay manual | Loses the review notification, which is what makes the review queue get looked at |
| **Upgrade the plan** | The design works as written | A cost, unverified, and not authorised |

**Recommendation: start with two scenarios** — submission validation and evidence registration —
and measure. Notification can be a daily digest the reviewer opens rather than a per-submission
email. That keeps the pilot inside the Free plan and produces the operation measurement needed to
size any upgrade honestly.

### 6.2 Which image bytes may pass through Make — corrected

Revision 1 said image bytes must "never" pass through Make. That was wrong as stated, because visual
AI analysis requires the model to see an image. The rule is now about *which* image:

| Class | Through Make? |
|---|---|
| **Original evidence** | **Never.** Not downloaded, not re-encoded, not opened by any processing path |
| **AI review derivative** (~400 KB) | **Yes, at pilot volume** — ~86 MB/month against the 512 MB limit, and 8% of the 5 MB per-file ceiling. Moves to a Workspace-side component before twenty projects, where it would breach |
| **Report derivative** | At document-generation time only, in release 1b |

Full design, sizes, transfer arithmetic and cost:
[`22-image-derivative-architecture.md`](22-image-derivative-architecture.md).

### 6.3 The operations ceiling — and a worse finding underneath it

The earlier "~800 operations" estimate was itself too optimistic: it counted scenario *runs*, not
*modules*. In Make each module that acts consumes an operation per bundle, so a six-module
per-photograph scenario costs six operations per photograph — **2,160 a month at three projects**,
twice the entire allowance for one scenario.

The prototype therefore removes per-photograph orchestration, which release 1 does not need because
release 1 produces no documents. The rebuilt budget lands at **703 operations, 70% of the limit**,
with retries, corrections, duplicates and administrative tests all funded, and with validation,
auditability and error handling untouched:
[`23-operations-budget.md`](23-operations-budget.md).

### 6.4 Make is not permanently free for this design

It is free **for a limited pilot** with two scenarios, identifiers-only payloads and three projects.
It is not free at ten or twenty projects: operations, active scenarios and transfer all grow with
project count. That is a future cost with a defined trigger, not a hidden one.

## 7. Corrections this forces in earlier documents

| Earlier statement | Correction |
|---|---|
| "Make may be USD 0 at pilot volume" | **Verified as accurate, but only under conditions**: two active scenarios, no image bytes through Make, and roughly three projects |
| "~800 operations/month at three projects" | Stands as an estimate, and is now known to be **80% of the ceiling**, with no overage |
| "Data stores may be tier-gated" | **Resolved.** One data store of 1 MB is available on this plan |
| "Whether the required integrations are available" | **Resolved.** All present, including a dedicated AppSheet connector |
| Log retention assumptions | **Resolved.** 7 days execution, 3 days webhook — our own tables remain the authoritative record |

## 8. What remains unverified about Make

| Unknown | How it gets answered |
|---|---|
| Cost of the next tier up | make.com is blocked from this environment; the owner can read it on their account's billing page |
| Whether a paid tier lifts the 2-scenario and 512 MB limits, and by how much | Same |
| Real operation consumption per visit and per photograph | Measured in Phase 3, on this account, with real scenarios |

## 9. Reproducing this inspection

Six read-only calls, in this order: `environment_get`, `organizations_get`, `scenarios_list`,
`data-stores_list`, `apps_list`, `apps_recommend`. Nothing else was called. The account was left
exactly as it was found: **0 active scenarios, 0 data stores, 0 operations consumed this period.**
