---
title: A file genre with leading or trailing spaces is kept trimmed, so a restore of tag set puts it back without them
found: at the build of #988, U339, 2026-11-23.
issue: no
---

**The mechanism.** `tag set` keeps each file's old genre as `tags.read_tags_checked` reads it, which trims every value, and `core/restore_tags.py` compares and writes the trimmed value. A genre tag stored with surrounding spaces is put back without them.

**Measured cost.** Not driven: no file in the fixtures or the brief carries a padded genre, and the trimmed value is the one every reader in the product uses, so routing and adoption read the restored file as before.

**Closes when:** the exact value is kept (`tags.read_tag_values_checked`) and the restore's read back compares exact values, or a test shows no container in use stores padded genres.
