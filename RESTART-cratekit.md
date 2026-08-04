# Restart: Cratekit parallel wave

**Session stopped 2026-08-04, out of weekly budget.** Seven parallel agents
were killed mid-flight by the API limit itself, not by any logical failure —
every one of them was actively working (mutation drivers running, files being
written) when the process was cut. Read this file first, before anything else,
when resuming.

## Do this first

1. Read `docs/wave-state-2026-08-04.md` in full. It is the durable record of
   every finding this session produced, kept current with `git push` after
   nearly every round. It is far more complete than this file — this file only
   exists to get you oriented fast.
2. Run the cleanup gate below.
3. Resume the seven fix/verify rounds that were in flight.

## Main, confirmed clean

`1943bf9`, pushed, clean working tree. **U32 is merged** — the first and only
unit landed this wave. Verify before trusting it stale:

    git log --oneline -1
    git status --porcelain            # must be empty
    .venv/bin/pytest --tb=no          # 3422 passed, 17 skipped, last verified
    .venv/bin/python scripts/board.py audit   # must be exit 0

## Cleanup gate — one worktree has uncommitted work, six do not

    u12   fc73b82   clean
    u16   3262bc8   clean
    u23   6f8db39   clean
    u24   52b5982   DIRTY — src/cratekit/core/tombstone.py modified, uncommitted
    u27   44ced7e   clean
    u34   85eb996   clean
    u38   171e058   clean

**u24's dirty file is real in-progress work, not garbage.** It is U24 fix
round 8, mid-implementation of the ISRC-folding fix (finding: `tombstone.fold`
does NFC + casefold + whitespace-collapse but not punctuation, so
`GBAYA1500001` and `GB-AYA-15-00001` read as two different recordings, which
permanently wedges the watermark — see wave-state doc, "F1 is the round" under
U24's most recent verification). Diff is 120 insertions / 10 deletions, one
file. Read the diff before deciding whether to finish it or discard it:

    git -C .worktrees/u24 diff src/cratekit/core/tombstone.py

Do not `git checkout --` it without reading it first — it may be substantially
done.

## The seven fix/verify rounds in flight when the session died

Every one of these was mid-round, not mid-review — i.e. the *previous* round
was verified BLOCKING and a fix agent (or in u24/u27/u34's case, possibly a
subsequent verifier) was actively working when killed. Check each worktree's
actual tip against the table above; if it advanced past what's listed in
`docs/wave-state-2026-08-04.md`'s last entry for that unit, a round completed
and just needs re-verification. If not, relaunch the fix round from the last
BLOCKING report (full reports are in the wave-state doc, in agent-output form,
one section per round).

| unit | last known action | what to check on resume |
|---|---|---|
| u12 | fix round 6 in flight (reap-budget determinism fix) | tip `fc73b82` — if this is new, round 6 landed; re-verify. Round 5 was verified BLOCKING for a coin-flip mutation row. |
| u16 | fix round 7 verification in flight | tip `3262bc8` is round 7's commit (confirmed landed pre-crash). **Needs verification**, not another fix round. |
| u23 | fix round 8 verification in flight | tip `6f8db39` is round 8's commit (landed). **Needs verification.** Round 8's R-33 residual (field-before-bytes collision) was the open question. |
| u24 | fix round 8 in flight, UNCOMMITTED | tip `52b5982` is round 7. Round 8 (ISRC punctuation fix) is sitting dirty in the worktree, unfinished. **Resume or restart this fix round.** |
| u27 | fix round 8 verification in flight | tip `44ced7e` is round 8's commit (landed, closed the `Finding`-classification channel). **Needs verification** — specifically the syscall-cost-of-constructor-I/O attack was queued. |
| u34 | fix round 9 verification in flight | tip `85eb996` is round 9's commit (landed — modeled the branch-rule path properly, rejected a flag-based fix with a mutation row proving why). **Needs verification.** |
| u38 | fix round 7 verification in flight | tip `171e058` is round 7's commit (landed — kept the resolver widening on an at-risk-population measurement, rebuilt the citation guard). **Needs verification.** |

**Pattern**: six of seven units have a landed, uncommitted-nothing fix round
sitting at a fresh tip that has not yet been adversarially verified. The
seventh (u24) has an unfinished fix round. The fastest path back to full speed
is: finish/restart u24's round 8, then fire six verification subagents in
parallel for u12/u16/u23/u27/u34/u38 (or five if u12's round 6 also isn't
done — check its tip against wave-state doc first).

## Standing rules this session established (all now in `docs/wave-state-2026-08-04.md`, keep following them)

- **Never pass `pytest -q`.** `pyproject.toml` sets `addopts = "-q"` already;
  a second `-q` becomes `-qq` and suppresses the summary line entirely. Use
  `pytest --tb=no`.
- **Mutation drivers run `PYTHONDONTWRITEBYTECODE=1`.** A stale `.pyc` from
  two same-length mutations written under a second apart can fabricate a
  result.
- **Read failing-test ids off a pytest plugin's `report.nodeid`.** Splitting
  the `FAILED` line on `" - "` breaks on parametrized ids that contain that
  substring.
- **Mutate a message by rewording, never appending.** The suite asserts with
  `in`, so an appended mutation measures zero for a reason unrelated to
  coverage.
- **A row on a timing-dependent assertion needs a repeat count and pass rate,
  never a single run.**
- **Mutation tables live in the repository**, not in chat — `docs/mutation-*`
  files per unit, or the shared `docs/mutation-rows.md` seeded from `main`.
- **Residual citations are by title, not number** — six numbers collide with
  different content across branches (R-17, R-19, R-20, R-21, R-22, R-23).
  Several units now have tests enforcing this.
- **Check `git log origin/main..main` before every push**, not just before
  one you think is a merge — a docs commit landed on top of an unpushed merge
  once and the push carried both.
- **Merge exit criterion is CLEAN**, not zero-blocking-with-residuals. Only
  U32 has cleared it so far.

## The four recurring defect patterns (for framing new findings)

1. Absence read as evidence of absence
2. Identity that is not unique to the thing it identifies
3. A fix that lands on the wrong object (correct in isolation, hole still open)
4. A claim justified by a fixture, a written explanation, or a measurement
   taken in the direction that cannot fail

Full detail, every round's findings, and the two agents that measured their
own instrument's failure modes are all in `docs/wave-state-2026-08-04.md` —
read it before doing anything else.
