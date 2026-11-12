---
title: The mutation driver writes test ids verbatim, so a table whose rows kill the scan's own tests quotes their planted credentials and fails the scan
found: at the mutation table of #686, U257, 2026-11-12.
issue: no
---

**The mechanism.** `scripts/mutate.py` lists each killed test by its node id
in `docs/mutation/<unit>.md`. `tests/test_portability.py` parametrizes some
tests with a credential shaped body assembled at runtime, so pytest's id for
the case spells the whole body, for example a JSON `access_token` field
holding the file's fake token. A table whose rows kill those tests then
carries the shape on disk, and `scripts/scan_repo.py` refuses it: U257's
table drew five findings (three OAuth token fields, two credential
assignments). The JSON sidecar escapes its quotes and stays clean.

**Measured cost.** Maintainer facing only. The unit that measured it spells
the token as a placeholder in the table by hand and says so in it, which is
an edit to a measured record. No shipped verb pays for it.

**Closes when:** the driver elides a parametrized id's value where it would
write a credential shape (for example by running the table's text through
`secret_violations` and replacing each span with a placeholder before
writing), or the portability tests take ids that do not spell the body.
Ledger only.
