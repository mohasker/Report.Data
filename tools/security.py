#!/usr/bin/env python3
"""Reference implementation of row-level access.

The platform's enforcement lives in AppSheet security filters and in server-side
re-validation. This module is the executable statement of the intended rule, so the
rule can be tested in Phase 1 before anything is built, and so the filters written in
Phase 2 have something to be checked against.

Access is derived ONLY from ProjectAssignments. Absence of an assignment grants
nothing; an expired assignment grants nothing.
"""
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OWNER_COLUMN = {
    "SiteVisits": "SupervisorUserID",
    "Photos": "CapturedBy",
    "Snags": "RaisedBy",
}


def active_assignments(data, user_id, as_of):
    """Project IDs the user may act on, with the role held on each."""
    out = {}
    for a in data.get("ProjectAssignments", []):
        if a.get("UserID") != user_id:
            continue
        if (a.get("IsActive") or "TRUE").upper() != "TRUE":
            continue
        frm = a.get("AssignedFrom") or "0001-01-01"
        to = a.get("AssignedTo") or ""
        if frm > as_of:
            continue
        if to and to < as_of:
            continue                      # expired assignment grants nothing
        out.setdefault(a["ProjectID"], set()).add(a["RoleID"])
    return out


def role_codes(model, data, user_id, project_id, as_of):
    """Role codes the user holds, on this project where one is given."""
    roles = {r["RoleID"]: r["RoleCode"] for r in data.get("Roles", [])}
    user = next((u for u in data.get("Users", []) if u["UserID"] == user_id), None)
    if not user or (user.get("IsActive") or "TRUE").upper() != "TRUE":
        return set()
    codes = set()
    default = roles.get(user.get("RoleID"))
    if default:
        codes.add(default)
    if project_id:
        assigned = active_assignments(data, user_id, as_of).get(project_id, set())
        project_codes = {roles.get(r) for r in assigned if roles.get(r)}
        if project_codes:
            # the role held ON THIS PROJECT governs; the default role never widens it
            return project_codes | ({default} if default in GLOBAL_ROLES else set())
        # no assignment: only globally-scoped roles retain any access at all
        return codes & GLOBAL_ROLES
    return codes


GLOBAL_ROLES = {"GeneralManager", "ReadOnlyAuditor", "FinanceReviewer", "SystemAdmin"}


def owner_of(data, table, row):
    col = OWNER_COLUMN.get(table)
    if col:
        return row.get(col)
    if table == "VisitActivities":
        visit = next((v for v in data.get("SiteVisits", [])
                      if v["VisitID"] == row.get("VisitID")), None)
        return visit.get("SupervisorUserID") if visit else None
    return row.get("CreatedBy")


def can(model, data, user_id, table, operation, row=None, as_of=None):
    """Return (allowed: bool, reason: str)."""
    as_of = as_of or datetime.date.today().isoformat()
    matrix = model["security"]["matrix"]
    project_id = (row or {}).get("ProjectID")
    codes = role_codes(model, data, user_id, project_id, as_of)
    if not codes:
        return False, "no active role for this row"

    best = ("none", None)
    order = {"none": 0, "own": 1, "assigned": 2, "all": 3}
    for code in codes:
        grant = matrix.get(code, {}).get(table)
        if not grant:
            continue
        scope = grant.get(operation, "none")
        if order[scope] > order[best[0]]:
            best = (scope, code)
    scope, code = best

    if scope == "none":
        return False, f"role(s) {sorted(codes)} have no {operation} grant on {table}"
    if scope == "all":
        return True, f"{code} has {operation}=all on {table}"
    if row is None:
        return True, f"{code} has {operation}={scope} on {table} (no row supplied)"
    if not project_id:
        return True, f"{code} has {operation}={scope} on {table} (row is not project-scoped)"
    assigned = active_assignments(data, user_id, as_of)
    if project_id not in assigned:
        return False, f"no active assignment to {project_id}"
    if scope == "assigned":
        return True, f"{code} has {operation}=assigned and holds {project_id}"
    if scope == "own":
        if owner_of(data, table, row) == user_id:
            return True, f"{code} has {operation}=own and owns the row"
        return False, f"{code} has {operation}=own and does not own the row"
    return False, "unhandled scope"


def readable_rows(model, data, user_id, table, as_of=None):
    return [r for r in data.get(table, [])
            if can(model, data, user_id, table, "read", r, as_of)[0]]
