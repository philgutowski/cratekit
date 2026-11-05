---
name: release
description: Cut a Cratekit release when Phillip asks for one, in any session. Plans what landed since the last tag, judges the semantic version bump, cuts the tag and the GitHub release with its notes, and reports the version. Use when Phillip says cut a release, ship a version, tag a release, or publish a release.
---

# Release

Phillip and the DJs the tool is shared with install tagged releases only,
never raw `main` (U159). A release is cut when Phillip asks, never on a
schedule and never on a session's own initiative. The releases section of
`docs/METHOD-local.md` is the rule; this is the procedure.

**A cloud session cannot cut.** Its git proxy refuses a tag push and the
REST git tags path, and the releases API refuses "this session type", all
measured on 2026-10-28. A cloud session asked for a release runs steps 1 to 3,
reports the bump it judged, and hands the cut to Phillip's Mac: an attended
card carrying `scripts/release.py cut --bump <kind> --mac-battery`. The Mac's
own git and `gh` credentials permit both.

## 1. Be on a clean, current main

    git fetch origin main
    git checkout main && git merge --ff-only origin/main
    git status --short          # must print nothing

## 2. The battery on this commit

On a cloud container:

    .venv/bin/python scripts/cloud_battery.py baseline    # only if none was measured on this machine
    .venv/bin/python scripts/cloud_battery.py compare

`compare` records its verdict for the commit it measured, and `cut` reads it.
On a Mac, skip this and pass `--mac-battery` to `cut`, which runs the full
battery itself. A red battery is a stop: no release goes out over it.

## 3. Plan and judge the bump

    .venv/bin/python scripts/release.py plan

It lists the pull requests merged since the last `vX.Y.Z` tag, then the merges
made without one, each with the bump its title asks for, and proposes the
largest. It reads every commit in the range, not only the first parent line,
so a unit merged on `origin/main` while a local session's commit waited is
counted, and a local `Merge branch 'main' of ...` is never itself listed
(U215). `plan --since vA.B.C --tip vX.Y.Z` reruns a past range, and `--notes`
prints only that range's release body, ready to replace a published one. Read the list rather than taking the proposal on trust: **major** when
a change breaks an existing library or config, **minor** when it adds a verb
or changes behaviour, **patch** when it only repairs. While the version is
below 1.0.0, a breaking change is a minor bump with the break said first in
the notes, never a jump to 1.0.0; that number is Phillip's to choose.

## 4. Cut

    .venv/bin/python scripts/release.py cut --bump minor

It refuses off `main`, on a dirty tree, behind or ahead of `origin/main`, and
without a clean battery on the commit. Otherwise it writes the version into
`pyproject.toml` and `src/cratekit/__init__.py`, commits `release: vX.Y.Z`,
makes the annotated tag, pushes `main` and the tag, and publishes the GitHub
release with the notes over REST. `main` and the tag go in one atomic push,
so either both land or neither does. If that push is refused because `main`
moved, delete the local tag (`git tag -d vX.Y.Z`), reset `main` to
`origin/main`, and start again at step 1; never force push. If only the
GitHub release is refused, the tag is out and a second `cut` finds nothing
landed: run the one `gh api` command `cut` printed, which publishes the notes
it kept. A shallow clone is refused; `git fetch --unshallow --tags origin`
first.

## 5. Report

Tell Phillip the version, the tag, the release URL `cut` printed, and the
notes. If a card asked for the release, comment on it under the heading
`Release` with the same three facts. `crate doctor` on an installed copy reads
the new tag and prints the upgrade command, which is how the release reaches
the people using it.
