---
title: The outbound suites' less work fixture caches the command tree and syncs nothing, so a later test patching a handler or a store pragma silently misses
found: at the review of #866, U309, 2026-11-22.
issue: no
---

**The mechanism.** `_less_work` in `tests/test_outbound_workers.py` is autouse in about fifteen of the card's test files that import it. It makes `os.fsync` a no-op, sets `PRAGMA synchronous=OFF` on every `PrivateStore`, and builds the command tree once per module membership for the life of the worker. The cached tree binds each verb's handler and registry entry when first built, so a test that patches either takes effect only when it happens to build the tree first; the review drove one that read "patch took effect: False" after another test and "True" alone. Its docstring now says so.

**Measured cost.** None today: no test in those files patches a handler, a registry entry or a build time default, and none is about durability or a store's pragmas. The recorded fsync kills on `core/config.py` are killed by files outside the set, and two replayed kills on `core/jobs.py` still die. The fixture halved the files' test time.

**Closes when:** the fixture moves to a shared helper module beside the other suite helpers, and either drops the parser cache or keys it on the handlers it binds. Ledger only.
