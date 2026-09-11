#!/usr/bin/env python3
"""Canonical serialisation and content hashing (ADR-0006, conflict C-06).

An approval is valid only for the ContentHash it recorded. That is only meaningful if
"the same content" has exactly one serialisation, so this module defines it:

  * only the fields in the table's content_hash_fields, in that exact order
  * FieldName=value pairs joined by U+001F (unit separator)
  * NULL and "" are indistinguishable, so they never differ by accident
  * text NFC-normalised and trimmed; Arabic normalised, never transliterated
  * decimals at the column's declared scale; dates ISO-8601; booleans TRUE/FALSE
  * child collections folded in as an ordered list of child hashes
  * advisory AI fields and UpdatedAt are excluded by design: an AI observation
    arriving later must never void a human approval
"""
import hashlib, os, sys, unicodedata
from decimal import Decimal, InvalidOperation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modeldef

SEP = "\x1f"
FIELD_SET_VERSION = "1.0.0"


def norm_text(value):
    return unicodedata.normalize("NFC", str(value)).strip()


def norm_value(col, raw):
    if raw is None:
        return ""
    raw = str(raw).strip()
    if raw == "":
        return ""
    t = col["type"]
    if t == "decimal":
        try:
            scale = int(col.get("scale", 2))
            return f"{Decimal(raw).quantize(Decimal(1).scaleb(-scale)):f}"
        except (InvalidOperation, ValueError):
            return norm_text(raw)
    if t == "bool":
        return "TRUE" if raw.upper() in ("TRUE", "1", "YES") else "FALSE"
    if t == "int":
        return str(int(raw))
    return norm_text(raw)


def canonical_string(model, table, row, children=None):
    t = model["tables"][table]
    cols = {c["name"]: c for c in t["columns"]}
    parts = []
    for field in t["content_hash_fields"]:
        col = cols[field]
        parts.append(f"{field}={norm_value(col, row.get(field))}")
    if children:
        for label, hashes in sorted(children.items()):
            parts.append(f"{label}=[{','.join(hashes)}]")
    return SEP.join(parts)


def content_hash(model, table, row, children=None):
    payload = canonical_string(model, table, row, children)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def visit_hash(model, data, visit):
    """A visit's hash folds in its approved photographs and their sequence."""
    photos = [p for p in data.get("Photos", []) if p.get("VisitID") == visit.get("VisitID")]
    approved = sorted(
        [p for p in photos if (p.get("ApprovedForReport") or "FALSE").upper() == "TRUE"],
        key=lambda p: (int(p.get("ReportSequence") or 0), p["PhotoID"]))
    child_hashes = [content_hash(model, "Photos", p) for p in approved]
    return content_hash(model, "SiteVisits", visit, {"ApprovedPhotos": child_hashes})
