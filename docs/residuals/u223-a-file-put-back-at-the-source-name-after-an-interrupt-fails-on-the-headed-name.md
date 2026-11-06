---
title: A file put back at an analyze run item's source name after an interrupt fails the item on the headed name the interrupted attempt took
found: at the review of #555, U223, 2026-11-05.
issue: no
---

**The mechanism.** An interrupt after the rename and before the commit
leaves the headed file and the evidence for it. If a person then puts a file
back at the source name (a second copy of the same track), the resume reads
the present source first, drops the evidence, analyses the new file, and
fails it `analysis-write-failed` because the headed name is taken by the
first attempt's file. The same outcome on main before U223.

**Measured cost.** Driven by the round two reviewer: the item failed, the
printed resume cannot finish the job, the first attempt's headed file intact
and analysed, the new file carrying the head in its title only. The person
deletes the duplicate and queues the folder again. Producer is a person's
action between the interrupt and the resume.

**Closes when:** the resume compares the present source with the evidence's
target (the same recording reading) and settles the item as resumed when
the target is there. Ledger only.
