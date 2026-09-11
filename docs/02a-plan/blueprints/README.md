# Disabled scenario blueprints

**These are specifications in JSON form, not exports from a live account.** No orchestration account
exists, nothing has been connected, and none of these has ever run.

Every file carries:

```json
"__specification_only": true,
"__not_connected": true,
"enabled": false
```

and contains **no URL, no secret, no account identifier and no connection reference**. An implementer
in Phase 3 supplies connections deliberately; nothing here can run by accident.

Read them alongside [`../07-make-scenario-specifications.md`](../07-make-scenario-specifications.md),
which explains each module and its error route in prose.
