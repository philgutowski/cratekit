# Mutation notes: r669

Two tables, `r669.md` and `r669-b.md`, one pass each, the author's own. Every
zero reads as "the author could not kill it", not as "nothing can".

## The pass

`r669.md`: 25 rows, the light cap exactly, 21 over the unit's own diff in
`write/naming_cli.py` and 4 over the verb's existing guards, run after the
review's fix round at `746e19b`. Subset of 2 files, 115 collected on every
subset row, baseline 10023, null control 0. Twenty four killed on the subset.
Three rows considered and dropped are logged in the table.

## The zero, and what it was

`G14_artist_not_sanitized` mutated the sanitizer in `_artist`, the one that
put each credit into its segment form before the join, and promoted to the
full suite killed nothing at 10023 collected. The reason is not a missing
test: `test_a_slash_in_a_tag_takes_the_body_form_of_a_segment` drives
`AC/DC` to `AC-DC - Affection.flac` through the dispatcher. The reason is a
second sanitizer. `naming.compose_body`, lifted into the core in the fix
round so the fallback fetch path and this verb share one join, sanitizes each
part again, so the copy in `_artist` was a guard covered by another guard.
METHOD's driver rule: remove each layer alone, and a guard covered by another
guard is a guard nothing covers.

The copy in `_artist` was removed at `27dc777`, so the composer's is the one
layer. `r669-b.md` is G14's composite: one row, `B1_composer_not_sanitized`,
dropping the composer's sanitizer over the two suites that reach it.

## What was not measured

`G15_empty_artist_values_kept` was promoted to the full suite and killed 26,
which is the naming apply suite failing at import shape rather than 26
independent proofs; the row's own test is
`test_an_empty_artist_value_does_not_lead_the_body_with_a_comma`. No timing
row, because the unit adds no bound with a coefficient.
