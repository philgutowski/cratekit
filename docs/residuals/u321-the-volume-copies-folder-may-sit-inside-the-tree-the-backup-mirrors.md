---
title: The volume copies folder may sit inside the tree the backup mirrors, where a restore from backup also refuses a target
found: at the review of #890, U321, 2026-11-21.
issue: no
---

**The mechanism.** U321 moves a sitting's library and database copies out of
the checkout, which is mirrored to Google Drive, into a folder one level down
in the library volume's scratch folder. Driven at the review in a sandbox with
that folder under the configured library root: the backup's mirror is one sync
of the whole root, excluding only its clutter patterns and the live
database's own files, so copies left there while a settlement's BEFORE and
AFTER backups run are sent to the remote, which is a Drive remote too. And
`crate restore run --from-backup --target` with a target inside the root
refuses, saying the target sits inside the live library, so the product's own
fetch cannot fill that folder.

**Measured cost.** Not driven on the Mac: whether the volume's scratch folder
sits inside the configured library root there is unmeasured, and sitting 102
fetched its copies by a means its record does not name. If it does, the copies
reach a mirrored remote all the same, and a restore into the folder is
refused.

**Closes when:** an attended sitting reads whether the volume's scratch folder
is inside the library root, and either records that it is not, or a docs unit
names a place outside it (or a mirror exclude for it) in the skill and its
worker rules. Ledger only.
