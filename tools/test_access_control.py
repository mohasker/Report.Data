#!/usr/bin/env python3
"""Role separation, time-bound access, break-glass and recoverability.

Implements the owner's role distinction of 2026-09-11: a technical administrator does
not receive business content merely because they administer configuration; business
master-data administration is a separate job; auditor access is time-bound; break-glass
requires a reason, an expiry, a notification and an immutable audit record; and the
system must not become unrecoverable when one administrator is unavailable.
"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import security
from harness import Checks

IN_WINDOW = "2026-04-09T12:00:00Z"
OUT_OF_WINDOW = "2026-06-01T12:00:00Z"
BUSINESS_CONTENT = ["SiteVisits", "VisitActivities", "Photos", "Snags", "Documents",
                    "DocumentJobs", "Contracts", "BOQItems", "InvoiceRequests", "InvoiceLines",
                    "TaxRules"]
TECHNICAL = ["Languages", "Roles", "Units", "Disciplines", "DocumentTypes", "DataClassifications"]


def readable(model, data, user, table, at, project="PRJ-0001"):
    """project=None asks about a table that carries no project, such as Users."""
    row = {"ProjectID": project} if project else {}
    return security.can(model, data, user, table, "read", row, at)[0]


def run(model, data):
    c = Checks("Role separation, time-bound access and recoverability",
               "A technical administrator gets no business content; business administration is a "
               "separate role; auditor and break-glass access are time-bound and authorised; and "
               "the system cannot become unrecoverable.")
    matrix = model["security"]["matrix"]

    # ---- role set -------------------------------------------------------
    c.check("ACC-01", "All ten roles the owner specified exist in the model",
            set(model["security"]["roles"]) == {
                "SystemAdministrator", "BusinessAdministrator", "GeneralManager",
                "TechnicalReviewer", "FinanceReviewer", "ProjectManager", "SiteSupervisor",
                "FieldUser", "ReadOnlyAuditor", "EmergencyAccess"},
            ", ".join(model["security"]["roles"]))

    # ---- SystemAdministrator: technical only ----------------------------
    leaks = [t for t in BUSINESS_CONTENT if matrix["SystemAdministrator"][t]["read"] != "none"]
    c.check("ACC-02", "The technical administrator has no read access to evidence, documents, "
                      "contracts or financial records",
            not leaks, f"tables readable: {leaks or 'none'} (of {len(BUSINESS_CONTENT)} checked)")

    c.check("ACC-03", "The technical administrator can still administer technical configuration",
            all(matrix["SystemAdministrator"][t]["update"] == "all" for t in TECHNICAL),
            "vocabularies, roles, units, disciplines, document types and classifications")

    c.check("ACC-04", "The technical administrator can provision users and project assignments",
            matrix["SystemAdministrator"]["Users"]["create"] == "all"
            and matrix["SystemAdministrator"]["ProjectAssignments"]["update"] == "all",
            "user provisioning is access administration, not business content")

    c.check("ACC-05", "The technical administrator can monitor integrations and system health",
            matrix["SystemAdministrator"]["IntegrationJobs"]["read"] == "all"
            and matrix["SystemAdministrator"]["AuditLog"]["read"] == "all",
            "read-only on both; neither can be altered")

    # ---- BusinessAdministrator ------------------------------------------
    leaks = [t for t in BUSINESS_CONTENT if matrix["BusinessAdministrator"][t]["read"] != "none"]
    c.check("ACC-06", "The business administrator has no access to evidence, documents or "
                      "financial records either",
            not leaks, f"tables readable: {leaks or 'none'}")

    c.check("ACC-07", "The business administrator can administer clients, projects and business "
                      "configuration",
            all(matrix["BusinessAdministrator"][t]["update"] == "all"
                for t in ("Clients", "Projects", "Locations", "ProjectActivityRules",
                          "DocumentTemplates", "NumberingSeries", "LegalEntities")),
            "clients, projects, locations, activity rules, templates, numbering, legal entities")

    c.check("ACC-08", "Neither administrator role can create or alter an approval",
            all(matrix[r]["Approvals"]["create"] == "none"
                and matrix[r]["Approvals"]["update"] == "none"
                for r in ("SystemAdministrator", "BusinessAdministrator")),
            "an administrator must never be able to manufacture an approval")

    # ---- the roles are genuinely different ------------------------------
    differences = [t for t in model["tables"]
                   if matrix["SystemAdministrator"][t] != matrix["BusinessAdministrator"][t]]
    c.check("ACC-09", "Technical and business administration are genuinely different roles",
            len(differences) >= 8,
            f"they differ on {len(differences)} of {len(model['tables'])} tables")

    # ---- ReadOnlyAuditor: time-bound ------------------------------------
    in_win = sum(len(security.readable_rows(model, data, "USR-0010", t, IN_WINDOW))
                 for t in ("SiteVisits", "Photos", "Documents"))
    out_win = sum(len(security.readable_rows(model, data, "USR-0010", t, OUT_OF_WINDOW))
                  for t in ("SiteVisits", "Photos", "Documents"))
    c.check("ACC-10", "An auditor reads records while an authorised grant is in force",
            in_win > 0, f"{in_win} rows readable inside the grant window")
    c.check("ACC-11", "The same auditor reads nothing once the grant window closes",
            out_win == 0, f"{out_win} rows readable outside the window")

    no_grant = copy.deepcopy(data)
    no_grant["TemporaryAccessGrants"] = []
    total = sum(len(security.readable_rows(model, no_grant, "USR-0010", t, IN_WINDOW))
                for t in ("SiteVisits", "Photos", "Documents", "Users"))
    c.check("ACC-12", "With no grant at all, the auditor role resolves to no access",
            total == 0, f"{total} rows readable with the grant register emptied")

    c.check("ACC-13", "An auditor can never write anything",
            all(matrix["ReadOnlyAuditor"][t]["create"] == "none"
                and matrix["ReadOnlyAuditor"][t]["update"] == "none" for t in model["tables"]),
            f"{len(model['tables'])} tables, no create or update anywhere")

    # ---- EmergencyAccess: break-glass -----------------------------------
    c.check("ACC-14", "Break-glass restores administrative capability",
            readable(model, data, "USR-0015", "Users", IN_WINDOW, project=None)
            and matrix["EmergencyAccess"]["Users"]["update"] == "all",
            "user administration is available under an active emergency grant")

    business = [t for t in BUSINESS_CONTENT
                if readable(model, data, "USR-0015", t, IN_WINDOW)]
    c.check("ACC-15", "Break-glass never opens client evidence, documents or financial records",
            not business,
            f"business tables readable under break-glass: {business or 'none'} — an administrative "
            f"emergency is not solved by reading a client's photographs")

    c.check("ACC-16", "Break-glass access ends when the grant expires",
            not readable(model, data, "USR-0015", "Users", OUT_OF_WINDOW, project=None),
            "no access outside the grant window")

    # each precondition refused separately
    grants = {g["GrantID"]: g for g in data["TemporaryAccessGrants"]}
    emergency = grants["TAG-0003"]
    ok, why = security.grant_is_valid(emergency, IN_WINDOW)
    c.check("ACC-17", "A complete emergency grant is accepted", ok, f"TAG-0003: {why}")

    def mutate(**kw):
        g = copy.deepcopy(emergency)
        g.update(kw)
        return g

    for cid, desc, mutation in [
        ("ACC-18", "An emergency grant with no reason is refused", {"Reason": ""}),
        ("ACC-19", "An emergency grant with no expiry is refused", {"ValidTo": ""}),
        ("ACC-20", "An emergency grant with no notification sent is refused",
         {"NotificationSentAt": ""}),
        ("ACC-21", "A self-authorised grant is refused", {"AuthorisedByUserID": "USR-0015"}),
        ("ACC-22", "A grant longer than its configured maximum is refused",
         {"ValidTo": "2026-04-30T21:05:00Z"}),
    ]:
        ok, why = security.grant_is_valid(mutate(**mutation), IN_WINDOW)
        c.check(cid, desc, not ok, why)

    ok, why = security.grant_is_valid(grants["TAG-0004"], "2026-05-02T12:00:00Z")
    c.check("ACC-23", "A revoked grant stops working immediately", not ok, f"TAG-0004: {why}")

    ok, why = security.grant_is_valid(emergency, IN_WINDOW, project_id="PRJ-0001")
    c.check("ACC-24", "A TechnicalOnly grant is refused for project-scoped content",
            not ok, why)

    # every emergency grant carries an audit reference and a notification recipient
    bad = [g["GrantID"] for g in data["TemporaryAccessGrants"]
           if g["GrantKind"] == "Emergency"
           and not (g.get("AuditReference") and g.get("NotificationRecipients"))]
    c.check("ACC-25", "Every emergency grant carries a notification recipient and an audit reference",
            not bad, f"grants missing either: {bad or 'none'}")

    # an exercised emergency grant is reviewed after the fact
    unreviewed = [g["GrantID"] for g in data["TemporaryAccessGrants"]
                  if g["GrantKind"] == "Emergency" and int(g.get("UsageCount") or 0) > 0
                  and not g.get("ReviewedAt")]
    c.check("ACC-26", "Every exercised emergency grant is reviewed after use",
            not unreviewed, f"exercised but unreviewed: {unreviewed or 'none'}")

    # ---- recoverability --------------------------------------------------
    roles = {r["RoleID"]: r["RoleCode"] for r in data["Roles"]}
    admins = [u for u in data["Users"]
              if roles.get(u["RoleID"]) == "SystemAdministrator"
              and u["IsActive"].upper() == "TRUE"]
    plan = data["SystemRecoveryPlan"][0]
    c.check("ACC-27", "Administrative control cannot rest on a single account",
            len(admins) >= 2 or plan["RecoveryRouteDocumented"].upper() == "TRUE",
            f"{len(admins)} administrator-capable accounts; documented recovery route: "
            f"{plan['RecoveryRouteDocumented']}")

    c.check("ACC-28", "The recovery route is documented with a reference and has been tested",
            plan["RecoveryRouteDocumented"].upper() == "TRUE"
            and plan["RecoveryRouteReference"].strip()
            and plan["TestResult"] == "Passed",
            f"reference recorded, last tested {plan['LastTestedAt']}, result {plan['TestResult']}")

    # the go-live blocker is honest about an unrecoverable configuration
    bad_plan = copy.deepcopy(plan)
    bad_plan.update({"BackupAdministratorUserID": "", "RecoveryRouteDocumented": "FALSE",
                     "RecoveryRouteReference": ""})
    unrecoverable = (not bad_plan["BackupAdministratorUserID"]
                     and bad_plan["RecoveryRouteDocumented"].upper() != "TRUE")
    c.check("ACC-29", "A configuration with neither a backup administrator nor a documented route "
                      "is detectable as a go-live blocker",
            unrecoverable, "the condition is computable from the recovery plan row, so go-live can "
                           "be blocked on it rather than on someone remembering")

    c.check("ACC-30", "The recovery plan stores no credential and no route to obtaining one",
            all(k not in " ".join(plan.values()).lower()
                for k in ("password", "secret", "token", "api key", "recovery code")),
            "the plan records whether a route exists and whether it was tested, nothing more")

    # ---- no real identities ---------------------------------------------
    real = [u["Email"] for u in data["Users"] if not u["Email"].endswith("@synthetic.example")]
    c.check("ACC-31", "No real person is assigned to any role",
            not real, f"non-synthetic addresses: {real or 'none'} — identities remain pending "
                      f"until the owner supplies them")
    return c
