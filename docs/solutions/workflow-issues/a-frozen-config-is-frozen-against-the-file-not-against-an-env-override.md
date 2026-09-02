---
title: "A frozen config is frozen against the file, not against an env override"
date: 2026-09-02
category: workflow-issues
module: "src/cratekit/core/jobs.py, src/cratekit/core/config.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: test_isolation
resolution_type: test_fix
applies_when:
  - "A test drives a divergence between a job's frozen configuration and the live one by moving the library between queue and resume"
  - "The test fixture sets CRATEKIT_LIBRARY_ROOT (or any config env override) and the test then edits the saved config file to simulate a later change"
  - "A mutation row on code that reads frozen_config() instead of the live config kills nothing and the guard looks untested rather than absent"
related_components:
  - "background_job"
tags:
  - "frozen-config"
  - "env-override"
  - "mutation-testing"
  - "test-that-cannot-fail"
---

## Context

U50 (`crate backup run`, #68) bound the backup worker to a queued job and had to
prove the published age envelope reads the job's own frozen configuration
(`jobs.frozen_config`, `src/cratekit/core/jobs.py:889`) rather than the live one,
per KTD9. The mutation table over the review fixes killed three of four rows; the
fourth, `test_the_ages_reported_are_the_ones_this_job_published` in
`tests/test_backup_cli.py`, killed zero mutants on that line. The test looked
correct, asserted the right thing, and could not fail.

## Guidance

`jobs.frozen_config(job)` rebuilds a `Config` by calling
`config.from_dict(tomllib.loads(job.config_toml))` (`src/cratekit/core/jobs.py:891`),
and `config.from_dict` applies environment overrides first, unconditionally,
before anything else is read (`src/cratekit/core/config.py:2902`,
`_apply_env_overrides`). That is true of every call to `from_dict`, live or
frozen: **a frozen configuration is frozen against its own bytes changing, not
against an environment variable that is still set when it is rebuilt.** If
`CRATEKIT_LIBRARY_ROOT` is set, both the live config and a job's frozen config
relocate their library root onto that variable's value, and they keep agreeing
no matter what the saved file says.

The test fixture `cfg` (`tests/test_backup_cli.py:62`, via
`tests/conftest.py:162`) sets `CRATEKIT_LIBRARY_ROOT` for the whole suite so
tests don't depend on a real filesystem layout. That default is exactly what
defeats a test trying to prove two config readings diverge:

- **Draft 1** moved only the saved TOML file (`config.save(replace(cfg, ...))`)
  while the env var was still set. Both the live read and the frozen rebuild
  relocated onto the env var's path, so the two readings never differed. Zero
  mutants died.
- **Draft 2** moved the env var too, "to be safe." That's worse than draft 1's
  bug, not a fix: `frozen_config` rebuilds through the identical `from_dict`
  code path the live read uses, so the override relocates the frozen
  configuration's root exactly as it relocates the live one. The two agree
  again, for the same reason.
- **The shape that actually works**: `monkeypatch.delenv(config.ENV_LIBRARY_ROOT)`
  so neither reading is overridden, then change only the saved file
  (`config.save(...)`, `config.reset_cache()`). That is the only combination
  where a live read and a frozen rebuild can disagree, because it's the only
  one where the divergent input (the file) is the thing both codepaths actually
  read.

Two more traps sit next to this one, both worth carrying into any future test
in this shape:

- Relocating the library root without relocating `db_path` produces a state the
  product itself refuses to save (KTD21b requires the database under the
  library root, because the only atomic commit available is a rename, and a
  rename is atomic only within one filesystem). A test that builds that state is
  measuring a shape `config.save` won't let a real user reach.
- After the move, assert the divergence actually exists before driving the
  behavior under test: `config.load().library.root == elsewhere` and the fact
  file not yet present at the relocated path. Otherwise a second latent zero
  (the live config still pointing at the original library) can silently pass
  the same test again.

## Why This Matters

A test that cannot fail is indistinguishable from a passing test until a
mutation table forces the question, and by then the property it was meant to
guard (KTD9: a job runs against the configuration it was queued with) has no
test actually pinning it. Nothing in this repository stated the override's
precedence over a frozen rebuild before this surfaced; the fixture's own
default (setting `CRATEKIT_LIBRARY_ROOT` everywhere) is what made the trap easy
to walk into twice in a row.

## When to Apply

Any test whose job is to prove a *frozen* value (config, snapshot, cached
input) differs from the *live* equivalent, in a suite where an environment
override participates in building both. Check whether the override is applied
inside the same rebuild path the frozen read uses before trusting that moving
one input is enough to produce a divergence.

## Examples

```python
# Wrong: env override still set, both readings relocate onto it, zero mutants die
config.save(replace(cfg, library=replace(cfg.library, root=elsewhere)))
config.reset_cache()

# Wrong: unsetting the override too just makes the frozen rebuild agree with
# the live read for the same reason draft 1 did
monkeypatch.delenv(config.ENV_LIBRARY_ROOT)
config.save(replace(cfg, library=replace(cfg.library, root=elsewhere)))
config.reset_cache()
# (missing: db_path must move with root, or config.save refuses)

# Right: unset the override, move root AND db_path together, then confirm the
# divergence exists before driving the behavior under test
monkeypatch.delenv(config.ENV_LIBRARY_ROOT)
config.save(replace(cfg, library=replace(
    cfg.library, root=elsewhere, db_path=elsewhere / "db" / "master.db",
)))
config.reset_cache()
assert config.load().library.root == elsewhere
assert not backup_facts.path_for(config.load()).exists()
```

See `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
and its mutation row in `docs/mutation/u50-review-fixes.md` for the driven case.
