---
title: A pass that downloaded nothing gives its account playlists no mirror
found: by U128 on `relay/295`, 2026-10-10, scoping the landing.
issue: no
---

**The mechanism.** The mirror is written by a landing, and a landing of an
empty staging folder is a plan of nothing that writes nothing, so a pass whose
every account playlist the library already owned lands no INBOX playlist for
any of them. A playlist fully owned in a pass where another playlist
downloaded something is mirrored, since that landing writes it.

**Measured cost.** Not driven against a real pass. The rerun scenarios
confirm an empty landing writes nothing.

**Closes when:** a verb writes the mirror of a pass with nothing to land, or
the author says an all owned playlist needs none in INBOX. Ledger only.
