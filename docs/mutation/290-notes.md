# U125 mutation notes

Card changes how the reserved-cause suite pins populations: totals become
derived from per-module (and per-slug) pins in
`tests/_pinned_reserved_populations.py`.

1. Delete one module entry from `PINNED_KEBAB_LITERALS_BY_MODULE`
   (`core/backup_facts.py`). Expect the at-risk pin test to fail naming that
   module. Observed: FAIL naming `core/backup_facts.py` and its literals.
2. Remove one slug (`cancelled`) from `PINNED_NON_RESERVED_CAUSES` while the
   tree still declares it. Expect the same test to fail naming the slug.
   Observed: FAIL naming `cancelled` as joined.
3. Add a fake module pin (`zz_fake_u125.py`) the tree does not hold. Expect
   the same test to fail naming the pin-only module. Observed: FAIL naming
   `zz_fake_u125.py`.
4. Restore a whole-repository total tuple assert beside the pins. Expect
   review to reject it: U125 forbids reintroducing the shared edit point.
   Observed: review.

Rows 1 to 3 were run by hand against scratch edits of the pin file and reverted.
A throwaway git merge of two branches that each added a dated comment on a
different module entry merged with no conflict markers.
