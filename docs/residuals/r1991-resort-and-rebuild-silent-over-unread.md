---
title: route resort's gate and the rebuild's report say nothing of a playlist converge names not compared, so a left behind count reads complete
found: at the review of #1022, R-1991, 2026-11-23.
issue: yes
---

**The mechanism.** A playlist `convergence_check.unidentified` names is not a
difference: `converged` does not wait on it, so a rebuild clears a restored
tree's flag over it (round one: a flag that could never clear blocked every
write), and `left_behind` reads only `unexpected`. Only `crate converge`
names it. `route resort`'s gate shows the left behind count of the check it
ran and the rebuild's envelope its own warnings, neither with a word that a
playlist was not read.

**Measured cost.** Driven at round two with the real `adopt apply` and the
resort gate: the tree not renamed, the gate shows `left behind: 4`; renamed,
`left behind: 3`, with nothing saying a fourth playlist was not read, while
`converge` names `not-compared:Loud! Room/Unsorted`. A count of zero over an
unread playlist was not driven. The rebuild clearing over one is driven in
`tests/test_unrecorded_genre_folder.py`.

**Closes when:** the resort gate and the rebuild carry the after check's
unidentified playlists as a warning beside left behind. An issue: a count a
person approves over state the check could not read (the bar's b).
