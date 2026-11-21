"""Reserved cause pins for ``master``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'master/cli.py': [
        'config-unusable',
        'join-order',
        'source-missing',
        'target-lufs-out-of-range',
    ],
}

LITERAL_HOLDERS = {
    'master/cli.py': ['config-unusable', 'source-missing', 'target-lufs-out-of-range'],
}
