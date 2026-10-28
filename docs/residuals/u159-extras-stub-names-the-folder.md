---
title: The missing extra stub still prints a folder install command on a release install
found: at the build of #340, U159, 2026-10-28.
issue: no
---

**The mechanism.** A module switched on without its extra attaches a stub
that prints `pipx install --force '.[analysis,vocals]'`
(`extras.install_command`), pointed at the folder a person installed from.
Since U159 the README installs a release tag from GitHub, so a person who
followed it has no folder, and the command the stub prints installs nothing
from where they stand.

**Measured cost.** Not driven. Read from `tests/test_install_command.py`,
which pins the folder form. The person's way out is the README's own extras
command with the tag, which the stub does not print.

**Closes when:** the stub reads the install origin doctor's `install.release`
check reads (`doctor._install_origin`) and prints the release form,
`"cratekit[...] @ git+<url>@<tag>"`, for a release install. Ledger only.
