---
title: Job drift reads the frozen configuration's raw bytes rather than through the loader, so a fold the loader applies is copied by hand
found: at the second review of #479, U197, 2026-11-02.
issue: no
---

**The mechanism.** `core/jobs.py::drift` flattens `job.config_toml` as written
and compares it with the current configuration rendered by the loader. Every
other reader of a frozen configuration goes through `frozen_config`, which is
the loader. So whatever the loader changes on the way in, a retired adapter
key folded to its current name or a field added later with a default, reads
as drift on every job open at the upgrade, while the job itself runs with the
loaded value. U197 copied the one fold it added into `drift` by hand.

**Measured cost.** None on U197's branch: the review found no other field
whose loaded value differs from its frozen bytes, so no producer was driven.
The next retired name, or the next field added with a default, would name a
key nobody changed in the drift warning of every open job.

**Closes when:** `drift` compares `frozen_config(job).to_toml_dict()` with the
current rendering, after a check that the loader's environment overrides do
not then hide a real move of an overridden key, and the hand copied fold goes.
Ledger only: the cost is a warning, not a wrong run.
