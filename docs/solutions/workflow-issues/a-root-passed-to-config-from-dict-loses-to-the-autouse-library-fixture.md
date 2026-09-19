---
title: A root passed to config.from_dict loses to the autouse library fixture
date: 2026-09-18
category: workflow-issues
module: tests/conftest.py
problem_type: testing_gap
component: testing_framework
severity: medium
root_cause: stale_fixture_premise
resolution_type: test_fix
applies_when:
  - A test builds a library-relative layout (Music/, staging, exports) under its
    own tmp_path and then passes that tmp_path as library.root to config.from_dict
  - The test asserts a guard that only fires for paths under the configured root
  - The guard under test silently never fires, or fires against files the test
    never planted
tags:
  - fixture
  - config
  - library-root
  - autouse
  - test-isolation
  - env-override
  - false-pass
---

# A root passed to config.from_dict loses to the autouse library fixture

## Context

`_block_real_library_paths` in `tests/conftest.py:191` is autouse. It sets
`CRATEKIT_LIBRARY_ROOT` to its own `tmp_path_factory.mktemp("library")` for
every test, so no test can accidentally resolve a real audio file or the real
rekordbox database.

`config.from_dict` (`src/cratekit/core/config.py:2888`) applies environment
overrides before validating. `_apply_env_overrides` (around `config.py:2538`)
reads `CRATEKIT_LIBRARY_ROOT` and, when set, does this unconditionally:

```python
library["root"] = str(root_override)
```

This runs whether or not the caller's dict already named a `root`. It is
correct production behaviour: an operator's environment variable is supposed
to outrank a config file's own path. But it means a test that writes

```python
cfg = config.from_dict({"library": {"root": str(tmp_path / "lib"), ...}})
```

does not get `tmp_path / "lib"`. It gets the fixture's own temp directory,
because the autouse fixture already set the env var before the test body ran.
`cfg.library.root` is silently something other than what the test wrote in the
dict literal.

U71's landing engine guards refuse a source folder that is inside the library,
and refuse a staging directory the library owns. A first draft of
`tests/test_landing.py` built the whole layout, staging included, from the
test's own `tmp_path`, then asserted the "refuses a folder the library owns"
guard. The guard never fired, because `cfg.library.root` was the fixture's
directory, not `tmp_path`, so nothing the test built was ever "inside the
library" as the running config saw it. The test still passed, for the wrong
reason: it was written to expect the guard to refuse, and a `tmp_path` folder
that is not under the effective root is refused by a different guard first,
so a loosely written assertion can pass without ever exercising the intended
line.

## Guidance

Never build a library-relative layout from the test's own `tmp_path` and
assume it lines up with the config. Build it from the config's own root:

```python
cfg = config.from_dict({"library": {"root": str(tmp_path / "lib"), ...}})
music = cfg.library.root / cfg.paths.music_dir
music.mkdir(parents=True)
```

`cfg.library.root` is `tmp_path / "lib"` here only because
`CRATEKIT_LIBRARY_ROOT` happens to be unset in that particular test process; do
not rely on that either. Read the root back off `cfg` every time, after
`from_dict` has run, rather than off the literal passed in. That is what
`tests/test_landing.py` does now, and it is the only way a guard that compares
a path against `library.root` is exercised against the root the guard will
actually see.

The same trap applies to `download_staging` through `CRATEKIT_DOWNLOAD_STAGING`
(`config.py:2563`), by the identical mechanism.

## Why This Matters

A guard whose test builds its fixture from the wrong root does not fail loudly.
It passes, either because a different, unintended guard catches the
mis-rooted path first, or because the intended guard is simply never reached
and the assertion downstream happens to hold anyway. Either way the battery
stays green while the guard under test goes undriven, and the gap is invisible
until the guard is read at the line number rather than at the test result.

## When to Apply

- Any new test that composes a library layout (Music, staging, exports,
  intake XML) to exercise a root-relative guard.
- Any test asserting a refusal or acceptance that depends on "is this path
  inside the library."
- Reviewing an existing test where the layout is built from `tmp_path`
  directly rather than from `cfg.library.root` or `cfg.paths.*`.

## Related

- `tests/conftest.py:191` (`_block_real_library_paths`): the fixture whose
  docstring already explains why its own temp directory is separate from the
  test's `tmp_path`, but not that it overrides a root the test tried to set
  explicitly.
- `src/cratekit/core/config.py:2538` (env override application): the
  production behaviour this fixture rides on. Correct outside tests; the trap
  is only in assuming a test-supplied `root` in the dict survives it.
