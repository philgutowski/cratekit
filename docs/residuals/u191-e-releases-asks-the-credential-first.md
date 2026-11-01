---
title: label playlists --releases asks for the provider credential before it reads the local sync record, so a run with nothing taken refuses instead of planning nothing
found: at the review of #402, U191, 2026-10-31.
issue: no
---

**The mechanism.** `label_playlists` in `src/cratekit/label/playlists_cli.py`
resolves the catalogue, which needs the provider session, before it reads the
label sync record. A label nobody follows is decided before any credential, by
the module's own rule; a followed label whose record holds nothing a go took
is not.

**Measured cost.** Driven at the review with the catalogue refusing
`credential-missing` and an empty record: the run exits on the credential
rather than ending with `label-playlists-nothing-taken`. Nothing false is
said, and the person who fixes the credential then gets the right answer.

**Closes when:** the releases build reads the record first and resolves the
catalogue only when there is a release to read. Ledger only.
