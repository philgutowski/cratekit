# u133 mutation notes

Author's table, 25 rows, one pass, in two batches `u133-a` (the upgrade
planner's hold and the keyword rule note, 13 rows) and `u133-b` (the shipped
template's Jazz declarations and one move guard, 12 rows). 23 detected, 2
zeros promoted to the full suite. The author ran it, so a zero reads as "the
author could not kill it". Two rows considered and dropped, each with its
reason in the rows files.

Three guards measured zero on the first pass, each reachable and driven, and
each had no test. A test was added for each after its batch, in its own
commit, and the same row was measured again in `u133-a-rerun` (P5, P8) and
`u133-b-rerun` (T6, with E2 carried for the null control). Those reruns are
the same rows, not new ones, so the count stays 25.

- **P5_vocabulary_owner, killed 1 on rerun.** A vocabulary row whose tag
  files in a bucket that shares the word by the template's design (the
  breaks bucket's "Trap / Wave") is not named when another bucket clashes.
- **P8_held_by_whole_copy, killed 2 on rerun.** A copy whose R&B bucket also
  tags "jazz" is held on both buckets, not the first declared.
- **T6_former_sub, killed 1 on rerun.** The former place's sub is the key a
  write before U133 recorded the old playlist's node under; pinned to the
  identifier the template declared before U133.
- **P6_spelling_once, zero.** Listing a spelling twice in a hold sentence.
  Maintainer facing, wording only.
- **T3_tag_alias_gone, zero, user facing, composite T2.** Jazz's tagging word
  "jazz" is redundant: measured on the template with it removed, the routing
  alias "Jazz" answers "jazz", "JAZZ" and " jazz " for tagging alike. T2,
  which removes that alias, kills 2, so what tags Jazz is held. The line is
  kept to mirror the old sub's word, as Hip-Hop keeps "hip-hop".
- **T1, T7, T11, collect errors.** Each changes what a test module derives
  from the shipped declarations at import, or makes the template refuse to
  load, so the suite turns red by collection rather than named deaths, as
  U118's T rows did.

**The batches were stopped four times by the driver's state guard**, each
time on a write to the real installation state that this branch's children
do not make: an hourly `crate doctor` run record at about 35 past the hour
(00:35 and 01:34 UTC), and a real provider call that advanced the live
provider gate's counter at 01:44 UTC, while another unit's mutation driver
and the watcher's checks were running. Batch a resumed from its stored rows;
batch b was rerun whole and measured clean on its fourth start.
