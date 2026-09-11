# Make Account Inspection — Read-Only Record

**Document ID:** AH-SYS-P2A-015 · **Revision:** 1 · **Date:** 2026-09-11
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
| **Active scenarios** | **0** |
| Scenarios that exist | **7**, every one inactive |
| Data stores | **0** |

Seven scenarios exist from earlier experiments — email monitoring, a Sheets-to-Canva-to-Drive flow,
a Telegram-to-Drive flow, a WhatsApp gateway, a Sheets-to-Gmail flow, an image-generation test. All
are switched off and none has consumed operations this period. The account is, in effect, dormant.

**Two of those seven would have to stay off** for this project to use its two active-scenario
allowance — or the allowance has to grow.

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

### 6.2 Image bytes must never pass through Make

512 MB a month against ~900 MB of photographs at three projects. This was already the design
(payloads carry identifiers, not content), and the verified limit turns a good habit into a hard
rule: **derivative creation must happen on the storage side, not by downloading and re-uploading
through the orchestration layer.**

### 6.3 The operations ceiling is too close for comfort

~800 estimated against 1,000 available, with **no overage** — work stops rather than overspending.
A busy month, a retry storm, or one more project breaches it. Consolidating to two scenarios and
batching derivative work reduces the estimate; measurement in Phase 3 replaces it.

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
