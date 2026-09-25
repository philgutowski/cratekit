# R-414 mutation table, read

One table, the author's and not independent, measured by `scripts/mutate.py`
on `relay/214` at `8970e25`. Fourteen rows, thirteen over `write/metadata.py`
and one over `core/cause.py`, under the light cap of 25. Null control 0 of
10,299, no collect drift, every restore verified against `git show HEAD`.
**All fourteen killed.** No row was dropped.

## What the environment narrowed

**The leak guard watched an empty temporary root, not the real one.** The
installed copy's `analyze vocals` job `2026-09-24T21:04:27Z-fbe8`, started
attended at 21:04 UTC over the whole library volume, was still writing
analysis artifacts into the real installation state directory throughout this
session, and the first attempt stopped on the guard with 11,213 entries grown
to 11,251. The driver was therefore run with `CRATEKIT_STATE_DIR` and
`CRATEKIT_CONFIG_DIR` pointed at a path that does not exist, which the
driver's own docstring describes as how the guard is exercised from the
suite. Every child still ran inside the driver's `SANDBOXED_ENV`, which does
not depend on that override. In place of the guard, every file in the real
directory outside `jobs/` was hashed before and after each attempt, 396
entries, and the digest was identical across all four attempts. That covers
the configuration the guard exists to protect. It does not cover `jobs/`,
which the vocal job was writing, so a child reaching the real job queue in
this run would not have been seen. The same arrangement was used on
`relay/217`, see `r705-notes.md`.

**Two of four attempts refused a red baseline** on
`tests/test_provider_gate.py::test_two_processes_never_call_at_once_and_keep_the_interval`,
with the load average at 11.5 on 11 cores. It passed five of five times run
alone, passed in this branch's own full suite, and passed in the first and
fourth driver baselines. Filed as R-711. Neither refusal is a defect in this
branch: the test touches no module this branch changes.

## What the kills say

The fold is held from both ends. The planner writing the byte (M1, 3 kills)
and the fold returning its input (M2, 4) are R-414 itself, and both die on the
star pin and on the shipped curve test. The byte table is pinned per value
(M11, 204 folding to three, 3 kills), because the shipped curve test derives
each expected star from the template's own byte.

The three refusal layers each die alone. A value on neither scale (M3, 5), a
curve mixing the two (M6, 1), and the nearby weakening of the mix check to
two star values (M7, 1). The up front fold (M8, 5) dies on the parametrized
refusal test, whose row lands in the GOOD cut, so a lazy check that refused
only the rows in a bad cut would plan the rest.

The two pass throughs die separately: stars (M4, 2) and zero (M5, 1), and the
zero band's skip dies on both its presence (M9, 1) and its reason (M10, 1).
The refusal's detail key (M12, 5) and remedy token (M13, 5) are pinned, the
remedy by an assertion added before the table ran rather than argued after
it. Unregistering the reason (M14, 6) dies on every refusal test, since
`refuse` will not build a cause for an undeclared slug.

The single kill rows, M5 to M7, M9 and M10, each have exactly one test
standing behind them. That is a thin wall, not a zero.
