# R-388 mutation notes

Seventeen rows, the author's own, one pass in three batches so each driver run
finished inside one foreground call, then a re-measure of one. The brief's two
named rows are M1, restoring `no-snapshot-available` on a named snapshot whose
identity listing fails, which kills 2, and M2, rewording `could not be listed`
in that refusal, which kills 1.

`r388-a.md` holds M1 to M6, the identity, contents and root listings, each as
a slug row and a wording row. `r388-b.md` holds M7 to M12: the share listing's
slug and wording, the three exit 3 branches the built in review's fix added,
and the listing failure's first step replaced with the take a backup step.
`r388-c.md` holds M13 to M17: the credential step, the `core.cause`
registration dropped and set to a disagreeing code, the named stamp step on
`no-snapshot-available`, and the enum value respelled.

The first pass left one zero, M16, user facing, promoted to the full suite of
9800 and still zero. It drops the step `no-snapshot-available` gained for a
typed stamp, and no test read that reservation's steps. It was pinned by
reading the steps back in the absent folder test for its two named cases, and
`r388-d.md` measures it killed twice. All seventeen are killed on the final
tree, by the author's own tests; the author found no way to leave one standing.

M12, M13 and M16's re-measure ran on the `cli/exit_codes.py` subset, which
collects 645. That is its own subset baseline, not drift.

Dropped: none. The walk over the newest snapshots reaches the same two raises
through `snapshot_identities`, so it has no guard of its own to revert.
