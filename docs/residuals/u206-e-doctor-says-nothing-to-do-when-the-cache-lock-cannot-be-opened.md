---
title: Doctor says a cache file that does not parse needs nothing done, also when the lock cannot be opened and no lookup will set it aside
found: at the second review of #496, U206, 2026-11-05.
issue: no
---

**The mechanism.** The `provider.isrc-cache` note in `src/cratekit/cli/doctor.py`
says of a cache file that does not parse that the next lookup sets it aside and
starts afresh, so there is nothing to do. The set aside needs the sibling lock.
When the lock file cannot be opened, `Cache._locked` yields not held, nothing is
set aside, and every lookup asks the provider while the note still says there
is nothing to do.

**Measured cost.** Driven with a hand made producer, a directory at the lock
path: three lookups asked three times and the note unchanged. The realistic
producer, a state directory this account cannot write, could not be driven on
a container that runs as root, so reachability is unmeasured. The cost is calls
and a note that reads clean over them, never data.

**Closes when:** the note asks whether the lock can be taken and, when it
cannot, says every lookup asks the provider until the folder is writable.
Ledger only.
