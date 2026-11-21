---
title: The landed row reader reads a landing whose playlists rekordbox deleted outright as rolled back, so its later removals are never offered
found: at the review of #913, R-1037, round one, 2026-11-21.
issue: no
---

**The mechanism.** `deletion.library.landed_absences` offers nothing of a
landing whose playlists the database no longer holds in any state, since a
restore of a capture from before the landing takes them away. Cratekit's own
rotation soft deletes a playlist, so the row stays and the guard holds. What
rekordbox 7.2.19 writes when a person deletes a playlist by hand was not
measured: A185's playlist was deleted after its AFTER copy, and the same
version deletes content rows outright.

**Measured cost.** Not driven, since only rekordbox produces it. If rekordbox
deletes the playlist row outright, every later removal of that landing's
tracks is never offered, and the gate shows no count of it; the files stay on
disk, which keeps rather than trashes.

**Closes when:** an attended check deletes a throwaway playlist made by hand
in rekordbox and reads djmdPlaylist on before and after copies, and the guard
is kept, replaced by the restore record guard alone, or narrowed to playlists
the landing made.
