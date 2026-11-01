---
title: intake land --label-from-tags files a file under any label tag it carries, so an unregistered Bandcamp seller's own tag makes a folder nobody registered
found: at the review of #359, U177, 2026-11-01.
issue: no
---

**The mechanism.** `crate acquire bandcamp-fetch` writes the label tag only on
a registered seller's files and leaves every other file as it came, and
`crate intake land --label-from-tags` (`intake/label_filing.py`,
`plan_for_tags`) files each file under whatever its label tag names, without
asking the registry. A seller no label names whose archive already carries a
label tag is therefore filed under that tag's text, and a folder for it is
made under `Record Labels`. The same holds for a file from any other source
landed with the flag, and two spellings that differ only in case make two
sibling folders, which is R-453's rule and not this unit's.

**Measured cost.** Driven at the review with a fake seller serving a FLAC
tagged `label=Somebody Else`: the plan said the seller is unregistered, the
staged file kept its tag, the record said `label: None`, and the landing
filed it under `Somebody Else`. The gate screen names every label folder the
write makes before anything is written, so the person sees it. Whether a real
Bandcamp archive carries a label tag is unmeasured: sitting 46 read none on
55 releases of one seller.

**Closes when:** a real archive with a label tag is seen, and the landing then
either files only a label the registry holds or the fetch clears a seller's
own tag. Ledger only: the write is shown on the gate before it happens.
