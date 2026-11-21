---
title: crate schedule install and remove hold the staging lock of the shell's installation, not the one the agent carries
found: at the review of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** `install` and `remove` in `src/cratekit/cli/schedule.py` hold `staging_lock.held` around their bootout so a night pass in progress is never ended by launchd. The lock is resolved under the shell's `installation_state_dir()`. A shell pointed at another `CRATEKIT_STATE_DIR`, or one that lost the XDG variable the install was found through, holds another lock, and boots the agent out while the night it runs holds its own. The lock is reentrant per process through module state, so holding a second one under the agent's carried state is not a one line change.

**Measured cost.** Driven at round two with launchd stood in: four of four cases exit 0 and call `launchctl bootout` while a process held the agent's lock as `crate sync night`. What launchd then does to the running pass, and what a pass ended mid download leaves in the staging folder, was not driven.

**Closes when:** install and remove also hold, or refuse beside, the lock under the state directory the installed agent carries.
