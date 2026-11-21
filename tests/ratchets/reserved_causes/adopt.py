"""Reserved cause pins for ``adopt``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'adopt/apply.py': ['adoption-ledger-unusable', 'utf-8'],
    'adopt/apply_cli.py': [
        'adopt-entries-failed',
        'adoption-nothing-applicable',
        'config-unusable',
        'decision-stale',
        'favorites-removals-owed',
        'favorites-skipped',
        'favorites-unverified',
        'internal-error',
        'no-op',
    ],
    'adopt/approval.py': ['decision-required', 'decision-stale'],
    'adopt/artifacts.py': ['adopt-artifacts', 'adopt-staging', 'utf-8'],
    'adopt/genres_cli.py': ['config-unusable'],
    'adopt/move.py': [
        'former-place-not-named-by-genre',
        'genre-names-no-style',
        'held-under-another-name',
        'no-reading',
        'one-sub-held-by-two-rows',
        'reading-names-neither-held',
        'withheld-by-verdict',
    ],
    'adopt/move_cli.py': [
        'adopt-entries-failed',
        'config-unusable',
        'decision-required',
        'decision-stale',
        'internal-error',
        'move-nothing-planned',
        'no-op',
    ],
    'adopt/plan.py': [
        'adopt-existing',
        'adoption-collision',
        'adoption-genre',
        'keep-separate',
        'no-bucket',
        'no-sub',
        'no-tag',
        'under-another-name',
    ],
    'adopt/revert.py': [
        'a-different-size',
        'adoption-file-unidentifiable',
        'adoption-ledger-unusable',
        'dev-ino',
        'not-a-regular-file',
        'took-too-long',
        'utf-8',
    ],
    'adopt/scan.py': ['needs-genre', 'not-a-path', 'online-only'],
    'adopt/scan_cli.py': [
        'adopt-item-absent',
        'collection-all-tombstones',
        'collection-empty',
        'config-unusable',
        'no-op',
    ],
    'adopt/shell.py': ['internal-error'],
}

NAMED_WITH_OWN = {
    'adopt/revert.py': ['a-different-size', 'not-a-regular-file', 'took-too-long'],
    'adopt/scan.py': ['needs-genre', 'not-a-path', 'online-only'],
}

NAMED_WITH_INTEGER = frozenset({
    'adopt/revert.py',
})

LITERAL_HOLDERS = {
    'adopt/apply.py': ['adoption-ledger-unusable'],
    'adopt/apply_cli.py': [
        'adopt-entries-failed',
        'config-unusable',
        'decision-stale',
        'internal-error',
    ],
    'adopt/approval.py': ['decision-required', 'decision-stale'],
    'adopt/genres_cli.py': ['config-unusable'],
    'adopt/move_cli.py': [
        'adopt-entries-failed',
        'config-unusable',
        'decision-required',
        'decision-stale',
        'internal-error',
    ],
    'adopt/revert.py': ['adoption-file-unidentifiable', 'adoption-ledger-unusable'],
    'adopt/scan_cli.py': ['adopt-item-absent', 'config-unusable'],
    'adopt/shell.py': ['internal-error'],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'adopt/revert.py',
})
