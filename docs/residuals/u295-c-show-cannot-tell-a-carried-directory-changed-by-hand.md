---
title: crate schedule show cannot tell a carried directory changed by hand, and settles the agent's night against the shell's configuration
found: at the review of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** `read_agent` fails over a carried directory that is missing or relative and a log outside the carried state, but a directory changed by hand to another absolute one, a directory put in front of the agent's PATH, or the crate pointed at another executable named crate reads clean. `_night_line` reads the night's record from the agent's carried state and then settles it through `sync_night.settle` against the shell's configuration and run store.

**Measured cost.** Driven at round two: three hand edits of that shape read clean at exit 0. Install was driven under five environment shapes and none produces such a plist; a hand edit is the only producer found. The settle against the shell's configuration was read, not driven.

**Closes when:** show compares the carried environment against what this install would write, and settles the record against the configuration the agent carries.
