# U179 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` with `--known-failures .cloud-battery/baseline.txt` on the
cloud container, so each is a Linux measure of a macOS suite, green net of the
166 failures bound to this machine.

**`u179.md`**, 25 rows over the verb (17: the plan, the fetch and its open
fetches, the staged files' tags, the landing's arguments, the rehearsal), the
batch name rule (3), the chain's new rehearsal step and its quoted stop
wording (4) and the shared preflight (1), null control 0 of 15131, every
restore verified against `git show HEAD`. 23 killed on their subsets.

**`u179-z.md`**, the two zeros measured again after the tests they bought.
Both killed, the null control 0 of 15133.

## The two zeros

- **S4, a part owned release counts as something to fetch.** Zero on the full
  suite, because every plan in it also held a wholly new release. Without
  `held` in the count, a plan whose only purchase is a compilation with one
  owned track reads as nothing new, and the other tracks are never fetched.
  `test_a_plan_holding_only_part_owned_releases_still_fetches_the_rest` kills it.
- **S9, only a refusal for good settles a failed fetch.** Zero, because no test
  failed a fetch with a retryable item. Without the permanence test, a release
  the account answered 503 for would be read as settled and the verb would go
  on to the tail over a batch still missing it.
  `test_a_fetch_failed_by_a_transient_answer_ends_the_verb_and_lands_nothing`
  kills it.

## Dropped below the cap

- The guard in `_fetch` that settles a fetch still open and not parked after
  its own drive. The first review measured it at zero kills: its only
  producer is a live driver elsewhere holding the job, reasoned and not driven.
- The rehearsal's `no_op` end in `tail.rehearse`, and `or not to_fetch` in
  `_plan`: zero kills, and no producer reaches either, since the verb runs the
  rehearsal only over a folder it has listed files in, and the plan verb's
  outcome already says nothing is new.
- Two rows of the first draft, the refused releases' warning and the fetch
  refusal with no job queued, gave their places to the second review's two
  rows, `D1_fetched_once` and `D2_refused_once`.
