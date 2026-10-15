---
title: A playlist a person made under a mirrored playlist's title in the folder keeps that playlist unmirrored until it is renamed
found: at the build of #326, U147, 2026-10-15.
issue: no
---

**The mechanism.** The brief names folder adoption and playlist creation and
says nothing of a person's playlist already carrying a mirror's title, for
example `Techno Low` inside a `Techno` folder Phillip made. `mirror.plan`
leaves it alone and names it (`LEFT`, "rename it on the account"), since
adopting it would let the mirror take tracks off a person's playlist, which
R-836 forbids, and making a second of the same title would put two `Techno
Low` in one folder.

**Measured cost.** Driven:
`test_a_persons_playlist_of_the_same_title_is_left_and_nothing_made_beside_it`.
That one rekordbox playlist is not on the account until the person renames or
deletes theirs; the gate says so on every run.

**Closes when:** the author chooses among leave and name (built), adopt add
only, or make the mirror's own beside it. Ledger only.
