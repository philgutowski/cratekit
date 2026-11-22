---
title: The scheduled night pass runs from the development checkout, so a pull during it ends it mid run with its downloads stranded in staging
found: at sitting 103, 2026-11-22, the attended session.
issue: no
---

**The mechanism.** `crate schedule install`, run from the development
checkout at sitting 102, wrote that checkout's `.venv/bin/crate` into the
launchd job, whose editable install reads the working tree. The night of
2026-11-21 ran from 15:38Z to 15:44Z on the 22nd. The checkout was fast
forwarded at 15:40:40Z across U298, and the run ended `internal-error`,
`ImportError: cannot import name 'load_config' from
'cratekit.cli.output'`, when it next imported lazily.

**Measured cost.** The download had succeeded, 32 of 32 settled with one
skipped. The pass never reached its tail or its gate, and `sync night`'s
record names no pass run, no staging and no gate, so its files sit in
download staging with no command naming them. The installed copy, 0.18.0,
has no `sync night`.

**Closes when:** the schedule names an installed copy rather than a
checkout, or a night that dies after its download records the pass run a
`crate sync land --pass-run` continues.
