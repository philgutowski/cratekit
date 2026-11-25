---
title: The answer lines a gate refusal prints name no actor and no digest, so an app answer finished by one is recorded as cli or session and bound to no screen
found: at the review of #1081, U962, 2026-11-25.
issue: no
---

**The mechanism.** U962 binds an answer as `app` to the digest its screen
showed: `run decide --actor app` on a gate that binds a plan is refused
without `--expect-digest`, and `decision-digest-mismatch`'s answer step names
the refused answer's actor and the flag. The other lines that tell a reader
how to answer do not: `gate-not-reached`'s last step (`then, once the run
shows GATE, answer it: crate run decide RUN GATE <option>`), the open and
stale gate screens' `answer:` line, and `run show`'s `answer` field all print
the bare decide, as they did before U962, for every actor. A caller that
follows one literally is recorded as `cli` at a terminal or `session` without
one, and its answer binds whatever plan the run offers then, the unbound
answer U962 exists to keep the app from giving.

**Measured cost.** Driven at round two of #1081: a `profile set` run reset to
before its gate by the suite's `_unreached` helper, `run decide RUN
profile.set.apply apply --actor app` refused as `gate-not-reached`, the run
continued as its first step says, then its last step run literally: exit 0,
recorded as `cli` with the offer's digest, never a screen the app showed. The
state was authored by a test helper; no producer of the app answering a plan
gate its run has not shown was driven, since the app answers the gate `run
show` shows, and the app (#1087) is unbuilt, so reachability is unmeasured. A
person typing the line at a terminal is truthfully `cli`, so nothing is
recorded falsely for anyone but the app.

**Closes when:** the menu bar app's gate view (#1087) builds every answer
from the waiting gate's `digest` with `--actor app --expect-digest`, never
from an `answer` line, with a test that it does, or the answer lines carry
the actor and the digest flag when the refused answer was bound. Ledger only.
