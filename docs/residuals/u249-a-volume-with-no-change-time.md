---
title: The index reader's memory trusts the volume's change time, which a FAT or exFAT volume may not keep, so a same size rewrite that puts the old time back while a pass runs is answered from memory
found: at the review of #678, U249, 2026-11-12.
issue: no
---

**The mechanism.** `match._read_from_disk` answers an unchanged file from
memory for the rest of the process when its path, name template, size,
modification time, change time, inode and device are all as they were and its
modification time is at least two seconds older than the entry. On APFS and on
Linux every write and every `os.utime` moves the change time, so a rewrite is
always read again. Where a volume reports no change time of its own (FAT and
exFAT under some drivers report the modification time or the creation time in
its place), a tool outside Cratekit that rewrites a library file to the same
size and puts its old modification time back, while one sync pass is running,
would be answered with the file's old tags until the process ends. The window
also reads the volume's clock against the machine's, which a network volume
need not share.

**Measured cost.** Not driven: no producer inside Cratekit restores a time
(round one found no `os.utime` in `src`, and every `copy2` lands where the
change time moves), and the live library is recorded on APFS
(`docs/cutover.md`). The window and every stamp field are pinned by
`tests/test_library_reads_remembered.py`.

**Closes when:** the change time on the volume the live library uses is read
on the Mac, or the reader keys on a content digest of the tag block. Ledger
only.
