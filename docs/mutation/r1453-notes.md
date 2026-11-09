# R-1453 mutation notes

The table, `r1453.md`, was measured at `5c7c9a2f`: 8 rows over R-1264's unread
keys in `plan_pair`, every one killed on its subset, the null control killing
none of 17600. Every row is the author's.

**The brief's verification.** S4, R-1434's zero row (the unread keys keep a key
a readable release carries), kills 2: the reorder test and the removal test of
R-1453's block in `tests/test_sync_pair_unread.py`. Its composite, no track
unread at all, kills 5, the control among them.

**U1, a zero driven to a test.** The first measurement, at `e6ad0ca3`, found
U1 (the unread keys read by each release's own key rather than through its
row's) a zero on the full suite, 17599 collected. On the brief's shape the
mutant is the same code, since t4, the unread release, is the row's own key.
Driven with the row's other release unread instead and the first gone from
the account, the mutant reads the row as taken off and removes it from
rekordbox while the account still lists it. The fourth test of the block,
committed at `5c7c9a2f`, pins that, and the table was measured again whole.

**The known failures copy.** The driver's first run refused a red baseline on
two inode bound tests in `tests/test_repair_rows.py`, which `cloud_battery.py
baseline` had caught passing. Measured on the base `7ab312f0` alone, the first
failed 7 of 7 runs and the second 1 of 3 runs of its file; a fresh file under
`/var/tmp` here took an inode near 600,000, under the 2,000,000 bound. So, by
the inode bound solutions entry, the driver read a scratch copy of the
baseline with those two ids added and the measurement written beside them, and
`.cloud-battery/baseline.txt` was not edited: 163 ids against its 161.
