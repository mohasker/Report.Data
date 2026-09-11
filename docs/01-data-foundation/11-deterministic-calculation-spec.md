# Deterministic Calculation Specification

**Document ID:** AH-SYS-P1-011 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Validated Locally · Submitted for Owner Review · **Not Verified in Integration** (no accounting system connected)
**Delivers:** D-15 item 13 · **Implements:** D-08, invariant I-4 · **Closes:** C-09
**Executable statement:** `tools/calc.py` · **Evidence:** `17-validation-evidence.md` (CALC-01 … CALC-22)

> No monetary or measured figure ever originates from, or passes through, a language model. AI may
> draft the human-readable service description and the covering email, and nothing else (spec 9.4,
> GOV-11).

---

## 1. Storage and rounding

| Rule | Value | Reason |
|---|---|---|
| Numeric storage | **Decimal, never floating point.** Money is carried as decimal strings | `0.1 + 0.2` is not `0.3` in binary floating point, and an invoice must not depend on that |
| Money scale | 2 decimal places (QAR minor units; per-currency by configuration) | |
| Quantity scale | 3 decimal places, or the unit's declared places | A quantity in `no.` has 0 places; in `m²` it has 2 |
| Rounding mode | **ROUND_HALF_UP**, everywhere, no exceptions | One policy, applied centrally. `0.125 → 0.13` (CALC-08) |
| Rounding points | At each line, then on each derived total | Rounding once at the end produces totals that do not match the printed lines |

## 2. Calculation order

Order matters: tax on a discounted base is not the same as a discounted tax.

```
1  currency agreement    contract, project, client and request must agree — no conversion, ever
2  line amount           quantity x unit rate, rounded at line level
3  subtotal              sum of already-rounded line amounts
4  discount              applied to the subtotal
5  taxable base          subtotal - discount
6  tax                   base x rate, rounded once  — OR UNDETERMINED (see §4)
7  retention             base x contract retention percentage
8  advance recovery      base x recovery percentage, capped at the outstanding advance
9  net payable           base + tax - retention - advance recovery
```

Each step appends to a `CalculationTrace` recording the expression, the result and the rule applied.
The trace is stored with the invoice request, so any figure can be re-derived and explained years
later (CALC-21).

## 3. Currency

An invoice request is single-currency, and the currency comes from the contract. Any mismatch
between contract, project, client and request stops the calculation with a specific error
(CALC-12). **No conversion is performed anywhere and no exchange rate is stored** (C-09).

The synthetic fixtures contain a deliberate mismatch — a client recorded in USD on a QAR project —
so that the rule is exercised rather than assumed (CALC-13).

## 4. Tax — the rule the owner corrected

> "Zero-rated", "exempt", "out of scope" and "no tax configured" are **not interchangeable** (D-08).

An earlier recommendation to configure a "zero-rate" rule was withdrawn by the owner, and the
withdrawal is right: naming a classification the accountant has not confirmed is inventing a tax
position, which is exactly what §11 forbids.

So the engine behaves as follows:

| Tax rule state | Tax amount | Net payable | Result |
|---|---|---|---|
| Not confirmed by the accountant, or no rate recorded | **`UNDETERMINED`** | **not computed** | `BLOCKED_TAX_UNCONFIRMED` |
| Confirmed in writing, with a rate | Calculated and rounded once | Calculated | `OK` |

An unconfirmed rule **does not quietly produce zero** (CALC-01). A draft may be prepared and
reviewed; it cannot be issued. Production invoicing is blocked until the confirmation exists
(GOV-04, GOV-05).

Every result and every trace carries the `TaxRuleID` **and its `Version`** (CALC-07), so an invoice
issued under one treatment stays explainable after the treatment changes.

## 5. Cumulative quantity control

```
cumulative  = previously certified + current
permitted   = contract quantity + approved variation quantity
```

| Situation | Behaviour | Check |
|---|---|---|
| `cumulative <= permitted` | Proceed | CALC-15 |
| `cumulative > permitted`, no override | **Rejected** with a specific message | CALC-14 |
| `cumulative > permitted`, override with approver **and** reason | Proceeds, recorded as an override | CALC-16 |
| Override missing an approver or a reason | **Rejected** | CALC-17 |
| Approved variation present | Extends the permitted quantity | CALC-18 |

## 6. Validation rules

| Input | Rule | Check |
|---|---|---|
| Zero quantity | Accepted; yields zero | CALC-09 |
| Negative quantity | Rejected | CALC-10 |
| Negative rate | Rejected | CALC-11 |
| Discount greater than subtotal | Rejected | CALC-20 |
| Advance recovery greater than the outstanding advance | Capped at the outstanding balance | CALC-19 |
| Duplicate billing period | Rejected by the unique key on client + project + contract + period + source document | Model constraint |

## 7. Worked example

Contract: 5% retention, no advance. Two BOQ lines. Tax rule: a synthetic test-only rule at 5% that
**asserts nothing about any jurisdiction** and must never appear in production data.

| Step | Expression | Result |
|---|---|---|
| Line 1 | 1,200.000 m² × 3.500 | 4,200.00 |
| Line 2 | 100.000 no. × 18.000 | 1,800.00 |
| Subtotal | 4,200.00 + 1,800.00 | 6,000.00 |
| Discount | — | 0.00 |
| Taxable base | 6,000.00 - 0.00 | 6,000.00 |
| Tax | 6,000.00 × 5% | 300.00 |
| Retention | 6,000.00 × 5% | 300.00 |
| Advance recovery | — | 0.00 |
| **Net payable** | 6,000.00 + 300.00 - 300.00 - 0.00 | **6,000.00** |

The same figures with the **real** (unconfirmed) tax rule: subtotal 6,000.00, retention 300.00, tax
`UNDETERMINED`, net payable **not computed**, status `BLOCKED_TAX_UNCONFIRMED`.

## 8. Boundaries

- The engine is **independent of the accounting product** (ADR-0008). If the accounting target changes, the integration changes and this layer does not.
- It performs **no posting**. Phases 1 and 6 produce drafts only; posting is Phase 7, sandbox first, and production posting stays disabled until the owner authorises it in writing (D-07).
- Before anything is marked synchronised, the accounting system's returned totals are reconciled against these figures to the last decimal.
- Finance approval is required before a draft may be created in the accounting system, and release approval before anything reaches a client.
