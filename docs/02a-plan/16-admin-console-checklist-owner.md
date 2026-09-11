# AppSheet Entitlement Check — Click by Click

**Document ID:** AH-SYS-P2A-016 · **Revision:** 1 · **Date:** 2026-09-11
**For:** the owner · **Time needed:** about 15 minutes · **Cost:** nothing
**Purpose:** find out what the existing Workspace subscription already includes, so nothing is bought unnecessarily

---

## Before you start

- Sign in at **admin.google.com** with an account that has administrator rights.
- You are only **looking**. Do not change any setting. Nothing in this checklist switches anything on or off.
- If a screen does not look like the description, the console layout has changed — use the search box at the top and search for the word in bold.

---

## Step 1 — Which Workspace plan is paid for *(3 minutes)*

1. On the left, click **Billing**.
2. Click **Subscriptions**.
3. Write down the **exact name** of the Google Workspace subscription, for example "Business Standard" or "Business Plus".
4. Write down **how many licences** it has.

> ✍️ **Workspace plan:** ______________________  **Licences:** ______

---

## Step 2 — Is AppSheet there at all *(3 minutes)*

1. On the left, click **Apps**.
2. Look for **AppSheet** in the list. It may be under **Google Workspace** or under **Additional Google services**.
3. Does AppSheet appear?

> ✍️ **AppSheet appears:** Yes / No

4. If it appears, click it. Look for a **plan** or **edition** name on that page.

> ✍️ **AppSheet plan shown:** ______________________

5. On the same page, check whether the service is **ON**.

> ✍️ **AppSheet is:** ON / OFF   **For everyone, or only some groups:** ______________________

---

## Step 3 — The two answers that decide everything *(4 minutes)*

These two decide whether the app can be built at all. Everything else has a workaround.

1. Still in **Apps → AppSheet**, open the AppSheet settings or the link to the AppSheet admin page.
2. Look for anything named **security filters** or **row-level security**.

> ✍️ **Security filters available:** Yes / No / Cannot tell

3. Look for anything named **offline** or **offline use**.

> ✍️ **Offline use available:** Yes / No / Cannot tell

**"Cannot tell" is a perfectly good answer.** It becomes one question to Google support rather than
a guess on my side.

---

## Step 4 — Two more, each with a free workaround *(2 minutes)*

Look for these on the same page. If either is missing, nothing is bought — we route around it.

> ✍️ **Webhooks / "call a webhook" automation:** Yes / No / Cannot tell
> ✍️ **API access:** Yes / No / Cannot tell

---

## Step 5 — Storage and Shared Drives *(3 minutes)*

1. On the left, click **Storage**.
2. Write down the **total storage** and **how much is already used**.

> ✍️ **Total storage:** ________  **Used:** ________

3. On the left, click **Apps → Google Workspace → Drive and Docs**, then **Shared drives**.

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

**No purchase is proposed under any of these outcomes without a written justification from me and
your written approval.**

## What this does not block

Everything else in Phase 2A continues on synthetic data while you do this: the workbook, the
expressions, the security filters, the views, the test protocols. This check blocks only the final
capture-platform decision and the first external connection.
