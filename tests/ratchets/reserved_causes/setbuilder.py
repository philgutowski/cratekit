"""Reserved cause pins for ``setbuilder``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'setbuilder/cli.py': [
        'library-root-absent',
        'setbuild-anchor-ambiguous',
        'setbuild-anchor-not-indexed',
        'setbuild-anchor-outside-library',
        'setbuild-anchor-unknown',
        'setbuild-supplied-needs-unowned',
        'setbuild-unowned-key-missing',
    ],
}

LITERAL_HOLDERS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'setbuilder/cli.py': [
        'library-root-absent',
        'setbuild-anchor-ambiguous',
        'setbuild-anchor-not-indexed',
        'setbuild-anchor-outside-library',
        'setbuild-anchor-unknown',
        'setbuild-supplied-needs-unowned',
        'setbuild-unowned-key-missing',
    ],
}
