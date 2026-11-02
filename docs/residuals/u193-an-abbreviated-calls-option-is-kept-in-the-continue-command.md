---
title: An abbreviated calls option is kept in the continue command beside the raised one
found: at the build of #464, U193, 2026-11-02.
issue: no
---

**The mechanism.** argparse accepts any unambiguous prefix of a long option, so
`crate --cal 600 ...` is read as `--calls 600`. The continue command the call
ceiling prints, `cli.continue_command`, takes out only `--calls N` and
`--calls=N` before it adds the raised `--calls`, so a command typed with the
prefix is given back carrying both, `--cal 600 --calls 1200`. argparse keeps
the last, so the printed command still runs with the raised ceiling.

**Measured cost.** Not driven past reading argparse's rule: one redundant
option in a printed command, which still continues the run. Nobody is told
anything false and nothing is lost.

**Closes when:** the continue command is built from the parsed options rather
than from the typed words, or the root parser sets `allow_abbrev=False`. Ledger
only.
