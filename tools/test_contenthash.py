#!/usr/bin/env python3
"""Content hashing and approval invalidation (ADR-0006, conflict C-06)."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contenthash
from harness import Checks


def run(model, data):
    c = Checks("Content hashing and approval binding",
               "An approval is valid only for the exact content it approved, and 'material' has "
               "one published definition (C-06).")
    visit = next(v for v in data["SiteVisits"] if v["VisitID"] == "VIS-0001")
    h0 = contenthash.visit_hash(model, data, visit)

    c.check("HASH-01", "A hash is a 64-character SHA-256 hex digest",
            len(h0) == 64 and all(ch in "0123456789abcdef" for ch in h0), h0)

    c.check("HASH-02", "The same content always hashes to the same value",
            contenthash.visit_hash(model, data, copy.deepcopy(visit)) == h0, "recomputed, identical")

    # material change: a quantity-bearing field inside the hash set
    v2 = copy.deepcopy(visit)
    v2["OverallDescriptionEN"] = visit["OverallDescriptionEN"] + " Additional works noted."
    c.check("HASH-03", "A material change produces a different hash, voiding the approval",
            contenthash.visit_hash(model, data, v2) != h0, "description edited -> hash changed")

    # immaterial change: a system field outside the hash set
    v3 = copy.deepcopy(visit)
    v3["UpdatedAt"] = "2030-01-01T00:00:00Z"
    v3["UpdatedBy"] = "someone.else@synthetic.example"
    c.check("HASH-04", "An immaterial change does not void an approval",
            contenthash.visit_hash(model, data, v3) == h0,
            "UpdatedAt and UpdatedBy changed -> hash unchanged")

    # advisory AI output must never void a human approval
    photo = next(p for p in data["Photos"] if p["PhotoID"] == "PHO-0001")
    ph0 = contenthash.content_hash(model, "Photos", photo)
    p2 = copy.deepcopy(photo)
    p2["AIObservation"] = '{"observable_facts": ["late arriving advisory analysis"]}'
    p2["AIConfidence"] = "0.99"
    p2["AIAnalysisStatus"] = "Completed"
    c.check("HASH-05", "Advisory AI output arriving later never voids a human approval",
            contenthash.content_hash(model, "Photos", p2) == ph0,
            "AI observation, confidence and status changed -> photo hash unchanged (C-06)")

    # a reviewer decision that changes what appears in the report IS material
    p3 = copy.deepcopy(photo)
    p3["ApprovedForReport"] = "FALSE"
    c.check("HASH-06", "Withdrawing a photograph from the report is material",
            contenthash.content_hash(model, "Photos", p3) != ph0,
            "ApprovedForReport TRUE -> FALSE changed the hash")

    # re-sequencing approved photographs changes the visit hash
    data2 = copy.deepcopy(data)
    for p in data2["Photos"]:
        if p["PhotoID"] == "PHO-0002":
            p["ReportSequence"] = "9"
    c.check("HASH-07", "Re-ordering the approved photographs changes the visit hash",
            contenthash.visit_hash(model, data2, visit) != h0,
            "report sequence altered -> parent hash changed")

    # adding an approved photograph to the visit changes the visit hash
    data3 = copy.deepcopy(data)
    for p in data3["Photos"]:
        if p["PhotoID"] == "PHO-0003":
            p["ApprovedForReport"] = "TRUE"
            p["ReportSequence"] = "3"
    c.check("HASH-08", "Approving an additional photograph changes the visit hash",
            contenthash.visit_hash(model, data3, visit) != h0,
            "a newly approved child photograph is folded into the parent hash")

    # null and empty string must not differ
    a = copy.deepcopy(visit); a["Weather"] = ""
    b = copy.deepcopy(visit); b["Weather"] = None
    c.check("HASH-09", "NULL and empty string hash identically, so they never differ by accident",
            contenthash.visit_hash(model, data, a) == contenthash.visit_hash(model, data, b),
            "'' and None produce the same canonical value")

    # whitespace and Unicode normalisation
    d1 = copy.deepcopy(visit); d1["OverallDescriptionAR"] = "  " + visit["OverallDescriptionAR"] + " "
    c.check("HASH-10", "Leading and trailing whitespace does not change a hash",
            contenthash.visit_hash(model, data, d1) == h0, "text is trimmed before hashing")

    # decimal scale normalisation: 1200 and 1200.000 are the same quantity
    act = next(a_ for a_ in data["VisitActivities"] if a_["VisitActivityID"] == "VAC-0001")
    a1 = copy.deepcopy(act); a1["Quantity"] = "1200"
    a2 = copy.deepcopy(act); a2["Quantity"] = "1200.000"
    c.check("HASH-11", "The same quantity written at different scales hashes identically",
            contenthash.content_hash(model, "VisitActivities", a1) ==
            contenthash.content_hash(model, "VisitActivities", a2),
            "1200 and 1200.000 normalise to the declared scale")

    # a genuinely different quantity must differ
    a3 = copy.deepcopy(act); a3["Quantity"] = "1200.001"
    c.check("HASH-12", "A quantity that differs at the declared scale changes the hash",
            contenthash.content_hash(model, "VisitActivities", a3) !=
            contenthash.content_hash(model, "VisitActivities", a1), "1200.000 vs 1200.001")

    # the canonical field set is published and versioned
    canonical = model["canonical_hash"]
    c.check("HASH-13", "The canonical field set is published and versioned",
            canonical["field_set_version"] == contenthash.FIELD_SET_VERSION
            and len(canonical["rules"]) >= 8,
            f"version {canonical['field_set_version']}, {len(canonical['rules'])} published rules")

    # every hashable table declares its field list
    hashable = [t for t, v in model["tables"].items() if v["content_hash_fields"]]
    c.check("HASH-14", "Every hashable entity declares exactly which fields are material",
            len(hashable) >= 3, f"hashable tables: {', '.join(hashable)}")
    return c
