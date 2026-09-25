# Mutation notes: r706

Author's table, no independent verifier (METHOD, 2026-09-07). Seventeen rows
in three batches, `r706-a-rows.toml` on the bounds, `r706-b-rows.toml` on
the partition and the walk, `r706-c-rows.toml` on the verbs and the pipeline,
under the light pass cap of 25. Split three ways so each batch ran in the
foreground under the harness ceiling, which this Relay session required of
every command; part A took 10 pytest runs, part B 9 and part C 7, each a
full baseline, a null control on the full suite and one subset per row.

**MEASURED, every row killed.** `r706-a.md`, `r706-b.md`, `r706-c.md` and
their JSON sidecars carry the numbers, at heads `3ef09fa`, `43beab0` and
`33066ed` on `relay/218`, every restore verified against HEAD, 10,319
collected on every baseline and control, 284 on every acrcloud subset and 86
on the workers file. No zero row, so no composite was owed. One row was
considered and dropped, A8, and filed as R-712: the run guard counting the
whole part rather than the owed chunks is unobservable behind a partition
that never builds an oversize part, a guard covered by another guard.

## How the guard was watched, and what that narrows

The installed copy's `crate analyze vocals --recursive` job
`2026-09-24T21:04:27Z-fbe8`, the same job that halted the R-414 and R-705
tables, was still running over the whole library volume and writing analysis
artifacts under the real jobs directory throughout this session, read from
the process list before the first batch and not assumed. It is not this
session's to stop. All three batches were therefore run with
`CRATEKIT_CONFIG_DIR` and `CRATEKIT_STATE_DIR` pointed at a fresh empty
temporary directory each, which the driver documents as the override that
wins over the platform path. The guard watched those roots, empty before and
after every child. In place of the guard over the real directory, every file
in it outside `jobs/` was hashed before batch A and after batch C, 390
entries, and the digest was identical. That covers the configuration the
guard exists to protect. It does not cover `jobs/`, which the vocal job was
writing, so a child reaching the real job queue in this run would not have
been seen. The same arrangement was used on `relay/214` and `relay/217`.

## What the kills say

The ceiling is held from three sides: dropped outright (A1, 6 kills), one
part wider (A2, 4) and the constant moved (A3, 5), so neither the refusal
nor its number can drift. The month asked of one run's worth instead of the
whole set (A4) dies on exactly one test, the one written for it, because a
per part reading admits the first part of a set the month cannot afford;
that single kill is the reason the test exists. The per part run guard (A5)
dies on the two partition cases, an oversize first part and an oversize
last, the second added at the review because the guard had been asked inside
the spend loop.

The partition is pinned by its arithmetic: flooring the part count (B2, 8
kills) hands the run guard a 732 chunk part; dropping the remainder (B3, 5)
loses chunks the order test and the sitting's shape both see; front loading
the remainder (B1) dies once, on the parametrized partition test, because
for 401 over 400 both cuts give 201 and 200 and only the 5 over 2 and 7
over 3 cases tell them apart. Reporting one part (B4, 7), counting the
first part's chunks (B5, 6) and skipping the partition (B6, 7) all die
across both verbs and the identifier.

The verb side is thin by design and each of its four rows dies on one or
two tests: the note never said (C1), the split not frozen (C2) and the
summary ignoring the payload (C3) each die on the resume assertion the
review asked for, and the pipeline dropping the field (C4) dies on both
verbs' notes.

## What a green suite cannot see, hunted

Every assertion in the new tests was read for an expected value derived
from the code under test. One is: the ceiling refusal test takes its
`planned` from `acrcloud.planned_calls(9 * 3600.0)`, a pure function pinned
by its own parametrized test above it, and the same test pins `ceiling` as
the product of two constants, so the derivation is over pinned inputs and
not over the guard. No new test forbids a feature by naming an old symbol;
the U103 test renamed here names the property it now pins. No mapping
gained a key. `parts` means one thing in `Identified`, `IdentifyResult`,
the job payload and the envelope: the number of runs. `identify` had one
caller before this unit and has the same one after it, `bound_identifier`.
