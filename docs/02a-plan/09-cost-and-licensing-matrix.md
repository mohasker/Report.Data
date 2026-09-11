# Cost and Licensing Matrix

**Document ID:** AH-SYS-P2A-009 · **Revision:** 2 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review
**Supersedes:** revision 1, whose USD 2,600–5,000 annual estimate the owner did not accept

---

## 1. What changed, and why the previous estimate was wrong

Revision 1 priced AppSheet as a **new** per-user subscription for 14–23 users. That was the error:
Al-Haram already pays for Google Workspace, and AppSheet Core may already be included in that
subscription. Pricing an included component as a new purchase inflated the whole estimate.

**Revision 2 treats Google Workspace as an existing cost and AppSheet as USD 0 incremental** until
the exact entitlement is confirmed in the Admin Console
([`12-appsheet-entitlement-checklist.md`](12-appsheet-entitlement-checklist.md)).

The previous figure is withdrawn. It is not corrected downward — it is withdrawn, because it was
built on the wrong question.

---

## 2. Category 1 — Existing subscriptions already paid by Al-Haram

**Incremental cost of this project: nil.** These exist whether or not the system is built.

| Item | Status | What the project uses it for | Incremental |
|---|---|---|---|
| **Google Workspace** (active paid subscription) | Existing | Identity and sign-in; Sheets as the operational store; Drive for evidence and documents; Docs for report templates; Gmail for internal notification | **USD 0** |
| **AppSheet** | **Assumed included** in the Workspace subscription, pending Admin Console confirmation (E-2, E-3) | The field capture and review application | **USD 0** *(assumed)* |
| **Google Drive pooled storage** | Included in the Workspace subscription | ~80 GB/year at 20 active projects — see [`14-storage-and-image-volume.md`](14-storage-and-image-volume.md) | **USD 0** unless the pool is already near full (E-7) |
| **QuickBooks Online** | Existing and in use | Accounting, from Phase 7 only | **USD 0** |

**If the Admin Console shows AppSheet is *not* included**, that becomes a decision to bring back to
the owner with a specific feature justification — not a purchase to assume. See §7.

---

## 3. Category 2 — New mandatory costs

**Honest answer for the lean MVP: none identified.**

| Item | Needed for | Cost | Basis |
|---|---|---|---|
| Make.com | Orchestration from Phase 3: validation, evidence registration, notification | **Possibly USD 0 for the pilot.** At three projects the design consumes roughly **800 operations a month**, which may sit inside a free tier | Operation count computed in `14-storage-and-image-volume.md` §6. **The tier and its limits are unverified** — make.com is also unreachable from this environment |
| Everything else | — | **USD 0** | |

Two things follow:

1. **Phase 2A costs nothing.** It is design on synthetic data, plus optionally the free development tier.
2. **Phase 2B may cost nothing either**, if AppSheet is included and the pilot's orchestration fits a free tier. That is a genuinely plausible outcome, not optimism.

---

## 4. Category 3 — Optional costs

Each is a capability the owner may choose. **None is required for the system to work.**

| Item | What it buys | Cost | If skipped |
|---|---|---|---|
| **Claude API** (AI evidence analysis and report drafting) | Advisory analysis to assist the reviewer; narrative drafting from approved records | **Usage-based, bounded by a hard monthly cap the owner sets** (EF-04) | The pipeline works unchanged. Reviewers read the evidence themselves and the report narrative is written by hand. **AI is assistance, never a control** |
| A higher AppSheet tier | Only a specific feature proven unavailable | Unknown | See §7. Not proposed |
| Professional report template design | A designer's polish on the monthly report | One-off, external | The template is built from the company's existing report format |
| Paid Make tier during the pilot | Headroom above a free tier | Unknown | Measure first, then decide |

---

## 5. Category 4 — Future scaling costs

These arrive with growth, not at go-live. Each has a **trigger** so it is a planned decision rather
than a surprise invoice.

| Item | Trigger | Likely timing | Note |
|---|---|---|---|
| **Make tier upgrade** | Operations exceed the free or current tier: ~2,600/month at 10 projects, ~5,200 at 20 | Year 1 at 10+ projects | **The fastest-growing cost line.** Grows with photographs, not with users |
| **Store migration off Sheets** | 40,000 rows in Photos, or median sync above 15 seconds: ~year 1.4 at 20 projects | Year 1–2 | Archiving closed periods first is cheaper and usually enough for a while |
| **Additional Workspace licences** | New office or field staff | With headcount | Existing per-user cost, not a project cost |
| **Storage beyond the pool** | Pooled storage exhausted | Unlikely within 3 years | ~80 GB/year at 20 projects |
| **AI usage growth** | More projects with analysis enabled | With adoption | Capped by construction; per-project on/off switch |

---

## 6. Category 5 — One-time implementation costs

**No external cash outlay is identified.** The build is done in this workspace; the costs are the
company's own time.

| Item | Who | Effort | Cash |
|---|---|---|---|
| Admin Console entitlement check | Owner or administrator | ~15 minutes | **USD 0** |
| Workspace and Shared Drive setup | Administrator | ~1 hour | **USD 0** |
| App build against synthetic data | This workspace | — | **USD 0** |
| Report template built from the company's existing format | Owner supplies the format; built here | ~2 hours of owner review | **USD 0** unless a designer is engaged (optional) |
| Master-data entry: projects, locations, activity rules, users | Administrator | ~2–4 hours for the first three projects, then ~20 minutes per project | **USD 0** |
| **Field testing with real supervisors** | 2–3 supervisors, half a day | Their time | **USD 0** |
| Legal identity, numbering register and tax confirmation | Owner, accountant | A few hours spread over weeks | **USD 0** |
| Parallel month alongside the existing manual process | Owner and reviewers | One reporting cycle | **USD 0**, and the cheapest insurance available |

---

## 7. The only circumstance in which a purchase is proposed

Per the owner's instruction, no additional AppSheet licence is to be bought unless **all four** hold:

1. A **specific required feature** is unavailable on the existing entitlement — named, not generalised.
2. The feature is genuinely required, not merely convenient.
3. **Make cannot handle it safely.** Both of the likely gaps have fallbacks: no webhooks → Make polls on a schedule; no API → Make writes to the Sheet directly. Neither needs a licence.
4. The owner approves the purchase in writing, with the cost stated.

The two features with **no** Make fallback are **security filters** and **offline image capture**. If
either is unavailable, that is not a purchase decision — it is a signal to re-evaluate the capture
layer before anything is built.

---

## 8. Summary

| Category | Amount |
|---|---|
| 1 · Existing subscriptions | **USD 0 incremental** — Workspace, AppSheet (assumed included), Drive storage, QuickBooks |
| 2 · New mandatory | **None identified.** Make may be USD 0 at pilot volume |
| 3 · Optional | Claude API, capped by the owner. Nothing else |
| 4 · Future scaling | Make tier first, then store migration — both with defined triggers |
| 5 · One-time | **No cash outlay.** Company time: roughly one day of administrator effort plus half a day of field testing |

**Expected incremental monthly cost for the pilot: USD 0, possibly plus a modest orchestration tier
if the free allowance is exceeded.**

## 9. What is still unverified

| Unknown | How it gets answered | Blocks |
|---|---|---|
| Whether AppSheet is included, and on what plan | Admin Console, ~15 minutes (E-1 … E-8) | The build |
| Make's free-tier operation allowance and whether Data Stores are included | The owner's Make account, or make.com when reachable | Phase 3 sizing |
| Real operation consumption | Measured in Phase 3 | The tier decision |
| Pooled storage headroom | Admin Console (E-7) | Nothing immediately |
| Photographs per visit in real use | One month of real usage | Every number in §5 |

**Vendor pages are unreachable from the build environment** — Google and make.com are both blocked by
the network egress policy. That is recorded rather than papered over with a third-party figure, and
it matters less than it sounds: the authoritative answer for this company is in the Admin Console,
not on a public page.
