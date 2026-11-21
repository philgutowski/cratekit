"""Reserved cause pins for ``backup``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'backup/cli.py': [
        'backup-already-queued',
        'backup-comparison',
        'backup-facts-unreadable',
        'backup-nothing-ran',
        'backup-rehearsal',
        'backup-transfer-failed',
        'config-unusable',
        'internal-error',
    ],
}

LITERAL_HOLDERS = {
    'backup/cli.py': [
        'backup-facts-unreadable',
        'backup-nothing-ran',
        'backup-transfer-failed',
        'config-unusable',
        'internal-error',
    ],
}
