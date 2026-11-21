"""Reserved cause pins for ``organize``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    # 2026-10-13, U143: the root step's kept warning joined.
    'organize/account.py': ['organize-root-kept'],
    # 2026-10-15, U147: the account mirror step joined.
    'organize/account_mirror.py': ['organize-mirror-kept'],
    'organize/cli.py': ['internal-error', 'organize-area-refused', 'organize-step-refused'],
    # 2026-10-13, U144: the INSPIRATION parity step, its write and its unread warning.
    'organize/inspiration.py': [
        'decision-stale',
        'folder-unread',
        'inspiration-parity',
        'session-committed-unverified',
        'two-of-one-name',
    ],
    # 2026-11-05, U204: the mirror downloads step's kind and its job source joined.
    'organize/mirror_downloads.py': ['account-mirror', 'mirror-downloads'],
    # 2026-11-05, U201: the mirror edits step's kind, its write refusals and
    # its untagged warning joined.
    'organize/mirror_edits.py': [
        'decision-stale',
        'mirror-edits',
        'organize-mirror-edits-untagged',
        'session-committed-unverified',
    ],
    # 2026-10-27, R-1031: the frozen mirror plan's encoding name joined.
    'organize/mirror_frozen.py': ['utf-8'],
    'organize/rekordbox.py': ['organize-inspiration-unread', 'record-labels', 'tree-unconverged'],
    # 2026-10-13, U143: the root step's kept refusal problems joined.
    'organize/root.py': [
        'ledger-claimed',
        'not-a-legacy-folder',
        'not-empty',
        'not-owned',
        'not-this-kind',
    ],
}

LITERAL_HOLDERS = {
    'organize/cli.py': ['internal-error'],
    # 2026-10-13, U144: the INSPIRATION parity step's two write refusals.
    'organize/inspiration.py': ['decision-stale', 'session-committed-unverified'],
    # 2026-11-05, U201: the mirror edits step's two write refusals joined.
    'organize/mirror_edits.py': ['decision-stale', 'session-committed-unverified'],
    'organize/rekordbox.py': ['tree-unconverged'],
}
