# U71 mutation notes

**Verdict: 25 rows over the landing engine's new guards, all 25 killing after
one test was strengthened.** This is the author's table, not an independent one,
so a row reads as "the author could kill it" and nothing stronger.

| Table | Rows | Killing | Zero |
|---|---|---|---|
| `u71.md` | 12, listing, fingerprint, batch name, root, ownership | 12 | 0 |
| `u71-b.md` | 13, device, export, placement, occupied, cleanup | 12 | 1, B9 |
| `u71-c.md` | 1, B9 measured again after the test change | 1 | 0 |

The table is split in three because one driver run of 25 rows can pass the
harness's 600 second ceiling, and a run killed mid row leaves its mutation in the
source. Each part ran in the foreground, waited on, and `git status` showed
`src/cratekit/intake/landing.py` clean after each.

## B9, the zero, and what closed it

B9 drops the refusal that runs before the batch folder is made when no file can
move. With it gone, the batch folder is made, the loop moves nothing, and the
refusal after the loop takes the batch folder back. So the error, the reason and
the batch folder all come out the same. The one difference is the `Music` folder
itself, which `mkdir(parents=True)` makes and nothing takes back. Before the
change, `test_a_batch_where_nothing_lands_leaves_no_batch_folder` asserted only
the batch folder. It now asserts that the music folder was never made either,
and `u71-c.md` measures the same mutation killing 1.

## Dropped below the cap

Five guards, listed in `u71-rows.toml` under `[[dropped]]`, each with its reason.
Two are reason slugs already asserted by name in a test. One is the symlink
halves, since `acquire download` never commits a symlink. One is the device
probe answering None, which needs no ancestor up to `/` to be stat'able. One is
the batch name recheck in `apply`, which only a hand built `Plan` reaches.

## A red baseline that was not this branch

The first attempt at `u71-c` refused with a red baseline:
`tests/test_write_session.py::test_the_latch_refuses_a_record_this_build_cannot_read`
failed once under the parallel full suite. Alone it passed three times out of
three, and its file passed whole at 77 of 77. The rerun's baseline was green.
The branch touches no file that test imports. The failure is recorded here
because it happened. It was one failure across this session's full runs, the
battery's and the driver's baselines, and that is not a measured rate.
