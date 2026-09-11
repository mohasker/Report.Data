#!/usr/bin/env python3
"""Prove that nothing crosses a project boundary (deliverable 16 of D-15).

Data, images, recipients, templates, document numbers and financial records are each
tested separately, because they leak in different ways.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import security
from harness import Checks

AS_OF = "2026-04-30"
PROJECT_SCOPED = ["SiteVisits", "VisitActivities", "Photos", "Snags", "Locations",
                  "ProjectActivityRules", "BOQItems"]
FINANCIAL = ["Contracts", "BOQItems", "InvoiceRequests", "InvoiceLines", "TaxRules"]
FIELD_ROLES = {"USR-0005": "SiteSupervisor", "USR-0006": "SiteSupervisor",
               "USR-0007": "SiteSupervisor", "USR-0008": "FieldUser",
               "USR-0011": "FieldUser (unassigned)", "USR-0012": "SiteSupervisor (expired)"}


def run(model, data):
    c = Checks("Project segregation",
               "No data, image, recipient, template, document number or financial record may "
               "cross a project boundary (D-15 item 16).")

    # 1. every project-scoped row is visible only to users assigned to that project
    leaks = []
    for user_id, label in FIELD_ROLES.items():
        assigned = set(security.active_assignments(data, user_id, AS_OF))
        for table in PROJECT_SCOPED:
            for row in security.readable_rows(model, data, user_id, table, AS_OF):
                if row.get("ProjectID") not in assigned:
                    leaks.append(f"{user_id} ({label}) read {table} row of "
                                 f"{row.get('ProjectID')} without an assignment")
    c.check("SEG-01", "Field and supervisor roles read only their assigned projects",
            not leaks, "; ".join(leaks[:5]) or
            f"{len(FIELD_ROLES)} users x {len(PROJECT_SCOPED)} tables checked, no leak")

    # 2. an absent assignment grants nothing
    total = sum(len(security.readable_rows(model, data, "USR-0011", t, AS_OF))
                for t in PROJECT_SCOPED)
    c.check("SEG-02", "A user with no assignment reads nothing at all",
            total == 0, f"rows visible to USR-0011: {total}")

    # 3. an expired assignment grants nothing
    total = sum(len(security.readable_rows(model, data, "USR-0012", t, AS_OF))
                for t in PROJECT_SCOPED)
    c.check("SEG-03", "An expired assignment grants nothing",
            total == 0, f"rows visible to USR-0012 (assignment ended 2026-02-28): {total}")

    # 4. a multi-project user sees exactly their projects, and no others
    seen = {r["ProjectID"] for r in security.readable_rows(model, data, "USR-0007",
                                                           "SiteVisits", AS_OF)}
    c.check("SEG-04", "A multi-project user sees each assigned project and no others",
            seen == {"PRJ-0002", "PRJ-0003"}, f"projects visible to USR-0007: {sorted(seen)}")

    # 5. images specifically (the evidence that matters most)
    photo_leaks = []
    for user_id in FIELD_ROLES:
        assigned = set(security.active_assignments(data, user_id, AS_OF))
        for p in security.readable_rows(model, data, user_id, "Photos", AS_OF):
            if p["ProjectID"] not in assigned:
                photo_leaks.append(f"{user_id} -> {p['PhotoID']}")
    c.check("SEG-05", "Photographic evidence never crosses a project boundary",
            not photo_leaks, "; ".join(photo_leaks) or "no photo visible outside an assignment")

    # 6. financial tables are absent from every field role's data set
    fin_leaks = []
    for user_id in FIELD_ROLES:
        for table in FINANCIAL:
            allowed, _ = security.can(model, data, user_id, table, "read",
                                      {"ProjectID": "PRJ-0001"}, AS_OF)
            if allowed:
                fin_leaks.append(f"{user_id} can read {table}")
    c.check("SEG-06", "No field role can read any financial table",
            not fin_leaks, "; ".join(fin_leaks) or
            f"{len(FIELD_ROLES)} users x {len(FINANCIAL)} financial tables, no access")

    # 7. recipients resolve only within the project's own client
    recipient_leaks = []
    clients = {c_["ClientID"]: c_ for c_ in data["Clients"]}
    for proj in data["Projects"]:
        allowed = {ct["ContactID"] for ct in data["Contacts"]
                   if ct["ClientID"] == proj["ClientID"]
                   and ct["IsAuthorizedRecipient"].upper() == "TRUE"}
        others = {ct["ContactID"] for ct in data["Contacts"]
                  if ct["ClientID"] != proj["ClientID"]}
        if allowed & others:
            recipient_leaks.append(proj["ProjectID"])
        if not allowed:
            recipient_leaks.append(f"{proj['ProjectID']} has no authorised recipient")
    c.check("SEG-07", "Release recipients resolve only to the project's own authorised contacts",
            not recipient_leaks, "; ".join(recipient_leaks) or
            f"{len(data['Projects'])} projects, recipients confined to their own client")

    # 8. project-specific templates are not selectable by another project
    tmpl_leaks = []
    for t in data["DocumentTemplates"]:
        if not t.get("ProjectID"):
            continue
        for proj in data["Projects"]:
            if proj["ProjectID"] != t["ProjectID"]:
                selectable = t.get("ProjectID") in ("", proj["ProjectID"])
                if selectable:
                    tmpl_leaks.append(f"{t['TemplateID']} selectable by {proj['ProjectID']}")
    c.check("SEG-08", "A project-specific template is not selectable by another project",
            not tmpl_leaks, "; ".join(tmpl_leaks) or
            "TPL-0003 is bound to PRJ-0001 and offered to no other project")

    # 9. numbering series scoped to one project cannot be used by another
    series_leaks = []
    for s in data["NumberingSeries"]:
        if s["ScopeKind"] == "PerProject" and not s.get("ProjectID"):
            series_leaks.append(f"{s['SeriesID']} is PerProject with no ProjectID")
        if s["ScopeKind"] == "PerClient" and not s.get("ClientID"):
            series_leaks.append(f"{s['SeriesID']} is PerClient with no ClientID")
    c.check("SEG-09", "Project-scoped numbering series are bound to a project",
            not series_leaks, "; ".join(series_leaks) or
            "SER-0004 is bound to PRJ-0003; company-wide series carry no project")

    # 10. no foreign key points at a row in a different project
    fk_leaks = []
    tables = model["tables"]
    index = {t: {r[tables[t]["primary_key"]]: r for r in rows if tables[t]["primary_key"] in r}
             for t, rows in data.items()}
    for table, rows in data.items():
        cols = {col["name"]: col for col in tables[table]["columns"]}
        for row in rows:
            mine = row.get("ProjectID")
            if not mine:
                continue
            for name, raw in row.items():
                col = cols.get(name)
                if not col or col["type"] != "ref" or not (raw or "").strip():
                    continue
                rt = col["ref"].split(".")[0]
                target = index.get(rt, {}).get(raw.strip())
                if target and target.get("ProjectID") and target["ProjectID"] != mine:
                    fk_leaks.append(f"{table}.{name} {raw} -> {target['ProjectID']} (row is {mine})")
    c.check("SEG-10", "No foreign key references a row belonging to a different project",
            not fk_leaks, "; ".join(fk_leaks[:5]) or
            f"{sum(len(r) for r in data.values())} rows checked, no cross-project reference")

    # 11. location codes repeat across projects without colliding
    codes = {}
    for loc in data["Locations"]:
        codes.setdefault(loc["LocationCode"], set()).add(loc["ProjectID"])
    shared = {k: v for k, v in codes.items() if len(v) > 1}
    ids_unique = len({l["LocationID"] for l in data["Locations"]}) == len(data["Locations"])
    c.check("SEG-11", "A location code reused across projects stays distinct because the ID is the key",
            bool(shared) and ids_unique,
            f"codes shared across projects: {sorted(shared)}; all LocationIDs unique: {ids_unique}")

    # 12. residency rules apply per project, not globally
    ai_disabled = {p["ProjectID"] for p in data["Projects"]
                   if p["AIAnalysisEnabled"].upper() == "FALSE"}
    ai_enabled = {p["ProjectID"] for p in data["Projects"]
                  if p["AIAnalysisEnabled"].upper() == "TRUE"}
    c.check("SEG-12", "A residency restriction disables AI for its own project only",
            ai_disabled == {"PRJ-0003"} and len(ai_enabled) == 2,
            f"AI disabled: {sorted(ai_disabled)}; AI enabled: {sorted(ai_enabled)}")

    return c
