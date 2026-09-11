#!/usr/bin/env python3
"""Per-project evidence rules and submission completeness (D-15 item 4, conflict C-07)."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence
from harness import Checks


def run(model, data):
    c = Checks("Evidence rules",
               "Evidence requirements are configuration, resolved per project, and a blocked "
               "submission always says exactly what to fix (C-07).")

    # 1. the global rule applies when a project has no override
    r = evidence.effective_rule(data, "PRJ-0002", "ACT-0016")
    c.check("EVD-01", "A project with no override inherits the global activity rule",
            r["RequiresBeforePhoto"] and r["sources"]["RequiresBeforePhoto"] == "Global",
            "PRJ-0002 / manual weeding inherits RequiresBeforePhoto from the catalogue")

    # 2. a project override wins, and its source is reported
    r = evidence.effective_rule(data, "PRJ-0001", "ACT-0004")
    c.check("EVD-02", "A project override replaces the global rule and says so",
            r["RequiresQuantity"] and r["sources"]["RequiresQuantity"] == "ProjectOverride"
            and r["MinPhotos"] == 2,
            "PRJ-0001 requires a quantity for irrigation inspection where the global rule does not")

    # 3. the same activity can have different rules on different projects
    a = evidence.effective_rule(data, "PRJ-0001", "ACT-0011")
    b = evidence.effective_rule(data, "PRJ-0002", "ACT-0011")
    c.check("EVD-03", "The same activity carries different rules on different projects",
            a["MinPhotos"] != b["MinPhotos"],
            f"pesticide application requires {a['MinPhotos']} photos on PRJ-0001 and "
            f"{b['MinPhotos']} on PRJ-0002")

    # 4. an activity can be withdrawn from one project without deleting it
    r = evidence.effective_rule(data, "PRJ-0001", "ACT-0021")
    r2 = evidence.effective_rule(data, "PRJ-0002", "ACT-0021")
    c.check("EVD-04", "An activity can be forbidden on one project and permitted on another",
            not r["IsPermitted"] and r2["IsPermitted"],
            "ceiling tile replacement is not permitted on the landscape project")

    # 5. a complete visit passes
    v1 = next(v for v in data["SiteVisits"] if v["VisitID"] == "VIS-0001")
    ok, fails = evidence.evaluate_visit(data, v1)
    c.check("EVD-05", "A visit meeting every effective rule is judged complete",
            ok, "; ".join(fails) or "VIS-0001 complete")

    # 6. a missing mandatory caption blocks, with a specific message
    v4 = next(v for v in data["SiteVisits"] if v["VisitID"] == "VIS-0004")
    ok, fails = evidence.evaluate_visit(data, v4)
    c.check("EVD-06", "A snag photograph without a caption blocks submission with a specific reason",
            not ok and any("caption is mandatory" in f for f in fails),
            "; ".join(fails))

    # 7. a missing 'After' photograph blocks
    d = copy.deepcopy(data)
    d["Photos"] = [p for p in d["Photos"] if p["PhotoID"] != "PHO-0002"]
    ok, fails = evidence.evaluate_visit(d, v1)
    c.check("EVD-07", "Removing the required 'After' photograph blocks submission",
            not ok and any("'After' photograph is required" in f for f in fails), "; ".join(fails))

    # 8. a missing required quantity blocks
    d = copy.deepcopy(data)
    for a_ in d["VisitActivities"]:
        if a_["VisitActivityID"] == "VAC-0001":
            a_["Quantity"] = ""
    ok, fails = evidence.evaluate_visit(d, v1)
    c.check("EVD-08", "A missing required quantity blocks submission",
            not ok and any("quantity is required" in f for f in fails), "; ".join(fails))

    # 9. a negative quantity is rejected
    d = copy.deepcopy(data)
    for a_ in d["VisitActivities"]:
        if a_["VisitActivityID"] == "VAC-0001":
            a_["Quantity"] = "-5"
    ok, fails = evidence.evaluate_visit(d, v1)
    c.check("EVD-09", "A negative quantity is rejected",
            not ok and any("negative" in f for f in fails), "; ".join(fails))

    # 10. a quantity on an activity that takes none is rejected
    d = copy.deepcopy(data)
    for a_ in d["VisitActivities"]:
        if a_["VisitActivityID"] == "VAC-0007":
            a_["Quantity"] = "10"
            a_["UnitID"] = "UNIT-M2"
    v6 = next(v for v in data["SiteVisits"] if v["VisitID"] == "VIS-0006")
    ok, fails = evidence.evaluate_visit(d, v6)
    c.check("EVD-10", "A quantity entered where the rule takes none is rejected",
            not ok and any("does not take one" in f for f in fails), "; ".join(fails))

    # 11. a visit with no activity cannot be submitted
    d = copy.deepcopy(data)
    d["VisitActivities"] = [a_ for a_ in d["VisitActivities"] if a_["VisitID"] != "VIS-0001"]
    ok, fails = evidence.evaluate_visit(d, v1)
    c.check("EVD-11", "A visit with no activity cannot be submitted",
            not ok and any("at least one activity" in f for f in fails), "; ".join(fails))

    # 12. every failure message is actionable
    d = copy.deepcopy(data)
    for a_ in d["VisitActivities"]:
        if a_["VisitActivityID"] == "VAC-0001":
            a_["Quantity"] = ""
    _, fails = evidence.evaluate_visit(d, v1)
    c.check("EVD-12", "Every blocking message names what to fix, never a generic rejection",
            all(len(f) > 25 and "invalid" != f.lower() for f in fails), "; ".join(fails))

    # 13. duplicate detection flags rather than deletes
    dupes = [p for p in data["Photos"] if (p.get("IsDuplicateSuspected") or "").upper() == "TRUE"]
    c.check("EVD-13", "A suspected duplicate is flagged and retained, never deleted or merged",
            dupes and all(p.get("DuplicateOfPhotoID") for p in dupes),
            f"{len(dupes)} suspected duplicate(s), each pointing at the original and still present")

    # 14. GPS is evidence, not a gate
    no_gps = [p["PhotoID"] for p in data["Photos"] if not (p.get("GPSLatitude") or "").strip()]
    blocked = []
    for pid in no_gps:
        p = next(x for x in data["Photos"] if x["PhotoID"] == pid)
        act = next((a_ for a_ in data["VisitActivities"]
                    if a_["VisitActivityID"] == p.get("VisitActivityID")), None)
        if act:
            ok, fails = evidence.evaluate_activity(data, act, [p])
            if any("GPS" in f for f in fails):
                blocked.append(pid)
    c.check("EVD-14", "Missing GPS never blocks a submission and is recorded as missing, not zero",
            not blocked and no_gps,
            f"{len(no_gps)} photographs without GPS, none blocked, none defaulted to 0")
    return c
