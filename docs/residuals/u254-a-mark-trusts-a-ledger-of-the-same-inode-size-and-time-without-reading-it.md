---
title: A mark appends without reading the applied ledger when its inode, size and modification time are as this process left them, whatever its bytes
found: at the review of #683, U254, 2026-11-12.
issue: no
---

**The mechanism.** `apply.mark_applied` skips the whole read of the journal
when `os.stat` gives the same device, inode, size and modification time this
process recorded after its own last write (`_LEFT`). An identity is not the
content: a file rewritten in place to the same size within one tick of the
volume's clock (a second on HFS+, two on FAT), or given its old time back with
`utime`, reads as untouched, and the record is appended to whatever it now
holds.

**Measured cost.** Driven by the review on a scratch copy: three marks, the
file overwritten in place with a schema 1 document of the same size and its
time restored, then one more mark. The record was appended to the document
and every later read refused it as not JSON, so `adopt apply` and the organize
reads stop until the file is repaired by hand. Four producers were driven and
none produces it: another process's mark (changes the size), a torn repair
across processes (a new inode), a staged restore of the same size and time (a
new inode, now pinned by a test), and an older build's mark (it refuses before
writing). An outside in place writer inside one clock tick is unmeasured.

**Closes when:** a mark proves the bytes it skips are the bytes it left, for
example a digest of the last record kept beside the identity and compared to
the file's tail, or the risk is accepted. Ledger only.
