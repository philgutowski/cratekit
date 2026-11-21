"""Reserved cause pins for ``backup``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'backup/cli.py': [
        'backup-already-queued',
        'backup-comparison',
        'backup-facts-unreadable',
        'backup-kind',  # 2026-11-21, U317
        'backup-nothing-ran',
        'backup-rehearsal',
        'backup-transfer-failed',
        'internal-error',
    ],
}

LITERAL_HOLDERS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'backup/cli.py': [
        'backup-facts-unreadable',
        'backup-nothing-ran',
        'backup-transfer-failed',
        'internal-error',
    ],
}
