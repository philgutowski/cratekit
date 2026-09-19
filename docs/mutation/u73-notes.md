# U73 mutation notes

Three tables, `u73.md`, `u73-b.md` and `u73-c.md`, one light pass split in three
so each driver run finished inside the tool's 600 second ceiling. 22 rows, 21
killing, null control 0 of 7859 in each, every restore verified against `HEAD`.
This is the author's table, not an independent one.

Rows cover every guard this unit added: the blank run refusal; each of the three
halves of the run selection, the run, the library and the intake handler key,
removed alone; the oldest first order; the open, failed, skip-failed and every
job skipped refusals; the refusal of a skip that lists nothing; the provenance's
every reference and first source wins; the refusal of `--skip-failed` with
`--job`; the manifest's `source_refs` written only when there are several, and
written at all; the `sync all` next step's filter, its intake key count and its
check row; and the landing hint's `--export`. Two existing U69 guards every run
job also passes through were sampled, the missing but unlistable refusal and
the reports by identifier comparison.

Two tests were added BEFORE the table ran, not in answer to a zero: a labels job
sharing the run is not selected, and a full pass that queued only labels and
favourites names no run verb. Neither guard had a test that could fail.

`B5_refs_deduplicated` is zero on the full suite and maintainer facing: dropping
the dedup would name one playlist twice only when that playlist lists the same
track twice, which no fixture does.

Two rows dropped. `A6_tie_break`: the job id only breaks a tie between jobs
created in the same timestamp, which the fixture cannot produce without faking
the clock, and `A5_oldest_first` measures the order itself. `A11_sync_run_dest`:
the flag writing `dest="run"` cannot be expressed as one site, since the handler
reads the new name; the first build measured the collision failing eleven tests.
