# R-662 mutation notes

**Verdict: measured, 22 rows in two batches, every user facing row killed or
held by a killed composite, one maintainer facing zero.** Written on
`relay/211`, 2026-09-25, by the author, so a kill here is the author's and a
zero is one the author could not kill.

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| `r662-a` | 9 | 6 | 3 |
| `r662-b` | 13 | 11 | 2 |

## What the rows cover

- **M1 to M5, the shared rule in `core/config.py`.**
  `backup_remote_disagreement`'s several-remotes return, its name comparison,
  its blank remote return, the validator's use of it, and the flag named in
  the validator's problem text.
- **M6 to M12 and M17, M18, the repair in `cli/setup.py`.** The flag recorded,
  the three guards on `_replace_a_remote_rclone_lacks` (an unreadable
  configuration, a spelled remote rclone knows, a destinations' remote rclone
  lacks), the absent binary short circuit, the note, the write, and the call
  site's two branches.
- **M13 to M16, the refusal and the parser.** The fix line reverted to
  `crate setup`, the token kept beside other problems, the advice naming the
  destinations' remote, and the flag declared.

## The zeros

- **M1 and M3, killed in `r662-b` as M1b and M3b.** Nothing compared a
  spelled remote against destinations naming several remotes, or read a blank
  spelled remote. `test_no_disagreement_is_read_where_there_is_nothing_to_compare`
  does both, and each row kills 1.
- **M7, user facing, held by `M7_composite_with_M9` in `r662-b`, 3 kills.**
  An unreadable configuration read as an empty one is then stopped by M9's
  guard, since an empty dump lacks the destinations' remote too. The
  composite removes both. The pairing is recorded here because `pairs_with` is
  same batch only.
- **M10, user facing, held by `M10_composite_with_M9`, 2 kills.** A missing
  binary asked anyway reaches the green machine's empty dump, which M9's guard
  stops for the same reason.
- **M17, maintainer facing, one line.** Running the repair after an explicit
  flag changes an outcome only when the flag names a remote rclone lacks and
  the destinations name one it has: the mutant overrides the flag with the
  destinations' name, the real code keeps the explicit answer for validation
  to refuse, and no test gives such a flag.

## The leak guard

Both batches ran with `CRATEKIT_STATE_DIR` and `CRATEKIT_CONFIG_DIR` pointed
at empty temporary roots under `/tmp`, listed empty after each run and removed
with `rmdir`.
