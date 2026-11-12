---
title: An older account adapter a caller kept meets a refusal and drops the newer session the held adapter was built over, costing a login
found: at the review of #690, U261, 2026-11-12, round two.
issue: no
---

**The mechanism.** `account.provider_failure` reads the refused adapter as
the one `account` holds and drops the shared session that one was built
over (`_forget_refused`). A caller that kept an older adapter
(`export/set_cli.py`, `organize/account.py`'s lazy holder, `sync/pair_cli.py`)
and meets a 401 through it, after the held adapter was rebuilt over a
session logged in since, drops that newer session instead.

**Measured cost.** Driven by the review on the suite's doubles (probe P4):
one extra login, two paced requests, never a refused client held. The
producer also needs the keychain to change in the middle of a process,
which only another process does, and was not driven.

**Closes when:** the refusal drops the held session whose client is the
refused adapter's own, rather than the session the module's held adapter
names. Ledger only.
