---
title: The needs genre backlog counts an alias's rows, while taxonomy alias retags every file under the root carrying the word
found: at the review of #849, U292, 2026-11-21.
issue: no
---

**The mechanism.** `word_of` in `tagging/backlog.py` counts the rows an alias would move: rows whose file holds the word alone. `crate taxonomy alias` walks every audio file under the library root (or `--folder`) and retags each whose one genre is the word, including files no library row names. Round one drove an alias detail saying one track's file is retagged where the alias gate listed four file writes, one of them a file in no row.

**Measured cost.** The backlog's alias option names fewer file writes than the alias verb's own gate will show. The gate lists every file before anything is written, so nothing is written unseen; the backlog's count is of rows moved out of needs genre, which is what it says.

**Closes when:** the option's detail names the files the alias would retag as well as the rows it moves, read from the verb's own file walk. Ledger only.
