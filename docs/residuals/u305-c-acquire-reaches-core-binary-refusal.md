---
title: Acquire still reaches core.binary_refusal, a core module off the named interface
found: at the build of #862, U305, 2026-11-22.
issue: no
---

**The mechanism.** `acquire/fallback_cli.py` imports `core.binary_refusal`
for the `yt-dlp-missing` refusal, as `intake/cli.py` does, and the module is
not on the import rules' interface list, so acquire's import allowance keeps
the one line `off-interface cratekit.core.binary_refusal`. The module and the
list belong to #858 (U301) and #869 (U312): folding `yt_dlp_missing` into
`core.binaries`, which is on the list, empties both packages' lines without a
copy in either.

**Measured cost.** None to a person; the seam bar of U290's point 4 holds one
line open in acquire and one in intake.

**Closes when:** the refusal lives in an interface module and acquire's
allowance is pruned. Ledger only.
