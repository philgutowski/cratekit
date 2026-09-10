---
title: A guard that refuses an empty list cannot see a barren one
date: 2026-09-10
category: integration-issues
module: "src/cratekit/core/session.py, src/cratekit/write/trees.py, src/cratekit/write/rebuild.py"
problem_type: integration_issue
component: write_session
root_cause: incorrect_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A new destructive write passes every session gate and its analysis watch fingerprints zero files"
  - "write_tree_membership's ValueError about an empty analysis_roots never fires, because the list has one entry"
  - "The whole suite is green, the mutation table kills the row, and the watch is still armed over nothing"
  - "A caller names root/Music while rekordbox keeps its ANLZ files under root/PIONEER/USBANLZ"
applies_when:
  - "A unit adds a new caller of write_tree_membership, restore, or anything else taking analysis_roots"
  - "A guard refuses an empty collection and the caller supplies a non-empty one whose CONTENTS are empty"
  - "A test asserts that a path was passed rather than asserting what that path covers"
related_components:
  - "beat_grid_protection"
  - "testing_framework"
tags:
  - "analysis-watch"
  - "beat-grid"
  - "emptiness"
  - "guard-bypass"
  - "first-caller"
  - "green-suite"
  - "r17"
---

# A guard that refuses an empty list cannot see a barren one

## Context

U53 bound the first callers in `src` of `cratekit.write.rebuild.rebuild_tree`,
under two handler keys, and added a second write path for the `route.inbox`
apply. All three hand `analysis_roots` to
`cratekit.write.trees.write_tree_membership`, which arms the runtime half of
R17's fifth surface: `cratekit.core.session.analysis_files_unmoved` fingerprints
every ANLZ file under those roots before the body runs and compares afterwards,
so a beat grid rewritten as a side effect of a membership write is caught. That
watch is one of the two mechanisms behind this project's absolute constraint
that nothing ever writes a beat grid.

`write_tree_membership` already guards the obvious failure, and its docstring is
emphatic about why:

> `analysis_roots` HAS NO DEFAULT AND MAY NOT BE EMPTY, which is the whole
> reason this unit was registered against U8's countdown. The watch it arms
> watches nothing when nobody names a root, and a guard that silently watches
> nothing is worse than an absent one.

Both new call sites passed `[Path(cfg.library.root) / cfg.library.music_dir]`.
That list has one entry. It passes the guard. It also covers no analysis file at
all, because rekordbox does not keep ANLZ files beside the audio: they live under
its own directory inside the library, and every other caller in the package
therefore names `cfg.library.root`.

## The distinction that matters

**An EMPTY list and a BARREN one are different failures and only one of them has
a guard.** The empty list is "nobody named a root", which is a mistake at the
call site the callee can see. The barren list is "somebody named a root that
holds none of the thing being watched", which is a mistake about the WORLD and
is invisible from inside the callee, because the callee cannot know where a
given library keeps its analysis files.

The symptom is identical in both cases and it is the worst possible symptom: the
watch fingerprints the empty set, compares the empty set afterwards, finds no
difference, and reports a clean session whatever happened to the grids. So the
guard that exists specifically to stop a watch that watches nothing is satisfied
by the one spelling of that failure it cannot detect.

The green suite could not see it either. Every test that reached these writes had
a temporary library with no ANLZ files anywhere in it, so the correct root and
the barren one fingerprinted the same empty set and produced the same result.

## How it was found and how it was fixed

The unit's own suite was green and its 25 row mutation table was written before
this was noticed. The built in `/code-review` found it by reading the call sites
against their five siblings, four of which pass the library root and two of which
say in a comment that they do so deliberately. That is the general method for
this class: **a new call site's argument is judged against what the existing call
sites pass, not against whether the callee accepted it.**

Both sites now pass `[Path(cfg.library.root)]`. The watch matches by FILENAME
(`ANLZ_NAME_PATTERN`), so a wider root costs a walk and nothing else, and the
pattern's own docstring already argues that being wider is the safe direction.

## The test shape this needs, which is not the obvious one

A test asserting that the call passed `cfg.library.root` would pin the string and
prove nothing about the world: the next person to change where a library keeps
its analysis files breaks the watch and the assertion still passes.

The guard that actually bites plants a real analysis file where rekordbox puts
one, wraps `session.assert_gates` to CAPTURE the roots each write armed without
disarming it, and then asserts over the tree:

```python
assert planted_grid in session.analysis_files_under(roots)
```

That is a measurement of what the watch covers rather than of what was passed.
Reverting either call site to the music directory fails it with the roots printed
in the message, which was verified by hand on the rebuild side before the
mutation table was re-run.

## The general rule

**When a guard refuses an empty collection, ask what a NON-EMPTY collection with
nothing in it would do.** A path that exists and contains none of the watched
thing, a glob that matches no file, a root the caller is confident about and
should not be: each of them satisfies the emptiness check and produces exactly
the outcome the check was written to prevent. This repository's first recurring
defect pattern is "absence read as evidence of absence"; this is that pattern
wearing a guard, where the absence is the watched set and the evidence is the
clean session report.

## See also

- `docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`,
  which is the other half of the same session: binding an engine makes its
  argument choices yours to defend.
- `docs/METHOD.md`, pattern 3, a fix that lands on the performing path instead of
  the checking path. This is its mirror: a check that lands on the argument's
  SHAPE instead of on its contents.
