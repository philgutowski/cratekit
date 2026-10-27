---
title: The known failures file is read with no check that it was measured on this commit's base or on this container
found: at the Fable review of the cloud-first commits, 2026-10-27.
issue: no
---

**The mechanism.** `scripts/cloud_battery.py baseline` writes the base's
failing ids under a header naming the commit and the hostname, and both
readers, `cloud_battery.read_baseline` and `mutate.read_known_failures`,
accept any id in the file. The hostname check in `read_baseline` does not
tell two containers apart, since every cloud container is named `vm`, and
`read_known_failures` reads no header at all. An id written by hand, or a
file measured on another commit, is subtracted from every later run.

**Measured cost.** The reader leg was driven: an appended id under a comment
line is returned among the machine's, and a file headed with another host is
read without refusal. The producer, a session adding its own flaky test, is
now forbidden by the skill and was not driven.

**Closes when:** both readers refuse a file whose header commit is not an
ancestor of `HEAD`, and the baseline carries a digest of its id list that a
hand edit breaks. Ledger only.
