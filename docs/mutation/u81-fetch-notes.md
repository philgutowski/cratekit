# U81 mutation notes, the fallback fetch

The author's table, 25 rows at the cap across two batches, `u81-fetch-a.md` (12
rows) and `u81-fetch-b.md` (13 rows). Every zero below reads as "the author
could not kill it", which is METHOD's standing caveat on a table nobody
independent ran.

THE FILES WERE RENAMED AFTER THE RUN. The driver wrote them as `u81-a` and
`u81-b`, and the `u81` prefix was already taken: `u81.md`, `u81-round-2.md`,
`u81-round-3.md` and `u81-notes.md` are R-322's table, from a Relay task that
happened to carry the number 81. The files were moved to `u81-fetch-*` and the
name string inside each was changed to match, and nothing else in them was
touched, so the rows and counts are the driver's own.

Both batches ran in the FOREGROUND, against METHOD's tracked background rule,
because an unattended Relay session exits when its turn ends and takes every
background task with it. Each batch was sized to finish well inside the 600
second tool ceiling, and `git status` after each showed only the new table
files, so no mutation was left in the source.

## Summary

| Row | Batch | Kills | Surface | What became of it |
|---|---|---|---|---|
| W1 to W12, bar W2 and W4 | a | 1 to 4 each | user | killed |
| W2_scheme_half | a | 0 | user | two addresses with a host and a non web scheme joined the test, re-run in b as W2_scheme_half_rerun: 2 kills |
| W4_empty_stem | a | 0 | user | a test queues a nameless row by hand, re-run in b as W4_empty_stem_rerun: 1 kill |
| Q1, Q3 to Q5, Y1 to Y3, L1, L2, S1 | b | 1 to 6 each | user | killed |
| Q2_state_not_checked | b | 0 | user | fixed by removing the covering half, NOT re-measured, see below |

## Q2, the one zero left

`accepted_rows` checked two things, that the answer was accepted and that it
named an upload. Removing the state half killed nothing, because
`fallback.settled` names an upload on an accepted answer and on no other, so
the URL half refused every waiting, rejected or stalled row by itself. Two
layers, each covering the other, is METHOD's "a guard covered by another guard
is a guard nothing covers".

The fix removes the URL half, so the state check is the one guard and
`test_nothing_accepted_queues_nothing_and_says_so` (a waiting row and a
rejected row) is what it answers to. An accepted answer naming no upload,
which `settled` cannot return, would freeze an empty address and the worker's
web address refusal would fail the item as `unavailable-permanent` without a
download. The cap was spent, so the kill after the fix was not measured by the
driver, and this line says so rather than claiming it.

## Dropped

Five considered rows are logged in `u81-fetch-b-rows.toml` under `[[dropped]]`
with the reason each ranked below the cap. D3, the URL half of the accepted
check, no longer exists after the Q2 fix.
