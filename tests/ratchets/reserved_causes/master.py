"""Reserved cause pins for ``master``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'master/cli.py': [
        'join-order',
        'source-missing',
        'target-lufs-out-of-range',
    ],
}

LITERAL_HOLDERS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'master/cli.py': ['source-missing', 'target-lufs-out-of-range'],
}
