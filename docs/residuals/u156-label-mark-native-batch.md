---
title: label mark still asks for an intake file, so a label batch landed natively with its filing cannot be marked
found: at the plan of #337, U156, 2026-10-28.
issue: yes
---

**The mechanism.** U156 lets a native landing file a label batch under Record
Labels, from `--manifest` or `--label`, which R-916 recorded as the thing
standing in front of it. `label/mark_cli.py` still calls
`marks.require_output(xml)` and reads the pass and the filed years off the
intake file `intake land` wrote on the bridge, and a native landing writes
none. The session record of a native landing now names every year it filed,
under the `labels` key (`intake/label_filing.py`, `RECORD_KEY`), beside the
pass under `PASS_KEY`, which is what `sync mark --pass` already reads through
`native.landings_of_pass`. The brief allowed this half to be split to its own
unit, and it was, to keep U156 to the landing.

**Measured cost.** Read, not driven: a person who lands a followed label's
batch natively has no path to prefix that label's year playlists on the
account `DOWNLOADED `, so the account keeps offering the years as unheard.
R-916 carries the earlier record of the same mechanism.

**Closes when:** `label mark` takes a native pass by name the way `sync mark
--pass` does, and reads the label and years filed from the `labels` key of
that pass's committed landings in place of the intake file. On the board,
since a workflow a DJ needs cannot finish.
