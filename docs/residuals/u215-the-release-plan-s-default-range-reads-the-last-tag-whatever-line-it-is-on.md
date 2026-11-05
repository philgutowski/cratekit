---
title: The release plan's default range starts at the highest version tag whatever line of history it is on
found: at the review of #529, U215, 2026-11-05.
issue: no
---

**The mechanism.** `gather` in `scripts/release.py`, with no `--since`, takes
the highest `vX.Y.Z` among every tag, and `plan` and `cut` read the range from
it. U215 added a crossed tag and reversed range refusal on the `--since` path
only. A version tag on a commit `main` never reached starts the default range
there.

**Measured cost.** Driven by the round two reviewer in a throwaway repository,
v0.9.0 tagged on an abandoned branch: `plan` prints `current version 0.2.0,
last tag v0.9.0`, lists one of two units on `main` and proposes a version
below an existing tag, with no refusal. Not produced on the real repository:
`cut` refuses off `main`, and origin carries six tags, every one on a `main`
release commit.

**Closes when:** the default range takes the highest version tag merged into
`HEAD` (`git tag --merged HEAD`), or refuses one that is not. Ledger only.
