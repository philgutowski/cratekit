---
title: crate session ack --as session ignores the run it is resumed under and any inline answer beside it
found: at the review of #381, U184, 2026-11-01.
issue: no
---

**The mechanism.** The flag's road in `src/cratekit/session/cli.py`,
`_mint_as_session`, asks no gate, so it never reads the run record or the
inline decisions. Three command lines reach that, each driven at the review:
`crate --run RUN session ack --as session` on a run a plain `session ack` left
at its gate mints and saves RUN with its gate still open; the same on a run
where a person recorded `abort` mints beside the abort, so `run show RUN`
lists the abort next to a fresh acknowledgment; and an inline
`-d session.ack.backup=abort` (or any value, or an unknown gate) beside the
flag is ignored with no warning while the default road refuses every inline
answer to this explicit gate.

**Measured cost.** No data loss and no false report: in every case the mint is
the session's age rule over young backups, exactly what a plain
`crate session ack --as session` mints, and the recorded actor is derived. What
is left is one stale open gate that `run show` reports and `run retire` later
lists, and a run record that disagrees with the acknowledgment file about what
was decided. No document prescribes any of these command lines.

**Closes when:** the flag refuses alongside `--run` or any `-d` answer to its
own gate, or closes the resumed run's open gate when it mints. Ledger only: the
cost is none of METHOD's four board bar kinds.
