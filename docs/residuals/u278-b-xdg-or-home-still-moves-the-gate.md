---
title: A copy run that redirects XDG_STATE_HOME or HOME still gets a provider gate of its own
found: at the review of #741, U278, 2026-11-12.
issue: no
---

**The mechanism.** `config.provider_gate_dir` reads
`platformdirs.user_state_dir`, which honours `XDG_STATE_HOME`, and on macOS
too (platformdirs 4.14.5's `MacOS` takes XDG variables over its defaults),
and resolves under `HOME`. A copy run that redirects either, rather than
`CRATEKIT_STATE_DIR`, resolves a fresh gate and a fresh hour. The suite relies
on exactly this, through its own pointer as well.

**Measured cost.** Driven by the round one review: with `XDG_STATE_HOME` set
to a scratch folder the gate resolved under it. No documented procedure, skill
or solutions entry sets either variable for a copy run; reachability is
unmeasured. 1 candidate was driven (the mutation driver, which also sets the
gate's pointer) and it does not produce it.

**Closes when:** the gate resolves by the account's own identity rather than a
directory a process environment can move, or doctor names a gate outside the
platform default that no pointer explains. Ledger only, since no producer is
known.
