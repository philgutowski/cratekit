---
title: On the full organize, a set landing between the two acts still stales the account gate, since only the mirror's plan is frozen on the run
found: at the review of #328, R-1031, 2026-10-27.
issue: no
---

**The mechanism.** R-1031 freezes the account mirror's plan on the run that
shows the account gate, so the run that answers rebuilds the mirror from it and
its digest holds however the library moved. The account area's other steps are
planned again as before. The sets step reads the INSPIRATION names from the
rekordbox database (`organize/account.py`, `set_cli.inspiration_names`), so a
set landing between the two acts of a full `crate organize` can change that
step's digest and the area's, and the approved answer is refused
`decision-stale` exactly as before R-1031. `--only mirror`, the live use the
residual was measured on, is not affected.

**Measured cost.** Not driven. Fable read it from the source at the review of
R-1031, and drove the full verb only with a playlist made in a mirrored folder
between the acts, which holds. The cost when it happens is a second plan pass,
now cheap for the mirror since its links and misses are recorded by the first.

**Closes when:** a set landing between the two acts of a full organize is
driven, and either the sets step reads a frozen input too or the record shows
the stale refusal is the right answer for it. Ledger only: it was not driven,
and the cost is a replan, not a lost write.
