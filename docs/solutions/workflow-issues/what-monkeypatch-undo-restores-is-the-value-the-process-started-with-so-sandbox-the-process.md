---
title: What monkeypatch.undo restores is the value the process started with, so sandbox the process
date: 2026-09-22
category: workflow-issues
module: scripts/mutate.py, tests/conftest.py
problem_type: workflow_issue
component: mutation_driver
severity: high
root_cause: reversible_isolation
resolution_type: guard
applies_when:
  - A child process runs the test suite and the suite isolates the real machine
    with monkeypatch, which any test can undo.
  - A real configuration or state directory was found holding test fixture
    values, and the full suite on the clean tree leaves it untouched.
  - A guard is being written for a driver whose children run a mutated tree.
  - A promoted row's only killer is the repository cleanliness test.
tags:
  - mutation-driver
  - test-isolation
  - monkeypatch-undo
  - r-343
  - r-661
  - state-leak
  - sandbox
---

# What `monkeypatch.undo()` restores is the value the process started with, so sandbox the process

## The symptom

On 2026-09-20 the live Cratekit configuration was overwritten with a test
fixture one. R-343 had predicted exactly that on 2026-09-16 and was filed
without a guard, because which mutant defeated the conftest's redirect could
not be established. The full suite on the clean tree leaves the real state
directory byte for byte unchanged, measured twice, six days apart. So the leak
needs a mutated tree, and only the mutation driver runs one.

## Where the cause actually was

Not in `config_dir()`, where R-343 looked. `tests/conftest.py` sets HOME, the
XDG variables and both Cratekit overrides with `monkeypatch`, and the
repository already recorded that `monkeypatch.undo()` inside a test reverts
the autouse isolation with everything else. Eleven live `undo()` calls sit in
the suite. What `undo()` restores is whatever the PROCESS started with. The
driver's child started with the real machine, so an undone test on a mutated
tree wrote where the mutation sent it, and the mutation sent it home.

The fix is therefore not to find the mutant. It is to make the process start
somewhere harmless: `run_pytest` hands every child a throwaway installation
state at process start, all eight variables inside the run's own workspace,
and an `undo()` now restores the sandbox. Measured before building: the full
suite under that environment is 9971 passed and 1 skipped, so nothing in the
suite depended on the real home.

## The guard beside it, and what it does not claim

A fingerprint of the real roots, taken after preflight and compared in a
`finally` around every child, stops the batch on any change and names the
child that was running. Three things the review found that a first draft gets
wrong:

- The check belongs in a `finally`. A child that leaks and then hangs leaves
  through `TimeoutExpired` first, the row loop files that as an ordinary error
  row, and the NEXT row's child is the one blamed.
- Files alone are not enough. A directory created inside the real root is a
  reach, and a same size rewrite inside one timestamp tick is invisible to a
  stat, so directories are entries and small files are hashed by content.
- Say what is watched. The sandbox redirects eight variables and the guard
  fingerprints two roots, so the table says the watched roots are unchanged,
  not that the installation state was guarded.

## The apparatus can lie, and this is what it looks like

The unit's first table reported four promoted rows killed, each by exactly one
test, the repository scan with identity checking on. The driver writes its
sidecar into `docs/mutation/` after the first row, and the sidecar carried the
guarded root under the home directory, which names the account. Every full
suite run after the first row failed on the driver's own artifact, and the null
control did not die because it runs before the sidecar exists. Across every
committed table, 11 of 37 promoted deaths are that test alone (R-661).

When a promoted row's killers are exactly one test and that test is a scan of
the tree, the row is a zero and the sidecar is the suspect. Anything the
driver writes into the tree has to pass the scan itself.

## How to tell the next one

A real directory holding fixture literals (`F1E2-D3C4`, `remote:mirror`, a
pytest temp path) with a single timestamp on the written files is one leaked
child, not a rolling leak. Fingerprint the directory, run the full suite on
the clean tree, and if the digest holds, look for a mutated tree and an
`undo()`, not for a resolver bug.
