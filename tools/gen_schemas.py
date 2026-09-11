#!/usr/bin/env python3
"""Generate one JSON Schema per table from model/model.json.

Generated, never hand-edited: the data dictionary and the schemas come from the same
source, so they cannot drift apart.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef

OUT = os.path.join(modeldef.ROOT, "schemas", "tables")


def build(table, enums):
    props, required = {}, []
    for c in table["columns"]:
        p = {"type": modeldef.json_type(c)}
        desc = []
        if c.get("note"):
            desc.append(c["note"])
        if c.get("validation"):
            desc.append("Validation: " + c["validation"])
        if c.get("ref"):
            p["x-references"] = c["ref"]
            desc.append("References " + c["ref"])
        if c["type"] == "enum":
            p["enum"] = [v["code"] for v in enums[c["enum"]]["values"]]
            p["x-enum"] = c["enum"]
        if c["type"] == "decimal":
            p["x-decimal-scale"] = c.get("scale", 2)
            p["x-storage"] = "decimal string; never a float (spec 11)"
        if c.get("sens"):
            p["x-sensitivity"] = c["sens"]
        if c.get("src"):
            p["x-source"] = c["src"]
        if c.get("lang"):
            p["x-language"] = c["lang"]
        if c.get("ar"):
            p["x-bilingual-pair"] = c["ar"]
        if c["name"] in table["content_hash_fields"]:
            p["x-in-content-hash"] = True
        if desc:
            p["description"] = " ".join(desc)
        props[c["name"]] = p
        if c.get("required"):
            required.append(c["name"])
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://alharam.local/schemas/tables/{table['name']}.schema.json",
        "title": table["name"],
        "description": table["description_en"],
        "x-description-ar": table["description_ar"],
        "x-category": table["category"],
        "x-scope": table["scope"],
        "x-sensitivity": table["sensitivity"],
        "x-built-in-phase": table["phase"],
        "x-primary-key": table["primary_key"],
        "x-content-hash-fields": table["content_hash_fields"],
        "x-unique-together": table["unique_together"],
        "x-at-least-one": table.get("at_least_one", []),
        "x-notes": table["notes"],
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }
    return schema


def main():
    model = modeldef.load()
    os.makedirs(OUT, exist_ok=True)
    for name in sorted(os.listdir(OUT)):
        if name.endswith(".schema.json"):
            os.remove(os.path.join(OUT, name))
    for tname, t in model["tables"].items():
        path = os.path.join(OUT, f"{tname}.schema.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(build(t, model["enums"]), fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    print(f"wrote {len(model['tables'])} table schemas to schemas/tables/")


if __name__ == "__main__":
    main()
