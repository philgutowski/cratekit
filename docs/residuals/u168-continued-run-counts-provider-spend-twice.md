---
title: A continued run reports its provider spend twice, and a recorded line that no longer parses prints usage on stderr
found: in Fable's review of #349, U168, 2026-10-31.
issue: no
---

**The mechanism.** `run decide --continue` dispatches the owning verb inside
the outer `_dispatched`, and both add the provider spend counted since their
own start, so calls the continued verb spends reach the envelope as two
identical `provider-spend` warnings. Separately, `cli.dispatch` turns a
recorded command line argparse refuses into `internal-error`, and argparse has
already written its usage text to the real stderr by then; stdout stays one
JSON object.

**Measured cost.** Fable drove both with synthetic inputs: a two call bump
inside the inner dispatch, and a recorded line edited to carry an unknown
flag. No landed verb both opens a gate and reaches the provider gate directly,
and no landed path writes a command line that fails to parse, so neither has a
measured producer today. The cost when one appears is a doubled count on the
screen, or a line of noise above a correct refusal.

**Closes when:** a gated verb reaches the provider in the same process, at
which point the outer dispatch should skip its spend line for a continued run.
Ledger only.
