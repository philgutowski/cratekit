---
title: A rehearsal under an absolute library.state_dirname refuses with a bare ValueError instead of naming the setting
found: at the review of #343, U162, 2026-10-31.
issue: no
---

**The mechanism.** `rehearsal.open_area` makes the area's volume half under the library state directory and redirects the config by that half's path relative to the library root. A `library.state_dirname` set to an absolute path puts the state directory outside the root, so `volume.relative_to(cfg.library.root)` raises a `ValueError`, which the verb reports as `internal-error` with the exception's text. `open_area` removes what it made.

**Measured cost.** Driven by the review with a hand edited config: exit 1, `internal-error`, the staging folder intact, nothing live touched. No verb writes `state_dirname`, so the producer is a hand edit only. A traceback sentence where a refusal naming the setting belongs.

**Closes when:** `open_area` refuses an area outside the library root by name, under `config-unusable`, before it copies anything. Ledger only.
