---
title: The held plans directory, when it cannot be listed, reads as holding no run's steps and nothing is named
found: at the review of #591, R-1372, round two, 2026-11-06.
issue: no
---

**The mechanism.** `core/held_plan.recorded_steps` and `prune` list with `Path.glob`, which on Python 3.12 swallows an `OSError` and answers an unlistable directory as an empty one, so their `except OSError` branches cannot be reached. R-1372's round one found the same in `carried()` and fixed that instance by listing with `iterdir`; the two listings one function over keep the shape. A held plans directory that cannot be listed reads as no run's steps, and a stop recorded only there is not looked for, with nothing said.

**Measured cost.** Driven by the round two reviewer: the directory replaced by a regular file after a stop. `recorded_steps` answered no steps and no problem, `carried()` named its own listing, and the verb then stopped at `gate-sibling-run` and wrote nothing. The shape that would write, a directory that can be written and not listed, cannot be produced as root in the container; its cost is unmeasured.

**Closes when:** both listings use `iterdir` and name an `OSError` other than a missing directory, as `carried()` does.
