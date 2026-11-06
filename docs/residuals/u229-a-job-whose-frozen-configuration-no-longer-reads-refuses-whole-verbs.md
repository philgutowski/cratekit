---
title: An intake job whose frozen configuration no longer reads refuses whole verbs as a configuration error rather than naming the job
found: at the review of #593, U229, 2026-11-06.
issue: no
---

**The mechanism.** A job's reports are read through its frozen configuration, and a configuration that no longer validates raises `config.ConfigError`, which is not a `CratekitError`. U229 passes such a job over when another pair's plan reads it, but the pair that queued it still re raises it, as the base did, so `crate sync pair` with no argument is refused for every pair (`src/cratekit/sync/pair_cli.py`, `_Reader.job_reports`). The same shape stands one file over: `src/cratekit/sync/mark_cli.py` refuses `sync mark` whole, `src/cratekit/organize/mirror_downloads.py` (`outcomes`) raises out of its step, and `src/cratekit/favorites/backfill.py` reads its jobs the same way (not driven). A `config_toml` that is not TOML at all raises `TOMLDecodeError` through U229's catch as an internal error.

**Measured cost.** Driven by round two's review on a hand edited store row: exit 30 `config-unusable` with the remedy to fix the configuration file, which is not what is wrong, for every pair, and for `sync mark` no items at all. Three candidate producers were driven (a configuration frozen today with recent keys removed, one with no provider table, today's enqueue round trip) and none produces it; the required keys are unchanged since before pair jobs existed. The guard that re raises for the owning pair kills no test.

**Closes when:** every reader of a job's reports names the one job whose frozen configuration does not read and goes on with the rest, or a measurement shows no build ever freezes one. Ledger only until a producer is found.
