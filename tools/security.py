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


# Roles whose reach is company-wide rather than project-assigned.
GLOBAL_ROLES = {"GeneralManager", "ReadOnlyAuditor", "FinanceReviewer", "SystemAdministrator",
                "BusinessAdministrator", "EmergencyAccess"}

# Roles that do nothing at all unless a valid TemporaryAccessGrant is in force.
GRANT_REQUIRED_ROLES = {"ReadOnlyAuditor", "EmergencyAccess"}


def grant_is_valid(grant, at, project_id=None):
    """Return (valid, reason). Every condition is checked separately so a refusal can say why."""
    if (grant.get("IsActive") or "TRUE").upper() != "TRUE":
        return False, "grant inactive"
    if grant.get("RevokedAt"):
        return False, "grant revoked"
    if not grant.get("Reason", "").strip():
        return False, "a grant without a stated reason is refused"
    if not grant.get("ValidTo", "").strip():
        return False, "a grant without an expiry is refused: no grant is open-ended"
    if not (grant["ValidFrom"] <= at <= grant["ValidTo"]):
        return False, "outside the grant window"
    if grant.get("AuthorisedByUserID") == grant.get("UserID"):
        return False, "self-authorised grants are refused"
    if grant["GrantKind"] == "Emergency" and not grant.get("NotificationSentAt", "").strip():
        return False, ("break-glass without a sent notification is refused: an unannounced "
                       "emergency grant is a back door")
    if grant.get("MaxDurationHours"):
        try:
            from datetime import datetime
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            hours = (datetime.strptime(grant["ValidTo"], fmt)
                     - datetime.strptime(grant["ValidFrom"], fmt)).total_seconds() / 3600
            if hours > float(grant["MaxDurationHours"]) + 1e-9:
                return False, (f"grant window of {hours:.0f}h exceeds the configured maximum of "
                               f"{grant['MaxDurationHours']}h")
        except ValueError:
            return False, "unparseable grant window"
    if project_id and grant["Scope"] == "SpecificProjects":
        allowed = [p for p in (grant.get("ProjectIDs") or "").replace(",", ";").split(";") if p]
        if project_id not in allowed:
            return False, "project not covered by the grant"
    if project_id and grant["Scope"] == "TechnicalOnly":
        return False, ("break-glass is scoped to technical administration and never opens "
                       "project content")
    return True, "valid"


def active_grant(data, user_id, role_code, at, project_id=None):
    roles = {r["RoleID"]: r["RoleCode"] for r in data.get("Roles", [])}
    for g in data.get("TemporaryAccessGrants", []):
        if g.get("UserID") != user_id:
            continue
        if roles.get(g.get("RoleID")) != role_code:
            continue
        ok, _ = grant_is_valid(g, at, project_id)
        if ok:
            return g
    return None


def _as_timestamp(as_of):
    """Accept a date or a full timestamp; grants are compared at second precision."""
    return as_of if "T" in as_of else f"{as_of}T12:00:00Z"


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

    # A grant-dependent role contributes nothing without a valid grant in force.
    refusals = []
    effective = set()
    for code in codes:
        if code in GRANT_REQUIRED_ROLES:
            if active_grant(data, user_id, code, _as_timestamp(as_of), project_id):
                effective.add(code)
            else:
                refusals.append(f"{code} has no valid access grant in force")
        else:
            effective.add(code)
    if not effective:
        return False, "; ".join(refusals) or "no effective role"
    codes = effective

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


# --- D-25: evidence still queued when access is revoked ------------------------------
QUARANTINE_REPORTABLE = ("NotQuarantined", "AcceptedIntoProject")


def revocation_disposition(photo, revoked_at):
    """What must happen to one queued photograph when its capturer's access is revoked.

    Returns (disposition, reason). Three outcomes only, and no fourth is permitted:

      "complete_to_quarantine" — provably captured BEFORE revocation. It completes, but into
                                 the restricted area, never into the active project register.
      "refuse"                 — captured at or after revocation, or the capture time cannot
                                 be established. Unprovable is refused, deliberately: a
                                 photograph whose capture time is unknown cannot be shown to
                                 predate anything.
      "normal"                 — no revocation applies.

    Discarding is not an outcome. Evidence the supervisor believes they submitted is never
    destroyed to keep the register tidy (D-25).
    """
    if not revoked_at:
        return "normal", "no revocation in force"
    captured = photo.get("CapturedAt")
    if not captured:
        return "refuse", "capture time is not recorded, so it cannot be shown to predate revocation"
    if captured < revoked_at:
        return "complete_to_quarantine", f"captured {captured}, before revocation at {revoked_at}"
    return "refuse", f"captured {captured}, at or after revocation at {revoked_at}"


def quarantine_is_reportable(photo):
    """May a report, calculation, approval or document read this photograph?"""
    return photo.get("QuarantineStatus", "NotQuarantined") in QUARANTINE_REPORTABLE


def quarantine_review_is_valid(photo):
    """Return an error string, or None when the reviewer's disposition is acceptable."""
    status = photo.get("QuarantineStatus")
    if status == "Rejected" and not (photo.get("QuarantineRejectionReason") or "").strip():
        return "a rejection requires a mandatory reason"
    if status in ("AcceptedIntoProject", "Rejected"):
        if not photo.get("QuarantineReviewedByUserID"):
            return "a quarantine decision requires an identified reviewer"
        if photo.get("QuarantineReviewedByUserID") == photo.get("CapturedBy"):
            return "the revoked capturer may not review their own quarantined evidence"
        if not photo.get("QuarantineReviewedAt"):
            return "a quarantine decision requires a timestamp"
    return None
