---
title: An unplugged library drive reads the status glance's attention as fail for as long as it is unplugged
found: at review round two of #1079, U960, 2026-11-25.
issue: no
---

**The mechanism.** The backup record is on the library volume, so with the
drive unplugged the glance reads `backup` unreadable and `attention` `fail`,
as the brief's rule for an unreadable source asks; the human line reads
`attention: fail (backup unreadable)`.

**Measured cost.** Driven with the root renamed away. On a laptop that is
often away from its library drive, the icon would read `fail` for the
ordinary state of being unplugged.

**Closes when:** the menu bar app's card (#1085) decides whether an absent
volume earns a word of its own ahead of `fail`. Ledger only.
