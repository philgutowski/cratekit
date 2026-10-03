# U112 mutation notes

The author's table, not an independent one: every zero reads as "the author
could not kill it" (METHOD, Verification is the author's). The unit composes
writes to the live database and to the account, so it gets the full 25 rows,
scoped to the composition's own guards. The step verbs' own guards are their
units' tables and were not re-measured here.

`u112` ran on a committed tree with a green full baseline, 12,737 collected.
Its null control killed nothing, and every restore was verified against
`git show HEAD:`. 25 rows, 22 killed, 3 zeros, each zero promoted to the full
suite before it was reported.

- The verb, 7 rows, 6 killed: C1 the report returns before the gates 10, C2
  the database area written only on approve 1, C3 the account area only on
  apply 1, C4 a refused area not asked 1, C5 an unexpected failure lets later
  steps run 1, C6 a failed step raised 1.
- **C7 zero, then killed.** An outcome of OK over a run that wrote nothing
  killed nothing on the full suite: no test asserted a no-op outcome. User
  facing, since the envelope says something happened. A test now drives both
  gates answered abort and asserts `no_op`.
- The area digest, 1 row, killed: S1 a step's own plan digest in the area's
  digest 5, among them the test that a plan moving after the answer is stale.
- The database area, 8 rows, 8 killed: R1 the backup acknowledgment 1, R2
  only outstanding entries planned 1, R3 the bridge tree refused 1, R4 the gate
  run on the job 1, R5 the approving actor 1, R6 the declared trees never the
  author's 1, R7 a rename suggested only for a batch named for its run 1, R8
  the author's INBOX nodes listed 1.
- The account area, 7 rows, 5 killed: A1 a put back mark is no mark 1, A2 a
  pending file over a retired one 1, A3 the retired files by number 1, A4 a
  playlist in the author's folder unlisted 1, A7 the set's proof read 4.
- **A5 and A6 zero, then killed.** Emptying every product made exclusion, and
  dropping the ledger's product made answer, each killed nothing: the fake
  account listing held no playlist the product made, so the assertion that the
  set is not the author's excluded nothing. The world fixture now lists the set
  playlist on the account, and a test lists an exported playlist the ledger
  records.
- The verified hand off, 1 row, killed: G1 the part's digest checked against
  the answer's document 1.
- The homes, 1 row, killed: O1 a label wins over a year 1.

`u112-b` re-measured the three former zeros after their tests landed, on a
committed tree, as its own light table: C7 1, A5 2, A6 1. All three killed.

Dropped as considered and ranked below the cap: the labels and export modules
switched off (a listed step, no write), the area's `writes` ignoring its own
refusal (structurally equal, a refused area has no steps), the shared account
listing for many passes (a cost, not a write; no test fixture builds two sync
passes), and the strict greater than in the latest file rule (A2 and A3 hold
the order from both ends).
