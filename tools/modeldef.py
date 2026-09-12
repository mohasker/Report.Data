#!/usr/bin/env python3
"""Shared model loader and type helpers. Standard library only."""
import json, os, re, unicodedata
from decimal import Decimal, InvalidOperation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT, "model", "model.json")

_JSON_TYPE = {
    "id": "string", "text": "string", "longtext": "string", "email": "string",
    "phone": "string", "uuid": "string", "checksum": "string", "filekey": "string",
    "url": "string", "enum": "string", "ref": "string", "date": "string",
    "datetime": "string", "time": "string", "json": ["object", "array", "string"],
    "bool": "boolean", "int": "integer", "decimal": "string",
}

RE = {
    "id": r"^[A-Z]{2,6}-[A-Za-z0-9\-]{1,32}$",
    "email": r"^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$",
    "date": r"^\d{4}-\d{2}-\d{2}$",
    "datetime": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
    "time": r"^\d{2}:\d{2}(:\d{2})?$",
    "bool": r"^(TRUE|FALSE)$",
    "decimal": r"^-?\d+(\.\d+)?$",
    "int": r"^-?\d+$",
    "phone": r"^\+?[0-9 \-()]{5,20}$",
    "checksum": r"^[A-Fa-f0-9]{8,64}$",
}


def load():
    with open(MODEL_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def model_date():
    """The deterministic stamp for every generated document.

    Never the system date. A generated file must depend on the model alone, so that
    regenerating it tomorrow produces the same bytes and "byte-identical regeneration"
    means what it says. Genuine event timestamps — when a validation run executed, when a
    package was built — are recorded by the tools that observe those events, not here.
    """
    return load()["model_date"]


def json_type(col):
    return _JSON_TYPE.get(col["type"], "string")


def nfc(value):
    return unicodedata.normalize("NFC", value)


def check_value(col, raw, enums):
    """Return an error string, or None when the value is acceptable."""
    t = col["type"]
    if raw is None or raw == "":
        if col.get("required") and col.get("default") is None:
            return "required value is empty"
        return None
    if t == "enum":
        allowed = [v["code"] for v in enums[col["enum"]]["values"]]
        return None if raw in allowed else f"'{raw}' is not in enum {col['enum']}"
    if t in ("bool", "int", "date", "datetime", "time", "email", "phone", "checksum", "id"):
        pat = RE.get(t)
        if pat and not re.match(pat, raw):
            return f"'{raw}' does not match the {t} format"
        return None
    if t == "decimal":
        if not re.match(RE["decimal"], raw):
            return f"'{raw}' is not a decimal"
        try:
            Decimal(raw)
        except InvalidOperation:
            return f"'{raw}' is not a valid decimal"
        return None
    if t == "json":
        try:
            json.loads(raw)
        except json.JSONDecodeError as exc:
            return f"invalid JSON: {exc}"
    return None
