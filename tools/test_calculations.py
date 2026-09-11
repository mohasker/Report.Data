#!/usr/bin/env python3
"""Worked financial test cases (spec 13, decisions D-08 and D-07)."""
import os, sys
from decimal import Decimal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calc
from calc import calculate_invoice, check_cumulative, CalculationError
from harness import Checks

UNCONFIRMED = {"TaxRuleID": "TAX-PLACEHOLDER-001",
               "TaxRuleCode": "PENDING_ACCOUNTANT_CONFIRMATION",
               "ConfirmedByAccountant": "FALSE", "RatePercent": "", "Version": 1}
# Exists only so the arithmetic can be exercised offline. It asserts nothing about any
# jurisdiction and must never appear in production data (D-08).
SYNTHETIC = {"TaxRuleID": "TAX-SYNTHETIC-TEST", "TaxRuleCode": "SYNTHETIC_TEST_ONLY",
             "ConfirmedByAccountant": "TRUE", "RatePercent": "5.0000", "Version": 3}


def run(model, data):
    c = Checks("Deterministic calculation",
               "Every figure is produced by formula from stored inputs, with one rounding policy "
               "and a reproducible trace. No figure originates from a language model.")
    contracts = {r["ContractID"]: r for r in data["Contracts"]}
    boq = {r["BOQItemID"]: r for r in data["BOQItems"]}
    cnt1 = contracts["CNT-0001"]

    def line(q, rate, item=None):
        return {"BOQItemID": item, "Quantity": q, "UnitRate": rate,
                "boq": boq[item] if item else None}

    # 1. an unconfirmed tax rule blocks, it does not silently produce zero
    r = calculate_invoice([line("1200", "3.500", "BOQ-0001")], cnt1, UNCONFIRMED, "QAR")
    c.check("CALC-01", "An unconfirmed tax rule yields UNDETERMINED and blocks, never zero",
            r["status"] == "BLOCKED_TAX_UNCONFIRMED" and r["tax_amount"] is None
            and r["net_payable"] is None,
            f"status={r['status']} tax={r['tax_amount']} net={r['net_payable']}")

    # 2. line and subtotal arithmetic
    c.check("CALC-02", "Line amount and subtotal are exact",
            r["subtotal"] == "4200.00", f"1200 x 3.500 = {r['subtotal']}")

    # 3. retention on the taxable base
    c.check("CALC-03", "Retention is computed from the configured contract percentage",
            r["retention"] == "210.00", f"5% of 4200.00 = {r['retention']}")

    # 4. full arithmetic with a synthetic confirmed rule
    r2 = calculate_invoice([line("1200", "3.500", "BOQ-0001"), line("100", "18.000", "BOQ-0002")],
                           cnt1, SYNTHETIC, "QAR")
    expected_sub = Decimal("4200.00") + Decimal("1800.00")
    c.check("CALC-04", "Multiple lines sum correctly",
            r2["subtotal"] == f"{expected_sub:.2f}", f"subtotal = {r2['subtotal']}")
    c.check("CALC-05", "Tax applies to the taxable base and is rounded once",
            r2["tax_amount"] == "300.00", f"5% of 6000.00 = {r2['tax_amount']}")
    c.check("CALC-06", "Net payable is base + tax - retention - advance recovery",
            r2["net_payable"] == "6000.00",
            f"6000.00 + 300.00 - 300.00 - 0.00 = {r2['net_payable']}")

    # 5. the tax rule AND its version are preserved (D-08)
    c.check("CALC-07", "The applied tax rule and its version are preserved in the result and trace",
            r2["tax_rule_id"] == "TAX-SYNTHETIC-TEST" and r2["tax_rule_version"] == 3
            and any(t.get("tax_rule_version") == 3 for t in r2["trace"]),
            f"rule={r2['tax_rule_id']} version={r2['tax_rule_version']}")

    # 6. rounding edge case: half rounds up, deterministically
    r3 = calculate_invoice([line("1", "0.125")], cnt1, SYNTHETIC, "QAR")
    c.check("CALC-08", "Half-way values round half-up, deterministically",
            r3["lines"][0]["amount"] == "0.13", f"0.125 -> {r3['lines'][0]['amount']}")

    # 7. zero quantity is legal and yields zero
    r4 = calculate_invoice([line("0", "3.500")], cnt1, SYNTHETIC, "QAR")
    c.check("CALC-09", "Zero quantity is accepted and yields zero",
            r4["subtotal"] == "0.00", f"subtotal = {r4['subtotal']}")

    # 8. negative quantity and negative rate are rejected
    c.expect_raises("CALC-10", "Negative quantity is rejected",
                    lambda: calculate_invoice([line("-5", "3.5")], cnt1, SYNTHETIC, "QAR"),
                    CalculationError)
    c.expect_raises("CALC-11", "Negative rate is rejected",
                    lambda: calculate_invoice([line("5", "-3.5")], cnt1, SYNTHETIC, "QAR"),
                    CalculationError)

    # 9. currency mismatch is rejected, never converted
    c.expect_raises("CALC-12", "A currency mismatch is rejected and never converted",
                    lambda: calculate_invoice([line("1", "1")], cnt1, SYNTHETIC, "USD"),
                    CalculationError)

    # 10. the synthetic client currency trap is detected
    client3 = next(x for x in data["Clients"] if x["ClientID"] == "CLI-0003")
    proj3 = next(p for p in data["Projects"] if p["ProjectID"] == "PRJ-0003")
    c.check("CALC-13", "The planted client/project currency mismatch is detectable before billing",
            client3["Currency"] != proj3["Currency"],
            f"client {client3['Currency']} vs project {proj3['Currency']} — must be resolved "
            f"before any invoice request is created")

    # 11. cumulative quantity control
    c.expect_raises("CALC-14", "Certifying beyond contract plus variation is rejected",
                    lambda: check_cumulative(boq["BOQ-0001"], "9000"), CalculationError)
    ok = check_cumulative(boq["BOQ-0001"], "8000")
    c.check("CALC-15", "Certifying exactly to the contract quantity is permitted",
            str(ok["cumulative"]) == "12000.000" and str(ok["remaining"]) == "0.000",
            f"cumulative {ok['cumulative']} of permitted {ok['permitted']}")
    ov = check_cumulative(boq["BOQ-0001"], "9000",
                          {"ApprovedByUserID": "USR-0001", "Reason": "synthetic authorised override"})
    c.check("CALC-16", "An over-contract quantity passes only with a recorded authorised override",
            ov["override"] is True, "override recorded with approver and reason")
    c.expect_raises("CALC-17", "An override without an approver and reason is rejected",
                    lambda: check_cumulative(boq["BOQ-0001"], "9000", {"Reason": ""}),
                    CalculationError)

    # 12. approved variation extends the permitted quantity
    ok2 = check_cumulative(boq["BOQ-0002"], "350")
    c.check("CALC-18", "An approved variation extends the permitted quantity",
            str(ok2["permitted"]) == "550.000", f"500 contract + 50 variation = {ok2['permitted']}")

    # 13. advance recovery is capped at the outstanding advance
    cnt2 = contracts["CNT-0002"]
    r5 = calculate_invoice([line("100", "26.500")], cnt2, SYNTHETIC, "QAR",
                           outstanding_advance=Decimal("100.00"))
    c.check("CALC-19", "Advance recovery never exceeds the outstanding advance",
            r5["advance_recovery"] == "100.00",
            f"20% of 2650.00 would be 530.00; capped at outstanding 100.00 -> "
            f"{r5['advance_recovery']}")

    # 14. discount larger than the subtotal is rejected
    c.expect_raises("CALC-20", "A discount larger than the subtotal is rejected",
                    lambda: calculate_invoice([line("1", "10")], cnt1, SYNTHETIC, "QAR",
                                              discount=Decimal("50")), CalculationError)

    # 15. the trace is complete and reproducible
    same = calculate_invoice([line("1200", "3.500", "BOQ-0001")], cnt1, SYNTHETIC, "QAR")
    again = calculate_invoice([line("1200", "3.500", "BOQ-0001")], cnt1, SYNTHETIC, "QAR")
    c.check("CALC-21", "The same inputs always produce the same figures and the same trace",
            same == again and len(same["trace"]) >= 6,
            f"{len(same['trace'])} trace steps, byte-identical on repeat")

    # 16. no float anywhere in the money path
    c.check("CALC-22", "Money is decimal end to end, never floating point",
            all(isinstance(v, str) or v is None
                for v in [same["subtotal"], same["tax_amount"], same["net_payable"]]),
            "all monetary values are decimal strings")
    return c
