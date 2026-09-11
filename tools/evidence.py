#!/usr/bin/env python3
"""Effective evidence rules and submission completeness (deliverable 4 of D-15).

A project that needs a different rule gets a configuration row, never a code change.
The effective rule is the global activity rule with any project override applied, and
the source of each decision is reported so a supervisor can be told why a submission
was blocked.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BOOL_FIELDS = ["RequiresBeforePhoto", "RequiresAfterPhoto", "RequiresQuantity", "RequiresCaption"]
CAPTION_MANDATORY_STAGES = {"Snag", "Observation", "Material", "Safety"}


def truthy(v):
    return str(v or "").upper() == "TRUE"


def effective_rule(data, project_id, activity_type_id):
    """Return the effective rule plus, per field, where it came from."""
    glob = next((a for a in data["ActivityTypes"]
                 if a["ActivityTypeID"] == activity_type_id), None)
    if glob is None:
        raise KeyError(f"unknown activity type {activity_type_id}")
    override = next((r for r in data.get("ProjectActivityRules", [])
                     if r["ProjectID"] == project_id
                     and r["ActivityTypeID"] == activity_type_id), None)

    rule = {"ActivityTypeID": activity_type_id, "ProjectID": project_id,
            "IsPermitted": True, "sources": {}}
    for f in BOOL_FIELDS:
        value = truthy(glob.get(f)) if f in glob else False
        rule["sources"][f] = "Global"
        if override and (override.get(f) or "") != "":
            value = truthy(override[f])
            rule["sources"][f] = "ProjectOverride"
        rule[f] = value
    rule["MinPhotos"] = int(glob.get("MinPhotos") or 0)
    rule["sources"]["MinPhotos"] = "Global"
    rule["QuantityUnitID"] = glob.get("QuantityUnitID") or ""
    rule["sources"]["QuantityUnitID"] = "Global"
    if override:
        if (override.get("MinPhotos") or "") != "":
            rule["MinPhotos"] = int(override["MinPhotos"])
            rule["sources"]["MinPhotos"] = "ProjectOverride"
        if (override.get("QuantityUnitID") or "") != "":
            rule["QuantityUnitID"] = override["QuantityUnitID"]
            rule["sources"]["QuantityUnitID"] = "ProjectOverride"
        rule["IsPermitted"] = truthy(override.get("IsPermitted"))
        rule["sources"]["IsPermitted"] = "ProjectOverride"
    return rule


def evaluate_activity(data, activity, photos):
    """Return (complete: bool, failures: [str]). Every failure names what to fix."""
    rule = effective_rule(data, activity["ProjectID"], activity["ActivityTypeID"])
    fails = []
    if not rule["IsPermitted"]:
        fails.append("This activity is not permitted on this project")
    stages = [p["EvidenceStage"] for p in photos]
    if rule["RequiresBeforePhoto"] and "Before" not in stages:
        fails.append("A 'Before' photograph is required")
    if rule["RequiresAfterPhoto"] and "After" not in stages:
        fails.append("An 'After' photograph is required")
    if len(photos) < rule["MinPhotos"]:
        fails.append(f"At least {rule['MinPhotos']} photographs are required, {len(photos)} attached")
    q = (activity.get("Quantity") or "").strip()
    if rule["RequiresQuantity"]:
        if q == "":
            fails.append("A quantity is required for this activity")
        else:
            try:
                if float(q) < 0:
                    fails.append("Quantity must not be negative")
            except ValueError:
                fails.append("Quantity must be numeric")
        if q != "" and not (activity.get("UnitID") or "").strip():
            fails.append("A unit is required when a quantity is entered")
    elif q != "":
        fails.append("A quantity was entered for an activity that does not take one")

    for p in photos:
        caption = (p.get("CaptionEN") or "").strip() or (p.get("CaptionAR") or "").strip()
        if p["EvidenceStage"] in CAPTION_MANDATORY_STAGES and not caption:
            fails.append(f"{p['PhotoID']}: a caption is mandatory for "
                         f"{p['EvidenceStage']} evidence")
        elif rule["RequiresCaption"] and not caption:
            fails.append(f"{p['PhotoID']}: this project requires a caption on every photograph")
    return (not fails), fails


def evaluate_visit(data, visit):
    """A visit is complete when it carries evidence.

    Owner decision D-22 removed the requirement to declare an activity before capturing.
    The normal path is: open the app, confirm project and location if necessary, capture
    the photographs, save and share. So a visit carrying photographs and no activity is a
    valid photographic submission, and its classification catches up afterwards.

    An activity that DOES exist still has to satisfy its effective rule in full: nothing
    about the quantity, caption or minimum-photograph rules is relaxed. What changed is
    that declaring an activity is no longer the price of submitting evidence.
    """
    acts = [a for a in data["VisitActivities"] if a["VisitID"] == visit["VisitID"]]
    visit_photos = [p for p in data["Photos"] if p.get("VisitID") == visit["VisitID"]]
    if not acts and not visit_photos:
        return False, ["A visit must carry at least one photograph or one activity"]
    fails = []
    for a in acts:
        photos = [p for p in data["Photos"] if p.get("VisitActivityID") == a["VisitActivityID"]]
        ok, f = evaluate_activity(data, a, photos)
        fails += [f"{a['VisitActivityID']}: {x}" for x in f]
    return (not fails), fails
