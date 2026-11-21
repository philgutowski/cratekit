---
title: A file moved away and back with the same size and time while a backup ran is trusted by the next run though the remote may lack it
found: at the build of #877, U317, 2026-11-21.
issue: no
---

**The mechanism.** `backup_record.settled` trusts an entry when the walk before
the transfer and the walk after it agree. A file moved out of the library and
back while rclone ran, keeping its size and time (a move keeps both), agrees in
both walks, yet the transfer may have missed it: a quick run's copy exits 0
over a listed path that is not there, and a full sync deletes it from the
mirror. The next quick run then compares it as unchanged and skips it, and the
remote lacks it until the weekly full check sends it again.

**Measured cost.** Not driven. It needs a move out and back inside one run's
transfer, which no verb does; organize moves files to new paths, which both
walks see.

**Closes when:** a quick run reads rclone's per path log for the listed paths
it did not transfer or find current, or the next full check, which closes each
instance within a week. Ledger only.
