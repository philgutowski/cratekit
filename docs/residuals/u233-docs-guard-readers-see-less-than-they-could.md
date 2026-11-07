---
title: The docs guard's readers miss five shapes of drift and would refuse one true shape
found: at the review of #622, U233, 2026-11-07.
issue: no
---

**The mechanism.** `tests/test_docs_current.py` reads the guide and the README with regular expressions, and Fable's round one drove five shapes past them, each on doctored text. A verb group written alone as a command (`crate label --help`) is reported as an unknown verb though argparse accepts it, so the first true line of that shape reddens the guard. A flag in a code span of its own (`` `--report` writes nothing ``) is judged against no verb. One stray backtick in a paragraph re-pairs every later span, so a mention after it can vanish unreported. `dotted_keys` matches `[a-z_]+\.[a-z_]+`, so a hyphenated doctor check (`provider.isrc-cache`) or a misspelling of one is never read. And a verb is "named" by any span opening with its words, so a verb's section can be deleted while one passing mention keeps the check green.

**Measured cost.** None today: the reviewer drove every candidate line in both docs, and neither carries any of the five shapes (zero odd parity paragraphs, the one stray flag span is `--yes`, which the guide says does not exist, no group alone as a command, no hyphenated key misspelt). A guard that misses a drift is a guard that kills nothing for that drift, maintainer facing.

**Closes when:** the readers accept a group alone followed by a help flag, judge a lone flag span against the verb its sentence names or the union of all flags, count backticks per paragraph, read hyphenated keys, and, if wanted, require a verb's `crate VERB` form somewhere. Ledger only.
