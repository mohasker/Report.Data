#!/usr/bin/env python3
"""Generate docs/01-data-foundation/01-data-dictionary.md from model/model.json."""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef

OUT = os.path.join(modeldef.ROOT, "docs", "01-data-foundation", "01-data-dictionary.md")

PHASE_LABEL = {
    1: "Phase 1–2 (MVP core)", 3: "Phase 3", 5: "Phase 5", 6: "Phase 6",
}


def esc(text):
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def main():
    m = modeldef.load()
    tables, enums = m["tables"], m["enums"]
    out = []
    w = out.append

    w("# Data Dictionary")
    w("")
    w("**Document ID:** AH-SYS-P1-001 · **Revision:** 1 · **Status:** generated — do not hand-edit")
    w(f"**Generated:** {modeldef.model_date()} from `model/model.json` "
      f"(model version {m['model_version']}) by `tools/gen_data_dictionary.py`")
    w("")
    w("> This document is produced from the canonical model, as are the JSON Schemas in")
    w("> `schemas/tables/`. They cannot drift apart, because both come from the same source.")
    w("> To change a column, edit `tools/build_model.py`, rebuild, and regenerate.")
    w("")
    w("## Conventions")
    w("")
    w("- **Scope** — `global` is reference or control data; `project` means every row carries "
      "`ProjectID` and is subject to row-level security.")
    w("- **Source** — `user` entered by a person · `system` set by the application · `device` from "
      "the capturing device · `integration` returned by an external system · `calculation` produced "
      "by the deterministic calculation module · `ai` **advisory only, never authoritative** · "
      "`config` administrator-maintained configuration.")
    w("- **Hash** — ✔ means the column is part of the entity's `ContentHash`, so changing it voids "
      "an approval (ADR-0006).")
    w("- **Decimal columns are stored as decimal strings, never as floating point** (spec 11).")
    w("- Every table carries `CreatedAt`, `CreatedBy`, `UpdatedAt`, `UpdatedBy`; most carry "
      "`IsActive`. Rows are deactivated or cancelled, never destroyed, because history is evidence.")
    w("- Columns ending `EN` have an `AR` counterpart. Arabic text is stored as given and is never "
      "transliterated (D-11).")
    w("")

    # summary
    w("## Tables at a glance")
    w("")
    w("| Table | Category | Scope | Sensitivity | Built in | Columns | Description |")
    w("|---|---|---|---|---|---|---|")
    for name, t in tables.items():
        w(f"| [`{name}`](#{name.lower()}) | {t['category']} | {t['scope']} | {t['sensitivity']} | "
          f"{PHASE_LABEL.get(t['phase'], 'Phase ' + str(t['phase']))} | {len(t['columns'])} | "
          f"{esc(t['description_en'])} |")
    w("")
    w(f"**{len(tables)} tables · {sum(len(t['columns']) for t in tables.values())} columns · "
      f"{len(enums)} controlled vocabularies.**")
    w("")
    w("---")
    w("")

    # per table
    for name, t in tables.items():
        w(f"## {name}")
        w("")
        w(f"{t['description_en']}")
        w("")
        w(f"*{t['description_ar']}*")
        w("")
        w(f"**Primary key:** `{t['primary_key']}` · **Category:** {t['category']} · "
          f"**Scope:** {t['scope']} · **Sensitivity:** {t['sensitivity']} · "
          f"**Built in:** {PHASE_LABEL.get(t['phase'], 'Phase ' + str(t['phase']))}")
        w("")
        if t["unique_together"]:
            for u in t["unique_together"]:
                w(f"**Unique together:** {', '.join('`%s`' % c for c in u)}")
            w("")
        for combo in t.get("at_least_one", []):
            w(f"**At least one required:** {', '.join('`%s`' % c for c in combo)}")
        if t.get("at_least_one"):
            w("")
        if t["content_hash_fields"]:
            w(f"**ContentHash covers:** {', '.join('`%s`' % c for c in t['content_hash_fields'])}")
            w("")
        w("| Column | Type | Req | Source | Sens | Hash | Validation / notes |")
        w("|---|---|---|---|---|---|---|")
        for c in t["columns"]:
            typ = c["type"]
            if typ == "enum":
                typ = f"enum `{c['enum']}`"
            elif typ == "ref":
                typ = f"ref → `{c.get('ref','')}`"
            elif typ == "decimal":
                typ = f"decimal({c.get('scale',2)})"
            bits = []
            if c.get("key") == "pk":
                bits.append("**PK.**")
            if c.get("uniq"):
                bits.append("**Unique.**")
            if c.get("default") is not None:
                bits.append(f"Default `{c['default']}`.")
            if c.get("validation"):
                bits.append(c["validation"] + ".")
            if c.get("note"):
                bits.append(c["note"])
            if c.get("ex"):
                bits.append(f"Example: `{c['ex']}`")
            w(f"| `{c['name']}` | {typ} | {'✔' if c.get('required') else ''} | "
              f"{c.get('src','')} | {c.get('sens','')} | "
              f"{'✔' if c['name'] in t['content_hash_fields'] else ''} | {esc(' '.join(bits))} |")
        w("")
        for n in t["notes"]:
            w(f"> {n}")
        if t["notes"]:
            w("")

    # enums
    w("---")
    w("")
    w("## Controlled vocabularies")
    w("")
    for ename, e in enums.items():
        w(f"### {ename}")
        w("")
        w(e["description"])
        w("")
        w("| Code | English | العربية | Meaning |")
        w("|---|---|---|---|")
        for v in e["values"]:
            w(f"| `{v['code']}` | {esc(v['label_en'])} | {esc(v['label_ar'])} | "
              f"{esc(v['description'])} |")
        w("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print(f"wrote {OUT} ({len(out)} lines)")


if __name__ == "__main__":
    main()
