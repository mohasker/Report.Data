#!/usr/bin/env python3
"""Generate the status-transition matrix and the security matrix from model/model.json."""
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef

DOCS = os.path.join(modeldef.ROOT, "docs", "01-data-foundation")
TODAY = datetime.date.today().isoformat()


def esc(t):
    return (t or "").replace("|", "\\|").replace("\n", " ").strip()


def transitions_doc(m):
    o = []
    w = o.append
    w("# Status Transition Matrix")
    w("")
    w("**Document ID:** AH-SYS-P1-003 · **Revision:** 1 · **Status:** generated — do not hand-edit")
    w(f"**Generated:** {TODAY} from `model/model.json` by `tools/gen_matrices.py`")
    w("**Tested by:** `tools/test_transitions.py` · **Evidence:** `17-validation-evidence.md` (TRN-01 … TRN-20)")
    w("")
    w("> Work advances only through a transition declared here. Anything not listed is refused,")
    w("> and the transitions listed as forbidden are refused explicitly so that the refusal is a")
    w("> decision on the record rather than an accident of implementation.")
    w("")
    w("## How to read this")
    w("")
    w("- **Roles** — who may cause the transition. `System` means an automated workflow acting on validated data, never a person clicking through a gate.")
    w("- **Preconditions** — every one must hold. A failed precondition returns a specific, correctable message, never a generic rejection.")
    w("- **Invalidates** — approvals that this transition voids. This is the mechanism behind acceptance criterion 11.")
    w("- **Terminal** states have no outgoing transition, which is asserted by check TRN-09.")
    w("")
    total_a = sum(len(s["allowed"]) for s in m["transitions"].values())
    total_f = sum(len(s["forbidden"]) for s in m["transitions"].values())
    w(f"**{len(m['transitions'])} lifecycles · {total_a} permitted transitions · "
      f"{total_f} explicitly forbidden.**")
    w("")
    for key, spec in m["transitions"].items():
        t = m["tables"][spec["entity"]]
        w(f"## {key}")
        w("")
        w(f"{t['description_en']}")
        w("")
        w("| From | To | Roles | Preconditions | Side effects | Invalidates |")
        w("|---|---|---|---|---|---|")
        for a in spec["allowed"]:
            w(f"| `{a['from']}` | `{a['to']}` | {', '.join(a['roles'])} | "
              f"{esc('; '.join(a['preconditions']) or '—')} | "
              f"{esc('; '.join(a['side_effects']) or '—')} | "
              f"{esc('; '.join(a['invalidates']) or '—')} |")
        w("")
        if spec["forbidden"]:
            w("**Explicitly forbidden:**")
            w("")
            for f in spec["forbidden"]:
                w(f"- {f}")
            w("")
        if spec["terminal_states"]:
            w(f"**Terminal states:** {', '.join('`%s`' % s for s in spec['terminal_states'])}")
            w("")
    return "\n".join(o) + "\n"


def security_doc(m):
    sec = m["security"]
    o = []
    w = o.append
    w("# Role and Row-Level Security Matrix")
    w("")
    w("**Document ID:** AH-SYS-P1-004 · **Revision:** 1 · **Status:** generated — do not hand-edit")
    w(f"**Generated:** {TODAY} from `model/model.json` by `tools/gen_matrices.py`")
    w("**Executable statement:** `tools/security.py` · **Tested by:** `tools/test_segregation.py`")
    w("**Evidence:** `17-validation-evidence.md` (SEG-01 … SEG-12, GOV-06 … GOV-08)")
    w("")
    w("## Principles")
    w("")
    for p in sec["principles"]:
        w(f"- {p}")
    w("")
    w("## Scopes")
    w("")
    w("| Scope | Meaning |")
    w("|---|---|")
    for k, v in sec["scopes"].items():
        w(f"| `{k}` | {v} |")
    w("")
    w("## Matrix")
    w("")
    w("Each cell is **read / create / update**. Delete is `none` for every role on every table, so")
    w("it is not shown: rows are deactivated or cancelled, never destroyed, because history is")
    w("evidence.")
    w("")
    tables = list(m["tables"].keys())
    groups = {}
    for t in tables:
        groups.setdefault(m["tables"][t]["category"], []).append(t)
    for cat, tbls in groups.items():
        w(f"### {cat.title()} tables")
        w("")
        w("| Table | " + " | ".join(sec["roles"]) + " |")
        w("|---" * (len(sec["roles"]) + 1) + "|")
        for t in tbls:
            cells = []
            for role in sec["roles"]:
                g = sec["matrix"][role][t]
                short = {"all": "ALL", "assigned": "ASG", "own": "OWN", "none": "-"}
                cell = "/".join(short[g[op]] for op in ("read", "create", "update"))
                if cell == "-/-/-":
                    cell = "—"
                if g.get("exception_reason"):
                    cell += " \\*"
                cells.append(cell)
            w(f"| `{t}` | " + " | ".join(cells) + " |")
        w("")
    w("Key: `ALL` every row · `ASG` rows in the user's assigned projects · `OWN` rows the user")
    w("created within those projects · `-` denied · `—` no access to the table at all.")
    w("`\\*` marks a deliberate exception, explained in the next section.")
    w("")
    w("## Deliberate exceptions")
    w("")
    w("Each of these narrows or widens the group default for a stated reason. An exception without a")
    w("reason is a bug.")
    w("")
    w("| Role and table | Reason |")
    w("|---|---|")
    for k, v in sec["exceptions"].items():
        w(f"| `{k}` | {esc(v)} |")
    w("")
    w("## What this matrix does not do")
    w("")
    w("It does not enforce anything by itself. It is the specification that the Phase 2 security")
    w("filters and the Phase 3 server-side re-validation must both implement, and that")
    w("`tools/security.py` implements now so the rule can be tested before anything is built.")
    w("Column visibility and view design are presentation, never enforcement (P-04).")
    return "\n".join(o) + "\n"


def main():
    m = modeldef.load()
    for name, text in (("03-status-transition-matrix.md", transitions_doc(m)),
                       ("04-security-model.md", security_doc(m))):
        with open(os.path.join(DOCS, name), "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote docs/01-data-foundation/{name}")


if __name__ == "__main__":
    main()
