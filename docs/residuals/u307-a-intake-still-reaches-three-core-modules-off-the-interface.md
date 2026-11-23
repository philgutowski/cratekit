---
title: Intake still reaches three core modules off the named interface, so its import allowance is not empty
found: at the build and round one review of #864, U307, 2026-11-22.
issue: no
---

**The mechanism.** `tests/ratchets/imports/intake.txt` still holds three lines: `off-interface cratekit.core.binary_refusal` (imported by `intake/cli_identify.py` for the missing downloader refusal), `off-interface cratekit.core.drift` (by `native.py` and `native_plan.py`, the dynamics tag) and `off-interface cratekit.core.rehearsal` (by `land_cli.py` and `land_native.py`, the landing's rehearsal). U307's brief asks for the allowance empty. The named interface in `tests/test_import_rules.py` is at its cap of 25, so none of the three can join it without another leaving, and the modules are #857's (`rehearsal`, `drift`) and #858's (`binary_refusal`). Re-exporting them through an interface module from intake would hide the reach rather than remove it, so U307 left them and names them for the audit.

**Measured cost.** None to a person: the imports work and nothing dangles with a toggle off. The cost is point 4 of #847's definition of done read on intake: three seam items left of the fifteen the survey counted.

**Closes when:** the core cards or the final audit (#872) decide where the three live: a module on the interface list that carries what intake needs, the reach moved into intake where only intake uses it (`rehearsal` has no other feature package user), or the list changed by the card that owns it. Then `scripts/refactor_measure.py prune intake` empties the file. Ledger only.
