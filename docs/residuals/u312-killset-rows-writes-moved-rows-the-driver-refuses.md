---
title: killset.py rows writes a row a later replay anchored without the moved reason the driver requires
found: at the replay of #869, U312, 2026-11-23.
issue: no
---

**The mechanism.** `read_kill_set` lets the newest replay table that still
applies speak for a row, so a guard that a split moved to another file is
written at its new file and text. `cmd_rows` renders it with `render_row` and
no `moved` reason, and `mutate_table.refuse_unrecorded_sources` refuses at
load any replay row whose file or text differs from its source table's unless
it says `moved`. Driven: `killset.py rows src/cratekit/write/routing_export.py`
writes `u88.L3_existing_members_replanned` at `routing_export.py` with no
`moved`, against `u88.json`'s `routing_cli.py`; on `a5d458bb`, 474 of
U312's 1,591 replay rows were such rows, and all eight before batches were
refused at load until each carried the replay's own `moved` text.

**Measured cost.** Maintainer facing: a replay built by `killset.py rows`
over any file a split touched is refused before it measures anything, which
cost U312 one round of eight helper containers.

**Closes when:** `cmd_rows` carries the `moved` reason of the replay that
anchored the row, and a test drives `rows` over a moved row and loads its
output through the driver's source check.
