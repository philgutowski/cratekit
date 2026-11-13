---
title: The provider gate's readers raise RecursionError on a state file nested past the parser's depth
found: at the review of #790, U284, 2026-11-13.
issue: no
---

**The mechanism.** `core/provider_gate.py`'s `read_spend`, `read_standing` and
`spend` catch `OSError` and `ValueError` around their JSON read, and the gate's
docstring promises that a corrupt counter reads as fresh. A file of
`"[" * 200000` raises `RecursionError` out of each. U284's refusal record had
the same shape and catches it since review round one; the gate is the same
class one file over, not made by U284.

**Measured cost.** Driven at review round two in a scratch copy: all three
raise. Only a hand edit or a damaged disk writes such a file, so no producer
was driven, and the cost to `crate doctor` or a provider call is unmeasured.

**Closes when:** the gate's readers read such a file as one that does not
parse. Ledger only.
