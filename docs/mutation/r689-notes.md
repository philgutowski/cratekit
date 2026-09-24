# Mutation notes: r689

Author's table, no independent verifier (METHOD, 2026-09-07). Twelve rows in
`r689-rows.toml`, under the cap, over the three files the unit touched: seven
on doctor's origin verdict in `cli/doctor.py`, two on setup's record write in
`cli/setup.py`, three on the digest, the fingerprint and the record parser in
`core/taxonomy.py`. Light pass, because the unit writes one small record
beside a copy setup already wrote, and doctor reports and never writes.

**NOT MEASURED.** There is no `r689.md` or JSON sidecar, because the driver
never got past its full baseline. Every row is unmeasured, so the table says
nothing about kills. The full suite was green at the branch head, the touched
suites were run after every edit, and each row below names the test written
to kill it.

Why: the same `crate analyze vocals --recursive` job over the whole DJ
library that halted R-693's table, `2026-09-24T21:04:27Z-fbe8`, started from
another session against the installed copy, was still running for the whole
of this session. It writes one analysis artifact per track under the
application support directory, so the watched root grew from 6,113 to 6,133
entries while the baseline ran and the driver's state leak guard stopped the
batch, exit 6. That is the second shape in the solutions entry on null
control halts, a live job from the installed copy, and the job's own process
was alive when the halt was read.

The run is repeatable as written, with no cratekit job running:

    ./.venv/bin/python scripts/mutate.py docs/mutation/r689-rows.toml

Every row's subset is `tests/test_doctor.py` and `tests/test_active_taxonomy.py`.

| Row | What it reverts | Written to kill it |
|---|---|---|
| D1 | the stale copy reads OK, not INFO | `test_a_copy_setup_made_that_the_shipped_template_has_since_outgrown_is_info` |
| D2 | edited is decided against the shipped text, not the record | the same, a stale unedited copy would read as edited |
| D3 | the name mismatch branch is gone | `test_a_record_naming_a_template_other_than_the_configured_one_is_info` |
| D4 | gained is computed in the wrong direction | `..._outgrown_is_info` asserts `[long_tracks]`; the dropped section test asserts both lines |
| D5 | dropped sections are never named | `test_a_shipped_template_that_dropped_a_section_the_copy_still_has_is_named_too` |
| D6 | with no record, the copy always "matches" | `test_a_copy_with_no_record_says_the_origin_is_unrecorded`, its second half |
| D7 | an unusable record reads OK | `test_a_record_that_cannot_be_used_is_said_rather_than_read_as_no_record` |
| S1 | setup writes no record and says it did | `test_setup_records_which_shipped_text_the_copy_was_made_from` |
| S3 | setup records a digest of other text | the same, and the unchanged OK test would read "edited" |
| T1 | the digest ignores the text | `..._outgrown_is_info`, every digest equal reads "has not changed" |
| T2 | the fingerprint has no sections | `..._outgrown_is_info` asserts `[long_tracks]` in the detail |
| T3 | any string is a digest | `..._cannot_be_used...` writes `sha256 = "short"` |

**Dropped, two rows, logged in the rows file.** S2 would write the record on
the already there path too, which is not one string replacement; the test for
a copy left alone is written to kill it. G1 would put doctor back on the
guard's shipped text allow list, a mutation of `tests/`, and on a clean tree
the guard has no offender to find, the same shape as R-685's G3.
