#!/usr/bin/env python3
"""Bilingual and RTL readiness (decision D-11).

Arabic must not require redesigning the database, templates, interface or workflows
later. These checks assert that the structure is already there and that Arabic text
survives the pipeline unchanged.
"""
import os, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contenthash
from harness import Checks

ARABIC = range(0x0600, 0x0700)


def has_arabic(text):
    return any(ord(ch) in ARABIC for ch in text or "")


def run(model, data):
    c = Checks("Bilingual and right-to-left readiness",
               "English and Arabic are supported from Phase 1, with no redesign required to add "
               "Arabic documents later (D-11).")
    tables = model["tables"]

    # 1. every displayed or printed text column has an Arabic counterpart
    missing = []
    for tname, t in tables.items():
        names = {col["name"] for col in t["columns"]}
        for col in t["columns"]:
            if col["name"].endswith("EN") and col["name"][:-2] + "AR" not in names:
                missing.append(f"{tname}.{col['name']}")
    c.check("LNG-01", "Every English text column has an Arabic counterpart",
            not missing, "; ".join(missing) or
            f"{sum(1 for t in tables.values() for col in t['columns'] if col['name'].endswith('EN'))} "
            f"bilingual pairs, none unpaired")

    # 2. the languages vocabulary carries direction
    langs = {l["LanguageCode"]: l for l in data["Languages"]}
    c.check("LNG-02", "Both languages are configured with an explicit text direction",
            langs["en"]["Direction"] == "LTR" and langs["ar"]["Direction"] == "RTL",
            f"en={langs['en']['Direction']}, ar={langs['ar']['Direction']}")

    # 3. users carry a language preference
    prefs = {u["Language"] for u in data["Users"]}
    c.check("LNG-03", "Users carry an individual language preference, and both are in use",
            prefs == {"en", "ar"}, f"preferences present in the fixture: {sorted(prefs)}")

    # 4. templates exist per language with matching direction
    tmpl = data["DocumentTemplates"]
    ar_tmpl = [t for t in tmpl if t["LanguageCode"] == "ar"]
    mismatch = [t["TemplateID"] for t in tmpl
                if (t["LanguageCode"] == "ar") != (t["TextDirection"] == "RTL")]
    c.check("LNG-04", "Templates are keyed by language and carry the correct text direction",
            ar_tmpl and not mismatch,
            f"{len(ar_tmpl)} Arabic template(s); direction mismatches: {mismatch or 'none'}")

    # 5. a project can select Arabic as its default document language
    ar_projects = [p["ProjectID"] for p in data["Projects"]
                   if p["DefaultDocumentLanguage"] == "ar"]
    c.check("LNG-05", "A project can be configured to produce Arabic documents by configuration alone",
            ar_projects, f"projects defaulting to Arabic: {ar_projects}")

    # 6. an Arabic-only client legal name is accepted, never transliterated
    cli = next(x for x in data["Clients"] if x["ClientID"] == "CLI-0002")
    c.check("LNG-06", "A client registered only in Arabic is accepted without an invented English name",
            not cli["LegalNameEN"] and has_arabic(cli["LegalNameAR"]),
            f"LegalNameEN is empty; LegalNameAR = {cli['LegalNameAR']}")

    # 7. Arabic survives hashing unchanged
    visit = next(v for v in data["SiteVisits"] if v["VisitID"] == "VIS-0003")
    ar = visit["OverallDescriptionAR"]
    canon = contenthash.canonical_string(model, "SiteVisits", visit)
    c.check("LNG-07", "Arabic text passes through canonical serialisation unchanged",
            ar in canon and has_arabic(canon),
            f"Arabic description preserved verbatim in the canonical string")

    # 8. NFC normalisation is applied, and does not corrupt Arabic
    c.check("LNG-08", "Arabic text is NFC-normalised without alteration",
            contenthash.norm_text(ar) == unicodedata.normalize("NFC", ar) == ar,
            "text is already NFC and is unchanged by normalisation")

    # 9. Arabic-Indic digits are preserved as written, not silently converted
    loc = next(l for l in data["Locations"] if l["LocationID"] == "LOC-0008")
    c.check("LNG-09", "Arabic-Indic digits in names are preserved as written",
            any(ch in loc["LocationNameAR"] for ch in "٠١٢٣٤٥٦٧٨٩"),
            f"{loc['LocationNameAR']} retains Arabic-Indic digits")

    # 10. every controlled vocabulary is bilingual
    unlabelled = [name for name, e in model["enums"].items()
                  if any(not v["label_ar"] for v in e["values"])]
    c.check("LNG-10", "Every controlled vocabulary carries an Arabic label for every value",
            not unlabelled, "; ".join(unlabelled) or
            f"{len(model['enums'])} vocabularies, every value labelled in both languages")

    # 11. seeded reference data is bilingual in practice, not only in structure
    gaps = []
    for table in ("Roles", "Units", "Disciplines", "ActivityTypes", "DocumentTypes",
                  "DataClassifications"):
        for row in data[table]:
            ar_cols = [k for k in row if k.endswith("AR")]
            if ar_cols and not any(has_arabic(row[k]) for k in ar_cols):
                gaps.append(f"{table}:{list(row.values())[0]}")
    c.check("LNG-11", "Seeded reference data is populated in Arabic, not merely capable of it",
            not gaps, "; ".join(gaps[:5]) or
            "roles, units, disciplines, activities, document types and classifications all carry Arabic")

    # 12. bilingual free text on operational records
    ar_visits = [v["VisitID"] for v in data["SiteVisits"] if has_arabic(v["OverallDescriptionAR"])]
    ar_photos = [p["PhotoID"] for p in data["Photos"] if has_arabic(p["CaptionAR"])]
    c.check("LNG-12", "Supervisors can record descriptions and captions in Arabic",
            len(ar_visits) >= 3 and len(ar_photos) >= 3,
            f"{len(ar_visits)} visits and {len(ar_photos)} photo captions carry Arabic")

    # 13. no transliteration: an Arabic name is never copied into the English column
    copied = [r["ClientID"] for r in data["Clients"]
              if r["LegalNameEN"] and has_arabic(r["LegalNameEN"])]
    c.check("LNG-13", "Arabic is never written into an English column to satisfy a requirement",
            not copied, "; ".join(copied) or "English columns contain no Arabic text")
    return c
