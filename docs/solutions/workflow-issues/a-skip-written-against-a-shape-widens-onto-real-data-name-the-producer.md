---
title: "A skip written against a shape widens onto real data; name the producer instead, and do not port the neighbour's rule without driving it"
date: 2026-09-20
category: workflow-issues
module: "src/cratekit/tagging/tag.py, src/cratekit/analysis/cli.py, src/cratekit/write/routing_cli.py"
problem_type: workflow_issue
component: item_derivation
severity: high
root_cause: unverified_assumption
applies_when:
  - "A walk has to skip something a known producer put on disk, and the producer's output has a recognisable shape"
  - "A fix is described as giving one walker the rule its neighbour already has"
  - "A guard is written as a filesystem or naming convention rather than as a list of names"
  - "A verb derives its job items from a walk, so what the walk drops is never queued and never reported"
  - "The data being walked is user authored, where titles and folder names are arbitrary"
symptoms:
  - "A verb reports that a folder holds nothing it can work on, over a folder holding tracks"
  - "A track is silently never queued and no report mentions it"
  - "A guard's docstring names two producers and the guard matches a much wider class than those two"
  - "Two walkers in the same product disagree about which files exist, and the older one is assumed correct"
related_components:
  - "item_derivation"
  - "tagging"
  - "analysis"
tags:
  - "walk"
  - "item-derivation"
  - "dotfile"
  - "guard-width"
  - "ported-rule"
  - "clean-report"
---
# A skip written against a shape widens onto real data; name the producer instead, and do not port the neighbour's rule without driving it

## Context

R-289 said `tagging.tag.audio_files` walks with `rglob` and skips nothing, so
`crate tag folder` over the download staging root queued the partial downloads a
killed attempt left and the landings `checked_landing` refused and deliberately
left as evidence. The staging tree is `.cratekit-acquire-staging`, a dot
directory, and the comment above the constant says that is safe because "the
folder walks that queue tagging and analysis skip dotfiles".

The entry's own closing condition was "`audio_files` gains the dot skip its
neighbour has". The neighbour is `analysis/cli._audio_in`, which skips any file
whose name starts with a dot, and whose docstring gives one reason: macOS writes
an AppleDouble sidecar, `._track.flac`, beside every file on the exFAT volume a
DJ stick is.

## What happened

The first cut did exactly what the entry asked. It skipped any path component
under the root beginning with a dot, and it was green: the two reproductions
died, the recursion still worked, the whole suite passed.

The code review drove it against a music library and it dropped real tracks.

- `...And Justice For All` is an album directory.
- `...Ready For It.flac` is a track.

Over a folder holding both, `audio_files` returned nothing, and `crate tag
folder` then reported `tag-folder-no-audio`, "this folder holds no audio files
this build can tag". That is a clean report over files the tool declined to see,
which is strictly worse than the defect the guard was written for: the original
bug queued files it should not have, and a person would have seen them in the
report. The fix hid files, and nothing anywhere said so.

## Why the rule was wrong

**A leading dot is not reserved.** It is a display convention that some shells
and file managers honour. No filesystem this product runs on refuses the name,
and the domain being walked is user authored text, where a title beginning with
an ellipsis is ordinary. Writing the guard as "hidden names" made it a guard
about a convention; what was actually wanted was a guard about two specific
producers.

**The neighbour was not authoritative.** `_audio_in` was read as the settled
answer because it is older and it states a reason. Its reason, the AppleDouble
sidecar, justifies skipping the prefix `._`, and it skips `.` instead. The
neighbour is one file with the same bug and a narrower blast radius, because it
walks one level and is not the thing R-289 was filed about. Porting its rule
ported its defect into a recursive walk, where the widening reaches whole album
directories rather than single files. It is now R-563.

## What it should be

Name the producers.

```python
SKIPPED_DIRNAMES: frozenset[str] = frozenset(
    {".cratekit-acquire-staging", ".cratekit-master-staging"}
)
APPLEDOUBLE_PREFIX = "._"
```

```python
if path.is_file()
and path.suffix.lower() in AUDIO_EXTS
and not path.name.startswith(APPLEDOUBLE_PREFIX)
and not SKIPPED_DIRNAMES.intersection(path.relative_to(root).parts[:-1])
```

Three things follow from naming them rather than matching a shape, and none of
them was available to the broad rule.

- **The set is auditable.** The names belong to this product and to macOS, so a
  reader can check the list against the producers. "Every dot name" cannot be
  checked against anything, because the set of things that might be dot named is
  open.
- **Both producers got covered, and one had been missed.** Writing the list made
  it obvious that `master.cli.staging_dir` builds the same kind of tree, and
  `.cratekit-master-staging` lands under `final.parent`, inside the music
  library, where a tagging sweep is far more likely to meet it than under the
  download root.
- **The prefix is two characters for a reason that is now written down.** One
  character is the defect above, and the comment says so, so the next person to
  "simplify" it meets the counterexample rather than rediscovering it.

The names are a hand copy, because `tagging.tag` is an engine and
`acquire.cli` and `master.cli` are shells that sit on top of the engines
(KTD23), so the engine cannot import either. An unpinned hand copy is the shape
that survives the rename it was supposed to follow, so the copy is pinned as set
equality:

```python
assert tag.SKIPPED_DIRNAMES == {
    acquire_cli.ACQUIRE_STAGING_DIRNAME,
    master_cli.MASTER_STAGING_DIRNAME,
}
```

Set equality rather than membership, so a THIRD staging tree added to a shell
and not to this set fails at that assertion instead of being walked into.

## The general shape

When a walk has to skip something, ask what put it there. If the answer is a
named producer, match the name. A shape is only safe to match when the shape is
reserved, and almost nothing in a filename is: not a leading dot, not a leading
underscore, not a trailing tilde, not a bracketed suffix. Every one of those is
also something a person types into a title.

The direction of the failure is what makes this worth a rule. A skip that is too
narrow leaves the original defect and the person can see it, because the unwanted
files appear in the report. A skip that is too wide removes files from a
derivation, and a derivation that is also the item derivation for a queued verb
means the files are never queued, never worked on, and never mentioned. The tool
says there is nothing to do, and it is believed.

## How it was caught, and what a green suite could not see

Not by the suite, which was green on the broad rule. By the code review reading
the guard against the domain and producing two real album and track names.

The mutation table then pinned both halves. `A2` widens the prefix back from
`._` to `.`, which is the exact defect, and it kills through the counterexample
test alone. `A4` forgets the master staging tree and kills 2. `A5` matches the
directory names on the absolute path rather than relative to the root and kills,
which pins the other decision in the clause: a person who points the verb
straight at a staging tree has named it deliberately and gets its files.
