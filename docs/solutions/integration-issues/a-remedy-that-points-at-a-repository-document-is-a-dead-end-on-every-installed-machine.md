---
title: A remedy that points at a repository document is a dead end on every installed machine
date: 2026-09-21
category: integration-issues
module: "src/cratekit/cli/render.py, pyproject.toml, src/cratekit/skills/assets/first-run/SKILL.md"
problem_type: integration_issue
component: cli_render
root_cause: unverified_assumption
resolution_type: wording_fix
severity: medium
symptoms:
  - "A user facing remedy names a docs/ path that exists in the checkout and in no wheel"
  - "The test pinning the pointer passes, because it reads the path from the repository it runs in"
  - "The author cannot reproduce the dead end, because the author is always in a checkout"
applies_when:
  - "A remedy, refusal, step or check detail names a file by repository path"
  - "A procedure a person must perform is written down in docs/ and nowhere the package carries"
  - "A test asserts a pointer by reading the file from REPO_ROOT"
related_components:
  - "cli_render"
  - "packaging"
  - "skills"
tags:
  - "remedy"
  - "packaging"
  - "package-data"
  - "wheel"
  - "user-facing-strings"
  - "checkout-only"
---

# A remedy that points at a repository document is a dead end on every installed machine

## Context

U97 closed R-411, where the remedy for a missing provider session rendered as
the bare command `crate login`. That verb records a value somebody already
holds and cannot mint one, so a first run person who followed the product's own
remedy reached a second refusal. The fix moves the token to advice naming the
three acts, and the unit's brief decided the advice should point at
`docs/adapters.md`, which is where the minting command is actually written
down.

## What happened

The pointer was written, a test was added asserting that `docs/adapters.md`
exists and carries the recording command, and the test passed. The built in
review then raised that `docs/` ships in no wheel.

Driven rather than argued: a wheel was built from the tree into a temporary
directory and its entries listed. There is no `docs/` in it. `pyproject.toml`
package-data names `templates/*.toml`, `cratekit.skills` assets, and the
vendored licence. Nothing else.

So the pointer resolves for exactly one population, the people who have the
repository, and those are the people who did not need it. Every pipx installed
person is told to open a file that is not on their machine.

## Why the source does not explain it

The packaging boundary is invisible at the place the string is written. Nothing
in `cli/render.py` is near `pyproject.toml`, the repository is full of
docstrings citing `docs/` paths legitimately, since a docstring is read by
somebody holding the source, and the difference between a docstring citation
and a user facing string is a difference in who reads it, not in how it looks.

The test made it worse rather than better. A pointer test that reads the file
from `REPO_ROOT` asserts that the CHECKOUT has it, which is the one thing never
in doubt. It looks like a guard over the pointer and it is a guard over the
repository.

## The rule

**Before naming a file in a string a user reads, ask which artifact carries it.**
Three answers are fine and they are not interchangeable:

- The package carries it, which means package-data names it. The first run
  skill asset is the worked example: R7 put the skills INSIDE the importable
  tree for exactly this reason, and its comment says so.
- The string carries it. Say the thing rather than pointing at where the thing
  is written. U97's advice names all three acts, which is why the document
  pointer is a supplement and not the payload.
- The project carries it, in which case say so. "docs/adapters.md in the
  project's repository" is honest on both populations and reads as a reference
  rather than as an instruction to open a path.

What is never fine is a bare repository path in a remedy, because it reads as
the second option and behaves as the first.

## Where else this applies

Every user facing string, not only a remedy: refusal messages, a cause's steps,
a doctor check's detail. The sweep worth doing once is every literal containing
`docs/` reachable from a rendered surface. R-617 records that the guard does not
exist yet and what it would need, which is a definition of a user facing string
this repository has not written down.

## See also

- R-617, the ledger entry, with the wheel measurement.
- `pyproject.toml`'s package-data comment on `cratekit.skills`, which is the
  same lesson learned once already and written at the packaging end rather than
  at the authoring end.
