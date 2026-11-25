---
title: No app fixture carries a pending human action, so a change to that shape passes the fixture guard
found: at the review of #1084, U965, 2026-11-25.
issue: no
---

**The mechanism.** `tests/test_app_fixtures.py` holds three envelopes to the real verbs (doctor, a gate refusal, a refusal with steps). None has a `pending_human_action`, and the Swift test of that shape decodes a dictionary built by hand. The review renamed `verify_verb` in `PendingHumanAction.to_json` and all six fixture tests passed.

**Measured cost.** Driven by the review on 13e3eee: the rename passes the battery. No shipped caller reads a pending action yet, so nobody pays today; a pending envelope from `sync land` would decode as undecodable in the app once a card reads one.

**Closes when:** the first card that reads a pending action in the app (the Sync card) adds a fixture from a real verb that leaves one, and its Swift test decodes that fixture. Ledger only.
