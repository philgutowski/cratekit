# U127 mutation notes

The author's table, not an independent one: every zero below reads as "the
author could not kill it".

Batch A, `u127.md`: 24 rows over the new guards in `native.py`, `land_cli.py`,
`file_cli.py` and `rb_writer.py`, every one user facing. 22 killed, 2 zero.

- `N6_digest_blind_to_vox`, zero on the full suite. The verb level rescore test
  also changes the file, whose fingerprint is in the landing's own digest, so
  the rows' score and answer were redundant there. They are not redundant at
  the engine, whose digest `intake file` and any later caller take without a
  file fingerprint, so `test_the_engine_digest_covers_each_rows_score_and_answer`
  pins it. Batch B, `u127-b.md`, re-measured it as `N6b_digest_blind_to_vox`:
  killed, 1.
- `N13_unscored_while_blocked`, zero on the full suite. Every caller of
  `NativePlan.vox_unscored` checks `vox_blocked` first (the screen line, the
  items, the warnings), so the guard is shadowed on every user facing path
  and the mutation changes nothing a person reads. The plan's own contract is
  now pinned by `test_a_blocked_plan_names_no_file_unscored`. NOT RE-MEASURED:
  batch B's one row was the 25th, the cap. The rerun is
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/u127-rows.toml --resume`
  after editing N13 alone back in.

Dropped below the cap: the marker filter inside adoption's reader, which
U127 calls and does not own, and the record's early return in
`_record_landing_commit`, whose tag branch only runs once a row was added.
