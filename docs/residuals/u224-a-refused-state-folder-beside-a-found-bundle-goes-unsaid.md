---
title: crate doctor's deadca7.push check leaves out a DEADCA7 state folder it could not read when it found the app's bundle
found: at the review of #576, U224, 2026-11-06.
issue: no
---

**The mechanism.** `_deadca7_presence` in `src/cratekit/cli/doctor.py` gathers every install place it could not stat into its unread list, and `_check_deadca7_push` says that list only when nothing was found or the support folder itself was unread. With `DEADCA7.app` present and the `deadcatalog` state folder refused, the detail reads "installed here and has recorded no push ... is here, and no push backup folder is", and the refused folder is never named, though `docs/GUIDE.md` now says a folder doctor cannot read is said as unread.

**Measured cost.** Driven by the round one review in process, with the real `Probes`, a scratch home and `os.stat` refused under the state folder: the reading is true, since the bundle alone proves the install and the push backups are not under the state folder, so the cost is an unsaid refusal, not a false sentence. No producer of a state folder closed to its own account was driven.

**Closes when:** the detail names every place it could not read in each reading, or the GUIDE line is narrowed to the readings that turn on the unread place. Ledger only.
