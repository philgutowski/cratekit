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
the latest release of Cratekit, a tagged version straight from GitHub:

```bash
pipx install --python python3.12 "cratekit @ git+https://github.com/philgutowski/cratekit@v0.2.0"
```

Install a release tag, never the moving `main`. The releases are listed at
https://github.com/philgutowski/cratekit/releases; put the newest tag where
the command says `v0.2.0`. That installs the `crate` command.
`--python python3.12` pins the Python version, because Cratekit needs 3.12 or
3.13 and pipx otherwise uses whichever Python Homebrew currently ships, which
can be newer and is refused. If you only have 3.13, write `python3.13`. Every
example in these docs writes the command as plain `crate`. If a command
answers `command not found: crate`, open a new terminal window, because
`pipx ensurepath` only affects windows opened after it ran.

That is the slim install: no audio DSP, no web framework, no machine-learning
stack. Feature modules that need heavy dependencies declare them as extras named
after the module. `analysis` adds key, BPM and energy detection, and `vocals`
adds vocal presence and singer gender. Name every extra you want in one
command, in brackets after `cratekit`:

```bash
pipx install --force "cratekit[analysis,vocals] @ git+https://github.com/philgutowski/cratekit@v0.2.0"
```

`--force` reuses the environment you already made and keeps its Python version,
so this command takes no `--python`, and pipx ignores one with a warning. The
quotes matter, since zsh reads square brackets as a pattern and refuses the
command without them. Turning on a module without its extra is not a crash. The
CLI attaches a stub that prints an install command and exits non-zero, so
`crate --help` keeps working on a slim machine. Outside pipx it is `pip`, run by
the Python `crate` itself runs on.

**To upgrade**, run `crate doctor`. When a newer release is published, its
`install.release` line says so and prints the one pipx command that moves to
it, keeping the extras you installed. It is the install command above with the
new tag, and you can run that yourself as well. If doctor cannot reach GitHub
(offline, or git has no credentials), it says it could not read the releases
rather than that your copy is current.

A developer working on Cratekit itself installs from a clone instead, with
`pipx install --python python3.12 .` inside the folder. Do not add
`--editable`, which links the command to the folder: an editable install makes
`crate doctor` treat your machine as a developer checkout and fail a check
about commit hooks, and that failure stops `crate setup`.

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
workflow. `crate --help` lists every verb.

## Working with an AI assistant

Cratekit is built to be run with a coding agent beside you, and it ships what one
needs: twelve short guides, one per workflow area, and a workspace that tells the
agent what it may do on its own and what waits for you.

The workspace goes outside this clone, because this clone's own instructions are
about building Cratekit rather than running it. Copy the shipped template once,
then install the guides into it:

```bash
mkdir -p ~/cratekit-work
cp operator/AGENTS.md operator/CLAUDE.md ~/cratekit-work/
crate skills install --into ~/cratekit-work/.claude/skills
```

Start the agent in `~/cratekit-work`. It reads `AGENTS.md`, which points at
`CLAUDE.md`, which is the operator contract: reporting verbs run freely, every
writing verb waits for you, a gate is answered by you, and the backup
acknowledgment is yours alone because the product will not accept one from a
session working on your behalf. `AGENTS.md` is there so the folder is not
specific to one tool, and the guides are plain markdown that any agent can read.

Run the install command again after updating Cratekit. Each copy carries the
version that wrote it, so the verb reports which guides were stale and refreshes
them in the same run.

None of this is required. Every workflow runs from the command line without an
agent, and the guides exist so the order is not something you have to work out.

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

## Developing Cratekit

Working on the product itself is a separate setup with its own rules, and none of
it is needed to run Cratekit. [`docs/DEVELOPING.md`](docs/DEVELOPING.md) has the
editable environment, the test battery and the commit guards. `CLAUDE.md` and
`AGENTS.md` at the root of this repository are the session contract for an agent
working on the code, and [`docs/METHOD.md`](docs/METHOD.md) is the pipeline.
