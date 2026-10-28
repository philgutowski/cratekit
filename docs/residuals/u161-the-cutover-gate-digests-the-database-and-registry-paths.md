---
title: The cutover and revert gates digest file paths, so no copy rehearsal of either can match the live one
found: at the build and review of #342, U161, 2026-10-28.
issue: no
---

**The mechanism.** `tree cutover` builds its one item in
`src/cratekit/cli/cutover.py` with `"registry": str(tree_registry.path_for(cfg))`
and `"database": str(rb_writer.live_db_path(cfg))`, and `_digested` digests the
whole item; `tree revert` digests the registry's path the same way. A
rehearsal reads a database copy at another path and a registry
under a redirected state directory by design, so its digest differs from the
live one even when the tree, the root, the source, the export and the precheck
are identical. This is the shape R-922 named for the native landing, which
U161 closed there by taking the path out of the digest, leaving it on the
screen and pinning it on the run; sitting 31 recorded it for the cutover. Left alone here because the
card's scope was the native landing.

**Measured cost.** Not driven on this card. By the shape alone, a session that
rehearses a cutover can never meet the equal digest rule, so each cutover goes
to its digest comparison by reading two screens; cutovers are rare and
attended, so the cost is a reading at a sitting, not a wrong write.

**Closes when:** each item digests the library by an identity two
copies share (the device and master id, or the root row) and shows its paths
outside the digest, pinned on the run the way U161 pins the native write's
file, and a copy rehearsal of a cutover or a revert matches the live plan.
Ledger only: it closes at an attended sitting and costs latency, not
correctness.
