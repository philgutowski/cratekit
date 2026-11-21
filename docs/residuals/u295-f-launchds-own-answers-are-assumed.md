---
title: The schedule assumes launchctl's answers, and none has been read on a Mac
found: at the record of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** `src/cratekit/cli/schedule.py` reads `launchctl print gui/<uid>/cratekit.sync-night` answering 113 as not loaded and anything else but 0 as unknown, bootstraps straight after a bootout, and expects `gui/<uid>` to exist for the logged in person. The suite stands launchd in whole and the container has no launchctl.

**Measured cost.** Not driven anywhere. If print answers another code for an absent service, every show reads launchd as unknown and every install refuses at its first bootout; the refusal names launchctl's words, so nothing is lost.

**Closes when:** the attended install (A183, #879) records each answer launchctl gave, and the code reads them as they are.
