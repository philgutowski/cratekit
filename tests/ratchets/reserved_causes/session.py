"""Reserved cause pins for ``session``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'session/cli.py': ['backup-facts-unreadable', 'internal-error'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'session/restore_cli.py': [
        'internal-error',
        'off-machine',
        'restore-flag-needs-pull',
        'restore-record-unusable',
        'restore-target-invalid',
        'restore-target-is-live-root',
    ],
}

LITERAL_HOLDERS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'session/cli.py': ['backup-facts-unreadable', 'internal-error'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'session/restore_cli.py': [
        'internal-error',
        'restore-flag-needs-pull',
        'restore-record-unusable',
        'restore-target-invalid',
        'restore-target-is-live-root',
    ],
}
