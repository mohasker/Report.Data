# AppSheet Entitlement Check — Click by Click

**Document ID:** AH-SYS-P2A-016 · **Revision:** 4 · **Date:** 2026-09-12
**For:** the owner · **Time needed:** about 15 minutes · **Cost:** nothing
**Purpose:** find out what the existing Workspace subscription already includes, so nothing is
bought unnecessarily

Revision 2 adds, for every item, what screenshot is useful, whether the answer blocks the
prototype, and what alternative applies if the answer is No or Cannot tell.

**Revision 4** adds the four screens revision 3 did not ask about — **group and organisational-unit
membership** for the pilot users, **Drive sharing policy**, **data regions**, and **device
management** — an **evidence register** with redaction rules, and a **design-impact matrix** that
says, answer by answer, which document changes and how.

> **On the screen paths below.** They are written from documentation that **could not be reached from
> the build environment** — `cloud.google.com`, `support.google.com` and `about.appsheet.com` were
> all unreachable, and that was recorded rather than papered over with a third-party guess. **Treat
> every bold word as a search term, not as a verified label.** If a path does not exist as written,
> that is expected: search the bold word, record what you actually saw, and the record is still
> good.

---

## Before you start

- Sign in at **admin.google.com** with an account that has administrator rights.
- You are only **looking**. Do not change any setting. Nothing in this checklist switches anything
  on or off.
- If a screen does not look like the description, the console layout has changed — use the search
  box at the top and search for the word in bold.
- **"Cannot tell" is a perfectly good answer.** It becomes one question to Google support rather
  than a guess on my side.

---

## Step 1 — Which Workspace plan is paid for *(3 minutes)*

| | |
|---|---|
| **Where to click** | Left menu → **Billing** → **Subscriptions** |
| **What to copy** | The exact subscription name (for example "Business Standard", "Business Plus") and the number of licences |
| **Useful screenshot** | The Subscriptions list, showing the plan name and licence count |
| **Blocks the prototype?** | **No.** It tells me which AppSheet tier is bundled, which changes what I build, not whether I can build |
| **If unavailable** | If Billing is not visible, your account is not a super administrator. Either use one that is, or record "no billing access" and I proceed on the AppSheet answers alone |

> ✍️ **Workspace plan:** ______________________  **Licences:** ______

---

## Step 2 — Is AppSheet there at all *(3 minutes)*

| | |
|---|---|
| **Where to click** | Left menu → **Apps**. Look for **AppSheet** under **Google Workspace** or under **Additional Google services**. Then click it |
| **What to copy** | Whether AppSheet appears; any plan or edition name on that page; whether the service is **ON**; and whether it is on for everyone or only some organisational units or groups |
| **Useful screenshot** | The AppSheet service page, showing the ON/OFF state and any edition name |
| **Blocks the prototype?** | **Yes, partly.** If AppSheet does not appear at all, the capture platform is undecided and I bring you a specific, costed option rather than assuming one |
| **If unavailable** | If it appears but is OFF, that is not a purchase — it is a switch, and turning it on is your decision, not mine to make. If it is on only for some groups, the pilot users must be inside one of those groups |

> ✍️ **AppSheet appears:** Yes / No
> ✍️ **AppSheet plan shown:** ______________________
> ✍️ **AppSheet is:** ON / OFF   **For everyone, or only some groups:** ______________________

---

## Step 2b — Which group or organisational unit the pilot users are in *(2 minutes)*

Only needed if Step 2 showed AppSheet is **ON for some groups**, not for everyone.

| | |
|---|---|
| **Where to click** | Left menu → **Directory** → **Users**, open one intended pilot supervisor → look at **Organisational unit** and **Groups** |
| **What to copy** | The organisational unit path, and the group names — **not** the person's email address |
| **Useful screenshot** | The organisational-unit and group panel, with the name and email masked |
| **Blocks the prototype?** | **Yes, in practice.** A supervisor outside the enabled unit cannot open the app at all, and the test would measure the wrong thing |
| **If unavailable** | Record "cannot see directory". The pilot then runs on whichever accounts do have access, and the mismatch is recorded as a risk before go-live |

> ✍️ **Pilot users' organisational unit:** ______________________
> ✍️ **AppSheet enabled for that unit or group:** Yes / No / Cannot tell

---

## Step 3 — The two answers that decide everything *(4 minutes)*

These two decide whether the app can be built at all. Everything else has a workaround.

| | |
|---|---|
| **Where to click** | Still in **Apps → AppSheet**, open the AppSheet settings or the link to the AppSheet admin page. Look for anything named **security filters** or **row-level security**, and anything named **offline** or **offline use** |
| **What to copy** | Yes / No / Cannot tell, for each — and the exact wording you see, if any |
| **Useful screenshot** | The feature or plan-comparison panel where those two words appear, or the page where you expected them and they were absent |
| **Blocks the prototype?** | **Yes — these two are the gate.** Security filters are how one supervisor is prevented from seeing another project. Offline use is how a site with no signal still captures a visit |
| **If unavailable** | Not a licence problem and not something a purchase fixes reliably. If either is genuinely absent, we **stop and rethink the capture tool** rather than buy a tier and hope. If the answer is "cannot tell", it becomes one written question to Google support |

> ✍️ **Security filters available:** Yes / No / Cannot tell
> ✍️ **Offline use available:** Yes / No / Cannot tell

---

## Step 4 — Two more, each with a free workaround *(2 minutes)*

| | |
|---|---|
| **Where to click** | The same AppSheet page. Look for **webhooks** or "call a webhook" automation, and for **API access** |
| **What to copy** | Yes / No / Cannot tell, for each |
| **Useful screenshot** | The automation or integrations panel |
| **Blocks the prototype?** | **No, neither.** Both have a free route around them |
| **If unavailable** | **Webhooks missing:** Make checks for new submissions on a schedule instead — free, with up to 15 minutes' delay. **API missing:** Make writes to the spreadsheet directly — free, slightly weaker validation |

> ✍️ **Webhooks / "call a webhook" automation:** Yes / No / Cannot tell
> ✍️ **API access:** Yes / No / Cannot tell

---

## Step 5 — Storage and Shared Drives *(3 minutes)*

| | |
|---|---|
| **Where to click** | Left menu → **Storage** for the totals. Then **Apps → Google Workspace → Drive and Docs → Shared drives** |
| **What to copy** | Total storage, how much is already used, and whether shared drives are available |
| **Useful screenshot** | The Storage summary showing total and used |
| **Blocks the prototype?** | **No.** It sizes the pilot. One project-month of live evidence is roughly 361 MB, or about 663 MB with one backup copy |
| **If unavailable** | If shared drives are not available, evidence lives in a folder owned by the dedicated system account instead. That works, but ownership is then a single account rather than the organisation — a recoverability point I would record as a risk |

> ✍️ **Total storage:** ________  **Used:** ________
> ✍️ **Shared drives available:** Yes / No

---

## Step 5b — Drive sharing policy *(2 minutes)*

| | |
|---|---|
| **Where to click** | **Apps → Google Workspace → Drive and Docs → Sharing settings** |
| **What to copy** | Whether sharing outside the organisation is **allowed**, **allowed with a warning**, or **off**; and whether "anyone with the link" is permitted |
| **Useful screenshot** | The sharing-settings panel |
| **Blocks the prototype?** | **No** — but it changes the risk, not the build. This design **never creates a public link to evidence**, by rule. If the domain permits "anyone with the link", then a person could create one by hand, and that is a control gap to record, not a design change |
| **If unavailable** | Record "cannot see sharing settings". The rule against public links holds regardless |

> ✍️ **External sharing:** allowed / allowed with warning / off
> ✍️ **"Anyone with the link" permitted:** Yes / No / Cannot tell

---

## Step 5c — Data regions *(2 minutes)*

| | |
|---|---|
| **Where to click** | Left menu → **Data** → **Compliance** → **Data regions** (older consoles: **Company profile → Legal and compliance**) |
| **What to copy** | Whether a data region is set, and which one |
| **Why it is here** | Decision **D-12** allows a project's AI analysis to be switched off where a contract or residency rule forbids third-party processing. **A data region setting is the only Workspace-side fact that bears on that**, and no document in this project currently records it |
| **Blocks the prototype?** | **No.** It blocks a *claim*: without it, nothing in this project may state where evidence is stored, and `09-data-classification-and-residency.md` keeps that question open |
| **If unavailable** | Record "not available on this plan". That is itself the answer, and an honest one |

> ✍️ **Data region set:** Yes / No / Cannot tell   **Which:** ______________________

---

## Step 5d — Device management *(2 minutes)*

| | |
|---|---|
| **Where to click** | Left menu → **Devices** → **Mobile and endpoints** → **Settings** → **Universal settings** |
| **What to copy** | Whether mobile management is **off**, **basic**, or **advanced** |
| **Why it is here** | `CAP-GATE` measures what a phone keeps after access is revoked. **Whether a company-side wipe is even possible depends on this screen**, and the answer changes what the revocation test can prove |
| **Blocks the prototype?** | **No.** It scopes one `CAP-GATE` measurement — see [`19-real-device-test-protocol.md`](19-real-device-test-protocol.md) §4c, G-5 |
| **If unavailable** | Record "cannot see". The revocation test then measures only what the application does, not what the organisation can force |

> ✍️ **Mobile management:** off / basic / advanced / cannot tell

---

## The evidence register — what to keep, and what to mask

Six answers are worth a screenshot. **Name them exactly like this**, so the record is unambiguous
later:

| File name | Of what |
|---|---|
| `AC-01-subscriptions.png` | Billing → Subscriptions, plan name and licence count |
| `AC-02-appsheet-service.png` | The AppSheet service page: ON/OFF, edition, who it applies to |
| `AC-03-security-filters-and-offline.png` | Wherever those two words appear — **or the page where you expected them and they were absent** |
| `AC-04-webhooks-and-api.png` | The automation or integrations panel |
| `AC-05-storage-and-shared-drives.png` | Storage totals, and whether shared drives exist |
| `AC-06-data-region.png` | The data-regions panel |

**Mask before sending — every one of these:**

- **any person's email address or full name**, including your own in the header bar;
- the **domain name**, wherever it appears;
- **billing identifiers**, customer IDs, order numbers, payment details;
- any **support case number** or reseller reference.

**None of that is needed to answer a single question in this checklist.** A screenshot with a plan
name and a licence count is useful; the same screenshot with a billing ID is a liability, and it
would be stored in a repository that is not a secrets store.

> **A screenshot is optional everywhere.** A typed answer of "yes", "no" or "cannot tell" is a
> complete answer. Nothing here is worth sending a document you would not want kept.

---

## Step 6 — Send it back

Copy this block, fill in the blanks, and send it:

```
Workspace plan            : ______________________   Licences: ______
AppSheet appears          : yes / no
AppSheet plan shown       : ______________________
AppSheet service          : ON / OFF   for: ______________________
Security filters          : yes / no / cannot tell      <-- decides the build
Offline use               : yes / no / cannot tell      <-- decides the build
Webhooks                  : yes / no / cannot tell
API access                : yes / no / cannot tell
Storage total / used      : ________ / ________
Shared drives             : yes / no
Pilot users' unit/group   : ______________________
AppSheet on for that unit : yes / no / cannot tell
External Drive sharing    : allowed / allowed with warning / off
"Anyone with the link"    : yes / no / cannot tell
Data region set           : yes / no / cannot tell   which: ____________
Mobile management         : off / basic / advanced / cannot tell
Checked on                : __________
Checked by (role, not name): ______________________
```

---

## What happens with each answer

| Your answer | What I do |
|---|---|
| AppSheet appears, security filters **and** offline both available | **Build.** No purchase. This is the expected case |
| Security filters **or** offline missing | **Stop and rethink the capture tool.** This is not a purchase decision — a licence would not fix a capability the platform does not have |
| Webhooks missing | Build anyway. Make checks for new submissions on a schedule instead. Free, with up to 15 minutes' delay |
| API missing | Build anyway. Make writes to the spreadsheet directly. Free, slightly weaker validation |
| AppSheet does not appear at all | I bring you a specific, costed option — I do not assume one |
| Everything present, but the **native share test fails on a real device** | Not an Admin Console answer, and not fixable by a licence. The capture-platform comparison runs instead ([`19-real-device-test-protocol.md`](19-real-device-test-protocol.md) §4b) |

### Design-impact matrix — which document changes, and how

| Answer | What changes in the design | Document affected |
|---|---|---|
| **Security filters: yes** | Segregation is enforced by the platform, and `P2B-SEG-01 … 14` test an enforcement that exists | `02-security-filter-specification.md` stands unchanged |
| **Security filters: no** | Segregation would rest on views alone — **which is not segregation, it is tidiness.** The capture platform changes; the data model does not | `26-phase-2b-platform-test-scripts.md` §4 re-runs on the replacement platform |
| **Offline: yes** | The offline plan stands, and `CAP-GATE` condition 10 is testable as written | `05-offline-test-plan.md` |
| **Offline: no** | A site with no signal cannot capture. That is not a degraded feature, it is the failure of the core use case, and it forces the platform comparison | `19-real-device-test-protocol.md` §4b, "the comparison that runs if it fails" |
| **Webhooks: no** | Make polls on a schedule. Costs **operations per poll, not per submission** — and the operations budget must be recalculated before it is quoted again | `23-operations-budget.md` §4 |
| **API: no** | Make writes to the spreadsheet directly; validation weakens slightly, and the idempotency claim needs re-checking | `14-orchestration-contract-and-runbook.md` |
| **Shared drives: no** | Evidence is owned by one account rather than the organisation. **Recoverability becomes a named risk**, and the recovery plan needs a second route | `20-administrator-role-placeholders.md`, `SystemRecoveryPlan` |
| **Data region: set** | The residency question can finally be answered rather than deferred, and `D-12` gains a factual basis | `09-data-classification-and-residency.md` |
| **Data region: not available** | **No document may state where evidence is stored.** The question stays open, and `AIAnalysisEnabled` stays the only residency control | Same |
| **Mobile management: off** | `CAP-GATE` G-5 measures only what the *application* does on revocation — the organisation cannot force a wipe, and no document may imply it can | `19-real-device-test-protocol.md` §4c |
| **AppSheet on for some groups only** | The pilot supervisors must be inside an enabled group, or the test measures the wrong thing | `19-real-device-test-protocol.md` §2, `27-cap-gate-prototype-specification.md` §3 |
| **External link sharing permitted** | No design change — **the rule against public evidence links is absolute either way.** It becomes a recorded control gap: the platform permits by hand what the design forbids by rule | Risk register |

**No purchase is proposed under any of these outcomes without a written justification from me and
your written approval.**

## What this does not block

Everything else in Phase 2A continues on synthetic data while you do this: the workbook, the
expressions, the security filters, the views, the test protocols. This check blocks only the final
capture-platform decision and the first external connection.
