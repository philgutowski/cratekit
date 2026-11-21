---
title: A track landed into a batch playlist that was already there is never offered by delete review when removed in rekordbox
found: at the review of #913, R-1037, round two, 2026-11-21.
issue: no
---

**The mechanism.** A landing's record names the playlists it made, and the
deletion pass offers a landed row only while the database holds every one of
them (`deletion.library.landed_absences`), because no database from before the
landing holds one: a `restore run`, a bare metal recovery from an older
snapshot and a hand copy all take the landing's rows away as a removal does,
and the last two leave no record. Round one's guard, a restore record started
after the landing, missed the bare metal recovery (round two's B1, driven end
to end to a file in the Trash). A landing into a batch playlist that already
existed, an explicit `--name` reused or a set landing adding to its recorded
INBOX playlist (U135), makes none, so it names none and offers nothing.

**Measured cost.** Driven: such a landing's track removed outright stays on
disk and is not offered (`tests/test_delete_landed_removed.py`). A person
trashes the file by hand, as before this card. Nothing is lost; the cost is
the card's goal unmet for that landing.

**Closes when:** a fact a removal keeps and every rollback takes away is found
for a landing that made no playlist (an attended comparison of a removal
against a restore), or the landing makes a marker row of its own that
rekordbox leaves. Ledger only.
