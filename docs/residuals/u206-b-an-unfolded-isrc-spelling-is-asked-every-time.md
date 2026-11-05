---
title: An ISRC spelled lower case or hyphenated is asked of the provider on every run and never kept
found: at the review of #496, U206, 2026-11-05.
issue: no
---

**The mechanism.** The ISRC cache keeps and recalls only a spelling that is
already its own fold (`_key` in `src/cratekit/acquire/isrc_cache.py`), because
the provider may answer another spelling differently and that answer must not
stand for the folded code. Four callers of `match_track` fold through
`match.isrc_token` first. `export set` (`src/cratekit/export/set_cli.py`) hands
over a list document's own `Wanted.isrc`, stripped but not folded.

**Measured cost.** Driven at the seam: `qzaaa2600001` and `QZ-AAA-26-00001`
asked twice each, four calls, nothing written. `export set` was not driven end
to end. A set exported from a list carrying such spellings pays every lookup on
every run, as it did before U206; nothing is wrong, only unsaved.

**Closes when:** `export set` folds the code before asking, as the other
callers do, and a test shows its second run asks nothing. Ledger only.
