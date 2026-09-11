#!/usr/bin/env python3
"""Deterministic financial calculation (spec 11, invariant I-4, decisions D-07 and D-08).

Every figure that can reach a certificate or an invoice is produced here, from stored
inputs, using decimal arithmetic and one central rounding policy — never by a language
model, and never by floating point.

Two rules from the owner's decisions are enforced in code rather than described in prose:

  * D-08. A tax rule that the accountant has not confirmed in writing yields an
    UNDETERMINED tax amount and a BLOCKED result. It does not quietly yield zero,
    because "no tax configured" and "zero-rated" are not the same statement.
  * The tax rule AND its version are copied into the result and the trace, so an
    invoice can always be re-explained with the rule that actually applied.
"""
import os, sys
from decimal import Decimal, ROUND_HALF_UP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MONEY_SCALE = 2          # QAR minor units; overridden per currency by configuration
QUANTITY_SCALE = 3
ROUNDING = ROUND_HALF_UP


def money(value):
    return Decimal(value).quantize(Decimal(1).scaleb(-MONEY_SCALE), rounding=ROUNDING)


def qty(value):
    return Decimal(value).quantize(Decimal(1).scaleb(-QUANTITY_SCALE), rounding=ROUNDING)


class CalculationError(Exception):
    pass


class Result(dict):
    @property
    def blocked(self):
        return self.get("status") != "OK"


def check_cumulative(boq_item, current_quantity, override=None):
    """Cumulative quantity must not exceed contract plus approved variation."""
    contract = qty(boq_item["ContractQuantity"])
    variation = qty(boq_item.get("ApprovedVariationQuantity") or 0)
    previous = qty(boq_item.get("PreviouslyCertifiedQuantity") or 0)
    current = qty(current_quantity)
    cumulative = previous + current
    permitted = contract + variation
    if cumulative > permitted:
        if not override:
            raise CalculationError(
                f"cumulative quantity {cumulative} exceeds contract plus approved variation "
                f"{permitted} for item {boq_item['ItemNumber']}; an authorised override is required")
        if not override.get("ApprovedByUserID") or not override.get("Reason"):
            raise CalculationError("an override must record an approver and a reason")
    return {"previous": previous, "current": current, "cumulative": cumulative,
            "permitted": permitted, "remaining": permitted - cumulative,
            "override": bool(override)}


def calculate_invoice(lines, contract, tax_rule, currency, discount=Decimal("0"),
                      outstanding_advance=Decimal("0"), overrides=None):
    """lines: [{'BOQItemID','Quantity','UnitRate','DescriptionEN', 'boq': row}]"""
    trace = []
    overrides = overrides or {}

    # 1. currency agreement -------------------------------------------------
    if contract.get("Currency") != currency:
        raise CalculationError(
            f"currency mismatch: contract is {contract.get('Currency')}, request is {currency}. "
            f"No conversion is performed anywhere in this system (C-09).")
    trace.append({"step": "currency", "value": currency,
                  "rule": "single currency, taken from the contract"})

    # 2. lines --------------------------------------------------------------
    computed, subtotal = [], Decimal("0")
    for i, line in enumerate(lines, start=1):
        q = qty(line["Quantity"])
        rate = Decimal(str(line["UnitRate"]))
        if q < 0:
            raise CalculationError(f"line {i}: negative quantity is rejected")
        if rate < 0:
            raise CalculationError(f"line {i}: negative rate is rejected")
        if line.get("boq"):
            cum = check_cumulative(line["boq"], q, overrides.get(line.get("BOQItemID")))
            trace.append({"step": f"line {i} cumulative check",
                          "value": str(cum["cumulative"]), "permitted": str(cum["permitted"]),
                          "override": cum["override"]})
        amount = money(q * rate)
        subtotal += amount
        computed.append({"line": i, "quantity": str(q), "rate": str(rate), "amount": str(amount)})
        trace.append({"step": f"line {i} amount", "expression": f"{q} x {rate}",
                      "value": str(amount),
                      "rule": f"rounded to {MONEY_SCALE} dp, ROUND_HALF_UP, at line level"})
    subtotal = money(subtotal)
    trace.append({"step": "subtotal", "value": str(subtotal),
                  "rule": "sum of already-rounded line amounts"})

    # 3. discount -----------------------------------------------------------
    discount = money(discount)
    if discount > subtotal:
        raise CalculationError("discount exceeds the subtotal")
    base = money(subtotal - discount)
    trace.append({"step": "taxable base", "expression": f"{subtotal} - {discount}",
                  "value": str(base)})

    # 4. tax — D-08 ---------------------------------------------------------
    tax_status = "UNDETERMINED"
    tax_amount = None
    confirmed = str(tax_rule.get("ConfirmedByAccountant", "FALSE")).upper() == "TRUE"
    rate_raw = tax_rule.get("RatePercent")
    if not confirmed or rate_raw in (None, ""):
        trace.append({
            "step": "tax", "value": "UNDETERMINED",
            "rule": "The applicable tax rule is not confirmed in writing by the accountant, so no "
                    "tax figure is produced. 'No tax configured' is NOT 'zero-rated', 'exempt' or "
                    "'out of scope' (D-08). Production invoicing stays blocked.",
            "tax_rule_id": tax_rule.get("TaxRuleID"),
            "tax_rule_version": tax_rule.get("Version")})
    else:
        rate = Decimal(str(rate_raw))
        tax_amount = money(base * rate / Decimal("100"))
        tax_status = "APPLIED"
        trace.append({"step": "tax", "expression": f"{base} x {rate}%", "value": str(tax_amount),
                      "tax_rule_id": tax_rule.get("TaxRuleID"),
                      "tax_rule_code": tax_rule.get("TaxRuleCode"),
                      "tax_rule_version": tax_rule.get("Version"),
                      "rule": "rate applied to the taxable base, rounded once"})

    # 5. retention ----------------------------------------------------------
    retention_pct = Decimal(str(contract.get("RetentionPercent") or 0))
    retention = money(base * retention_pct / Decimal("100"))
    trace.append({"step": "retention", "expression": f"{base} x {retention_pct}%",
                  "value": str(retention)})

    # 6. advance recovery ---------------------------------------------------
    recovery_pct = Decimal(str(contract.get("AdvanceRecoveryPercent") or 0))
    recovery = money(base * recovery_pct / Decimal("100"))
    outstanding_advance = money(outstanding_advance)
    if recovery > outstanding_advance:
        recovery = outstanding_advance
        trace.append({"step": "advance recovery capped",
                      "value": str(recovery),
                      "rule": "recovery may never exceed the outstanding advance"})
    else:
        trace.append({"step": "advance recovery", "expression": f"{base} x {recovery_pct}%",
                      "value": str(recovery)})

    # 7. net payable --------------------------------------------------------
    if tax_status == "APPLIED":
        net = money(base + tax_amount - retention - recovery)
        status = "OK"
        trace.append({"step": "net payable",
                      "expression": f"{base} + {tax_amount} - {retention} - {recovery}",
                      "value": str(net)})
    else:
        net = None
        status = "BLOCKED_TAX_UNCONFIRMED"
        trace.append({"step": "net payable", "value": "NOT COMPUTED",
                      "rule": "A net payable is not produced while the tax treatment is "
                              "unconfirmed. The draft exists; it cannot be issued (D-08)."})

    return Result({
        "status": status,
        "currency": currency,
        "lines": computed,
        "subtotal": str(subtotal),
        "discount": str(discount),
        "taxable_base": str(base),
        "tax_status": tax_status,
        "tax_amount": None if tax_amount is None else str(tax_amount),
        "tax_rule_id": tax_rule.get("TaxRuleID"),
        "tax_rule_version": tax_rule.get("Version"),
        "retention": str(retention),
        "advance_recovery": str(recovery),
        "net_payable": None if net is None else str(net),
        "rounding_policy": f"ROUND_HALF_UP, money {MONEY_SCALE} dp, quantity {QUANTITY_SCALE} dp",
        "trace": trace,
    })
