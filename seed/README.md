# Seed and synthetic data

**SYNTHETIC TEST DATA ONLY. NEVER LOAD INTO A PRODUCTION ENVIRONMENT.**

Nothing in this directory is real. There is no real client, project, person, contract, address,
contact, quantity, rate or account identifier anywhere in it. Names use the reserved `.example`
domain and are obviously fictional. Company identity is the placeholder
`LEGAL_ENTITY_NAME_PENDING_VERIFICATION` until the current Commercial Registration is checked (D-02).

Two kinds of file live here:

| Kind | Files | Purpose |
|---|---|---|
| **Controlled vocabularies** | the files in this directory | Real, intended reference data — roles, units, disciplines, activities, document types, classifications. These become production master data after review. |
| **Synthetic fixtures** | `synthetic_projects/` | Three materially different fabricated projects used to prove segregation and configurability before any real data exists (D-01, D-12). |

## Deliberate traps

The fixtures contain planted problems so that a bug is visible rather than subtle. Each is asserted
by a test in `tools/`:

| Trap | What it proves |
|---|---|
| `Block A` exists in two different projects with different IDs | Location lookups filter by project, and a name is never a key |
| `USR-0007` is assigned to two projects | Multi-project users work without leaking between them |
| `USR-0011` has no assignment at all | Absence of an assignment grants nothing |
| `USR-0012` has an assignment that expired | An expired assignment grants nothing |
| `CLI-0003` records a currency different from its project | The currency-mismatch validation fires (C-09) |
| `PRJ-0003` carries a `NoThirdPartyAI` residency rule | AI analysis is disabled per project by configuration (D-12) |
| `CLI-0002` has an Arabic legal name and no English one | Arabic is preserved, never transliterated (D-11) |
| A BOQ item is certified beyond contract plus variation | Over-certification is rejected without a recorded override |
| Two photographs share one checksum | Duplicates are flagged, never deleted or merged |

## Omitted columns

Seed files omit columns the application populates itself — `CreatedAt`, `CreatedBy`, `UpdatedAt`,
`UpdatedBy`, and any required column that has a default or a `system`, `integration`, `calculation`
or `ai` source. `tools/validate_seed.py` applies that rule explicitly rather than assuming it.
