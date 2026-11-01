---
title: tag-folder-unwritten tells a person to check the lock on a file that is only truncated
found: at the review of #358, U178, 2026-10-31.
issue: no
---

**The mechanism.** `tagging/tag.py`'s `_written` refuses with
`tag-folder-unwritten` whenever `tags.write_genre` answers False, and its step
says to check the file can be written, is not locked and is not on a read only
volume. A zero byte or truncated `.flac` also answers False, since mutagen
cannot open it, and the art repair's own diagnosis of that file sits in a
report that is not committed for a failed item.

**Measured cost.** Driven at the review: a sweep over an empty `bad.flac`
fails its item with the lock remedy. The item fails, which is correct, and on
`main` the same file was reported tagged; the cost is a remedy that sends a
person to the wrong place for a truncated download.

**Closes when:** the refusal's step also names a file that cannot be read as
audio, or the art repair's detail rides on the refusal. Ledger only, wording.
