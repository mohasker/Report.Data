# Loading Synthetic Data into a Prototype

**Document ID:** AH-SYS-P2A-010 · **Revision:** 1 · **Date:** 2026-09-11
**Status:** Completed · Submitted for Owner Review

---

## 1. What exists

31 seed files, 206 rows: controlled vocabularies intended to become real reference data, plus
synthetic fixtures for three materially different projects.

**All synthetic.** No real client, person, contract, address, contact, quantity or rate appears
anywhere. Every email uses the reserved `@synthetic.example` domain, and a check (ACC-31, GOV-02)
fails if that ever stops being true.

## 2. Deliberate traps

The fixtures contain planted problems, so a bug is visible rather than subtle. Each is asserted by a
check:

| Trap | Proves |
|---|---|
| `Block A` exists in two projects | Lookups filter by project; a name is never a key |
| `USR-0007` assigned to two projects | Multi-project users work without leaking |
| `USR-0011` has no assignment | Absence of an assignment grants nothing |
| `USR-0012` has an expired assignment | Expiry is enforced, not just recorded |
| `CLI-0003` records a currency different from its project | The currency-mismatch validation fires |
| `PRJ-0003` carries a no-third-party-AI residency rule | AI is disabled per project, by configuration |
| `CLI-0002` has an Arabic legal name and no English one | Arabic is preserved, never transliterated |
| Two photographs share a checksum | Duplicates are flagged, never deleted |
| A BOQ item certified beyond contract plus variation | Over-certification is refused without an override |
| `TAG-0002` grant expired, `TAG-0004` grant revoked | Time-bound access genuinely ends |

## 3. Loading into a prototype workbook

```
1  create one worksheet per table, named exactly as the table
2  header row = the column names from the data dictionary, in order
3  paste each seed CSV under its header
4  leave system columns empty: CreatedAt, CreatedBy, UpdatedAt, UpdatedBy,
   EntityVersion, ContentHash — the application populates them
5  confirm the row counts match `python3 tools/validate_seed.py`
```

Load order follows the references — vocabularies, then legal entities and clients, then projects,
then assignments and locations, then visits, activities and photographs, then access grants. Loading
a child before its parent produces broken references that look like a schema fault and are not.

## 4. Rules while prototyping

1. **Synthetic data only.** No real photograph, client or contract enters any environment until the residency review permits it for that project (EF-16).
2. **Do not "improve" the traps.** A fixture that looks wrong is usually the one doing the work.
3. **Re-run `python3 tools/validate_seed.py` after any edit.** It checks types, vocabularies, uniqueness, referential integrity and project consistency in under a second.
4. **Never copy production data down into the prototype.** The direction of travel is one way: synthetic first, real later, and only once the segregation tests are recorded.

## 5. When real data arrives

1. Residency review complete for that project (EF-16).
2. Legal identity verified, if any document will be issued (EF-02).
3. Segregation tests recorded as passing on the real platform.
4. Import through the same validator, with every row attributed to the file and person it came from.
5. Projects load in a draft state and are activated only after review.
6. **Synthetic fixtures are never loaded into a production environment.** `seed/README.md` says so at the top, and it means it.
