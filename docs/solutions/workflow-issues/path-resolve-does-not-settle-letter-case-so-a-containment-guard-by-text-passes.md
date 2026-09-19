---
title: "Path.resolve does not settle letter case, so a containment guard that compares resolved paths as text passes a path that is inside"
date: 2026-09-19
category: workflow-issues
module: "src/cratekit/intake/fetch.py"
problem_type: workflow_issue
component: path_guards
severity: high
root_cause: identity_not_unique
applies_when:
  - "A guard decides whether one folder is inside another by `root in path.parents`, `is_relative_to`, or equality of resolved paths"
  - "Either path comes from an environment variable, a config value or a command line, so a person chose its spelling"
  - "The volume is case insensitive, which is the default for macOS and for the exFAT drives a DJ library sits on"
symptoms:
  - "A path spelled in lower case under a folder recorded in mixed case is reported OUTSIDE it, with no error"
  - "A test of the guard built with a symlink passes, because resolve does follow links, and says nothing about case"
  - "The guard is green on CI, which runs on a case sensitive volume where the two spellings really are two folders"
related_components:
  - "fetch"
  - "landing"
  - "snapshot"
  - "restore"
tags:
  - "path-containment"
  - "case-insensitive-volume"
  - "samefile"
  - "identity-not-unique"
  - "library-root"
---
# Path.resolve does not settle letter case

## What happened

U104 fetches a mix into a scratch folder and must never let one land under the
library root. The guard resolved both paths and asked whether the library was
among the scratch folder's parents. The code review said it would miss a
differently cased spelling. Driven on the project's own machine, in a temporary
directory: make `Library/Music`, spell a path under `library/music/state`, and

- the lower case spelling EXISTS, because the volume is case insensitive,
- `resolve()` returns it in lower case, exactly as typed,
- `Library.resolve() in that.resolve().parents` is `False`.

So a state root pointed inside the library in the wrong case passes the guard,
and the mix lands beside the music.

## Why the obvious test does not catch it

The natural test makes a symlink to the library and puts the scratch path under
the link. `resolve` follows links, so that test passes and proves the guard
handles ONE way two names can be one folder. Letter case is another, and
`resolve` does nothing about it. Unicode normalisation on the same volumes is
presumably a third and was not driven.

## The rule

A path's text is not its identity. When a guard protects a folder that exists,
ask the filesystem: compare every existing ancestor with `samefile`, which
answers whether two names are one folder by device and inode. Keep the textual
check as well, because it is the only layer that can answer when the protected
folder is NOT there, and an unplugged library drive is an ordinary state here.
Each layer needs its own test, since either one covers for the other whenever
both can answer.

To test the filesystem layer on any volume, including a case sensitive CI
runner, do not skip. Make the second spelling a symlink where it is not
already the same folder, and hold `Path.resolve` still with a monkeypatch, so
the textual layer cannot answer and only `samefile` can.

## Where else

Thirteen other sites in `src` carry the textual shape and were not driven. They
are listed in the ledger under the residual "Thirteen containment checks
compare resolved paths as text".
