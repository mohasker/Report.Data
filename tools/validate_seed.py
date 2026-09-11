#!/usr/bin/env python3
"""Validate every seed file against model/model.json.

Checks: unknown columns, missing required columns, value types and formats, enum
membership, inline 'A|B|C' vocabularies, primary-key and unique constraints,
unique-together constraints, referential integrity, cross-table project consistency,
and the location hierarchy (same project, no cycles, bounded depth).

Seed files legitimately omit columns the application populates: any column with a
default, or whose source is system, integration, calculation or ai. That rule is
applied explicitly here rather than assumed.
"""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef
from seedmap import SEED_FILES

APP_POPULATED = {"system", "integration", "calculation", "ai"}
INLINE_VOCAB = re.compile(r"^[A-Za-z0-9]+(\|[A-Za-z0-9]+)+$")


def load_seed():
    """Return {table: [rowdicts]} plus the raw file path per table."""
    data, paths = {}, {}
    for rel, table in SEED_FILES:
        path = os.path.join(modeldef.ROOT, rel)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
        data[table] = rows
        paths[table] = rel
    return data, paths


def validate(model, data, paths):
    errors, warnings = [], []
    tables, enums = model["tables"], model["enums"]

    for table, rows in data.items():
        t = tables[table]
        cols = {c["name"]: c for c in t["columns"]}
        rel = paths[table]
        header = list(rows[0].keys()) if rows else []

        for h in header:
            if h not in cols:
                errors.append(f"{rel}: column '{h}' is not in the model")

        for c in t["columns"]:
            if not c.get("required"):
                continue
            if c["name"] in header:
                continue
            if c.get("default") is not None or c.get("src") in APP_POPULATED:
                continue
            errors.append(f"{rel}: required column '{c['name']}' is missing "
                          f"(source={c.get('src')}, no default)")

        seen_pk, seen_unique, seen_ut = set(), {}, set()
        for i, row in enumerate(rows, start=2):
            pk = t["primary_key"]
            if pk in row:
                v = (row[pk] or "").strip()
                if not v:
                    errors.append(f"{rel}:{i}: empty primary key")
                elif v in seen_pk:
                    errors.append(f"{rel}:{i}: duplicate primary key '{v}'")
                seen_pk.add(v)

            for name, raw in row.items():
                if name not in cols:
                    continue
                c = cols[name]
                raw = (raw or "").strip()
                err = modeldef.check_value(c, raw, enums)
                if err:
                    errors.append(f"{rel}:{i}: {name}: {err}")
                v = c.get("validation") or ""
                if raw and INLINE_VOCAB.match(v) and raw not in v.split("|"):
                    errors.append(f"{rel}:{i}: {name}: '{raw}' is not one of {v}")
                if raw and c.get("uniq"):
                    key = (name, raw)
                    if key in seen_unique:
                        errors.append(f"{rel}:{i}: {name}: duplicate unique value '{raw}'")
                    seen_unique[key] = i

            for combo in t.get("at_least_one", []):
                if all(k in row for k in combo):
                    if not any((row[k] or "").strip() for k in combo):
                        errors.append(f"{rel}:{i}: at least one of {combo} must be present")

            for combo in t["unique_together"]:
                if all(k in row for k in combo):
                    key = tuple((row[k] or "").strip() for k in combo)
                    if key in seen_ut:
                        errors.append(f"{rel}:{i}: duplicate unique-together {combo} = {key}")
                    seen_ut.add(key)

    # referential integrity and project consistency
    index = {}
    for table, rows in data.items():
        pk = tables[table]["primary_key"]
        index[table] = {(r.get(pk) or "").strip(): r for r in rows if r.get(pk)}

    for table, rows in data.items():
        t = tables[table]
        rel = paths[table]
        cols = {c["name"]: c for c in t["columns"]}
        for i, row in enumerate(rows, start=2):
            for name, raw in row.items():
                c = cols.get(name)
                if not c or c["type"] != "ref":
                    continue
                raw = (raw or "").strip()
                if not raw:
                    continue
                rtable = c["ref"].split(".")[0]
                if rtable not in data:
                    warnings.append(f"{rel}:{i}: {name} -> {rtable} not seeded; "
                                    f"reference '{raw}' not checked")
                    continue
                target = index[rtable].get(raw)
                if target is None:
                    errors.append(f"{rel}:{i}: {name}: '{raw}' does not exist in {rtable}")
                    continue
                mine = (row.get("ProjectID") or "").strip()
                theirs = (target.get("ProjectID") or "").strip()
                if mine and theirs and mine != theirs:
                    errors.append(f"{rel}:{i}: {name}: '{raw}' belongs to project {theirs} "
                                  f"but this row belongs to {mine} — cross-project reference")

    # location hierarchy
    locs = index.get("Locations", {})
    for lid, row in locs.items():
        seen, cur, depth = set(), row, 0
        while cur and (cur.get("ParentLocationID") or "").strip():
            pid = cur["ParentLocationID"].strip()
            if pid in seen:
                errors.append(f"Locations: cycle detected at {lid}")
                break
            seen.add(pid)
            parent = locs.get(pid)
            if not parent:
                break
            if parent.get("ProjectID") != row.get("ProjectID"):
                errors.append(f"Locations: {lid} has a parent in a different project")
            depth += 1
            if depth > 5:
                errors.append(f"Locations: {lid} exceeds the maximum depth of 5")
                break
            cur = parent
    return errors, warnings


def main():
    model = modeldef.load()
    data, paths = load_seed()
    errors, warnings = validate(model, data, paths)
    total = sum(len(r) for r in data.values())
    print(f"seed files : {len(data)}")
    print(f"rows       : {total}")
    print(f"warnings   : {len(warnings)}")
    for w in warnings:
        print("   ~", w)
    if errors:
        print(f"ERRORS     : {len(errors)}")
        for e in errors:
            print("   x", e)
        return 1
    print("ERRORS     : 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
