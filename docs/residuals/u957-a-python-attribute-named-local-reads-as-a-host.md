---
title: A Python attribute named local reads as a host form, so a machine named by a word the code uses as a variable stays red
found: at U957, #1025, 2026-11-23, driving the words the brief's ten files share.
issue: no
---

**The mechanism.** The `<t>.local` host form cannot tell `first.local !=
second.local` or `str(self.local / "config")` in code from a host name in
prose. A machine named by one of the words the tree writes as a variable
with a `local` attribute (first, second, other, self, area, among the words
driven) still fails the scan on those files.

**Measured cost.** Driven with the hostname patched to each word: the files
`tests/test_intake_land_rehearse.py` and `src/cratekit/core/rehearsal.py`,
and three mutation records quoting the latter, are red for those words. The
base was red for them too, bare, so nothing regressed; the brief's goal is
unmet for a machine named by one of them.

**Closes when:** the `.local` form refuses an attribute shape it can tell
apart (a following operator, method or path join) without missing a host in
prose, or the variables are renamed. Ledger only: maintainer facing.
