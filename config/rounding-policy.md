# Rounding Policy

**Document ID:** AH-SYS-CFG-001 · **Revision:** 1 · **Date:** 2026-09-11
**Implemented by:** `tools/calc.py` · **Evidence:** `docs/01-data-foundation/17-validation-evidence.md` (CALC-08)

One policy, applied centrally, so that a printed line, a printed total and an accounting entry
can never disagree.

## Rules

| Rule | Value |
|---|---|
| Numeric storage | **Decimal, never floating point.** Money is carried as decimal strings |
| Rounding mode | **ROUND_HALF_UP** everywhere. No exceptions, no per-step variation |
| Money scale | 2 decimal places (QAR minor units). Configurable per currency |
| Quantity scale | 3 decimal places by default; a unit may declare fewer (`no.` uses 0) |
| Percentage storage | 4 decimal places, so a rate such as 12.3456% is exact |

## Where rounding happens

```
1  each line amount      rounded at line level
2  subtotal              sum of ALREADY-ROUNDED line amounts
3  discount              rounded
4  taxable base          rounded
5  tax                   rounded once, from the base
6  retention             rounded once, from the base
7  advance recovery      rounded once, then capped at the outstanding advance
8  net payable           rounded
```

Rounding at line level and summing rounded amounts is deliberate. Summing unrounded amounts and
rounding once at the end produces a total that does not equal the sum of the printed lines — which a
client will notice, and be right to query.

## Worked edge cases

| Input | Result | Why |
|---|---|---|
| 0.125 → 2 dp | **0.13** | Half rounds up |
| 0.124 → 2 dp | 0.12 | |
| 0.135 → 2 dp | **0.14** | Half rounds up regardless of the preceding digit (unlike banker's rounding) |
| 1200 vs 1200.000 quantity | Identical | Both normalise to the declared scale |
| 1200.0004 vs 1200.0006 at 3 dp | 1200.000 vs 1200.001 | Distinct at the declared scale |

## Changing this policy

A change to rounding changes historical reproducibility. It requires a decision record, a new
calculation version stamped on subsequent invoice requests, and re-running the worked test cases.
Documents already issued keep the policy that produced them.
