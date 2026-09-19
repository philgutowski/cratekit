# U101 mutation table, read

One table, the author's and not independent, measured by `scripts/mutate.py`
on `relay/146` at `6e7ac6d`. Every zero row in this record means the author
could not kill it, not that nobody could.

**`u101.md`**, 23 rows. 21 over the guards this unit added to
`label/approved_cli.py`, subset `tests/test_label_approved.py` named
explicitly, 56 collected on every row with no drift. 2 over the engine it is the
first caller of, `core/routing.py`, subsets derived from imports and both
promoted to the full suite. Null control 0 of 8245, every restore verified
against `git show HEAD`. 21 killed, 2 zero. Two more rows were considered and
logged as dropped in `u101-rows.toml`, both reports about a release the gate
held, whose tracks are not listed either way.

The table measured the tree after the review's fix round, so the unread label
guard (G5, G6) is measured and not only argued.

## The two zeros

- **E2, a keep rule answering its family.** An equivalent mutant, badly chosen.
  `taxonomy._build_gate` refuses a rule that declares both `keep` and `family`,
  so on a keep rule `rule.family` is already `None` and the mutation changes
  nothing. A row that skips the keep rule instead would have measured the
  guard. Not re-measured, one pass per unit.
- **E1, the share bound.** `n / classified < share` made `<=`. User facing: it
  decides whether a family at exactly the share is held. No test sat on the
  boundary. It bought `test_a_family_exactly_at_the_share_belongs_and_is_listed`,
  nine house releases and one hip hop, which is exactly 10%. That test was added
  after the table and was confirmed once against the E1 mutation by a one off
  script that restored the file and compared it to `git show HEAD`: 1 failed.
  It is not a driver row and is recorded as a single confirmation, not a
  measurement.
