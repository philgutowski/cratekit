---
title: A refusal raised behind a function level import is unseen by the reserved causes named cause scan
found: at the build of #856, U299, 2026-11-22.
issue: no
---

**The mechanism.** U299 moved `Config` to `core/config_schema.py`, and
`Config.assert_rekordbox_pin_recorded` imports `ConfigInvalid` and `Remedy`
from `core.config` inside the method, since `config` imports the schema. The
reserved causes suite's named cause scan resolves names through module level
imports, so `core/config_schema.py` holds no named cause by its reading and
`record-rekordbox-pin` left `core/config.py`'s pinned population without
joining another module's. The pins were measured again on the tree, as their
file says.

**Measured cost.** None today: `ConfigError` and its subclasses are excluded
from the derivation by name (`CONVERTED_ELSEWHERE`), so the refusal is held
by the command line boundary either way. A refusal of a type that is not
excluded, raised behind a local import, would be missed by the scan.

**Closes when:** the scan also reads function level imports, or a test pins
that no module in the package raises a structured refusal behind one. Ledger
only.
