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

Built, and being cut over from the system it replaces one workflow at a time.
Every planned verb exists and the test suite covers them. Setup and the health
check have run on a real library, and four attended sittings have run backup,
download, vocal scoring, playlist export and a favourites sweep on one.

Some workflows have not had a live sitting yet, and some that have carry known
problems. [`docs/cutover.md`](docs/cutover.md) is the per workflow record of
which is which, and [`docs/GUIDE.md`](docs/GUIDE.md) summarises it. Read the
guide's "Where it stands" table before pointing a writing verb at a library you
care about, and keep a current backup either way.

## Requirements

- Python 3.12 or 3.13
- pipx, which the install below sets up with Homebrew
- rekordbox 7.x
- macOS today. The code carries no macOS-only assumptions, so a Windows adapter
  is an addition rather than a rewrite, but it has not been written.
- Some command line programs, depending on which modules you use: `ffmpeg` and
  `ffprobe`, `yt-dlp`, `rclone` for backup, and `keyfinder-cli` for key
  detection. `crate doctor` reports each one that is missing and names the
  package to install.
- A keychain the operating system provides, where credentials are stored. Nothing
  secret is written to the configuration file.

## Install

The repository is private, so your GitHub account needs an invitation first. If
git asks for a password, give it a personal access token, since GitHub no longer
accepts account passwords for git.

Cratekit installs with pipx, which gives a command line tool its own private
Python environment and puts the command where every terminal window can find it,
so there is nothing to activate afterwards. Set pipx up once per machine:

```bash
brew install pipx
pipx ensurepath
```

`pipx ensurepath` adds pipx's folder to your PATH by editing your shell startup
files. Open a new terminal window afterwards so it takes effect. Then install
Cratekit:

```bash
git clone https://github.com/philgutowski/cratekit.git
cd cratekit
pipx install --python python3.12 .
```

That installs the `crate` command. `--python python3.12` pins the Python version,
because Cratekit needs 3.12 or 3.13 and pipx otherwise uses whichever Python
Homebrew currently ships, which can be newer and is refused. If you only have
3.13, write `python3.13`. pipx copies Cratekit into its own environment, so the
folder is needed again only when you update. Do not add `--editable`, which links
the command to the folder instead of copying it. An editable install makes
`crate doctor` treat your machine as a developer checkout and fail a check about
commit hooks, and that failure stops `crate setup`. Every example in these docs
writes the command as plain `crate`. If a command answers
`command not found: crate`, open a new terminal window, because
`pipx ensurepath` only affects windows opened after it ran.

That is the slim install: no audio DSP, no web framework, no machine-learning
stack. Feature modules that need heavy dependencies declare them as extras named
after the module. `analysis` adds key, BPM and energy detection, and `vocals`
adds vocal presence and singer gender. Add the ones you will use, from inside the
cratekit folder, and list every extra you want in one command:

```bash
pipx install --force '.[analysis,vocals]'
```

`--force` reuses the environment you already made and keeps its Python version,
so this command takes no `--python`, and pipx ignores one with a warning. The
quotes matter, since zsh reads square brackets as a pattern and refuses the
command without them. Turning on a module without its extra is not a crash. The
CLI attaches a stub that prints an install command and exits non-zero, so
`crate --help` keeps working on a slim machine. That printed command starts with
`pip`, which is written for a plain virtual environment and installs into the
wrong place for a pipx install. Use the pipx command above instead.

To update, pull and reinstall from inside the cratekit folder. Pulling alone
changes nothing, since pipx holds its own copy. A reinstall keeps the extras you
chose:

```bash
git pull
pipx reinstall --python python3.12 cratekit
```

## First run

```bash
crate setup
crate doctor
```

`crate setup` records your library location, taxonomy, profile and rekordbox
version pin. `crate doctor` verifies the environment before anything writes.

`crate setup` asks only what it cannot work out, and every answer is also a flag,
so it can be scripted. It is safe to re-run. It keeps answers you already gave,
refuses to overwrite a configuration it cannot read, and refuses to record a
library volume that is not actually mounted. It ends by running the health check
and exits on that check's verdict.

`crate doctor` reads the machine and writes nothing to your library. Every line
is `ok`, `fail` or `note`. A `fail` blocks a verb and names the fix, and a `note`
is worth knowing and needs no action.

Credentials are recorded separately, and only for the modules that need them.
`crate login NAME --from-file PATH` stores one in the keychain. Signing in to the
streaming account takes two commands, described in
[`docs/adapters.md`](docs/adapters.md).

## Using it

[`docs/GUIDE.md`](docs/GUIDE.md) is the user guide. It explains how the pieces
fit, what to check before a session, how to answer a confirmation, how to record
the backup acknowledgment every write needs, and gives a recipe for each
workflow. `crate --help` lists every verb, and `crate skills install` copies a
set of short operator guides where an AI coding agent can find them.

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

Development uses its own editable environment inside the checkout rather than
pipx. Because it is editable, `crate doctor` checks that the commit hooks under
Guards are installed, and fails until they are. Set it up once, and activate it
in each terminal window you work in:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Then:

```bash
ruff check src tests scripts
pytest -q
```

CI runs both on Python 3.12 and 3.13, plus a cold-install job that proves a
clean checkout installs and imports with nothing preinstalled.

### Guards

Set up the commit hooks once per clone. Both hook types matter. A bare
`pre-commit install` writes only the first, and the closing check on commit
messages then silently never runs.

```bash
pip install pre-commit && pre-commit install --hook-type pre-commit --hook-type commit-msg
cp .scan-identity.example .scan-identity
```

Then open `.scan-identity` and list your own drive and account names.
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

A guard can be written before the module it governs. Such a guard keeps its full
assertion, is never stubbed, and is skipped with a reason naming the unit that
arms it. This prints every skip with the unit that unblocks it:

```bash
pytest -q -rs
```

`tests/_pending.py` is the register and `tests/test_pending_units.py` holds it
accountable: adding a skip without recording it fails the build, and so does
keeping one after its module lands. A skip is a countdown, not a hiding place.
The register is empty today, because every guard has been armed.
