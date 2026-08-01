# Cratekit

Acquisition and curation for rekordbox DJs. One CLI verb, `crate`, over a slim
core plus feature modules you turn on individually.

Cratekit gets music into your rekordbox library and keeps that library
organized: it matches external track lists against what you already own,
acquires what is missing, tags it, names it to your template, and writes it into
your own playlist taxonomy. Library writes go through a guarded layer that
refuses rather than risks your database.

This is a private tool shared with a handful of DJs. It is not published and not
for sale.

## Status

Early. The package foundation is landing; most feature modules have not been
ported yet. Nothing here is ready to point at a library you care about.

## Requirements

- Python 3.12 or 3.13
- rekordbox 7.x
- macOS today. The code carries no macOS-only assumptions, so a Windows adapter
  is an addition rather than a rewrite, but it has not been written.

## Install

```bash
git clone <your private remote> cratekit
cd cratekit
python3.12 -m venv .venv
.venv/bin/pip install -e .
```

That is the slim install: no audio DSP, no web framework, no machine-learning
stack. Feature modules that need heavy dependencies declare them as extras named
after the module:

```bash
.venv/bin/pip install -e '.[analysis]'   # key, BPM, energy detection
.venv/bin/pip install -e '.[vocals]'     # vocal presence and singer gender
```

Turning on a module without its extra is not a crash. The CLI attaches a stub
that prints the exact install command and exits non-zero, so `crate --help`
keeps working on a slim machine.

## First run

```bash
crate setup     # library location, credentials, taxonomy, profile
crate doctor    # verify the environment before anything writes
```

Neither exists yet; they land with the setup wizard.

## Safety posture

Three rules the code enforces rather than documents:

- **Beat grids are never written.** Not a tempo element, not a BPM tag, not an
  average-BPM field. rekordbox derives grids from the audio and nothing here
  biases that. This is not configurable, and two test suites fail the build if a
  code path could emit one.
- **Database writes go through one guarded layer.** Version pins, a refusal
  while rekordbox or its background agent is running, a cloud-sync canary, a
  snapshot taken before the session, a cross-process lock that lives with the
  library, a dry run, and a post-commit read-back through a fresh connection.
  Any of those refusing stops the write.
- **Music files are never modified**, except metadata tag writes,
  content-preserving renames, and the move to the system Trash that deletion
  performs after proving no active library row references the file.

Every write session is restorable by a documented verb.

## Licensing

Code authored here is MIT (see `LICENSE`). A vendored third-party component
keeps its own license, shipped intact alongside its source.

## Development

```bash
ruff check src tests scripts
pytest -q
```

CI runs both on Python 3.12 and 3.13, plus a cold-install job that proves a
clean checkout installs and imports with nothing preinstalled.

### Guards

Set up the commit hooks once per clone:

```bash
pip install pre-commit && pre-commit install
cp .scan-identity.example .scan-identity   # then list your own drive and account names
```

`scripts/scan_repo.py` runs on every commit and again in CI. It scans **every**
tracked path, vendored trees included, for two things: personal literals (a home
directory, a volume, an account, a machine name) and credential-shaped content
(OAuth tokens, API keys, private keys, and filenames that are credential stores
regardless of what is inside them). Nothing here should name a person or carry a
secret, and the hook is what stops one reaching the history, where removing it
becomes a rewrite everybody has to follow.

`.scan-identity` is gitignored and optional. It tells the scan which bare names
are yours, so "the X drive must be mounted" is caught even when X is not
currently plugged in. Path-shaped literals are caught without it.

### Deferred guards

Some test suites carry guards for modules that have not been written yet. Those
are ported complete, never stubbed, and skipped with a reason naming the unit
that arms them:

```bash
pytest -q -rs        # every skip prints the unit that unblocks it
```

`tests/_pending.py` is the register and `tests/test_pending_units.py` holds it
accountable: adding a skip without recording it fails the build, and so does
keeping one after its module lands. A skip is a countdown, not a hiding place.
