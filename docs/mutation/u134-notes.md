# U134 mutation tables, read

The author's tables, not independent, driven by `scripts/mutate.py` on
`relay/307` at `c11ec06c`. Two batches were written, 20 rows in all under the
cap of 25, with two more considered and logged as dropped in the rows files.

**Four rows measured, sixteen owed.** `u134-a.json` holds what the driver
measured before it stopped: a green full baseline of 13,735 collected, the
null control at 0 on the full suite, no collect drift, every restore verified
against `git show HEAD`.

| Row | Guard reverted | Deaths | Killed by |
|---|---|---|---|
| A1_outside_inbox | the refusal of a recorded mirror live outside INBOX | 1 of 19 | `test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_before_any_report_is_read` |
| A2_mirror_is_first | the oldest recorded entry of the pass as the mirror | 1 of 19 | `test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror` |
| A3_gone_listed | a gone mirror listed rather than replaced by a name | 1 of 19 | `test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed` |
| A4_others_excluded | the name match skipping another pass's playlist | 1 of 19 | `test_the_name_is_not_asked_of_a_playlist_a_record_gives_another_pass` |

**Why the rest is owed.** Three Relay lanes and the watcher were running on the
machine. The driver's leak guard stopped batch a three times, each a new entry
in the real installation state while a child ran: once a lane's run record,
once a `crate doctor` run record written by another session, while the U133
and U135 lanes ran their own drivers in their worktrees. The guard cannot tell
those from a child of its own, and it is right to stop. The harness also killed
one attempt at its background limit mid row, leaving the A5 mutation in
`refill.py`; it was restored from `git show HEAD` and verified byte equal
before anything else ran.

**Rerun, with nothing else using the installation state:**

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/u134-a-rows.toml --name u134-a --resume
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/u134-b-rows.toml --name u134-b

`--resume` reuses the four rows above by fingerprint. Batch b holds two
composite pairs, B1 with B1c and B2 with B2c, because the read back's two
guards are expected zeros: no test makes the commit lose or reorder a
membership, so what each holds is shown by a mutation of the write itself.
