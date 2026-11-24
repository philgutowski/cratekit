---
title: A name a listed module re-exports is bound twice, so a test that patches its origin does not reach a caller reading the listed module
found: at review round one of #980, U331, 2026-11-23.
issue: no
---

**The mechanism.** U331 routes each feature package's reach into an unlisted core module through a listed module that re-exports the names, `from cratekit.core.snapshot import assert_room_for_check as assert_room_for_check` in `core/session.py` among them (`session` for `preflight`, `processes` and `snapshot`, `config` for `profiles`, `jobs` for `discovery`, `pool` for the cores' ceiling, `active_taxonomy` for `foreign_tree`). Each is a second binding of the same object. A caller in a feature package now reads `session.assert_room_for_check`, so a test that monkeypatches `snapshot.assert_room_for_check` changes nothing that caller sees.

**Measured cost.** Maintainer facing. Round one found the room test patched the name it was meant to hold, and it now takes the room away below both bindings. `tests/test_import_rules.py` asserts every re-exported name is its origin's object, which holds the bindings equal at import and not under a patch. No user facing cost was driven.

**Closes when:** a test of a re-exported guard patches what both bindings call, or the rules name each re-export a patch must reach. Ledger only.
