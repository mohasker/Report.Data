#!/usr/bin/env python3
"""Numbering service: uniqueness under concurrency, lifecycle, no silent reuse (D-10)."""
import os, sqlite3, sys, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numbering import NumberingService
from harness import Checks


def run(model, data):
    c = Checks("Document numbering",
               "One service, many configurable series, with a reserved to issued or cancelled "
               "lifecycle and no silent reuse (D-10, ADR-0005 rev 1).")
    entity_code = {e["LegalEntityID"]: e["EntityCode"] for e in data["LegalEntities"]}
    series = {s["SeriesID"]: dict(s, _entity_code=entity_code[s["LegalEntityID"]])
              for s in data["NumberingSeries"]}

    # 1. concurrency: 8 threads x 25 reservations must yield 200 distinct numbers
    svc = NumberingService()
    for s in series.values():
        svc.register_series(s)
    got, errors = [], []
    lock = threading.Lock()

    def worker(n):
        for i in range(25):
            try:
                r = svc.reserve("SER-0001", "2026", "COMPANY", f"JOB-{n}-{i}")
                with lock:
                    got.append(r["formatted"])
            except Exception as e:                      # pragma: no cover
                with lock:
                    errors.append(repr(e))

    threads = [threading.Thread(target=worker, args=(n,)) for n in range(8)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    c.check("NUM-01", "200 concurrent reservations produce 200 distinct numbers",
            len(got) == 200 and len(set(got)) == 200 and not errors,
            f"issued {len(got)}, distinct {len(set(got))}, errors {len(errors)}")

    # 2. formatting follows the configured pattern
    c.check("NUM-02", "Numbers follow the configured pattern for their series",
            got and got[0].startswith("AH-TR-2026-") and len(got[0].split("-")[-1]) == 3,
            f"first number: {sorted(got)[0]}")

    # 3. series are independent: a second document type does not share the counter
    a = svc.reserve("SER-0002", "2026", "COMPANY", "JOB-Q1")
    c.check("NUM-03", "A different document type uses a different series and restarts at its own start number",
            a["sequence"] == 1 and a["formatted"].startswith("AH-QT-2026-"),
            f"quotation series first number: {a['formatted']}")

    # 4. a per-project series is partitioned from the company-wide one
    p1 = svc.reserve("SER-0004", "2026", "IRRG-003", "JOB-P1")
    c.check("NUM-04", "A project-scoped series is partitioned from the company-wide series",
            p1["sequence"] == 1 and "IRRG-003" in p1["formatted"],
            f"project series first number: {p1['formatted']}")

    # 5. a second legal entity has its own sequence
    e2 = svc.reserve("SER-0006", "2026", "COMPANY", "JOB-E2")
    c.check("NUM-05", "A second legal entity gets its own independent sequence and its own prefix",
            e2["sequence"] == 1 and e2["formatted"].startswith("AHX-"),
            f"second entity first number: {e2['formatted']} (company-wide AH series is unaffected)")

    # 6. lifecycle: reserve -> issue
    r = svc.reserve("SER-0003", "2026", "COMPANY", "JOB-CC1")
    svc.issue(r["number_id"], "DOC-CC1")
    states = dict((f, s) for f, s, _ in svc.all_numbers())
    c.check("NUM-06", "A reserved number can be issued",
            states.get(r["formatted"]) == "Issued", f"{r['formatted']} -> Issued")

    # 7. lifecycle: reserve -> cancel, with a mandatory reason
    r2 = svc.reserve("SER-0003", "2026", "COMPANY", "JOB-CC2")
    svc.cancel(r2["number_id"], "generation failed during template merge")
    reasons = dict((f, reason) for f, s, reason in svc.all_numbers() if s == "Cancelled")
    c.check("NUM-07", "A cancelled number records a reason, so the gap is explainable",
            reasons.get(r2["formatted"]), f"{r2['formatted']} cancelled: {reasons.get(r2['formatted'])}")

    c.expect_raises("NUM-08", "Cancelling without a reason is rejected",
                    lambda: svc.cancel(svc.reserve("SER-0003", "2026", "COMPANY", "J")["number_id"], ""),
                    ValueError)

    # 8. no silent reuse
    c.expect_raises("NUM-09", "Reusing a cancelled sequence value is rejected by the register",
                    lambda: svc.reuse_attempt("SER-0003", "2026", "COMPANY",
                                              r2["sequence"], "JOB-CC3"),
                    sqlite3.IntegrityError)

    # 9. an issued number cannot be re-issued or cancelled
    c.expect_raises("NUM-10", "An issued number cannot be issued again",
                    lambda: svc.issue(r["number_id"], "DOC-OTHER"), ValueError)
    c.expect_raises("NUM-11", "An issued number cannot be cancelled",
                    lambda: svc.cancel(r["number_id"], "changed my mind"), ValueError)

    # 10. migration from an existing manual register continues rather than colliding
    svc2 = NumberingService()
    for s in series.values():
        svc2.register_series(s)
    svc2.seed_manual_history("SER-0001", "2026", "COMPANY", 147)
    nxt = svc2.reserve("SER-0001", "2026", "COMPANY", "JOB-MIG")
    c.check("NUM-12", "Migration continues the existing manual register instead of restarting it",
            nxt["sequence"] == 148, f"last manual number 147, next issued {nxt['formatted']}")

    # 11. year partitioning
    y = svc2.reserve("SER-0001", "2027", "COMPANY", "JOB-Y")
    c.check("NUM-13", "A new year starts its own sequence where the series resets per year",
            y["sequence"] == 1, f"2027 first number: {y['formatted']}")
    return c
