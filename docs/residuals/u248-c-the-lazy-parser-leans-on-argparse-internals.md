---
title: The lazy parser subclasses argparse's private subcommand action and reads its private listing
found: at the build of #677, U248, 2026-11-12.
issue: no
---

**The mechanism.** `_LazyChoices` in `src/cratekit/cli/__init__.py` subclasses
`argparse._SubParsersAction`, overrides `__call__` and `_get_subactions`, and
takes the listing line from `_choices_actions[-1]` after `add_parser`. None of
these is public. They hold on Python 3.12 and 3.13, which the parity tests in
`tests/test_cli_lazy.py` and the cold install in CI exercise, and the package
declares `<3.14`.

**Measured cost.** None today. A Python whose argparse renames or reshapes one
of them would fail the parity tests and CI's `crate --help`, not a user
silently, since the build fails loudly.

**Closes when:** the supported range widens past 3.13, at which point the
parity tests run on the new interpreter before it is allowed. Ledger only.
