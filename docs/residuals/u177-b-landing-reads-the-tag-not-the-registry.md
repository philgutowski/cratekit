---
title: A label renamed between a Bandcamp fetch and its landing is filed under the name its files were tagged with
found: at the review of #359, U177, 2026-11-01.
issue: no
---

**The mechanism.** The fetch freezes each release's label display name in
the job and writes it into the label tag of every staged file, and
`--label-from-tags` reads the tag, never the registry. A rename made with
`crate label registry rename` after the fetch and before the landing files
the batch under the old name, beside a folder of the new one if that exists.

**Measured cost.** Not driven end to end. The freeze is pinned by
`tests/test_bandcamp_labels.py`'s rename test, which is the KTD9 rule the job
engine holds everywhere. The gate screen names each label folder the write
makes, so a second folder for one label is shown before it is written.

**Closes when:** a landing that resolves each tag through the registry, by
name or by the label's identifier written beside the name, is built, if a
rename between the two steps is ever seen. Ledger only.
