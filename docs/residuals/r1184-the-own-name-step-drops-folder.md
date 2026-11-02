---
title: The own name refusal's step names the alias over the whole library root when --folder narrowed the run
found: at the review of #473, R-1184, 2026-11-02.
issue: no
---

**The mechanism.** `crate taxonomy alias WORD OTHER --folder F`, where WORD is a genre folder's own name in another case, is refused with a step built in `core/taxonomy_word.py` (`own_name_answer`), which knows nothing of `--folder`. The step names `crate taxonomy alias WORD <its own folder>` with no `--folder`, so following it retags every file under the library root carrying the word rather than only those under F.

**Measured cost.** Driven by the review on a disposable library: the refusal's step omits `--folder`. Every file the wider run retags is retagged to the exact name of the folder its word already names, so no file is given a wrong genre; the cost is the scope of a correct retag, behind the verb's explicit gate, which lists every file first.

**Closes when:** the verb carries `--folder` into the step it offers, or the step says the command takes it. Ledger only: no file is damaged and the gate shows the files.
