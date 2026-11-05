---
title: A staged track is known by its ISRC alone, so a staged file with no ISRC tag is downloaded again
found: at the build of #506, U212, 2026-11-05.
issue: no
---

**The mechanism.** `intake missing` subtracts a missing row from the download
list when a file in the download staging folder carries the row's ISRC, read
by the index reader (`missing_cli._staged`). A row with no ISRC, or a staged
file whose ISRC tag is absent, malformed or unreadable, matches nothing, so the
track is listed and downloaded again, and at the name step `name apply` cannot
call the collision a second copy either (`naming_cli.second_copy` reads the
same tag). The provider id is not read: not in a staged file's name, which the
downloader writes as `{track_id}` until `name apply` renames it, and not in the
`URL` tag the vendored downloader writes when `metadata_write_url` is on.

**Measured cost.** Not driven live. The downloader writes the Vorbis `isrc`
comment on every file it delivers (R-355's note in `core/tags.py`), so the
miss needs a provider row with no ISRC. In sitting 55 both copies carried one.

**Closes when:** a sitting meets a staged file with no ISRC that a pass lists
again, then the staged set also reads an identifier stem and the URL tag.
Ledger only: the cost is the collision the unit started from, now with a
plainer message.
