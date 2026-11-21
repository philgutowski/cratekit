---
title: tag backlog's alias question counts the files rows name, while the campaign retags every file under the root carrying the word
found: at round two of the review of #851, U294, 2026-11-21.
issue: no
---

**The mechanism.** R-1733's shape, one verb over. `word_of` in `tagging/backlog.py` says how many files an alias retags by counting the files backlog rows name. `crate tag campaign` lists, and retags, every audio file under the library root whose one genre is the word, a file no row names included. Round two drove 12 stray files carrying the word: the question said 2 files and the campaign's gate listed 14.

**Measured cost.** The question Phillip answers from understates the files an alias rewrites. The campaign's gate lists every one before anything is written, so nothing is written unseen. How many such files the real library holds is not measured.

**Closes when:** the alias option reads its file count from the alias verb's own walk. Ledger only.
