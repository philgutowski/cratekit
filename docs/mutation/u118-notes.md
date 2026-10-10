# u118 mutation notes

Author's table, 25 rows, one pass, in four batches `u118-a` to `u118-d`
measured on heads a40f717 and 3ab7616, which differ only in the rows files. 23
detected, 2 maintainer facing zeros promoted to the full suite of 12995. The
author ran it, so a zero reads as "the author could not kill it".

The unit decides which memberships a move removes, so the table is the full
light pass over the new guards: the split place loader, the tagging alias
order, what competes, the placement reader, the move plan's listing and
settling, and the template's declarations. Four rows were considered and
dropped, each with its reason in the rows files.

Batches were split because one batch over this suite runs past the tool's
600 second ceiling, and a killed driver can leave a mutation in the source.
Batch c's first run was refused on a red baseline, one timing test in
`tests/test_pool_sizing.py` under load; it passed alone, 267 of 267, and the
rerun's baseline was green. Batch d was refused once for want of a Python row
for the null control, so M11 moved in from the dropped list and T3 went out.

- **L7, T1, T2, T4, collect errors.** Each removes a declaration the shipped
  template needs. L7 makes the template refuse to load, so every verb
  refuses; T1, T2 and T4 change what the test modules unpack from the shipped
  declarations at import. All four turn the suite red by a collection error
  rather than by named deaths, which the driver reports as it is.
- **M9_standing_split_target, zero.** Dropping the refusal of an entry whose
  sub is a split place kills nothing: such an entry already holds its target,
  so nothing is stale and no move is planned. Maintainer facing, kept as the
  same belt and braces the former place has beside it.
- **M11_genre_names_fallback, zero.** Counting the fallback tier as naming a
  bucket matters only for a taxonomy whose fallback bucket declares split
  places, which the shipped one does not. Maintainer facing.

One guard had no test reaching it before the table was written, the renamed
playlist reason on the split listing. Its test was added first, in its own
commit, and M7 is the row that measures it.
