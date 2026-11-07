---
title: The config key analysis.energy_calibration is accepted and read by no verb
found: at the docs sweep of #622, U233, 2026-11-07.
issue: no
---

**The mechanism.** `AnalysisConfig.energy_calibration` in `src/cratekit/core/config.py` defaults to `"auto"`, round trips through the file, and is fingerprinted with every queued job, but nothing outside `config.py` reads it (a grep of `src/cratekit` for `.energy_calibration` finds no reader) and the validator checks no value of it. The energy calibration a verb uses is the library state file `energy_calibration.json`, chosen by `analyze calibrate`, never by this key.

**Measured cost.** None driven. A person who sets the key changes nothing and is told nothing; `docs/GUIDE.md`'s settings table now says no verb reads it, so the guide does not mislead.

**Closes when:** the key is read by the analysis verbs or removed from the schema with its migration. Ledger only: a wording of the settings table already tells the truth, and nothing is lost.
