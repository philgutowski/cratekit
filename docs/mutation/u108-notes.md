# U108 mutation notes

The author's table, as METHOD sets it, over the guards the guided label
sync's go added and its first review round added. Twenty five rows, the cap
for a unit that writes files, run in three batches so each fits the tool
ceiling: `u108-a.md`, `u108-b.md` and `u108-c.md`. The ranking and the three
rows dropped below the cap are in `u108-a-rows.toml`.

## Summary

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| a | 9 | 9 | 0 |
| b | 8 | 5 | G11, G14, G16 |
| c | 8 | 6 | G18, G20 |
| d, the zeros again | 5 | 5 | 0 |

25 of 25 killed after one round of tests for the zeros.

## The zeros, and what each needed

- **G11**, the refusal under the record's lock when another go queued while
  this one waited. User facing. The race test let the gate's own digest see
  the change first, so it refused before the lock and the guard was never
  reached. The test now hides the other go's job from both summaries.
- **G14**, a go job whose cause says no retry can succeed is not resumed.
  User facing. No test had a go job fail permanently; one now does.
- **G16**, only a job a go queued is a go's. User facing. No test put a
  download queued by hand beside a go; one now does.
- **G18**, settling checks the answer at a place is the one summarised.
  User facing only through a record rewritten while a go waits, which no
  verb was driven to produce. Pinned with a direct test of `settle_in`.
- **G20**, an answer already settled is not settled again. Maintainer facing.
  Pinned with a direct test of `settle_in`.

Every zero row reads as "the author could not kill it" until batch d, and
batch d measured each at one death or more. The author ran the table, not
an independent verifier, which is the gap METHOD records.
