---
title: An album's artist comes only from the album artist tag, and an album the library holds with none is not linked by a file that names one
found: at the build of #344, U163, 2026-10-31.
issue: no
---

**The mechanism.** A landing links `AlbumArtistID` only from the file's
`albumartist` tag (TPE2, `aART`), never from the track artist, and finds an
album by its name and album artist together. A file naming an album artist
therefore mints a second album beside one of the same name the library holds
with no album artist, and a file with no album artist tag leaves the album's
artist empty.

**Measured cost.** None driven against rekordbox. Whether Reload Tags falls
back to the track artist, and how it matches an album, is unmeasured, so a
landed album may group differently in rekordbox's album view from one it made.

**Closes when:** an attended landing compares a Reload Tags album with a landed
one for the same tags, and the rule follows rekordbox's. Ledger only.
