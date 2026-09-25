# R-663 mutation notes

**Verdict: measured, 15 rows in two batches, every row killed but one
maintainer facing zero.** Written on `relay/210`, 2026-09-25, by the author,
so a kill here is the author's and a zero is one the author could not kill.

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| `r663-a` | 14 | 12 | 2 |
| `r663-b` | 1 | 1 | 0 |

## What the rows cover

- **M1 to M10, the copy's classification in `core/rb_writer.py`.** The size
  asked before the open, the canary reason gate, a listing that failed kept
  apart from an empty one, one canary table enough to be drift, the listing's
  failure answer, the listing asking the header for the key, the size, the
  configured path and the remedy in the refusal, and the size in its detail.
- **M11 to M14, setup's step in `cli/setup.py`.** The step called before the
  save, its reason gate, and its two early returns.

## The zeros

- **M2, user facing, killed in `r663-b`.** Removing the canary reason gate
  killed nothing in batch a, since no test put a foreign file behind a
  refusal raised before the canary. `test_a_refusal_on_the_way_in_is_not_
  reclassified_as_a_wrong_path` does, with the binding pin, and M2 alone in
  batch b kills 1.
- **M14, maintainer facing, one line.** Setup's missing file return saves a
  copy that would fail anyway: without it the copy raises `OSError` on the
  missing file, which the step already swallows, so the outcome is the same.

## The leak guard

Both batches ran with `CRATEKIT_STATE_DIR` and `CRATEKIT_CONFIG_DIR` pointed
at empty temporary roots, removed afterwards with `rmdir`, so they held
nothing. The first run of batch b refused on a red baseline, one failure in
`tests/test_provider_gate.py::test_two_processes_never_call_at_once_and_keep_the_interval`,
a timing test in a module this branch does not touch; it passed three of
three alone, and the rerun's baseline was green.
