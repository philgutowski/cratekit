---
title: An analyze run whose M4As all settle skipped-no-decoder ends ok with no warning a person at the terminal sees
found: at the review of #692, U263, round one, 2026-11-12.
issue: no
---

**The mechanism.** `analyze run` reports each item's status in the JSON
envelope's `by_status`, which the human rendering does not show, on the base
as on the branch. A machine fault, ffmpeg absent, is reported per item like
a file's own fault, with no envelope warning of the kind `unscored_warning`
gives for a missing vocal model.

**Measured cost.** Driven by the review: three M4As with ffmpeg off the PATH
ended `analyze.run: ok`, `items: 3 of 3 settled`, exit 0, `warnings: []`;
`skipped-no-decoder` appeared only in the JSON. `crate doctor` fails the
`binary.ffmpeg` row on that machine.

**Closes when:** the run carries a warning naming ffmpeg when any item
settled `skipped-no-decoder`, as it does for the vocal model. Ledger only.
