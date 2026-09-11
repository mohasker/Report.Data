# AppSheet Entitlement Verification Checklist

**Document ID:** AH-SYS-P2A-012 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · **Awaiting the owner's Admin Console check** · **Nothing purchased**

> **Working assumption, on the owner's instruction (2026-09-11):** Al-Haram has an active paid
> Google Workspace subscription. **AppSheet is therefore treated as USD 0 incremental cost** until
> the exact entitlement is confirmed in the Google Admin Console.
>
> **No purchase of any kind is proposed.** Nothing beyond the existing Workspace subscription is to
> be bought unless a specific required feature is proven unavailable *and* cannot be handled safely
> through Make.

---

## 1. Why this is a console check, not a research task

Vendor pricing and feature pages are unreachable from the build environment — the network egress
policy blocks them, and the attempt is recorded honestly rather than substituted with a third-party
guess (operating rule 2). It does not matter much, because the **authoritative** answer for this
company is not on a public page anyway: it is in the Admin Console, which states what *this
subscription* actually includes.

Ten minutes in the console beats an hour of reading marketing pages.

## 2. What to check, and where

Sign in to `admin.google.com` as a Workspace administrator.

| # | Question | Where to look | Record |
|---|---|---|---|
| **E-1** | Which Workspace **edition** is subscribed, and how many licences? | Billing → Subscriptions | Edition name and licence count |
| **E-2** | Is **AppSheet** listed as an included or available service? | Apps → Additional Google services, or Apps → Google Workspace | Whether AppSheet appears, and whether it is ON |
| **E-3** | Which **AppSheet plan** does the console show for the organisation? | Apps → AppSheet → (settings or plan) | The plan name shown, exactly as written |
| **E-4** | Is AppSheet turned **ON** for the organisational units the users sit in? | Apps → AppSheet → Service status | ON or OFF, and for which OUs |
| **E-5** | Do the licensed users already have what they need, or is a separate AppSheet licence assignment required? | Billing → Subscriptions, and AppSheet admin | Whether any additional assignment exists |
| **E-6** | Does the edition include **Shared Drives**? | Apps → Drive and Docs → Shared drives | Enabled or not |
| **E-7** | What **pooled storage** does the subscription provide, and how much is already used? | Storage | Total and remaining |
| **E-8** | Is **data region** control available and set? | Data → Data regions (if present) | Available or not; current setting |

## 3. Feature questions, once the plan name is known

The three that decide whether the design works as specified:

| # | Question | If YES | If NO |
|---|---|---|---|
| **F-1** | Are **security filters** available on this plan? | Segregation is enforced as designed | **Blocking.** Do not proceed. Re-evaluate the capture layer before building anything |
| **F-2** | Are **webhooks** (automation calling an external URL) available? | The Make pipeline works as designed | Fall back to Make **polling** the sheet on a schedule — slower and more operations, but workable. No purchase required |
| **F-3** | Is the **API** available for reading and writing rows? | Make writes statuses back cleanly | Fall back to Make writing to the Sheet directly. Weaker validation, no purchase required |

And the ones that shape the build rather than block it:

| # | Question | Consequence if unavailable |
|---|---|---|
| F-4 | Offline use with image capture | Blocking for field work. Re-evaluate |
| F-5 | Image upload quality setting | Falls back to the platform default; the D-13 write-once wording already covers it |
| F-6 | Per-row change history and retention | Our own `AuditLog` is the authoritative trail regardless |
| F-7 | Deep links to a record | Notifications carry a link to the app instead of to the row |
| F-8 | Barcode/QR scanning | A convenience only; manual location selection works |

**F-2 and F-3 both have a Make fallback.** That is the point of the owner's instruction: a missing
convenience is a workaround, not a purchase.

## 4. Decision rule

```
E-2/E-3 show AppSheet included, and F-1 and F-4 are available
        -> BUILD. Incremental licence cost: USD 0.

F-1 or F-4 unavailable
        -> STOP. This is a capture-layer decision, not a purchase decision.
           Re-evaluate before any app is built.

F-2 or F-3 unavailable
        -> BUILD anyway, using the Make polling fallback.
           Record the extra operations in the cost matrix. Still USD 0 in licences.

Any additional AppSheet licence proposed
        -> Requires a written statement of WHICH required feature is unavailable,
           WHY Make cannot handle it safely, and what it would cost.
           No purchase without the owner's written approval.
```

## 5. What to send back

A short note is enough:

```
Workspace edition          : ____________________
Licences                   : ____________________
AppSheet shown in console  : yes / no      Plan name: ____________________
AppSheet service status    : ON / OFF      For which OUs: ______________
Security filters available : yes / no / unclear
Webhooks available         : yes / no / unclear
API available              : yes / no / unclear
Offline + image capture    : yes / no / unclear
Shared Drives              : enabled / not
Pooled storage             : ______ total, ______ used
Data regions               : available / not,  current: ____________
Checked by ______________  on ____________
```

Where a row says "unclear", that is a perfectly good answer — it becomes a question for Google
support rather than a guess in this document.

## 6. Until this comes back

| Activity | Permitted now? |
|---|---|
| Phase 2A design, expressions, security-filter specification | **Yes** — all on synthetic data |
| Prototyping on the free development tier | **Yes**, if the owner wishes; it costs nothing |
| Building the production app | No — wait for E-2, E-3, F-1, F-4 |
| Buying anything at all | **No** |
