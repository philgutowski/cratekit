---
title: A label go reached at the end of the walk and stopped at the call ceiling names the walk, without --go, as its continue
found: at the review of #647, U239, 2026-11-10.
issue: no
---

**The mechanism.** The ceiling's continue command is the stopped command
line with `--run` and `--calls` (`continue_command` in
`src/cratekit/cli/__init__.py`). A go reached at the end of the interactive
walk (`crate label sync`, then `run decide --continue`) stopped there, so its
continue is `crate --run RUN --calls N label sync`, which walks first. With
nothing new it reaches the go and lands; with a new release on another label
and no terminal it refuses `label-sync-unanswerable` and the download stays
parked.

**Measured cost.** Driven at the review (`test_C`, `test_C3`). A way through
exists, `crate --run RUN --calls N label sync --go`, which the guide names.

**Closes when:** the go's ceiling cause names its own command line with
`--go`, whatever command reached it. Ledger only: a wording of the way on.
