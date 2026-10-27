# Release pipeline: pull requests per unit, releases on request

Brainstormed with Phillip on 2026-10-27, in the attended cloud session that
set up the cloud lane. Read for reasoning; the cards are the brief.

## Idea

One clear path from a card to code that is safe to install. Where work lands,
when a pull request is used, and what makes a release, now that cloud sessions
build and merge every card.

## Who it is for

Phillip, rebuilding his installed copy at sittings, and the handful of DJs the
tool is shared with, who should never install a commit nobody chose to ship.

## What exists today

- Every unit merges straight to `main`, with no pull request, the cloud's
  included.
- No tags, no GitHub releases, and the version has been 0.1.0 since the start.
- Installs are `pipx install .` from a clone; the installed copy is rebuilt by
  hand at sittings from whatever commit `main` is at.
- CI checks packaging, portability, the repo scan and the closing check on
  every push; it does not run the suite.
- Branch protection is not available on this private repository's plan, so a
  gate is the workflow's to enforce, not GitHub's.

## Decisions

| question | answer |
|---|---|
| What do people install? | Tagged releases only, never raw `main`. |
| What gates a release? | The cloud's Linux battery. No Mac step; regressions only a Mac would catch, in the doctor, backup and restore tests above all (R-1041), are the accepted cost. |
| Does a unit reach `main` through a pull request? | Yes, one per unit, merged by the worker itself once CI is green, with no wait on Phillip. |
| When is a release cut? | Only when Phillip asks, in any session. |
| How are versions numbered? | Semantic versions, the bump judged by the session cutting the release: patch for fixes, minor for new verbs or behaviour, major for a change that breaks existing libraries or configs. |
| How does an install learn of a release? | `crate doctor` warns when the installed copy is older than the latest release and prints the one pipx command that upgrades it. Nothing upgrades by itself. |

## Chosen approach: session-gated pull requests

The worker builds on `cloud/N-slug` and runs the Linux battery in its own
container, as it does now. Instead of merging locally it pushes the branch and
opens a pull request whose body carries the brief's link, the battery result
(`cloud_battery.py compare` output), the Fable review rounds and the mutation
table. It waits for the existing CI checks on the pull request, then merges
through the GitHub API with a merge commit whose message ends with the closing
trailer, numbers the residuals on `main` as before, and posts `Landed`.

A release is cut by a script and a skill when Phillip asks: it reads the
merged pull requests since the last tag, judges the bump, writes the version
into `pyproject.toml` and `src/cratekit/__init__.py`, tags `vX.Y.Z`, and
publishes a GitHub release whose notes list the pull requests and carry the
upgrade command. Installs move from `pipx install .` to installing a tag
straight from GitHub, and `crate doctor` compares the installed version with
the latest release tag.

## Approaches considered

- **CI-gated pull requests.** CI would also run the Linux battery on every
  pull request against its base, so the worker could not skip the gate. Not
  chosen: roughly forty Actions minutes per pull request on a two core runner
  and a free plan's monthly allowance, against METHOD's rule that the battery,
  not CI, is the merge gate. It can be added later if a worker's own report
  is ever shown wrong.
- **GitHub merges and releases.** An Action would merge green pull requests and
  cut releases. Not chosen: GitHub does not fire other workflows for changes
  made with its built in token, so an issue closed by such a merge would never
  trigger the board workflow, and the board would stop cascading silently
  unless the Action merged with the board token.

## Out of scope

- A Mac in the release path.
- Required reviews or branch protection, which the plan does not offer.
- Publishing to PyPI or any index; the tool stays private.
- Automatic upgrades on any machine.

## Open questions

- Whether `crate doctor` can read the latest release for a friend whose
  machine has no GitHub credentials for this private repository. The check
  must then say it could not read the releases, never that the copy is
  current.
- Whether the merge through the API is permitted from a cloud session on a
  pull request the session opened, which the first unit proves.
