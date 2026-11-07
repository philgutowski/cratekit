# Cratekit

Acquisition and curation for rekordbox DJs: one command, `crate`, over a slim
core and feature modules you switch on per profile.

It matches external track lists against the library you own, acquires what is
missing, tags and names it to your template, and files it into your playlist
taxonomy. Library writes go through a guarded layer that refuses rather than
risks the database.

A private tool shared with a few DJs; not published and not for sale.

## Status

In use on a real library, replacing an older system one workflow at a time.
[`docs/cutover.md`](docs/cutover.md) records which workflows have run live and
which carry known problems. Read it before pointing a writing verb at a library
you care about, and keep a current backup either way.

## Requirements

- macOS, the only platform run against a real library
- Python 3.12 or 3.13
- rekordbox 7
- pipx (installed below with Homebrew)
- access to the private GitHub repository, with git signed in to that account
- per module, command line tools: `ffmpeg` and `ffprobe`, `yt-dlp`, `rclone`
  (backup) and `keyfinder-cli` (key detection); `crate doctor` names each
  missing one and its package

Credentials live in the operating system keychain, never in the configuration
file.

## Install

Sign git in to GitHub once, for example with `brew install gh`, `gh auth login`
and `gh auth setup-git`. Both the install and `crate doctor`'s release check
read the repository with your git credentials.

```bash
brew install pipx
pipx ensurepath        # then open a new terminal window
pipx install --python python3.12 "cratekit @ git+https://github.com/philgutowski/cratekit@v0.13.0"
```

Use the newest tag from https://github.com/philgutowski/cratekit/releases in
place of `v0.13.0`, never `main`. `--python` pins an interpreter Cratekit
supports; write `python3.13` if that is what you have. `command not found:
crate` means the terminal window predates `pipx ensurepath`.

Modules with heavy dependencies take an extra of the same name: `analysis`
(key, BPM, energy) and `vocals` (vocal presence, singer gender). Name every
extra you want in one command; the quotes stop zsh reading the brackets:

```bash
pipx install --force "cratekit[analysis,vocals] @ git+https://github.com/philgutowski/cratekit@v0.13.0"
```

A module switched on without its extra prints the install command and exits
non-zero; `crate --help` still works.

**Upgrade:** `crate doctor`'s `install.release` line names a newer release and
prints the pipx command that installs it with your extras kept.

## First run

```bash
crate setup
crate doctor
```

`crate setup` asks only what it cannot work out, takes every answer as a flag,
keeps earlier answers when re-run and ends by running `crate doctor`, which
writes nothing. Each doctor line is `ok`, `fail` (blocks a verb, names the fix)
or `note` (no action). [`docs/GUIDE.md`](docs/GUIDE.md) says what setup records.

`crate login NAME --from-file PATH` records a credential in the keychain.
Signing in to the streaming account is set out in
[`docs/adapters.md`](docs/adapters.md).

## Using it

[`docs/GUIDE.md`](docs/GUIDE.md) is the user guide: how the pieces fit, the
pre-session checks, a recipe per workflow, gates, the backup acknowledgment and
running Cratekit with an AI assistant. `crate --help` lists every verb.

## Safety posture

- **Beat grids are never written**: no tempo element, BPM tag or average-BPM
  field. Not configurable; tests fail the build on any code path that could.
- **Database writes go through one guarded layer**: version pins, refusal while
  rekordbox or its background agent runs, a backup acknowledgment, a cloud-sync
  canary, a snapshot before writing, an additive whitelist, a cross-process
  lock and a read-back after the commit. Any refusal stops the write.
- **Music files change only by** tag writes, content-preserving renames, and a
  move to the system Trash once no library row references the file.

`crate restore run` restores any write session's snapshot.

## Licensing

Authored code is MIT (`LICENSE`). The vendored downloader is AGPL-3.0-only and
ships with its licence; see [`docs/vendoring.md`](docs/vendoring.md).

## Developing

[`docs/DEVELOPING.md`](docs/DEVELOPING.md). None of it is needed to run
Cratekit.
