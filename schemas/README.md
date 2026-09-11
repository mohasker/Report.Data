# Schemas

Two kinds of contract live here.

## `tables/` — generated, never hand-edited

One JSON Schema per table, generated from `model/model.json` by `tools/gen_schemas.py`. The data
dictionary comes from the same source, so the two cannot drift apart. To change a column, edit
`tools/build_model.py`, rebuild, and regenerate:

```
python3 tools/run_validation.py
```

Each schema carries non-standard `x-` annotations that the platform needs and plain JSON Schema does
not express: `x-primary-key`, `x-references`, `x-content-hash-fields`, `x-unique-together`,
`x-at-least-one`, `x-sensitivity`, `x-source`, `x-language`, `x-bilingual-pair`, `x-decimal-scale`,
`x-built-in-phase`.

## `ai/` — hand-written contracts for a later phase

Written now, used in Phase 4. Defining the contract before building the integration is what makes
the integration testable.

| File | Purpose |
|---|---|
| `evidence-analysis.v1.json` | Advisory analysis of one photograph (spec 9.1) |
| `evidence-analysis-batch.v1.json` | Advisory analysis of one **capture batch** — every photograph captured in a single action, in one request (D-17). One request per capture rather than one per photograph: the capture-once unit, and the only affordable one |
| `report-qa.v1.json` | Review of a generated draft against its source records (spec 9.3) |

All three are **closed** (`additionalProperties: false`) and validated before anything is stored. A
response that does not validate is classified `SchemaMismatch`, dead-lettered with the sanitised
payload, and never retried blindly.

### The deliberate absence

Both evidence schemas contain **no numeric quantity, measurement, area, length or count field
of any kind**. A model cannot report a quantity because the schema gives it nowhere to put one. This
is a structural control, not an instruction that can be argued with — and it is why GOV-09 and
GOV-11 can assert that no AI field reaches a content hash or a monetary path.

`confidence_0_to_1` is the one number the schema permits. It is advisory metadata about the analysis
itself, never a measurement of the work, and never a threshold for automatic approval.

## Versioning

AI schemas are versioned in the filename. A breaking change creates `v2`; `v1` is retained so that
output stored under it stays interpretable. Every stored analysis records the model and prompt
version that produced it.
