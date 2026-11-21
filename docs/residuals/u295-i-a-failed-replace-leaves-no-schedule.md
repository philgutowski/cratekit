---
title: A replace that fails at the load leaves no schedule rather than the earlier one
found: at the build of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** `crate schedule install` over an installed agent boots the earlier one out, writes the new plist and bootstraps it. When the bootstrap fails, the new plist is removed and nothing is installed; the earlier schedule is not restored. The refusal says the earlier schedule was removed too. Decided at the build as the conservative reading of the brief's "leaves no half installed agent".

**Measured cost.** Driven with launchd stood in: no agent afterwards, and the refusal says so. The person installs again.

**Closes when:** Phillip rules that a failed replace should restore the earlier agent, or the ledger keeps this as decided.
