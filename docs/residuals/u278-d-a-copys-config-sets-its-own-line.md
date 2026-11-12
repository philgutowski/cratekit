---
title: The hour's window is one per account but its line is read from each process's own configuration
found: at the build of #741, U278, 2026-11-12.
issue: no
---

**The mechanism.** Every process counts into the one gate's window, and each
compares it with `[provider] calls_per_hour` and `reserve_share` off the
configuration it loaded. A copy run that redirects `CRATEKIT_CONFIG_DIR` to a
config with a higher budget spends further into the shared hour than the
live config allows, and the live run then meets a window past its own line.

**Measured cost.** Not driven. A copy's config is copied from the live one, so
the two agree unless someone edits the copy's provider section.

**Closes when:** the line a call is held to is written into the gate file by
the live configuration, or doctor names a difference between the two. Ledger
only.
