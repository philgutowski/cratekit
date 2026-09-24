# R-677 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/195` in the foreground under the Relay session's
rule. Every row names the same subset, the five test files that import the
landing verb or its engine, `tests/test_intake_land.py`,
`tests/test_landing.py`, `tests/test_landing_labels.py`,
`tests/test_intake_imported.py` and `tests/test_sync_mark.py`. Null control 0
of 10128, no collect drift, every restore verified against `git show HEAD`.

**`r677.md`**, 12 rows at `db458fc`. Six over the verb's new call site and
refusal path in `intake/land_cli.py`: the plan read asking nothing (the
original defect), the preflight asked of a plan of nothing, the refusal never
replacing the gate, the remedy condition dropped so any gate refusal gives
way, the refusal raised at once so a recorded abort cannot stand, and the
manifest's label rows withheld. Six over the engine's shared preflight in
`intake/landing.py`: the export asked before the library, and the library,
intake file and export checks each removed alone, plus two samples of the
existing guards now behind the shared call, `apply` skipping the preflight
and `apply` asking it with no label rows (R-455). 11 killed, 1 zero.

**`r677-b.md`**, 1 row at `c463f82`: V4 measured again after the test that
pins it. Killed, 1.

12 distinct mutations, 13 rows, under the cap of 25. Nothing was dropped.

## The one zero, and what closed it

`V4_remedy_condition_dropped` killed nothing on the full suite. Without the
condition, a stale answer resumed against an export that is not there is told
the export is unusable rather than that its answer is stale. Both refuse with
nothing moved, so the cost is which true thing a person is told first. It was
closed with a test rather than a composite, since a test was cheap:
`test_a_stale_answer_stays_stale_over_an_export_that_is_not_there` records an
answer against one export, resumes against an absent one, and reads
`decision-stale`. `r677-b` measures the row killing it.
