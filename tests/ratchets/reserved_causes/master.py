"""Reserved cause pins for ``master``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

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
