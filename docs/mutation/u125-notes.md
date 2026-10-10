# U125 mutation notes

Card changes how the reserved-cause suite pins populations: totals become
derived from per-module (and per-slug) pins in
`tests/_pinned_reserved_populations.py`.

Rows live in `docs/mutation/u125-rows.toml` (author's table, light cap). They
cover the pin file's guards and the fixed derive test:

1. Drop one module entry from `PINNED_KEBAB_LITERALS_BY_MODULE`.
2. Drop one slug from `PINNED_NON_RESERVED_CAUSES`.
3. Add a pin module the tree does not hold.
4. Add a literal to a pinned module the tree does not carry.
5. Change `PINNED_RESERVED_CAUSE_COUNT`.
6. Weaken the derive test's tree comparison back to a tautology.

The watcher measures the rows on macOS and posts the two table files for this
lane to commit byte for byte.

## Two-branch merge check (brief)

From tip `0061b847`, two throwaway branches each added one kebab literal in a
different module entry of `PINNED_KEBAB_LITERALS_BY_MODULE`
(`acquire/adapter.py` vs `core/binaries.py`). Merging either order produced no
conflict markers in the pin file. Branches deleted locally after the check.
(The earlier notes recorded comment edits instead of this check; that was
wrong.)

## Known limit

The pins are sorted, so two cards adding neighbouring slugs or neighbouring
module entries still edit adjacent lines and can conflict. U125 removes the
whole-repository total hotspot, not every adjacent-line collision.
