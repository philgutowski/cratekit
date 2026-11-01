---
title: acquire bandcamp --seller reads a followed label's name before an account of the same spelling, with no warning
found: at the second review of #359, U177, 2026-11-01.
issue: no
---

**The mechanism.** `_sellers` in `acquire/bandcamp_cli.py` resolves each
`--seller` value through the label registry first, so a value that is both a
followed label's name and another seller's account plans the label's account.
A label registered as `otherlabel` selling from `pulsromania` makes
`--seller otherlabel` plan the pulsromania purchases and mark the otherlabel
account's own purchases filtered.

**Measured cost.** Driven at the second review. No warning says the value was
read as a label, though the summary's `sellers` names the account planned and
each row names its seller and label. The producer, a label named exactly like
an unrelated seller's account, was built by hand and is not known on a real
account.

**Closes when:** a value that resolves both ways is warned about by name, or
planned as both. Ledger only.
