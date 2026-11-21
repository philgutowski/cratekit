"""Reserved cause pins for ``session``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'session/cli.py': ['backup-facts-unreadable', 'config-unusable', 'internal-error'],
    'session/restore_cli.py': [
        'config-unusable',
        'internal-error',
        'off-machine',
        'restore-flag-needs-pull',
        'restore-record-unusable',
        'restore-target-invalid',
        'restore-target-is-live-root',
    ],
}

LITERAL_HOLDERS = {
    'session/cli.py': ['backup-facts-unreadable', 'config-unusable', 'internal-error'],
    'session/restore_cli.py': [
        'config-unusable',
        'internal-error',
        'restore-flag-needs-pull',
        'restore-record-unusable',
        'restore-target-invalid',
        'restore-target-is-live-root',
    ],
}
