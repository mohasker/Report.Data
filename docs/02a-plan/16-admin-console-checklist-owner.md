# AppSheet Entitlement Check — Click by Click

**Document ID:** AH-SYS-P2A-016 · **Revision:** 3 · **Date:** 2026-09-11
**For:** the owner · **Time needed:** about 15 minutes · **Cost:** nothing
**Purpose:** find out what the existing Workspace subscription already includes, so nothing is
bought unnecessarily

Revision 2 adds, for every item, what screenshot is useful, whether the answer blocks the
prototype, and what alternative applies if the answer is No or Cannot tell.

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
Checked on                : __________
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

**No purchase is proposed under any of these outcomes without a written justification from me and
your written approval.**

## What this does not block

Everything else in Phase 2A continues on synthetic data while you do this: the workbook, the
expressions, the security filters, the views, the test protocols. This check blocks only the final
capture-platform decision and the first external connection.
