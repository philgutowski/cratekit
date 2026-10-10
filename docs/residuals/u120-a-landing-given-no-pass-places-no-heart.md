---
title: A landing given no pass places no heart, and a landing on the bridge places none
found: at the build of #277, U120, 2026-10-10.
issue: no
---

**The mechanism.** The native landing knows a file is a heart only through the
pass's hearts job: `account_playlists.hearted` reads `batch_name.pass_jobs` for
the pass given with `--pass`, keeps the hearts job among them, and ties its
carried rows to the planned files by the match rule. A landing run with no
pass, as `crate intake playlist favorites` followed by `crate acquire download`
and `crate intake land --name` is, has no job to read, so its files land as any
other and no heart is placed. The bridge medium writes an export and places
nothing on either path. The three September hearts landed exactly this way,
which is why the backfill exists.

**Measured cost.** On the live library every heart that landed before U120,
and any that lands by hand after it, sits in INBOX until `crate favorites
backfill` is run. The backfill finds them all, so the cost is one attended
run, not a lost heart.

**Closes when:** the landing resolves its files against every hearts job on
the library rather than the pass's, which is wrong while the open question
about owned hearts stands, since an old hearts job carried every heart the
library then lacked; or `crate intake land` grows a `--hearts` flag naming a
job. Ledger only until the author answers the question.
