"""Reserved cause pins for ``session``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'session/cli.py': ['backup-facts-unreadable', 'internal-error'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'session/restore_cli.py': [
        'internal-error',
        'off-machine',
        'restore-flag-needs-pull',
        'restore-record-unusable',
        'restore-tags-unwritten',  # 2026-11-23, R-1924
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
        'restore-tags-unwritten',  # 2026-11-23, R-1924
        'restore-target-invalid',
        'restore-target-is-live-root',
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-11-23, R-1924: a restore refusing a file that did not take its old tags back.
    'session/restore_cli.py': ['restore-tags-unwritten'],
}

NAMED_WITH_OWN = {
    # 2026-11-23, R-1924: the same name, counted with the file's own declarations.
    'session/restore_cli.py': ['restore-tags-unwritten'],
}
