---
title: A label whose needle begins with a four digit year is never named by its own copyright line, since the line's year is stripped before the needle is looked for
found: at the fix round of the review of #648, U240, 2026-11-11.
issue: no
---

**The mechanism.** `copyright_matcher` in `src/cratekit/tagging/cli.py` reads the line through `labels_from_copyright`, which strips a leading mark and year, then looks for the whole needle. A label named `2020 Vision` is therefore never named by `℗ 2020 Vision`, chosen at round two so that the year can never complete a needle (`℗ 2020 Vision Quest` named it before).

**Measured cost.** Driven in the suite on the matcher. No followed label's name is known to begin with a year; the card's five do not. Its files are asked of the catalogues, the behaviour before U240.

**Closes when:** a needle that begins with a year is matched against the line with only its mark stripped, keeping the round two test. Ledger only.
